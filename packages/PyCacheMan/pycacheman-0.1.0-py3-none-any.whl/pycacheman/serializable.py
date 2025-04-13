from __future__ import annotations

import datetime
from pathlib import Path

import mdit as mdit
import pkgdata
import pyserials
from loggerman import logger


class SerializableCacheManager:
    def __init__(
            self,
            retention_time: dict[str, datetime.timedelta],
            path: str | Path | None = None,
        ):
        def log_msg_new_cache(reason: str | None = None, traceback: bool = False):
            msg = (
                mdit.inline_container(
                    "The provided filepath ",
                    mdit.element.code_span(str(self._path)),
                    f" for control center cache {reason}. ",
                    "Initialized a new cache.",
                )
                if reason
                else "No filepath provided for control center cache. Initialized a new cache."
            )
            log_content = [msg]
            if traceback:
                log_content.append(logger.traceback())
            logger.warning(log_title, *log_content, stack_up=1)
            return


        self._path = Path(path).resolve() if path else None
        self._cache = {}
        self._retention_time = retention_time

        log_title = "Cache Initialization"

        if not self._path:
            log_msg_new_cache("is not defined")
            return
        if not self._path.exists():
            log_msg_new_cache("does not exist")
            return
        try:
            cache = pyserials.read.from_file(path=self._path)
        except pyserials.exception.read.PySerialsReadException as e:
            log_msg_new_cache("is corrupted", traceback=True)
            raise e
        try:
            pyserials.validate.jsonschema(
                data=cache,
                schema=pyserials.read.yaml_from_file(
                    path=pkgdata.get_package_path_from_caller(top_level=True) / "data" / "schema" / "serializable_cache.yaml"
                ),
            )
        except pyserials.exception.validate.PySerialsJsonSchemaValidationError as e:
            log_msg_new_cache("is invalid", traceback=True)
            raise e
        for key in cache:
            if key not in self._retention_time:
                raise ValueError(
                    f"Cache type '{key}' is not defined in retention time. Please check your configuration."
                )

        self._cache = cache
        logger.success(
            log_title,
            mdit.inline_container(
                "Loaded control center cache from ",
                mdit.element.code_span(str(self._path)),
            ),
        )
        return

    def get(self, typ: str, key: str):
        log_title = mdit.inline_container(
            "Cache Retrieval for ", mdit.element.code_span(f"{typ}.{key}")
        )
        if typ not in self._retention_time:
            logger.warning(
                log_title,
                mdit.inline_container(
                    "Retention time not defined for cache type ",
                    mdit.element.code_span(typ),
                    ". Skipped cache retrieval.",
                ),
            )
            return None
        item = self._cache.get(typ, {}).get(key)
        if not item:
            logger.info(log_title, "Item not found.")
            return None
        timestamp = item.get("timestamp")
        if timestamp and self._is_expired(typ, timestamp):
            logger.info(
                log_title,
                f"Item expired.\n- Timestamp: {timestamp}\n- Retention Hours: {self._retention_hours}",
            )
            return None
        logger.info(
            log_title,
            "Item found.",
            mdit.element.code_block(pyserials.write.to_yaml_string(item["data"]), language="yaml"),
        )
        return item["data"]

    def set(self, typ: str, key: str, value: dict | list | str | float | bool):
        new_item = {
            "timestamp": datetime.datetime.now(tz=datetime.UTC).isoformat(),
            "data": value,
        }
        self._cache.setdefault(typ, {})[key] = new_item
        logger.info(
            mdit.inline_container("Cache Set for ", mdit.element.code_span(f"{typ}.{key}")),
            mdit.element.code_block(pyserials.write.to_yaml_string(value), language="yaml"),
        )
        return

    def save(self):
        log_title = "Cache Save"
        if self._path:
            pyserials.write.to_yaml_file(
                data=self._cache,
                path=self._path,
                make_dirs=True,
            )
            logger.success(
                log_title,
                mdit.inline_container(
                    "Saved control center cache to ",
                    mdit.element.code_span(str(self._path)),
                ),
            )
        else:
            logger.warning(
                log_title, "No filepath provided for control center cache. Skipped saving cache."
            )
        return

    def _is_expired(self, typ: str, timestamp: str) -> bool:
        time_delta = self._retention_time[typ]
        if not time_delta:
            return False
        exp_date = datetime.datetime.fromisoformat(timestamp).astimezone(datetime.UTC) + time_delta
        return exp_date <= datetime.datetime.now(tz=datetime.UTC)
