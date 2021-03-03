import json
import math


def jsons_equal(first: str, second: str) -> bool:
    """Takes two JSON strings and
    returns whether objects they represent are equal"""
    first_parsed = json.loads(first)
    second_parsed = json.loads(second)
    return are_equal(first_parsed, second_parsed)


def are_equal(first, second) -> bool:
    if type(first) != type(first):
        return False
    if isinstance(first, float):
        return math.isclose(first, second, rel_tol=1e-05, abs_tol=1e-05)
    elif isinstance(first, list):
        return len(first) == len(second) and all(map(are_equal, first, second))
    elif isinstance(first, dict):
        return first.keys() == second.keys() and \
               all(map(
                   lambda key: are_equal(first[key], second[key]),
                   first.keys()
               ))
    return first == second
