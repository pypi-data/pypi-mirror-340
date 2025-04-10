"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import inspect
import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union, Literal, Iterable
from pathlib import Path
from datetime import datetime, timezone, timedelta

# * Third Party Imports --------------------------------------------------------------------------------->
from tzlocal import get_localzone

# * Gid Imports ----------------------------------------------------------------------------------------->
from gidapptools.gid_logger.enums import LoggingLevel, LoggingSectionAlignment
from gidapptools.general_helper.string_helper import StringCase, StringCaseConverter

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


def get_all_func_names(file: Path, recursive: bool = True):
    import ast

    def _get_names(source_file: Path) -> list[str]:
        root = ast.parse(source_file.read_text(encoding='utf-8', errors='ignore'))
        return sorted({node.name for node in ast.walk(root) if isinstance(node, ast.FunctionDef)})

    def _process_item(_item: Path):
        if _item.is_file() and _item.suffix == '.py':

            yield _get_names(_item)

        elif _item.is_dir():
            for _sub_item in _item.iterdir():
                yield from _process_item(_sub_item)
    if recursive is False:
        names = _get_names(file)
    else:
        names = []
        for _names in _process_item(file.parent):
            names += _names
    return sorted(set(names), key=len)


def get_all_module_names(file: Path) -> list[str]:

    def _get_module_name(_item: Path) -> str:
        module_name = _item.stem
        return module_name

    def _process_item(_item: Path):
        if _item.is_file() and _item.suffix == '.py':
            yield _get_module_name(_item)
        elif _item.is_dir():
            for _sub_item in _item.iterdir():
                yield from _process_item(_sub_item)

    if file.is_file():
        file = file.parent
    return sorted({i for i in _process_item(file)}, key=len)


class AbstractLoggingStyleSection:
    default_alignment: LoggingSectionAlignment = LoggingSectionAlignment.LEFT
    default_width: int = 0
    default_text: str = str(None)

    __slots__ = ("position",
                 "width",
                 "alignment")

    def __init__(self,
                 position: int = None,
                 width: int = None,
                 alignment: Union[LoggingSectionAlignment, str] = None) -> None:
        self.position = position
        self.width = width or self.default_width

        if alignment is None:
            self.alignment = self.default_alignment
        elif isinstance(alignment, str):
            self.alignment = LoggingSectionAlignment(alignment)
        else:
            self.alignment = alignment

    @abstractmethod
    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:
        ...

    def align(self, text: str) -> str:
        width = self.width() if callable(self.width) else self.width
        if len(text) > width:
            text = '...' + text[-(width - 3):]
        return self.alignment.align(text, width)

    def format(self, record: "LOG_RECORD_TYPES") -> str:
        try:
            text = str(self.get_formated_value(record=record))
        except AttributeError:
            text = self.default_text
        return self.align(text)

    @classmethod
    def ___section_name___(cls) -> str:
        return StringCaseConverter.convert_to(cls.__name__.removesuffix("Section"), StringCase.SNAKE)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(position={self.position!r})"


class TimeSection(AbstractLoggingStyleSection):

    local_timezone: timezone = get_localzone()
    default_time_format = '%Y-%m-%d %H:%M:%S'
    default_msec_format = '.{msec:03.0f}'
    default_alignment: LoggingSectionAlignment = LoggingSectionAlignment.LEFT

    __slots__ = ("time_zone",
                 "time_format",
                 "msec_format")

    def __init__(self,
                 position: int = None,
                 time_zone: timezone = None,
                 time_format: str = None,
                 msec_format: str = None,
                 width: int = None,
                 alignment: Union[LoggingSectionAlignment, str] = None) -> None:
        super().__init__(position=position, alignment=alignment)

        self.time_zone = time_zone
        self.time_format = time_format or self.default_time_format
        self.msec_format = msec_format or self.default_msec_format

        self.width = width or (len(self.time_format) + len(self.msec_format.format(msec=0)) + self._get_time_zone_width() + 2)

    def _get_time_zone_width(self) -> int:
        time_zone_width = 1
        if self.time_zone is not None:
            time_zone_width += len(self.time_zone.tzname(datetime.now()))
        else:
            time_zone_width += len(get_localzone().tzname(datetime.now()))

        return time_zone_width

    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:
        time_value = datetime.fromtimestamp(record.created, tz=self.local_timezone)
        msec_value = record.msecs
        msec_string = self.msec_format.format(msec=msec_value).strip()
        if msec_string == ".1000":
            msec_string = ".000"
            time_value = time_value + timedelta(seconds=1)
        if self.time_zone is not None:
            time_value = time_value.replace(tzinfo=self.time_zone)
        if self.time_format.casefold() == "isoformat":
            return time_value.isoformat(timespec='seconds') + self.msec_format.format(msec=msec_value)
        return (time_value.strftime(self.time_format) + msec_string + time_value.strftime(" %Z")).strip()


class LevelSection(AbstractLoggingStyleSection):
    default_case: StringCase = StringCase.UPPER
    default_alignment: LoggingSectionAlignment = LoggingSectionAlignment.LEFT_EXTRA_PADDED_ONCE
    default_width: int = max(len(i) for i in LoggingLevel._member_names_) + 2
    __slots__ = ("case",
                 "_formated_value_cache")

    def __init__(self,
                 position: int = None,
                 case: StringCase = None,
                 width: int = None,
                 alignment: Union[LoggingSectionAlignment, str] = None) -> None:
        super().__init__(position=position, alignment=alignment, width=width)
        if case is None:
            self.case = self.default_case
        elif isinstance(case, str):
            self.case = StringCase(case)
        else:
            self.case = case

        self._formated_value_cache: dict[str, str] = {}

    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:
        try:
            is_qt = record.extras["is_qt"]

        except (AttributeError, KeyError):
            is_qt = False

        raw_level_name = record.levelname

        if is_qt is True:
            raw_level_name = "Qt_" + raw_level_name

        try:
            return self._formated_value_cache[raw_level_name]
        except KeyError:
            formated_level_name = StringCaseConverter.convert_to(raw_level_name, self.case)
            self._formated_value_cache[raw_level_name] = formated_level_name

            return formated_level_name


class ThreadSection(AbstractLoggingStyleSection):
    default_alignment: LoggingSectionAlignment = LoggingSectionAlignment.CENTER
    default_width: int = 20
    __slots__ = tuple()

    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:
        return record.threadName


class LineNumberSection(AbstractLoggingStyleSection):
    default_alignment: LoggingSectionAlignment = LoggingSectionAlignment.CENTER
    default_width: int = 5
    __slots__ = tuple()

    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:
        return record.lineno


class PathSection(AbstractLoggingStyleSection):
    default_alignment: LoggingSectionAlignment = LoggingSectionAlignment.LEFT
    __slots__ = ("with_extension",
                 "_width_cache")

    def __init__(self,
                 position: int = None,
                 with_extension: bool = True,
                 width: int = None,
                 alignment: Union[LoggingSectionAlignment, str] = None) -> None:
        super().__init__(position=position, width=self.width_from_env, alignment=alignment)
        self.with_extension = with_extension
        self._width_cache: int = width or None

    def width_from_env(self) -> int:
        if self._width_cache is None:
            self._width_cache = int(os.getenv("MAX_MODULE_NAME_LEN", "20"))
        return self._width_cache

    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:
        if record.extras.get("file_path", None) is not None:
            path = Path(record.extras["file_path"]).resolve()
        else:
            path = Path(record.pathname).resolve()
        if os.getenv("_MAIN_DIR", None) is not None:
            path = path.relative_to(Path(os.getenv("_MAIN_DIR")).resolve())
        if self.with_extension is False:
            path = path.with_suffix('')

        return './' + path.as_posix()


class LoggerNameSection(AbstractLoggingStyleSection):
    default_alignment: LoggingSectionAlignment = LoggingSectionAlignment.LEFT
    default_width: int = 20
    __slots__ = tuple()

    def __init__(self,
                 position: int = None,
                 width: int = None,
                 alignment: Union[LoggingSectionAlignment, str] = None) -> None:
        super().__init__(position=position, width=width, alignment=alignment)

    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:
        if record.extras.get("module", None) is not None:
            return record.extras["module"]
        return record.name


class FunctionNameSection(AbstractLoggingStyleSection):
    default_alignment: LoggingSectionAlignment = LoggingSectionAlignment.LEFT
    default_width: int = 20
    default_text: str = "-"
    __slots__ = tuple()

    def __init__(self, width: int = None) -> None:
        super().__init__(width=width)

    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:
        if record.funcName == "<module>":
            return self.default_text
        if record.extras.get("function_name", None) is not None:
            return record.extras["function_name"]
        return record.funcName


class ExtrasSection(AbstractLoggingStyleSection):
    __slots__ = tuple()

    def __init__(self) -> None:
        super().__init__(width=100)

    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:
        try:
            extras = record.extras
        except AttributeError:
            return ""

        return ' + '.join(f"{k}={v!r}" for k, v in extras.items())


class PackageNameSection(AbstractLoggingStyleSection):
    __slots__ = tuple()

    def __init__(self,
                 position: int = None,
                 width: int = None,
                 alignment: Union[LoggingSectionAlignment, str] = None) -> None:
        super().__init__(position, width or 12, alignment)

    def get_formated_value(self, record: "LOG_RECORD_TYPES") -> str:

        name_parts = record.name.split('.')

        package_name = name_parts[0]

        try:
            if record.extras.get("is_qt", False) is True:
                package_name = "Qt"
        except AttributeError:
            pass
        return package_name


class AbstractSectionLoggingStyle(ABC):
    default_separator: str = " | "
    default_message_start_indicator: str = ' ||--> '
    __slots__ = ("sections",
                 "sorted_sections",
                 "separator",
                 "message_start_indicator",
                 "message_section")

    def __init__(self, sections: Iterable[Union[str, AbstractLoggingStyleSection]], separator: str = None, message_start_indicator: str = None, message_section: AbstractLoggingStyleSection = None):
        self.sections = self._handle_sections(sections)
        self.sorted_sections: tuple[AbstractLoggingStyleSection] = self.sort_sections()
        self.separator = separator or self.default_separator
        self.message_start_indicator = message_start_indicator or self.default_message_start_indicator
        self.message_section = message_section

    def _handle_sections(self, sections: Iterable[Union[str, AbstractLoggingStyleSection]]) -> tuple[AbstractLoggingStyleSection]:
        _out = []
        for section in sections:
            if isinstance(section, str):
                section = self.all_section_classes[section]()
            if inspect.isclass(section):
                section = section()
            _out.append(section)
        return tuple(_out)

    def sort_sections(self) -> tuple[AbstractLoggingStyleSection]:
        temp_sorted = [i[0] for i in sorted([(v, idx) for idx, v in enumerate(self.sections)], key=lambda x: (x[0].position, x[1]))]
        for idx, sect in enumerate(temp_sorted):
            if sect.position is None:
                sect.position = idx
        return tuple(temp_sorted)

    def usesTime(self) -> bool:
        return False

    @ abstractmethod
    def validate(self) -> None:
        ...

    @ abstractmethod
    def _format(self, record: "LOG_RECORD_TYPES") -> str:
        ...

    def format(self, record: "LOG_RECORD_TYPES"):
        return self._format(record)

    @classmethod
    def all_section_classes(cls) -> dict[str, type[AbstractLoggingStyleSection]]:
        _out = {}
        for klass in AbstractLoggingStyleSection.__subclasses__():
            _out[klass.___section_name___] = klass
        return _out


class GidSectionLoggingStyle(AbstractSectionLoggingStyle):
    __slots__ = tuple()

    def validate(self) -> None:
        if any(isinstance(i, AbstractLoggingStyleSection) is False for i in self.sections):
            raise ValueError("invalid format")

    def _format(self, record: "LOG_RECORD_TYPES") -> str:

        message_part = record.getMessage() if self.message_section is None else self.message_section.format(record)

        return self.separator.join(section.format(record) for section in self.sorted_sections) + self.message_start_indicator + message_part


class GidLoggingFormatter(logging.Formatter):
    default_fmt = (TimeSection(), LineNumberSection(), LevelSection(), ThreadSection(), PackageNameSection(), LoggerNameSection(), FunctionNameSection())

    def __init__(self,
                 fmt: Union[str, Iterable[Union[str, AbstractLoggingStyleSection]]] = None,
                 style: Literal["section", "$", "{", "$"] = "section",
                 validate: bool = False,
                 **kwargs) -> None:
        if style == "section":
            if fmt is None:
                fmt = self.default_fmt
            self._style = GidSectionLoggingStyle(sections=fmt, separator=kwargs.pop("separator", None), message_start_indicator=kwargs.pop("message_start_indicator", None), message_section=kwargs.pop("message_section", None))
        else:
            self._style = logging._STYLES[style][0](fmt)
            if validate:
                self._style.validate()

            self._fmt = self._style._fmt
            self.datefmt = kwargs.pop("datefmt", None)

    def set_time(self, record: "LOG_RECORD_TYPES") -> "LOG_RECORD_TYPES":
        return record

    def format_message(self, record: "LOG_RECORD_TYPES") -> str:
        return self.formatMessage(record=record)

    def format_stack(self, stack_info):
        return self.formatStack(stack_info=stack_info)

    def format_exception(self, record: "LOG_RECORD_TYPES") -> "LOG_RECORD_TYPES":
        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(ei=record.exc_info)
        return record

    def modify_meta_record(self, record: "LOG_RECORD_TYPES") -> "LOG_RECORD_TYPES":

        if getattr(record, "is_meta", False) is False:
            return record

        record.name = "__META__"
        record.module = "-"
        record.funcName = "-"
        record.lineno = "-"
        extras = getattr(record, "extras", {})
        extras["module"] = "-"
        record.extras = extras
        return record

    def format(self, record: "LOG_RECORD_TYPES") -> str:
        record = self.set_time(record=record)
        record = self.modify_meta_record(record)
        text = self.format_message(record=record)
        record = self.format_exception(record=record)
        if record.exc_text:
            if text[-1:] != "\n":
                text = text + "\n"
            text = text + record.exc_text
        if record.stack_info:
            if text[-1:] != "\n":
                text = text + "\n"
            text = text + self.format_stack(record.stack_info)
        return text

# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]
