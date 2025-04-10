"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
import os
import sys
import inspect
from typing import Any, Callable
from pathlib import Path
from functools import partial

# * Gid Imports ----------------------------------------------------------------------------------------->
from gidapptools.utility.helper import meta_data_from_path
from gidapptools.meta_data.config_kwargs import ConfigKwargs
from gidapptools.general_helper.conversion import str_to_bool
from gidapptools.meta_data.meta_info.meta_info_item import MetaInfo
from gidapptools.abstract_classes.abstract_meta_factory import AbstractMetaFactory

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


class License:
    special_licenses: dict[str, "License"] = {}

    def __init__(self, name: str, osi_approved: bool, description: str = None):
        self.name = name
        self.osi_approved = osi_approved
        self.description = description or ""

    @classmethod
    def from_classifier_string(cls, classifier_string: str):
        parts = [i.strip() for i in classifier_string.split("::")]
        osi_approved = True if "OSI Approved" in parts else False
        name = parts[-1]
        try:
            return cls.special_licenses[name]
        except KeyError:
            return cls(name=name, osi_approved=osi_approved)

    @classmethod
    def add_to_special_licenses(cls, special_license: "License"):
        cls.special_licenses[special_license.name] = special_license

    def __str__(self) -> str:
        return self.name


License.add_to_special_licenses(License(name="MIT License", osi_approved=True, description=""))
License.add_to_special_licenses(License(name="Unknown", osi_approved=False, description="License is missing or unknown."))


class MetaInfoFactory(AbstractMetaFactory):
    product_class = MetaInfo
    prefix_arg_getters = '_arg_get_'
    is_dev_env_name = 'IS_DEV'
    is_code_runner_env_name = 'IS_CODE_RUNNER'

    def __init__(self, config_kwargs: ConfigKwargs) -> None:
        super().__init__(config_kwargs=config_kwargs)

        self.init_path = Path(config_kwargs.get('init_path'))
        self.package_metadata = meta_data_from_path(self.init_path)
        self.package_metadata['app_name'] = self.package_metadata.pop('name')
        self.package_metadata['app_author'] = self.package_metadata.pop('author')

        self.arg_getters_map: dict[str, Callable] = None
        self.needed_arg_names: list[str] = None

    def setup(self) -> None:
        self.arg_getters_map = self._collect_arg_getters_map()
        self.needed_arg_names = self._retrieve_needed_arg_names()
        self.is_setup = True

    def _collect_arg_getters_map(self) -> dict[str, Callable]:
        arg_getters_map = {}
        for meth_name, meth_obj in inspect.getmembers(self, inspect.ismethod):
            if meth_name.startswith(self.prefix_arg_getters):
                arg_name = meth_name.removeprefix(self.prefix_arg_getters)
                arg_getters_map[arg_name] = meth_obj
        return arg_getters_map

    def _retrieve_needed_arg_names(self) -> list[str]:
        parameters = inspect.signature(self.product_class).parameters
        return list(parameters)

    def _build_meta_info_args(self) -> dict[str, Any]:
        meta_info_kwargs = {arg_name: self.config_kwargs.get(arg_name, None) for arg_name in self._retrieve_needed_arg_names()}
        for arg_name, arg_value in meta_info_kwargs.items():

            if arg_value is not None:
                continue

            arg_value_getter = self.arg_getters_map.get(arg_name, partial(self._default_arg_getter, arg_name))

            meta_info_kwargs[arg_name] = arg_value_getter()
        return {k: v for k, v in meta_info_kwargs.items() if v is not None}

    def _default_arg_getter(self, arg_name: str) -> Any:

        return self.package_metadata.get(arg_name.casefold())

    def _arg_get_app_license(self) -> License:
        license_classifier = next((i for i in self.package_metadata.get("classifier", []) if i.startswith("License")), "License :: Unknown")
        return License.from_classifier_string(license_classifier)

    def _arg_get_other_urls(self) -> dict[str, str]:
        _out = {}
        for item in self.package_metadata.get('project-url', []):
            if item.startswith("Source"):
                continue

            parts = [i.strip() for i in item.split(",") if i.strip()]
            if len(parts) != 2:
                continue
            if not parts[1].startswith("http"):
                continue
            _out[parts[0]] = parts[1]
        return _out

    def _arg_get_url(self) -> str:
        url_list = self.package_metadata.get('project-url', [])

        url_text = next((i for i in url_list if i.startswith("Source")), "")

        parts = map(lambda x: x.strip(), url_text.split(','))
        for part in parts:
            if part.startswith('http'):
                return part

    def _arg_get_is_dev(self) -> bool:
        is_dev_string = os.getenv(self.is_dev_env_name, '0').casefold()
        return str_to_bool(is_dev_string, strict=True) or sys.flags.dev_mode

    def _arg_get_is_gui(self) -> bool:
        if str_to_bool(os.getenv(self.is_code_runner_env_name, '0'), strict=True) is True:
            return False
        stdout_is_gui = sys.stdout is None or sys.stdout.isatty() is False
        stderr_is_gui = sys.stderr is None or sys.stderr.isatty() is False
        stdin_is_gui = sys.stdin is None or sys.stdin.isatty() is False
        return all([stdout_is_gui, stderr_is_gui, stdin_is_gui])

    def _build(self) -> MetaInfo:
        if self.is_setup is False:
            # TODO: maybe raise error instead
            self.setup()
        meta_info_kwargs = self._build_meta_info_args()
        instance = self.product_class(**meta_info_kwargs)
        return instance


# region [Main_Exec]


if __name__ == '__main__':
    pass

# endregion [Main_Exec]
