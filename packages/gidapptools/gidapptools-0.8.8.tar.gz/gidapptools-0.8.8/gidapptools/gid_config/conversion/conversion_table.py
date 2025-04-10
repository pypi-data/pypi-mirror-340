"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
from typing import Mapping, Iterable
from pathlib import Path
from collections import ChainMap

# * Gid Imports ----------------------------------------------------------------------------------------->
from gidapptools.errors import UnconvertableTypusError
from gidapptools.general_helper.enums import MiscEnum
from gidapptools.general_helper.timing import get_dummy_profile_decorator_in_globals
from gidapptools.gid_config.conversion.base_converters import ConfigValueConverter, get_standard_converter
from gidapptools.gid_config.conversion.converter_grammar import ConverterSpecData

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]
get_dummy_profile_decorator_in_globals()
THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


class ConversionTable:
    __slots__ = ("_standard_converters", "_extra_converters", "_resolved_converters")

    def __init__(self,
                 extra_converter: Iterable[type[ConfigValueConverter]] = None) -> None:
        self._standard_converters: tuple[type[ConfigValueConverter]] = tuple(get_standard_converter())
        self._extra_converters: tuple[type[ConfigValueConverter]] = tuple(extra_converter or [])
        self._resolved_converters: dict[str, ConfigValueConverter] = None

    @property
    def converters(self) -> Mapping[str, type[ConfigValueConverter]]:
        if self._resolved_converters is None:

            self._resolved_converters = ChainMap(*self._resolve_converters(self._extra_converters), *self._resolve_converters(self._standard_converters))

        return self._resolved_converters

    @property
    def available_value_types(self) -> set[str]:
        return set(self.converters.keys())

    def _resolve_converters(self, converters: tuple[ConfigValueConverter]) -> tuple[Mapping[str, ConfigValueConverter]]:
        converter_map = {}
        converter_alias_map = {}
        for converter in converters:
            converter_map[converter.value_typus] = converter
            converter_alias_map = converter_alias_map | {a: converter for a in converter.value_typus_aliases}

        return converter_map, converter_alias_map

    def get_converter(self, converter_data: ConverterSpecData) -> ConfigValueConverter:

        converter = self.converters.get(converter_data["typus"], MiscEnum.NOT_FOUND)

        if converter is MiscEnum.NOT_FOUND:
            raise UnconvertableTypusError(f"No Converter for typus {converter_data['typus']!r} found.")

        return converter(self, **converter_data["kw_arguments"])

    def add_extra_converter(self, converter: type[ConfigValueConverter]) -> None:
        self._extra_converters = tuple(self._extra_converters + (converter,))
        self._resolved_converters = None


# region [Main_Exec]
if __name__ == '__main__':
    pass

# endregion [Main_Exec]
