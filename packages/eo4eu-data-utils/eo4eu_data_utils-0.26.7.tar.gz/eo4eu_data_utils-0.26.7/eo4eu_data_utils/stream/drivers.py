from pathlib import Path
from abc import ABC, abstractmethod
from eo4eu_base_utils import OptionalModule, if_none
from eo4eu_base_utils.typing import Any, Callable, Self, List

from .model import PathSpec


class Downloader(ABC):
    @abstractmethod
    def download(self, src: Path, dst: Path) -> Path:
        pass


class Uploader(ABC):
    @abstractmethod
    def upload(self, src: Path, dst: Path) -> Path:
        pass


class Lister(ABC):
    @abstractmethod
    def ls(self, src: Path) -> List[PathSpec]:
        return []


class LocalDriver(Lister):
    def __init__(self, root: Path|str = ""):
        self._root = Path(root).absolute()

    def ls(self, src: Path) -> List[PathSpec]:
        return [
            PathSpec(name = path, path = path, meta = {})
            for path in self._root.joinpath(src).rglob("*")
        ]


_s3_module = OptionalModule(
    package = "eo4eu_data_utils",
    enabled_by = ["s3", "full"],
    depends_on = ["boto3"]
)


if _s3_module.is_enabled():
    import boto3

    class S3Driver(Downloader, Uploader, Lister):
        def __init__(
            self,
            config: dict[str,str],
            bucket: str,
            ls_func: Callable[[Any],PathSpec]|None = None
        ):
            ls_func = if_none(ls_func, lambda summary: PathSpec(
                name = Path(summary.key),
                path = Path(summary.key),
                meta = {}
            ))

            self.resource = boto3.resource("s3", **config)
            self.bucket = self.resource.Bucket(bucket)
            self.bucket_name = bucket
            self._ls_func = ls_func

        def upload(self, src: Path, dst: Path):
            self.bucket.upload_file(str(src), str(dst))
            return dst

        def download(self, src: Path, dst: Path):
            dst.parent.mkdir(parents = True, exist_ok = True)
            self.bucket.download_fileobj(str(src), dst.open("wb"))
            return dst

        def ls(self, src: Path) -> list[PathSpec]:
            return [
                self._ls_func(summary)
                for summary in self.list_objects(src)
            ]

        def list_objects(self, input_path: Path) -> list[Any]:
            input_path_str = str(input_path)
            if input_path_str == ".":
                input_path_str = ""
            elif input_path_str.startswith("./"):
                input_path_str = input_path_str[2:]

            return [
                summary
                for summary in self.bucket.objects.filter(Prefix = input_path_str)
                if summary.key != input_path_str and summary.key != f"{input_path_str}/"
            ]

        def upload_bytes(self, key: str|Path, data: bytes):
            self.bucket.put_object(Key = str(key), Body = data)

        def download_bytes(self, key: str|Path) -> bytes:
            return self.resource.Object(self.bucket_name, str(key)).get()["Body"].read()
else:
    S3Driver = _s3_module.broken_class("S3Driver")
