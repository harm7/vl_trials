from unittest.mock import patch, ANY
from asyncio import Semaphore
from pathlib import Path

import aiohttp
import pytest
from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from uploader import upload_task, upload_controller


test_data_folder = Path(__file__).parent / 'test_data'
local_server_url = 'http://localhost:8888/images'


async def handler(request: Request) -> Response:
    post = await request.post()
    if 'file' not in post:
        return web.HTTPBadRequest(text='No file in request')
    if not post['file'].content_type.startswith('image/'):
        return web.HTTPUnsupportedMediaType()
    filename = post['file'].filename
    file_stream = post['file'].file
    image = file_stream.read()
    with open(test_data_folder / filename, 'rb') as fp:
        image_original = fp.read()
    if len(image) == len(image_original) and image == image_original:
        return web.HTTPOk()
    return web.HTTPBadRequest(text='Original and received images do not match')


async def bad_handler(request: Request) -> Response:
    post = await request.post()
    return web.HTTPBadRequest(text='Bad server')


@pytest.fixture
def good_server(loop, aiohttp_server):
    app = web.Application()
    app.router.add_post('/images', handler)
    return loop.run_until_complete(aiohttp_server(app, port=8888))


@pytest.fixture
def bad_server(loop, aiohttp_server):
    app = web.Application()
    app.router.add_post('/images', bad_handler)
    return loop.run_until_complete(aiohttp_server(app, port=8888))


async def test_single_file_upload(good_server):
    semaphore = Semaphore(value=1)
    session = aiohttp.ClientSession()
    await upload_task(session, test_data_folder / 'cat_caviar.jpg', local_server_url, semaphore)


async def test_single_file_bad_server(bad_server):
    semaphore = Semaphore(value=1)
    session = aiohttp.ClientSession()
    with pytest.raises(RuntimeError):
        await upload_task(session, test_data_folder / 'cat_caviar.jpg', local_server_url, semaphore)


@patch('uploader.upload_task')
async def test_multiple_file_upload_mocked(mock_task):
    await upload_controller(Path(test_data_folder), local_server_url)
    try:
        mock_task.assert_called_with(ANY, test_data_folder / 'some_text.txt', local_server_url, ANY)
    except AssertionError:
        return
    else:
        raise AssertionError('upload_task is not supposed to be called with non-image file path')


async def test_multiple_file_upload(good_server):
    await upload_controller(Path(test_data_folder), local_server_url)


async def test_multiple_file_bad_server(bad_server):
    with pytest.raises(RuntimeError):
        await upload_controller(Path(test_data_folder), local_server_url)


async def test_multiple_file_nonexistent_folder(good_server):
    with pytest.raises(FileNotFoundError):
        await upload_controller(Path('wtf'), local_server_url)
