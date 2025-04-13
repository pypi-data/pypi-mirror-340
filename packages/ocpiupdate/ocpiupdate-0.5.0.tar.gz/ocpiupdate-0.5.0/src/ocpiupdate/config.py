"""Functions for handling reading the config file."""

from __future__ import annotations

import pathlib
import tomllib as toml
from copy import deepcopy
from typing import Any, Literal, Self, TypedDict, cast

AnyDict = dict[str, Any]
NestedDict = dict[str, "str | list[str] | NestedDict"]

InplaceSearchType = Literal["component", "hdl-worker", "rcc-worker"]
VALID_INPLACE_SEARCHES: set[InplaceSearchType] = {
    "component",
    "hdl-worker",
    "rcc-worker",
}

TranslateFromType = Literal["makefile"]
TRANSLATE_FROM_TYPES: set[TranslateFromType] = {"makefile"}

TranslateToType = Literal["xml"]
TRANSLATE_TO_TYPES: set[TranslateToType] = {"xml"}

ConfigMigrateRenameIdentifierDict = TypedDict(
    "ConfigMigrateRenameIdentifierDict",
    {
        "from": str | list[str],
        "to": str | list[str],
        "inplace-search": list[InplaceSearchType],
        "inplace-from": list[str],
        "inplace-to": str,
    },
)

ConfigMigrateRenameDict = TypedDict(  # noqa: UP013
    "ConfigMigrateRenameDict",
    {
        "component": ConfigMigrateRenameIdentifierDict,
        "protocol": ConfigMigrateRenameIdentifierDict,
    },
    total=False,
)

ConfigMigrateTranslateIdentifierDict = TypedDict(
    "ConfigMigrateTranslateIdentifierDict",
    {
        "from": TranslateFromType,
        "to": TranslateToType,
    },
)

ConfigMigrateTranslateDict = TypedDict(
    "ConfigMigrateTranslateDict",
    {
        "applications": ConfigMigrateTranslateIdentifierDict,
        "hdl-adapters": ConfigMigrateTranslateIdentifierDict,
        "hdl-assemblies": ConfigMigrateTranslateIdentifierDict,
        "hdl-cards": ConfigMigrateTranslateIdentifierDict,
        "hdl-device": ConfigMigrateTranslateIdentifierDict,
        "hdl-platforms": ConfigMigrateTranslateIdentifierDict,
        "hdl-primitives": ConfigMigrateTranslateIdentifierDict,
        "hdl-worker": ConfigMigrateTranslateIdentifierDict,
        "project": ConfigMigrateTranslateIdentifierDict,
        "rcc-worker": ConfigMigrateTranslateIdentifierDict,
    },
    total=False,
)


class ConfigMigrateDict(TypedDict):
    """Dictionary declaring the types of all aspects of the migrate table."""

    rename: ConfigMigrateRenameDict
    translate: ConfigMigrateTranslateDict


ConfigParseMakefileIdentifierDict = TypedDict(
    "ConfigParseMakefileIdentifierDict",
    {
        "inherit": str,
        "node-fragments-to-ignore": list[str],
        "node-types-to-ignore": list[str],
        "paths": list[str],
    },
    total=False,
)


ConfigParseMakefileDict = TypedDict(
    "ConfigParseMakefileDict",
    {
        "inherit": str,
        "node-fragments-to-ignore": list[str],
        "node-types-to-ignore": list[str],
        "paths": list[str],
        # Identifiers
        "applications": ConfigParseMakefileIdentifierDict,
        "hdl-adapters": ConfigParseMakefileIdentifierDict,
        "hdl-assemblies": ConfigParseMakefileIdentifierDict,
        "hdl-cards": ConfigParseMakefileIdentifierDict,
        "hdl-device": ConfigParseMakefileIdentifierDict,
        "hdl-platforms": ConfigParseMakefileIdentifierDict,
        "hdl-primitives": ConfigParseMakefileIdentifierDict,
        "hdl-worker": ConfigParseMakefileIdentifierDict,
        "project": ConfigParseMakefileIdentifierDict,
        "rcc-worker": ConfigParseMakefileIdentifierDict,
    },
    total=False,
)


class ConfigParseDict(TypedDict, total=False):
    """Dictionary declaring the types of all aspects of the parse table."""

    makefile: ConfigParseMakefileDict


class ConfigDict(TypedDict, total=False):
    """Dictionary declaring the types of all aspects of the config file."""

    migrate: ConfigMigrateDict
    parse: ConfigParseDict


def merge_dict(left: AnyDict, right: AnyDict) -> AnyDict:
    """
    Merge a dictionary of dictionaries of arbitrary depth.

    Raises
    ------
    TypeError
        If the type of the value of any overlapping key is not dict for both
        inputs.

    """
    ret = {}
    overlapping_keys = left.keys() & right.keys()
    for key in overlapping_keys:
        if isinstance(left[key], dict) and isinstance(right[key], dict):
            ret[key] = merge_dict(
                left[key],
                right[key],
            )
        else:
            message = f"Dictionaries are not congruent: '{left}', '{right}'"
            raise TypeError(message)
    for key in left.keys() - overlapping_keys:
        ret[key] = deepcopy(left[key])
    for key in right.keys() - overlapping_keys:
        ret[key] = deepcopy(right[key])
    return ret


class Config:
    """Class to handle reading a config file."""

    _config_dict: ConfigDict

    @classmethod
    def from_files_and_toml_strings(
        cls,
        path_args: list[pathlib.Path],
        string_args: list[str],
    ) -> Self:
        """
        Read a config from a list of files and TOML strings.

        Raises
        ------
        FileNotFoundError
            If any path provided can't be opened.
        RuntimeError
            If any config is invalid.

        """
        dct: AnyDict = {}
        for path in path_args:
            if not path.exists():
                message = f"File '{path}' not found"
                raise FileNotFoundError(message)
            with pathlib.Path.open(path, "rb") as f:
                ocpiupdate_config_dict = toml.load(f)
            config_dict = ocpiupdate_config_dict.get("ocpiupdate")
            if config_dict is None:
                message = f"Config file '{path}' does not contain '[ocpiupdate]'"
                raise RuntimeError(message)
            dct = merge_dict(dct, config_dict)
        for string in string_args:
            try:
                config_dict = toml.loads(string)
            except toml.TOMLDecodeError as err:
                message = f"Config '{string}' could not be parsed as TOML"
                raise RuntimeError(message) from err
            dct = merge_dict(dct, config_dict)
        return cls(cast("ConfigDict", dct))

    def __init__(self, config_dict: ConfigDict) -> None:
        """Construct."""
        self._config_dict = config_dict

    def __repr__(self) -> str:
        """Dunder method: Convert to string evaluating to class constructor."""
        return f"{self.__class__.__name__}({self._config_dict!r})"

    def __str__(self) -> str:
        """Dunder method: Convert to string."""
        return str(self._config_dict)

    def get_dict_setting_for_parse(
        self,
        file_type: str,
        file_identifier: str,
        setting: str,
    ) -> AnyDict:
        """Get a setting of type dict from the `parse` category of the config."""
        # Get the `ocpiupdate.parse` category
        # or fail
        parse_config = self._config_dict.get("parse")
        if parse_config is None:
            return {}
        # Get the `ocpiupdate.parse.$file_type` category
        # or fail
        filetype_config = parse_config.get(file_type)
        if filetype_config is None:
            return {}
        # Get the `ocpiupdate.parse.$file_type.$file_identifier` category,
        # or try `ocpiupdate.parse.$file_type.$setting`
        # or fail
        subcategory_config = filetype_config.get(file_identifier)  # type: ignore[attr-defined]
        if subcategory_config is None:
            setting_config = filetype_config.get(setting)  # type: ignore[attr-defined]
            if setting_config is not None:
                return cast("AnyDict", setting_config)
            return {}
        # Get settings from `ocpiupdate.parse.$file_type.$file_identifier.inherit`
        # or try `ocpiupdate.parse.$file_type.$setting`
        ret = {}
        inherit_config = subcategory_config.get("inherit")
        if inherit_config is not None:
            ret.update(
                self.get_dict_setting_for_parse(
                    file_type,
                    inherit_config,
                    setting,
                ),
            )
        else:
            setting_config = filetype_config.get(setting)  # type: ignore[attr-defined]
            if setting_config is not None:
                ret.update(setting_config)
        # Get settings from `ocpiupdate.parse.$file_type.$file_identifier.$setting`
        setting_config = subcategory_config.get(setting)
        if setting_config is not None:
            ret.update(setting_config)
        return ret

    def get_list_setting_for_parse(
        self,
        file_type: str,
        file_identifier: str,
        setting: str,
    ) -> list[str]:
        """Get a setting of type list from the `parse` category of the config."""
        # Get the `ocpiupdate.parse` category
        # or fail
        parse_config = self._config_dict.get("parse")
        if parse_config is None:
            return []
        # Get the `ocpiupdate.parse.$file_type` category
        # or fail
        filetype_config = parse_config.get(file_type)
        if filetype_config is None:
            return []
        # Get the `ocpiupdate.parse.$file_type.$file_identifier` category,
        # or try `ocpiupdate.parse.$file_type.$setting`
        # or fail
        subcategory_config = filetype_config.get(file_identifier)  # type: ignore[attr-defined]
        if subcategory_config is None:
            setting_config = filetype_config.get(setting)  # type: ignore[attr-defined]
            if setting_config is not None:
                return cast("list[str]", setting_config)
            return []
        # Get settings from `ocpiupdate.parse.$file_type.$file_identifier.inherit`
        # or try `ocpiupdate.parse.$file_type.$setting`
        ret: list[str] = []
        inherit_config = subcategory_config.get("inherit")
        if inherit_config is not None:
            ret.extend(
                self.get_list_setting_for_parse(
                    file_type,
                    inherit_config,
                    setting,
                ),
            )
        else:
            setting_config = filetype_config.get(setting)  # type: ignore[attr-defined]
            if setting_config is not None:
                ret.extend(setting_config)
        # Get settings from `ocpiupdate.parse.$file_type.$file_identifier.$setting`
        setting_config = subcategory_config.get(setting)
        if setting_config is not None:
            ret.extend(setting_config)
        return ret

    def get_setting_for_parse(
        self,
        file_type: str,
        file_identifier: str,
        setting: str,
    ) -> str | None:
        """Get a setting of type string from the `parse` category of the config."""
        # Get the `ocpiupdate.parse` category
        # or fail
        parse_config = self._config_dict.get("parse")
        if parse_config is None:
            return None
        # Get the `ocpiupdate.parse.$file_type` category
        # or fail
        filetype_config = parse_config.get(file_type)
        if filetype_config is None:
            return None
        # Get the `ocpiupdate.parse.$file_type.$file_identifier` category,
        # or try `ocpiupdate.parse.$file_type.$setting`
        # or fail
        subcategory_config = filetype_config.get(file_identifier)  # type: ignore[attr-defined]
        if subcategory_config is None:
            return cast("str | None", filetype_config.get(setting))  # type: ignore[attr-defined]
        # Get setting from `ocpiupdate.parse.$file_type.$file_identifier.inherit`
        # or try `ocpiupdate.parse.$file_type.$setting`
        ret: str | None = None
        inherit_config = subcategory_config.get("inherit")
        if inherit_config is not None:
            ret = self.get_setting_for_parse(file_type, inherit_config, setting)
        else:
            ret = filetype_config.get(setting)  # type: ignore[attr-defined]
        # Get setting from `ocpiupdate.parse.$file_type.$file_identifier.$setting`
        setting_config = subcategory_config.get(setting)
        if setting_config is not None:
            ret = setting_config
        return ret

    def validate(self) -> None:  # noqa: C901, PLR0912, PLR0914, PLR0915
        """
        Validate the config.

        Raises
        ------
        RuntimeError
            If the config file is invalid.
        TypeError
            If any call to `eval` that this method does results in an incorrect
            type.

        """
        key = []
        migrate = self._config_dict.get("migrate")
        if migrate is None:
            message = "ocpiupdate.migrate is not defined"
            raise RuntimeError(message)

        key.append("migrate")
        rename = migrate.get("rename")
        if rename is not None:
            key.append("rename")
            for identifier, table in rename.items():
                table = cast("ConfigMigrateRenameIdentifierDict", table)
                key.append(identifier)

                from_item = table.get("from")
                if from_item is None:
                    message = f"{'.'.join(key)}.from is not defined"
                    raise RuntimeError(message)
                if isinstance(from_item, str):
                    from_item = [from_item]
                for i, e in enumerate(from_item):
                    try:
                        pathlib.Path("/").glob(e)
                    except ValueError as err:
                        message = (
                            f"{'.'.join(key)}.from[{i}] contains an invalid glob: '{e}'"
                        )
                        raise RuntimeError(message) from err

                to = table.get("to")
                if to is None:
                    message = f"{'.'.join(key)}.to is not defined"
                    raise RuntimeError(message)
                if isinstance(to, str):
                    to = [to]
                for i, e in enumerate(to):
                    try:
                        evaluated_to = eval(  # noqa: S307
                            e,
                            {},  # {"__builtins__": __builtins__},
                            {"file": pathlib.Path("/")},
                        )
                    except Exception as err:
                        message = (
                            f"Evaluation of {'.'.join(key)}.to[{i}] threw exception"
                        )
                        raise RuntimeError(message) from err
                    if not isinstance(evaluated_to, pathlib.Path):
                        message = (
                            f"{'.'.join(key)}.to[{i}] does not resolve to a path: "
                            f"{type(evaluated_to)}"
                        )
                        raise TypeError(message)

                inplace_search = table.get("inplace-search")
                if inplace_search is None:
                    message = f"{'.'.join(key)}.inplace-search is not defined"
                    raise RuntimeError(message)
                valid_searches = VALID_INPLACE_SEARCHES
                invalid_search_values = set(inplace_search) - valid_searches
                if len(inplace_search) == 0:
                    message = f"{'.'.join(key)}.inplace-search is empty"
                    raise RuntimeError(message)
                if len(invalid_search_values) != 0:
                    message = (
                        f"{'.'.join(key)}.inplace-search contains invalid "
                        f"values: {invalid_search_values}"
                    )
                    raise RuntimeError(message)

                inplace_from = table.get("inplace-from")
                if inplace_from is None:
                    message = f"{'.'.join(key)}.inplace-from is not defined"
                    raise RuntimeError(message)
                if len(inplace_from) == 0:
                    message = f"{'.'.join(key)}.inplace-from is empty"
                    raise RuntimeError(message)
                for i, e in enumerate(inplace_from):
                    try:
                        evaluated_inplace_from = eval(  # noqa: S307
                            e,
                            {},  # {"__builtins__": __builtins__},
                            {"file": pathlib.Path("/")},
                        )
                    except Exception as err:
                        message = (
                            f"Evaluation of {'.'.join(key)}.inplace-from[{i}] "
                            "threw exception"
                        )
                        raise RuntimeError(message) from err
                    if not isinstance(evaluated_inplace_from, str):
                        message = (
                            f"{'.'.join(key)}.inplace-from[{i}] does not "
                            f"resolve to a str: {type(evaluated_inplace_from)}"
                        )
                        raise TypeError(message)

                inplace_to = table.get("inplace-to")
                if inplace_to is None:
                    message = f"{'.'.join(key)}.inplace-to is not defined"
                    raise RuntimeError(message)
                try:
                    evaluated_inplace_to = eval(  # noqa: S307
                        inplace_to,
                        {},  # {"__builtins__": __builtins__},
                        {"file": pathlib.Path("/")},
                    )
                except Exception as err:
                    message = (
                        f"Evaluation of {'.'.join(key)}.inplace-to threw exception"
                    )
                    raise RuntimeError(message) from err
                if not isinstance(evaluated_inplace_to, str):
                    message = (
                        f"{'.'.join(key)}.inplace-to does not resolve to a str: "
                        f"{type(evaluated_inplace_to)}"
                    )
                    raise TypeError(message)

                key.pop()
            key.pop()
        translate = migrate.get("translate")
        if translate is not None:
            key.append("translate")
            for identifier, table in translate.items():
                table = cast("ConfigMigrateTranslateIdentifierDict", table)
                key.append(identifier)

                from_item = table.get("from")
                if from_item is None:
                    message = f"{'.'.join(key)}.from is not defined"
                    raise RuntimeError(message)
                invalid_from_values = {from_item} - TRANSLATE_FROM_TYPES
                if len(invalid_from_values) != 0:
                    message = (
                        f"{'.'.join(key)}.from value is invalid: {invalid_from_values}"
                    )
                    raise RuntimeError(message)

                to = table.get("to")
                if to is None:
                    message = f"{'.'.join(key)}.to is not defined"
                    raise RuntimeError(message)
                invalid_to_values = {to} - TRANSLATE_TO_TYPES
                if len(invalid_to_values) != 0:
                    message = (
                        f"{'.'.join(key)}.to value is invalid: {invalid_to_values}"
                    )
                    raise RuntimeError(message)

                key.pop()
            key.pop()

    def __getitem__(self, indices: str | list[str]) -> str | list[str] | NestedDict:
        """
        Get a config item.

        Raises
        ------
        TypeError
            If `indices` has too many elements.

        """
        if isinstance(indices, str):
            indices = indices.split(".")
        ret: str | list[str] | NestedDict = cast("NestedDict", self._config_dict)
        for indice in indices:
            if not isinstance(ret, dict):
                message = (
                    f"Couldn't consume all indices. Next: '{indice}', Value: '{ret}'"
                )
                raise TypeError(message)
            ret = ret[indice]
        return ret
