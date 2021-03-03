import asyncio
import os
from asyncio import Semaphore

import aiohttp
from aiohttp import web
from tqdm.asyncio import tqdm
import click
import filetype
from pathlib import Path


MAX_CONCURRENT_FILES_PROCESSED = os.getenv('MAX_CONCURRENT_FILES_PROCESSED', 500)
SERVER_URL = f"{os.getenv('BASE_URL', 'http://localhost:8888')}/images"


async def upload_task(session: aiohttp.ClientSession, path: Path, url: str, semaphore: Semaphore):
    print(f'File {path} is about to be uploaded')
    async with semaphore:
        response = await session.post(url, data={'file': path.open('rb')})
        if response.status != web.HTTPOk.status_code:
            raise RuntimeError(f'Server returned bad status {response.status} on upload of {path}')


async def upload_controller(src_folder: Path, dst_url: str):
    if not src_folder.exists():
        raise FileNotFoundError('Folder you specified does not exist')
    image_files = filter(lambda path: Path.is_file(path) and filetype.is_image(str(path)), src_folder.rglob('*'))
    loop = asyncio.get_event_loop()
    semaphore = asyncio.Semaphore(value=MAX_CONCURRENT_FILES_PROCESSED)
    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(upload_task(session, path, dst_url, semaphore)) for path in image_files]
        for task in tqdm(asyncio.as_completed(tasks), total=len(tasks)):
            await task


@click.command()
@click.argument('src_folder')
def upload(src_folder: str):
    '''This script uploads all image files in SRC_FOLDER to server
    (can be overriden in BASE_URL env variable)'''
    asyncio.run(upload_controller(Path(src_folder), SERVER_URL))


if __name__ == '__main__':
    upload()
