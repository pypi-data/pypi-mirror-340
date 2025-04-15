from pathlib import Path
from eo4eu_base_utils import if_none
from eo4eu_base_utils.typing import List, Any


def format_list(prefix: str, items: List[Any]) -> str:
    spaces = " " * len(prefix)
    if len(items) == 0:
        return f"{prefix}[]"
    if len(items) == 1:
        return f"{prefix}{items[0]}"

    head, tail = items[0], items[1:]
    return f"{prefix}{head}\n" + "\n".join([
        f"{spaces}{item}"
        for item in tail
    ])


def _get_idx_of_last_common_part(path_parts_list: List[List[str]]) -> int:
    max_len = max([len(parts) for parts in path_parts_list])
    for idx in range(max_len):
        parts = set()
        for path_parts in path_parts_list:
            if len(path_parts) <= idx:  # a path ends before this part
                return idx

            parts.add(path_parts[idx])
            if len(parts) > 1:  # two paths are not the same
                return idx
    return 0


# Returns the given paths starting from the deepest COMMON directory
def trim_root(paths: List[Path]) -> List[Path]:
    if len(paths) == 0:
        return paths
    if len(paths) == 1:
        return [Path(paths[0].name)]

    path_parts_list = [path.parts for path in paths]
    last_common_part_idx = _get_idx_of_last_common_part(path_parts_list)
    if last_common_part_idx == 0:
        return paths

    return [
        Path("").joinpath(*[
            part for part in path.parts[last_common_part_idx:]
        ])
        for path in paths
    ]


def _get_shortest_unique(
    parts_list: List[tuple[int,List[str]]],
    aggregator: List[str]
) -> List[str]:
    unique_parts = {}
    for idx, (orig_idx, parts) in enumerate(parts_list):
        first_part = parts[0]
        if first_part not in unique_parts:
            unique_parts[first_part] = [idx]
        else:
            unique_parts[first_part].append(idx)

    next_parts_list = []
    for name, indices in unique_parts.items():
        if len(indices) == 1:  # the path is unique, life is good
            orig_idx = parts_list[indices[0]][0]
            aggregator[orig_idx] = name
        else:
            for idx in indices:
                orig_idx, parts = parts_list[idx]
                if len(parts) <= 1:  # give up trying to make them shorter
                    aggregator[orig_idx] = parts[0]
                else:
                    next_parts_list.append((
                        orig_idx,
                        [f"{parts[1]}/{parts[0]}"] + parts[2:]
                    ))

    if len(next_parts_list) > 0:
        _get_shortest_unique(next_parts_list, aggregator)

    return aggregator


# Returns the given paths matching each to the shortest unique subpath
# Basically looks at path names, and if two paths have the same name,
# it moves back one directory until they become unique. If two or more
# paths are the same, it doesn't change them.
# This is more effective but less predictable than "trim_root"
# It does NOT preserve the folder structure!!
def shortest_unique(paths: List[Path]) -> List[Path]:
    parts_list = [list(path.parts)[::-1] for path in paths]
    if min([len(parts) for parts in parts_list]) <= 0:
        return paths

    return [
        Path(path_str)
        for path_str in _get_shortest_unique(
            parts_list = [(idx, part) for idx, part in enumerate(parts_list)],
            aggregator = [None for _ in parts_list]
        )
    ]


def _preprocess_distance_matrix(
    distance_matrix: List[List[float]],
    offset = 1
) -> tuple[int,List[List[float]]]:
    max_distance = max([max(distances) for distances in distance_matrix])
    invalid_value = int(max_distance + offset)

    return (invalid_value, [
        [
            distance if distance >= 0 else invalid_value
            for distance in distances
        ]
        for distances in distance_matrix
    ])


def unique_sort_match(distance_matrix: List[List[float]]) -> List[int]:
    if len(distance_matrix) == 0 or len(distance_matrix[0]) == 0:
        return []

    invalid_value, dist_matrix = _preprocess_distance_matrix(distance_matrix)
    result = [-1 for _ in dist_matrix]

    sorted_distances = [
        [
            idx,
            sorted(distances),
            sorted(range(len(distances)), key = distances.__getitem__),
        ]
        for idx, distances in enumerate(dist_matrix)
    ]

    for level in range(len(dist_matrix[0])):
        sorted_distances.sort(key = lambda item: item[1][level])

        for idx, distances, match_indices in sorted_distances:
            if result[idx] >= 0:  # the entry has already been filled
                continue

            match_idx = match_indices[level]
            distance = distances[level]
            if match_idx in result or distance == invalid_value:
                continue

            result[idx] = match_idx

    return result


def _get_appropriate_path_part(
    id_str: str,
    path: Path,
    sep: str = "/",
    ljust = True
) -> tuple[str,str,bool]:
    num_elem = id_str.count(sep) + 1
    start_idx = len(path.parts) - num_elem
    if start_idx < 0:
        start_idx = 0

    result = sep.join(path.parts[start_idx:])
    if len(result) == len(id_str):
        return (id_str, result, True)

    length = max([len(result), len(id_str)])
    if ljust:
        return (id_str.ljust(length), result.ljust(length), False)
    else:
        return (id_str.rjust(length), result.rjust(length), False)


def _wrap_dist_func(id_str: str, path: Path, sep: str, func, **kwargs):
    id_str, part, same_lengths = _get_appropriate_path_part(id_str, path, sep)
    left_dist = func(id_str, part, **kwargs)
    if same_lengths:
        return left_dist / len(id_str)
    else:
        id_str, part, _ = _get_appropriate_path_part(id_str, path, sep, ljust = False)
        right_dist = func(id_str, part, **kwargs)

        return min(left_dist, right_dist) / len(id_str)


def _char_dist_basic(c0: str, c1: str) -> float:
    if c0 == c1:
        return 0.0
    elif c0.lower() == c1.lower():
        return 0.25
    elif c0.casefold() == c1.casefold():
        return 0.5
    else:
        return 1.0


def strict_distance(id_str: str, path: Path, sep: str = "/") -> float:
    id_str, part, _ = _get_appropriate_path_part(id_str, path, sep)
    return 0 if part == id_str else -1


def _simple_distance(
    id_str: str,
    part: str,
    char_dist_func = None
) -> float:
    char_dist_func = if_none(char_dist_func, _char_dist_basic)
    return sum([
        char_dist_func(id_char, path_char)
        for id_char, path_char in zip(id_str, part)
    ])


def _group_distance(
    id_str: str,
    part: str,
    char_dist_func = None,
    tolerance = 1e-6
) -> float:
    char_dist_func = if_none(char_dist_func, _char_dist_basic)

    group_lengths = []
    current_group_length = 0
    total_dist = 0
    for id_char, path_char in zip(id_str, part):
        dist = char_dist_func(id_char, path_char)
        total_dist += dist

        if dist < tolerance:
            current_group_length += 1
        elif current_group_length > 0:
            # larger groups are rewarded
            group_lengths.append(current_group_length ** 2)
            current_group_length = 0

    if current_group_length > 0:
        group_lengths.append(current_group_length ** 2)

    try:
        return 10 * (total_dist ** 0.5) / sum(group_lengths)
    except Exception as e:
        return 10 * (total_dist ** 0.5)


def simple_distance(id_str: str, path: Path, sep = "/", **kwargs):
    return _wrap_dist_func(id_str, path, sep, _simple_distance, **kwargs)


def group_distance(id_str: str, path: Path, sep = "/", **kwargs):
    return _wrap_dist_func(id_str, path, sep, _group_distance, **kwargs)
