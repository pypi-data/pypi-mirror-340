from pathlib import Path

from ..drivers.s3 import _s3_module, S3Driver


if _s3_module.is_enabled():
    def get_last_modified_s3_prefix(s3_driver: S3Driver) -> str:
        objects = s3_driver.bucket.objects.filter()
        sorted_objects = sorted(objects, key = lambda obj: obj.last_modified, reverse = True)
        if len(sorted_objects) <= 0:
            raise ValueError("No objects found")

        # if no subfolders are found, list top level
        last_modified_prefix = ""
        for obj in sorted_objects:
            obj_parts = Path(obj.key).parts
            if len(obj_parts) > 1:
                last_modified_prefix = obj_parts[0]
                break

        return last_modified_prefix


    def list_last_modified_s3_prefix(s3_driver: S3Driver) -> list[Path]:
        last_modified_prefix = get_last_modified_s3_prefix(s3_driver)
        return s3_driver.source(last_modified_prefix)
else:
    get_last_modified_s3_prefix = _s3_module.broken_func("get_last_modified_s3_prefix")
    list_last_modified_s3_prefix = _s3_module.broken_func("list_last_modified_s3_prefix")
