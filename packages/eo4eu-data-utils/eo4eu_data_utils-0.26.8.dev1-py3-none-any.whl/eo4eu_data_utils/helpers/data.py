import functools
from eo4eu_base_utils.typing import Callable, Any, Dict


def _dict_like_predicate(item: Any, kwargs: Dict) -> bool:
    for key, val in kwargs.items():
        is_satisfied = False
        if callable(val):
            is_satisfied = val(item[key])
        elif isinstance(val, list) or isinstance(val, set):
            is_satisfied = item[key] in val
        else:
            is_satisfied = item[key] == val

        if not is_satisfied:  # all predicates must be true
            return False
    return True


def select(**kwargs) -> Callable[[Any],bool]:
    return functools.partial(_dict_like_predicate, kwargs = kwargs)


def _dict_like_attach(item: Any, kwargs: Dict) -> Any:
    for key, val in kwargs.items():
        if callable(val):
            item[key] = val(item)
        else:
            item[key] = val

    return item


def attach(**kwargs) -> Callable[[Any],Any]:
    return functools.partial(_dict_like_attach, kwargs = kwargs)
