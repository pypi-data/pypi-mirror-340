"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import re
import sys
import logging
from typing import TYPE_CHECKING, Any
from pathlib import Path
import weakref
# * Gid Imports ----------------------------------------------------------------------------------------->
from gidapptools.gid_logger.logger import get_logger, get_meta_logger

# * Type-Checking Imports --------------------------------------------------------------------------------->
if TYPE_CHECKING:
    from gidapptools.gid_logger.records import LOG_RECORD_TYPES

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


class ProhibitiveSingletonMeta(type):
    _instance = None

    def _unset_instance(cls, *args, **kwargs) -> None:
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is not None and cls._instance() is not None:
            raise RuntimeError(f"There can only be one instance of {cls.__name__}")
        instance = super(ProhibitiveSingletonMeta, cls).__call__(*args, **kwargs)
        cls._instance = weakref.proxy(instance, cls._unset_instance)

        return instance


class QtMessageHandler(metaclass=ProhibitiveSingletonMeta):
    received_records: list["LOG_RECORD_TYPES"] = []
    __slots__ = ("msg_split_regex",
                 "is_installed",
                 "_old_messagehandler",
                 "__weakref__")

    def __init__(self) -> None:
        self.msg_split_regex = re.compile(r"(?P<q_class>.*)\:\:(?P<q_method>.*)\:(?P<actual_message>.*)")
        self.is_installed: bool = False
        self._old_messagehandler = None

    def install(self, overwrite_install: bool = False) -> "QtMessageHandler":
        if self.is_installed is True and overwrite_install is False:
            return self
        from PySide6.QtCore import qInstallMessageHandler
        self._old_messagehandler = qInstallMessageHandler(self)
        self.is_installed = True

        return self

    def mode_to_log_level(self, in_mode):
        in_mode = str(in_mode).rsplit('.', maxsplit=1)[-1].strip().removeprefix("Qt").removesuffix("Msg").upper()
        if in_mode == "FATAL":
            in_mode = "ERROR"
        elif in_mode == "SYSTEM":
            in_mode = "INFO"

        elif in_mode.isnumeric():
            _in_mode = int(in_mode)
            if _in_mode < 10:
                _in_mode = _in_mode * 10
            return _in_mode
        return logging.getLevelNamesMapping()[in_mode]

    def get_context(self, in_context: None):
        _logger = None
        frame_count = 2
        _context_data = None

        if all(_context_attr is not None for _context_attr in (in_context.file, in_context.function, in_context.line)):
            _context_data = {"fn": in_context.file,
                             "func": in_context.function,
                             "lno": in_context.line}

        while _logger is None:
            # if frame_count >= 50:
            #     break
            try:
                frame = sys._getframe(frame_count)
                if frame is None:
                    raise RuntimeError(f"unable to get a frame for {in_context!r}")

                _context_data = {"fn": in_context.file or frame.f_code.co_filename,
                                 "func": in_context.function or frame.f_code.co_name,
                                 "lno": in_context.line or frame.f_lineno}

                _logger = get_logger(frame.f_globals["__name__"])
            except AttributeError:
                frame_count = frame_count + 1

            except Exception as e:

                break
        if _context_data is None:
            raise RuntimeError(f"unable to get a frame for {in_context!r}")
        return _context_data, _logger or get_meta_logger()

    def modify_message(self, in_msg: str) -> str:

        if re_match := self.msg_split_regex.match(in_msg):
            named_parts = re_match.groupdict()
            _message = named_parts.pop("actual_message").strip()
            return _message, {"is_qt": True} | named_parts

        return in_msg, {"is_qt": True}

    def __call__(self, mode, context, message) -> Any:
        try:
            context_data, logger = self.get_context(context)
        except Exception as e:
            logger = get_meta_logger()
            logger.error("encountered Error %r while trying to log QT-Message %r", e, message, exc_info=True)
            return
        log_level = self.mode_to_log_level(mode)
        msg, extras = self.modify_message(message)
        record = logger.makeRecord(logger.name, log_level, msg=msg, extra=extras, exc_info=None, args=None, ** context_data)
        logger.handle(record)
        self.received_records.append(record)


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]
