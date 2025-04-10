"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any, Union, Iterable, Optional
from pathlib import Path
from colorsys import hls_to_rgb, hsv_to_rgb, rgb_to_hls, rgb_to_hsv
from functools import cached_property

# * Third Party Imports --------------------------------------------------------------------------------->
import attr

# * Gid Imports ----------------------------------------------------------------------------------------->
from gidapptools.gidcolor.preset_colors.web_colors import _load_webcolors_data
import numpy as np
try:
    from PySide6.QtGui import QColor
    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()


from warnings import warn_explicit, warn
from . import color

warn(message=f"Submodule {__name__!r} is deprecated, please use submodule {color.__name__!r}.",
     category=DeprecationWarning,
     stacklevel=2)


# endregion [Constants]


INT_OR_FLOAT = Union[int, float]

COLOR_FLOAT_TYPE = Union[tuple[float, float, float], tuple[float, float, float, float]]

COLOR_INT_TYPE = Union[tuple[int, int, int], tuple[int, int, int, float]]


def _validate_color_float(instance: object, attribute: attr.Attribute, value: Optional[float]) -> None:

    if 0.0 > value > 1.0:

        raise ValueError(f"{attribute.name!r}-value can only be between 0 and 1, not {value!r}.")


def _alpha_converter(alpha: Union[int, float] = None) -> float:
    if alpha is None:
        return 1.0

    return float(alpha)


def rgb_to_hex(r, g, b):
    parts = []
    for part in [r, g, b]:
        if isinstance(part, float):
            part = int(255 * part)
        parts.append(part)
    return '#' + ''.join(f"{p:X}"for p in parts)


def rgb_float_to_rgb_int(in_rgb_float: tuple[float, float, float]) -> tuple[int, int, int]:
    return tuple(int(255 * i) for i in in_rgb_float)


class ColorTypus(Enum):
    RGB = auto()
    HLS = auto()
    HSV = auto()


class BaseColor(ABC):
    float_round_n: int = 4

    def __iter__(self):
        return (getattr(self, field.name) for field in attr.fields(self.__class__) if field.metadata.get("is_core_color", False) is True)

    @abstractmethod
    def as_rgb_float(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        ...

    @abstractmethod
    def as_rgb_int(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_INT_TYPE:
        ...

    @abstractmethod
    def as_hls(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        ...

    @abstractmethod
    def as_hsv(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        ...

    def as_hex(self, include_alpha: bool = True) -> str:
        _rgb = self.as_rgb_int(include_alpha=include_alpha, alpha_as_int=True)
        _hex = rgb_to_hex(*_rgb[:3])
        if include_alpha is True and len(_rgb) == 4:
            _hex += f"{_rgb[-1]:X}"

        return _hex

    @cached_property
    def qcolor(self) -> Optional["QColor"]:
        if PYSIDE6_AVAILABLE:
            return QColor(*self.as_rgb_int(True, True))

    def to_q_style_rgba_string(self,) -> str:
        values = (str(i) for i in self.as_rgb_int(alpha_as_int=True))
        return "rgba(" + ', '.join(values) + ')'

    def __repr__(self) -> str:
        class_name = self.__class__.__name__.removesuffix("Color")
        _out = f"{class_name}(" + ', '.join(repr(x) for x in self)
        if self.name is not None:
            _out += f', name={self.name!r}'

        if self.aliases:
            _out += f", aliases={tuple(self.aliases)!r}"
        return _out + ')'

    def with_alpha(self, alpha: Union[int, float]) -> "BaseColor":
        if isinstance(alpha, int) or alpha > 1:
            alpha = round(alpha / 255, self.float_round_n)
        return self.__class__(*list(self)[:-1], alpha)


@attr.s(auto_attribs=True, auto_detect=True, slots=True, weakref_slot=True, frozen=True, order=True, repr=False)
class RGBColor(BaseColor):
    red: float = attr.ib(validator=_validate_color_float, metadata={'is_core_color': True})
    green: float = attr.ib(validator=_validate_color_float, metadata={'is_core_color': True})
    blue: float = attr.ib(validator=_validate_color_float, metadata={'is_core_color': True})

    alpha: float = attr.ib(default=1.0, converter=_alpha_converter, validator=_validate_color_float, metadata={'is_core_color': True})

    name: str = attr.ib(default=None)
    aliases: Iterable[str] = attr.ib(factory=set, converter=attr.converters.default_if_none(factory=set))

    np_value: "np.ndarray" = attr.ib()

    @np_value.default
    def _np_value_default(self):
        return np.asarray(self.as_rgb_float(True, False), dtype=np.float32)

    def as_rgb_float(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        _out = list(self)[:-1]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return tuple(_out)

    def as_rgb_int(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_INT_TYPE:
        _out = [int(sub_col * 255) for sub_col in list(self)[:-1]]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return tuple(_out)

    def as_hls(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        _out = [round(col, self.float_round_n) for col in rgb_to_hls(*list(self)[:-1])]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return _out

    def as_hsv(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        _out = [round(col, self.float_round_n) for col in rgb_to_hsv(*list(self)[:-1])]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return _out


@attr.s(auto_attribs=True, auto_detect=True, slots=True, weakref_slot=True, frozen=True, order=True, repr=False)
class HLSColor(BaseColor):
    hue: float = attr.ib(validator=_validate_color_float, metadata={'is_core_color': True})
    saturation: float = attr.ib(validator=_validate_color_float, metadata={'is_core_color': True})
    lightness: float = attr.ib(validator=_validate_color_float, metadata={'is_core_color': True})

    alpha: float = attr.ib(default=1.0, converter=_alpha_converter, validator=_validate_color_float, metadata={'is_core_color': True})

    name: str = attr.ib(default=None)
    aliases: Iterable[str] = attr.ib(factory=set, converter=attr.converters.default_if_none(factory=set))

    np_value: np.ndarray = attr.ib()

    @np_value.default
    def _np_value_default(self):
        return np.asfarray(self.as_rgb_float(True, False), dtype=np.float32)

    def as_hls(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        _out = list(self)[:-1]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return tuple(_out)

    def as_rgb_float(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        _out = [round(col, self.float_round_n) for col in hls_to_rgb(*list(self)[:-1])]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return tuple(_out)

    def as_rgb_int(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_INT_TYPE:
        _out = [int(sub_col * 255) for sub_col in hls_to_rgb(*list(self)[:-1])]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return tuple(_out)

    def as_hsv(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        _out = [round(col, self.float_round_n) for col in rgb_to_hsv(*hls_to_rgb(*list(self)[:-1]))]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return _out


@attr.s(auto_attribs=True, auto_detect=True, slots=True, weakref_slot=True, frozen=True, order=True, repr=False)
class HSVColor(BaseColor):
    hue: float = attr.ib(validator=_validate_color_float, metadata={'is_core_color': True})
    saturation: float = attr.ib(validator=_validate_color_float, metadata={'is_core_color': True})
    value: float = attr.ib(validator=_validate_color_float, metadata={'is_core_color': True})

    alpha: float = attr.ib(default=1.0, converter=_alpha_converter, validator=attr, metadata={'is_core_color': True})

    name: str = attr.ib(default=None)
    aliases: Iterable[str] = attr.ib(factory=set, converter=attr.converters.default_if_none(factory=set))
    np_value: np.ndarray = attr.ib()

    @np_value.default
    def _np_value_default(self):
        return np.asfarray(self.as_rgb_float(True, False), dtype=np.float32)

    def as_hsv(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        _out = list(self)[:-1]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return tuple(_out)

    def as_hls(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        _out = [round(col, self.float_round_n) for col in rgb_to_hls(*hsv_to_rgb(*list(self)[:-1]))]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return _out

    def as_rgb_float(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_FLOAT_TYPE:
        _out = [round(col, self.float_round_n) for col in hsv_to_rgb(*list(self)[:-1])]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return tuple(_out)

    def as_rgb_int(self, include_alpha: bool = True, alpha_as_int: bool = False) -> COLOR_INT_TYPE:
        _out = [int(sub_col * 255) for sub_col in hsv_to_rgb(*list(self)[:-1])]
        if include_alpha is True:
            if alpha_as_int is True:
                _out.append(int(self.alpha * 255))
            else:
                _out.append(self.alpha)
        return tuple(_out)


color_class_map: dict[str, type[BaseColor]] = {"rgb": RGBColor,
                                               "hls": HLSColor,
                                               "hsv": HSVColor}


class ColorRegistry:
    color_typus = ColorTypus

    def __init__(self) -> None:
        self.colors_by_name: dict[str:RGBColor] = {}

    def _add_color(self, color: RGBColor) -> None:
        if color.name:
            self.colors_by_name[color.name.casefold()] = color
        for alias in color.aliases:
            self.colors_by_name[alias.casefold()] = color

    def color_factory(self, value: tuple, typus: ColorTypus, name: str = None, aliases: Iterable[str] = None):
        if len(value) == 3:
            value = (value[0], value[1], value[2], 1.0)

        if typus is ColorTypus.RGB:
            _values = []
            for v in value:
                if isinstance(v, int) and v != 0:
                    v = round(v / 255, BaseColor.float_round_n)
                _values.append(v)

            color = RGBColor(*_values, name=name, aliases=aliases)

        elif typus is ColorTypus.HLS:
            ...

        elif typus is ColorTypus.HSV:
            ...

        self._add_color(color)
        return color

    def __call__(self, value: tuple, typus: ColorTypus, name: str = None, aliases: Iterable[str] = None) -> Any:
        return self.color_factory(value=value, typus=typus, name=name, aliases=aliases)

    def get_color_by_name(self, name: str) -> "RGBColor":
        if len(self.colors_by_name) == 0:
            for _p_color in _load_webcolors_data():
                Color(**_p_color, typus=Color.color_typus.RGB)

        return self.colors_by_name[name.casefold()]


xyx = []
Color = ColorRegistry()
for p_color in _load_webcolors_data():
    xyx.append(Color.color_factory(**p_color, typus=Color.color_typus.RGB))

# region [Main_Exec]
if __name__ == '__main__':
    from pympler.asizeof import asizeof
    from gidapptools.general_helper.conversion import bytes2human
    import inspect
    print(f"{bytes2human(asizeof(xyx[0]))=}")
    print(f"{bytes2human(asizeof(xyx[0].np_value))=}")
    print(f"{xyx[0].np_value=}")

    print(f"{RGBColor.f_code}")


# endregion [Main_Exec]
