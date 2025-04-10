"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import importlib.util
import os
from typing import TYPE_CHECKING, Any, Union, Literal, Hashable, Iterable, Optional
from pathlib import Path
from datetime import timezone, datetime
from contextlib import contextmanager
import inspect
import sys
import importlib
# * Type-Checking Imports --------------------------------------------------------------------------------->
if TYPE_CHECKING:
    from gidapptools.general_helper.date_time import DateTimeFrame
    from gidapptools.gid_config.parser.config_data import ConfigData
    from gidapptools.gid_config.conversion.spec_item import SpecEntry
    from gidapptools.meta_data.meta_paths.meta_paths_item import NamedMetaPath

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


def show_basic_error_pop_up(message: str, title: str = None) -> None:
    from tkinter import messagebox
    messagebox.showerror(title=title or "Error", message=message)


class GidAppToolsBaseError(Exception):
    """
    Base Exception For GidAppTools.
    """


class GidAppToolsFatalError(RuntimeError):
    ...


class ConversionError(GidAppToolsBaseError):
    ...


class NotUsableError(GidAppToolsBaseError):

    def __init__(self,
                 subject: object | type,
                 reason: Literal["unfinished", "broken", "unknown"] | None = None) -> None:
        self.subject = subject
        self.reason = reason if reason is not None else "unknown"
        self.msg = f"{self.subject!r} is not usable, reason: {self.reason!r}."
        super().__init__(self.msg)


class ApplicationInstanceAlreadyRunningError(GidAppToolsFatalError):
    def __init__(self, app_name: str, running_pid: int) -> None:
        self.app_name = app_name
        self.running_pid = running_pid
        os.environ["FATAL_ERROR_RAISED"] = "1"
        super().__init__(f"There is already an instance of {self.app_name!r} running with the pid of {self.running_pid!r}.")


class MissingOptionalDependencyError(GidAppToolsBaseError):
    _checked_import_names: dict[str, tuple[Path, int]] = {}

    def __init__(self, dependency_name: str, package_name: str = None) -> None:
        self.dependency_name = dependency_name
        self.package_name = package_name
        self.msg = f"Missing optional dependency {self.dependency_name!r}"
        if self.package_name is not None:
            self.msg += f", try installing by doing 'pip install -U {self.package_name!s}'"
        elif self.package_name == self.dependency_name:
            self.msg += f", try installing by doing 'pip install -U {self.package_name!s}[{self.dependency_name!s}]'"
        self.msg += "."
        super().__init__(self.msg)

    @classmethod
    @contextmanager
    def try_import(cls, package_name: str = None):
        try:
            yield
        except (ImportError, ModuleNotFoundError) as e:
            if e.path is None:
                dependency_name = e.name
                raise cls(dependency_name=dependency_name, package_name=package_name)

            raise e

    @classmethod
    def check_is_importable(cls, package_name: str, install_name: str | None = None):
        if os.getenv("is_dev", "false") != "false":

            _frame_info = inspect.stack()[1]

            cls._checked_import_names[install_name or package_name] = (Path(_frame_info.filename).resolve(), _frame_info.lineno, inspect.getmodule(_frame_info[0]).__name__)
        try:
            importlib.import_module(package_name)

        except (ImportError, ModuleNotFoundError) as e:

            if e.path is None:
                e.__suppress_context__ = True
                raise cls(dependency_name=e.name, package_name=install_name or package_name)

            raise e

    @classmethod
    def get_all_optional_imports(cls, package_dir: Path, package_name: str = None):

        import pkgutil

        for loader, module_name, is_pkg in pkgutil.walk_packages([package_dir], prefix=f"{package_name}." if package_name is not None else "", onerror=lambda x: ...):
            ...

        return cls._checked_import_names.copy()


class FlagConflictError(GidAppToolsBaseError):
    def __init__(self, flag_names: Iterable[str], conflicting_bool_value: bool = True):
        self.flag_names = tuple(flag_names)
        self.conflicting_bool_value = conflicting_bool_value
        self.msg = self._build_msg()

        super().__init__(self.msg)

    def _build_msg(self) -> str:
        text = "No more than one of "
        flags = list(self.flag_names)
        last_flag = flags.pop(-1)
        text += ', '.join(flags) + ' or ' + repr(last_flag)
        text += f" can be {self.conflicting_bool_value!r}."
        return text


class DispatchError(GidAppToolsBaseError):
    ...

# TODO: accept AdvancedDict instance as parameter and show path_taken maybe.


class DictMergeConflict(GidAppToolsBaseError):
    def __init__(self, first_dict: dict, second_dict: dict, conflicting_key: Hashable, none_values: set[Hashable]) -> None:
        self.first_dict = first_dict
        self.second_dict = second_dict
        self.conflicting_key = conflicting_key
        self.none_values = none_values
        self.message = f"Unable to merge key {self.conflicting_key!r}, because it already exists in the first dictionary and has an value that is not a 'none_value'({', '.join(f'{item!r}' for item in self.none_values)}"
        super().__init__(self.message)


class AdvancedDictError(GidAppToolsBaseError):
    ...


class GidConfigError(GidAppToolsBaseError):
    ...


class GidQtError(GidAppToolsBaseError):
    ...


class ApplicationNotExistingError(GidQtError):

    def __init__(self, msg: str = None) -> None:
        self.msg = msg or "No Application instance found."
        super().__init__(self.msg)


class ApplicationExistsError(GidQtError):

    def __init__(self, existing_application, msg: str) -> None:
        self.existing_application = existing_application
        self.msg = f"{msg} -> application: {self.existing_application!r}"
        super().__init__(self.msg)


class ApplicationNotSetupError(GidQtError):
    ...


class SectionExistsError(GidConfigError):
    ...


class SectionMissingError(GidConfigError):

    def __init__(self, section_name: str, config_data: "ConfigData") -> None:
        self.section_name = section_name
        self.config_data = config_data
        self.message = f"No Section named {self.section_name!r} in config_data {self.config_data}."
        super().__init__(self.message)


class EntryMissingError(GidConfigError):
    def __init__(self, section_name: str, entry_key: str, config_data: "ConfigData") -> None:
        self.section_name = section_name
        self.entry_key = entry_key
        self.config_data = config_data
        self.message = f"No Entry with key {self.entry_key!r} in Section named {self.section_name!r} in config_data {self.config_data}."
        super().__init__(self.message)


class ValueValidationError(GidConfigError):

    def __init__(self, config_value: Any, spec_entry: "SpecEntry", validation_description: str = None) -> None:
        self.config_value = config_value
        self.spec_entry = spec_entry
        self.validation_description = validation_description
        self.msg = f"Value {self.config_value!r} with Spec {self.spec_entry!r} failed its validation"

        if self.validation_description is not None:
            self.msg += f", {self.validation_description}"
        self.msg += "."

        super().__init__(self.msg)


class ConfigSpecError(GidConfigError):
    ...


class InvalidConverterValue(ConfigSpecError):
    ...


class UnconvertableTypusError(ConfigSpecError):
    ...


class SpecDataMissingError(ConfigSpecError):
    ...


class ConversionError(GidConfigError):
    ...


class MissingTypusOrSpecError(GidConfigError):
    ...


class IniParsingError(GidConfigError):
    ...


class MissingDefaultValue(GidConfigError):
    ...


class TrailingCommentError(IniParsingError):
    ...


class NotLoggingLevelError(GidConfigError):

    def __init__(self, value, converter, section_name: str = None, entry_name: str = None, config=None) -> None:
        self.value = value

        self.converter = converter
        self.section_name = section_name
        self.entry_name = entry_name
        self.config = config
        self.msg = f"Entry {self.entry_name!r} of section {self.section_name}, of config {self.config!r} has a value ({self.value!r}) that is not a valid value of converter {self.converter!r}."
        super().__init__(self.msg)


class MinError(GidConfigError):

    def __init__(self, value, min_value, converter, section_name: str = None, entry_name: str = None, config=None) -> None:
        self.value = value
        self.min_value = min_value
        self.converter = converter
        self.section_name = section_name
        self.entry_name = entry_name
        self.config = config
        self.msg = f"Entry {self.entry_name!r} of section {self.section_name}, of config {self.config!r} has a value ({self.value!r}) that is less than the min_value({self.min_value!r}) of converter {self.converter!r}."
        super().__init__(self.msg)


class MaxError(GidConfigError):

    def __init__(self, value, max_value, converter, section_name: str = None, entry_name: str = None, config=None) -> None:
        self.value = value
        self.max_value = max_value
        self.converter = converter
        self.section_name = section_name
        self.entry_name = entry_name
        self.config = config
        self.msg = f"Entry {self.entry_name!r} of section {self.section_name}, of config {self.config!r} has a value ({self.value!r}) that is less than the max_value({self.max_value!r}) of converter {self.converter!r}."
        super().__init__(self.msg)


class KeyPathError(AdvancedDictError):
    def __init__(self, missing_key: Hashable, key_path: list[Hashable], last_key: Hashable = None) -> None:
        self.missing_key = missing_key
        self.last_key = last_key
        self.key_path = key_path if self.last_key is None else key_path + [last_key]
        self.missing_key_pos = self.key_path.index(self.missing_key) + 1
        self.missing_key_pos_verbose = f"{self.missing_key_pos}."
        self.message = f"The {self.missing_key_pos_verbose} key {self.missing_key!r} was not found, full key_path: {self.key_path!r}."
        super().__init__(self.message)


class NotMappingError(AdvancedDictError):
    def __init__(self, key: Hashable, value: Any, key_path: list[Hashable], action: Union[Literal['set'], Literal['get']], last_key: Hashable = None) -> None:
        self.key = key
        self.value = value
        self.value_type = type(value)
        self.action = action
        self.last_key = last_key
        self.key_path = key_path if self.last_key is None else key_path + [last_key]
        self.key_pos = self.key_path.index(self.key) + 1
        self.key_pos_verbose = f"{self.key_pos}."
        self.message = f"Unable to {self.action} {self.key_pos_verbose} {self.key!r} (key_path={self.key_path!r}), because value is not a Mapping but {self.value_type!r}."
        super().__init__(self.message)


class DateTimeFrameTimezoneError(GidAppToolsBaseError):
    def __init__(self, duration_item: "DateTimeFrame", start_tz: Optional[timezone], end_tz: Optional[timezone], message: str) -> None:
        self.duration_item = duration_item
        self.start_tz = start_tz
        self.end_tz = end_tz
        self.message = message + f", {start_tz=}, {end_tz=}."
        super().__init__(self.message)


class NotUtcDatetimeError(GidAppToolsBaseError):
    def __init__(self, datetime_obj: datetime) -> None:
        self.datetime_obj = datetime_obj
        self.actual_timezone = datetime_obj.tzinfo
        self.message = f"{self.datetime_obj!r} has to be of timezone {timezone.utc!r}, not {self.actual_timezone!r}"
        super().__init__(self.message)


class BaseMetaDataError(GidAppToolsBaseError):
    """
    Base Error for Meta Data Errors.
    """


class RegisterAfterSetupError(BaseMetaDataError):
    ...


class MetaItemNotFoundError(BaseMetaDataError):
    def __init__(self, requested_name: str, existing_item_names: list[str]) -> None:
        self.requested_name = requested_name
        self.existing_item_names = existing_item_names
        self.message = f"Item {self.requested_name!r} was not found in existing meta_items, existing_meta_item names: {self.existing_item_names!r}"
        super().__init__(self.message)


class NoFactoryFoundError(BaseMetaDataError):
    def __init__(self, app_meta_item_name) -> None:
        self.app_meta_item_name = app_meta_item_name
        self.message = f"Unable to find a factory for {self.app_meta_item_name!r}."
        super().__init__(self.message)


class NotSetupError(BaseMetaDataError):
    def __init__(self, app_meta_data) -> None:
        self.app_meta_data = app_meta_data
        self.message = f'{self.app_meta_data.__class__.__name__!r} has to set up from the base_init_file first!'
        super().__init__(self.message)


class NotBaseInitFileError(BaseMetaDataError):
    """
    Raised if the calling file is not the base __init__.py file of the App.
    """

    def __init__(self, calling_file: Path) -> None:
        self.calling_file = calling_file
        self.calling_folder = calling_file.parent
        self.message = f"This function has to be called from the '__init__.py' file in the base directory of the App, actual calling file: {self.calling_file.as_posix()!r}"
        super().__init__(self.message)


class BaseMetaPathsError(GidAppToolsBaseError):
    """
    Base error for meta_paths.
    """


class UnknownMetaPathIdentifier(BaseMetaPathsError):

    def __init__(self, identifier: str) -> None:
        self.identifier = identifier
        self.msg = f"{self.identifier!r} is not an valid identifier for a Meta-Path."
        super().__init__(self.msg)


class NotImplementedMetaPath(BaseMetaPathsError):

    def __init__(self, identifier: "NamedMetaPath") -> None:
        self.identifier = identifier
        self.msg = f"No Path implemented for identifer {self.identifier!r}."
        super().__init__(self.msg)


class AppNameMissingError(BaseMetaPathsError):

    def __init__(self) -> None:
        self.message = "The name of the App was not found in the 'kwargs_holder' or in the env ('APP_NAME')."
        super().__init__(self.message)


class UnparsableHumanTimedelta(ConversionError):

    def __init__(self, human_text: str) -> None:
        self.human_text = human_text
        self.message = f"Unable to parse the text {self.human_text!r} to a valid timedelta."
        super().__init__(self.message)


# region [Main_Exec]
if __name__ == '__main__':
    pass


# endregion [Main_Exec]
