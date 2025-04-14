import os
import re
from pathlib import Path
from abc import ABC, abstractmethod
from eo4eu_base_utils.typing import List, Dict, Any, Callable, Self


def _format_keys(keys: List[Any], sep: str = "."):
    return sep.join([str(key) for key in keys])


class SourceError(Exception):
    pass


class SimpleSource(ABC):
    @abstractmethod
    def get(self, keys: List[Any]) -> Any:
        return None


class SimpleFileSource(SimpleSource):
    def __init__(
        self,
        root: str|Path = "/",
        reader: Callable[[Path],Any]|None = None
    ):
        if reader is None:
            reader = lambda path: path.read_text()

        self._root = Path(root)
        self._reader = reader

    def get(self, keys: List[Any]) -> Any:
        path = self._root.joinpath(*keys)
        return self._reader(path)


class SimpleDictSource(SimpleSource):
    def __init__(self, data: Dict):
        self._data = data

    def get(self, keys: List[Any]) -> Any:
        result = self._data
        for key in keys:
            result = result[key]

        return result


class SimpleEnvSource(SimpleSource):
    def __init__(self, converter: Callable[[List[Any]],str]|None = None):
        non_alphanum_re = re.compile("[^a-zA-Z0-9_]")
        if converter is None:
            converter = lambda keys: "_".join([
                non_alphanum_re.sub("", str(key).replace("-", "_")).upper()
                for key in keys
            ])

        self._converter = converter

    def get(self, keys: List[Any]) -> Any:
        env_var = self._converter(keys)
        if env_var in os.environ:
            return os.environ[env_var]
        else:
            raise SourceError(f"Failed to find environment variable \"{env_var}\"")


# This class is a procedural alternative to the declarative
# "ConfigBuilder" class; it is much simpler
class ConfigSource:
    def __init__(self, sources: List[SimpleSource]|None = None):
        if sources is None:
            sources = []

        self._sources = sources

    def get(
        self,
        *keys: Any,
        apply: Callable[[Any],Any]|None = None
    ) -> Any:
        if apply is None:
            apply = lambda x: x

        errors = []
        for source in self._sources:
            try:
                return apply(source.get(keys))
            except Exception as e:
                errors.append(str(e))

        error_blurb = "\n\t".join(errors)
        raise SourceError(
            f"Failed to get \"{_format_keys(keys)}\":\n\t{error_blurb}"
        )

    def try_get(
        self,
        *keys: Any,
        default: Any = None,
        **kwargs
    ) -> Any:
        if "default" in kwargs:
            default = kwargs["default"]
            del kwargs["default"]

        try:
            return self.get(*keys, **kwargs)
        except Exception:
            return default

    def use(self, source: SimpleSource) -> Self:
        self._sources.append(source)
        return self

    def use_files(self, *args, **kwargs) -> Self:
        return self.use(SimpleFileSource(*args, **kwargs))

    def use_dict(self, *args, **kwargs) -> Self:
        return self.use(SimpleDictSource(*args, **kwargs))

    def use_env(self, *args, **kwargs) -> Self:
        return self.use(SimpleEnvSource(*args, **kwargs))
