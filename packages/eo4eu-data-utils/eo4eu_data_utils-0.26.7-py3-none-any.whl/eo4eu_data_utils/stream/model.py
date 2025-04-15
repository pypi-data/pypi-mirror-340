from pathlib import Path
from abc import ABC, abstractmethod
from eo4eu_base_utils import if_none
from eo4eu_base_utils.unify import overlay
from eo4eu_base_utils.typing import Self, Any, List, Dict, Iterator

from ..settings import Settings


class PathSpec:
    __slots__ = ("name", "path", "meta")

    def __init__(self, name: Path, path: Path, meta: dict[str,Any]):
        self.name = Path(name)
        self.path = Path(path)
        self.meta = meta

    def but(self, **kwargs) -> Self:
        return PathSpec(**({
            "name": self.name,
            "path": self.path,
            "meta": self.meta.copy(),
        } | kwargs))

    def __getitem__(self, name: str) -> Any:
        return self.meta[name]

    def __setitem__(self, name: str, val: Any):
        self.meta[name] = val

    def __repr__(self) -> str:
        return Settings.PATHSPEC_FORMATTER(self.name, self.path, self.meta)


class Data:
    __slots__ = ("passed", "failed", "kwargs")

    def __init__(
        self,
        passed: List[Any]|None = None,
        failed: List[Any]|None = None,
        kwargs: Dict[str,Any]|None = None
    ):
        self.passed = if_none(passed, [])
        self.failed = if_none(failed, [])
        self.kwargs = if_none(kwargs, {})

    @classmethod
    def empty(self) -> Self:
        return Data([], [], {})

    def but(self, **kwargs) -> Self:
        return Data(**({
            "passed": self.passed,
            "failed": self.failed,
            "kwargs": self.kwargs,
        } | kwargs))

    def __iter__(self) -> Iterator[Any]:
        for item in self.passed:
            yield item

    def iter_all(self) -> Iterator[Any]:
        for passed in self.passed:
            yield passed
        for failed in self.failed:
            yield failed

    def merge(self, other: Self) -> Self:
        return Data(
            passed = self.passed + other.passed,
            failed = self.failed + other.failed,
            kwargs = overlay(self.kwargs, other.kwargs)
        )

    def len(self) -> int:
        return len(self.passed)

    def stats(self) -> tuple[int,int]:
        return (len(self.passed), len(self.failed))

    def warn_stats(self) -> tuple[int,int]:
        return (len(self.failed), len(self.passed) + len(self.failed))

    def any_failed(self) -> bool:
        return len(self.failed) > 0

    def __repr__(self) -> str:
        return Settings.DATA_FORMATTER(
            self.passed, self.failed, self.kwargs
        )



class Action(ABC):
    @abstractmethod
    def act(self, input: Data) -> Data:
        return input
