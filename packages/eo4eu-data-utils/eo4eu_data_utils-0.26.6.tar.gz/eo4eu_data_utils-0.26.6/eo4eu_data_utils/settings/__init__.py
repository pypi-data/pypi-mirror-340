import logging
import functools
from pprint import pformat
from eo4eu_base_utils.typing import List, Dict, Any

from .safe_dict import SafeDict
from .data import (
    recover_soft_fail,
    recover_raise_exc,
    recover_continue,
)
from ..helpers import (
    trim_root,
    format_list,
    shortest_unique,
    unique_sort_match,
    strict_distance,
    simple_distance,
    group_distance,
)

logger = logging.getLogger("eo4eu.data")
logger.setLevel(logging.INFO)


def _default_error_callback(item, exc, name, level):
    logger.log(
        level,
        f"Failed to {name} \"{item}\": {exc}"
    )


def _default_pathspec_formatter(name: str, path: str, meta: dict):
    try:
        name_is_in_path = path.match(name)
        if name_is_in_path:
            name_str = str(name)
            start = str(path)[::-1][len(name_str):][::-1]
            return f"{start}({name_str})"
        else:
            return f"{path}:({name})"
    except Exception as e:
        return f"[Failed to format path: {e}]"


def _default_data_formatter(passed: List[Any], failed: List[Any], kwargs: Dict):
    return "\n".join([
        format_list("passed: ", passed),
        format_list("failed: ", failed),
        f"kwargs: {pformat(kwargs)}",
    ])


class Settings:
    LOGGER = logger

    RENAME_METHODS = SafeDict({
        "trim_root":       trim_root,
        "shortest_unique": shortest_unique,
    }, default = shortest_unique)

    FILL_META_METHODS = SafeDict({
        "unique_sort_match": unique_sort_match,
    }, default = unique_sort_match)

    STRING_DISTANCE_METHODS = SafeDict({
        "strict_distance": strict_distance,
        "simple_distance": simple_distance,
        "group_distance":  group_distance,
    }, default = group_distance)

    RECOVERY_METHODS = SafeDict({
        "soft_fail": recover_soft_fail,
        "raise_exc": recover_raise_exc,
        "continue":  recover_continue,
    }, default = recover_soft_fail)

    PATHSPEC_FORMATTER = _default_pathspec_formatter

    DATA_FORMATTER = _default_data_formatter

    @classmethod
    def make_default_err_callback(cls, name: str, level: int = logging.WARNING):
        return functools.partial(
            _default_error_callback,
            name = name,
            level = level
        )
