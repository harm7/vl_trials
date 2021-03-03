from main import are_equal
import pytest

EMPTY_LIST = []
EMPTY_DICT = {}
FLAT_LIST = [1, 2, 3, 4, 5]
FLAT_LIST_ANOTHER = [5, 4, 3, 2, 1]
FLAT_DICT = {
    'int': 12345,
    'float': 0.2e-5,
    'bool': True,
    'string': 'yay!',
}
FLAT_DICT_ANOTHER = {
    'int': 54321,
    'float': 3.1415926,
    'bool': False,
    'string': 'oh no!'
}
FLAT_DICT_DIFFERENT_KEY = {
    'yeent': 12345,
    'float': 0.2e-5,
    'bool': True,
    'string': 'yay!'
}
FLAT_DICT_DIFFERENT_VALUE_TYPE = {
    'int': 'yep, int',
    'float': 0.2e-5,
    'bool': True,
    'string': 'yay!'
}
FLAT_DICT_DIFFERENT_INT = {
    'int': 67890,
    'float': 0.2e-5,
    'bool': True,
    'string': 'yay!'
}
FLAT_DICT_DIFFERENT_FLOAT = {
    'int': 67890,
    'float': 0.3e-5,
    'bool': True,
    'string': 'yay!'
}
FLAT_DICT_DIFFERENT_BOOL = {
    'int': 67890,
    'float': 0.2e-5,
    'bool': True,
    'string': 'yay!'
}
FLAT_DICT_DIFFERENT_STR = {
    'int': 67890,
    'float': 0.2e5,
    'bool': True,
    'string': 'oh no!'
}

NESTED_LIST_LIST = [[1, 2], [3, 4]]
NESTED_LIST_LIST_ANOTHER = [[5, 6], [7, 8]]
NESTED_DICT_LIST = [{'int': 1}, {'float': 2.0}]
NESTED_DICT_LIST_ANOTHER = [{'int': 2}, {'float': 2.0}]

TWO_LEVEL_DICT = {
    **FLAT_DICT,
    'list': FLAT_LIST,
    'dict': FLAT_DICT_ANOTHER
}
TWO_LEVEL_DICT_ANOTHER = {
    **FLAT_DICT_ANOTHER,
    'list': FLAT_LIST_ANOTHER,
    'dict': FLAT_DICT_DIFFERENT_FLOAT
}

test_data = (
    (EMPTY_DICT, EMPTY_DICT, True),
    (EMPTY_LIST, EMPTY_LIST, True),
    (FLAT_LIST, FLAT_LIST, True),
    (FLAT_DICT, FLAT_DICT, True),
    (EMPTY_DICT, FLAT_DICT, False),
    (FLAT_DICT, FLAT_DICT_DIFFERENT_KEY, False),
    (FLAT_DICT, FLAT_DICT_DIFFERENT_INT, False),
    (FLAT_DICT, FLAT_DICT_DIFFERENT_FLOAT, False),
    (FLAT_DICT, FLAT_DICT_DIFFERENT_BOOL, False),
    (FLAT_DICT, FLAT_DICT_DIFFERENT_STR, False),
    (FLAT_DICT, FLAT_DICT_DIFFERENT_VALUE_TYPE, False),

    (TWO_LEVEL_DICT, TWO_LEVEL_DICT, True),
    (TWO_LEVEL_DICT, TWO_LEVEL_DICT_ANOTHER, False),
    (NESTED_LIST_LIST, NESTED_LIST_LIST_ANOTHER, False),
    (NESTED_DICT_LIST, NESTED_DICT_LIST, True),
    (NESTED_DICT_LIST, NESTED_DICT_LIST_ANOTHER, False),
)


@pytest.mark.parametrize("first, second, expected", test_data)
def test_empty(first, second, expected):
    assert are_equal(first, second) == expected
