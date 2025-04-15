from eo4eu_base_utils.typing import Dict, Any, Self


class SafeDict:
    def __init__(self, attrs: Dict, default: Any):
        self._attrs = attrs
        self._default = default

    def __getitem__(self, name: str) -> Any:
        return self._attrs.__getitem__(name)

    def __setitem__(self, name: str, value: Any) -> Any:
        return self._attrs.__setitem__(name, value)

    def get(self, name: str, default_key: str = None) -> Any:
        try:
            return self._attrs[name]
        except KeyError:
            if default_key is None:
                return self._default
            try:
                return self._attrs[default_key]
            except KeyError:
                return self._default

    def set_default(self, default: Any) -> Self:
        self._default = default
        return self
