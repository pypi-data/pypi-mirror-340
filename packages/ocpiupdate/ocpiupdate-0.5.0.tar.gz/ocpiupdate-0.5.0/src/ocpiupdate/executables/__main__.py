#!/usr/bin/env python3

"""Script that automatically updates OpenCPI Projects."""

# ruff: noqa: C901

from __future__ import annotations

import argparse
import importlib.metadata
import logging
import pathlib
import sys
import typing

from lxml import etree

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

from ocpiupdate import treesitter
from ocpiupdate.config import (
    Config,
    ConfigMigrateDict,
    ConfigMigrateRenameIdentifierDict,
    ConfigMigrateTranslateIdentifierDict,
)
from ocpiupdate.version import V2_4_7, Version

MODELS = ["hdl", "rcc"]
XML_PARSER = etree.XMLParser(recover=True)

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("ocpiupdate")


def owd_path_from_worker_directory(
    worker_directory: pathlib.Path,
) -> pathlib.Path:
    """Get the path to the OWD file from the worker directory path."""
    model = worker_directory.suffix[1:]
    owd = worker_directory / f"{worker_directory.stem}-{model}.xml"
    if not owd.exists():
        owd = worker_directory / f"{worker_directory.stem}.xml"
    return owd


def yield_owd_from_project(
    project_directory: pathlib.Path,
    models: list[str] = MODELS,
) -> Iterable[pathlib.Path]:
    """
    Yield a generator of worker directory paths from a project path.

    Yields
    ------
    pathlib.Path
        The next OWD from the project.

    """
    for path in (f for model in models for f in project_directory.rglob(f"*.{model}")):
        if not path.is_dir():
            continue
        owd = owd_path_from_worker_directory(path)
        if owd.exists():
            yield owd


def yield_libraries_from_project(
    project_directory: pathlib.Path,
) -> Iterable[pathlib.Path]:
    """
    Yield a generator of library directory paths from a project path.

    Yields
    ------
    pathlib.Path
        The next library from the project.

    """

    def directory_is_a_library(directory: pathlib.Path) -> bool:
        # It's a library if
        # - Contains Library.mk
        file_path = directory / "Library.mk"
        if file_path.exists():
            return True
        # - Contains Makefile referencing library.mk
        file_path = directory / "Makefile"
        fragment = b"include $(OCPI_CDK_DIR)/include/library.mk"
        fragment_node = treesitter.parser.MAKE.parse(fragment).root_node.children[0]
        if file_path.exists():
            tree = treesitter.parser.MAKE.parse(file_path.read_bytes())
            for node in tree.root_node.children:
                if treesitter.node.structural_equality(node, fragment_node):
                    return True
        # - Contains <name>.xml with tag `library`
        xml_file_path = directory / f"{directory.stem}.xml"
        if xml_file_path.exists():
            et_tree = etree.parse(xml_file_path, parser=XML_PARSER)
            root = et_tree.getroot()
            if root.tag == "library":
                return True
        return False

    components_directory_path = project_directory / "components"
    if components_directory_path.exists():
        if directory_is_a_library(components_directory_path):
            yield components_directory_path
        else:
            yield from (
                path
                for path in components_directory_path.iterdir()
                if path.is_dir() and directory_is_a_library(path)
            )
    # hdl/adapters if it exists
    hdl_adapters_path = project_directory / "hdl" / "adapters"
    if hdl_adapters_path.exists():
        yield hdl_adapters_path
    # hdl/cards if it exists
    hdl_cards_path = project_directory / "hdl" / "cards"
    if hdl_cards_path.exists():
        yield hdl_cards_path
    # hdl/devices if it exists
    hdl_devices_path = project_directory / "hdl" / "devices"
    if hdl_devices_path.exists():
        yield hdl_devices_path


def yield_workers_from_library(
    library_directory: pathlib.Path,
) -> Iterable[pathlib.Path]:
    """
    Yield a generator of worker directory paths from a library path.

    Yields
    ------
    pathlib.Path
        The next worker from the library.

    """
    for path in library_directory.iterdir():
        if not path.is_dir():
            continue
        if len(path.suffixes) == 0:
            continue
        model = path.suffix[1:]
        if model not in MODELS:
            continue
        yield path


def yield_components_from_project(
    project_directory: pathlib.Path,
) -> Iterable[pathlib.Path]:
    """
    Yield a generator of component file paths from a project path.

    Yields
    ------
    pathlib.Path
        The next component from the project.

    """

    def yield_specs_from_directory(directory: pathlib.Path) -> Iterable[pathlib.Path]:
        specs = directory / "specs"
        if not specs.exists():
            return
        for path in specs.iterdir():
            if path.suffix != ".xml":
                continue
            if not path.stem.endswith("spec"):
                continue
            yield path

    # Project level specs
    yield from yield_specs_from_directory(project_directory)
    # Libraries
    for library in yield_libraries_from_project(project_directory):
        # Specs folder
        yield from yield_specs_from_directory(library)
        # Comp directories
        for path in library.iterdir():
            if not path.is_dir():
                continue
            if path.suffix != ".comp":
                continue
            for child in path.iterdir():
                if child.suffix != ".xml":
                    continue
                if not child.stem.endswith("comp") and not child.stem.endswith("spec"):
                    continue
                yield child


def yield_recursive_findall(
    element: etree._Element,
    tag: str,
) -> Iterable[etree._Element]:
    """
    Yield all occurrences of a given XML tag at any depth in an XML tree.

    Yields
    ------
    etree._Element
        The next XML element with the requested tag.

    """
    if element.tag == tag:
        yield element
    for child in element:
        yield from yield_recursive_findall(child, tag)


class Arguments:
    """Class containing all globally relevant command line arguments."""

    dry_run: bool
    to_version: Version
    verbose: bool

    def __init__(self, namespace: argparse.Namespace) -> None:
        """Construct."""
        self.dry_run = namespace.dry_run
        self.to_version = namespace.to_version
        self.verbose = namespace.verbose


# There are three ways to declare slaves
def yield_slave_workers_from_proxy(path: pathlib.Path) -> Iterable[str]:
    """
    Yield the names of all of the workers that this worker is a proxy for.

    Yields
    ------
    str
        The next slave worker name from the proxy.

    """
    tree = etree.parse(path, parser=XML_PARSER)
    root = tree.getroot()
    slave = root.attrib.get("slave")
    if slave is not None:
        yield slave.split(".")[-2]
    else:
        slaves = root.find("slaves")
        if slaves is not None:
            for instance in yield_recursive_findall(slaves, "instance"):
                worker = instance.attrib.get("worker")
                if worker is None:
                    logger.error(
                        "File '%s' is malformed: instance without worker. "
                        "File renaming could operate incorrectly",
                        path,
                    )
                else:
                    yield worker.split(".")[-2]
        else:
            slaves = root.findall("slave")
            if slaves is not None:
                for slave in slaves:
                    worker = slave.attrib.get("worker")
                    if worker is not None:
                        yield worker.split(".")[-2]


def rename_file_in_project(
    project_directory: pathlib.Path,
    from_files: str | list[str],
    to_files: str | list[str],
    arguments: Arguments,
) -> list[tuple[pathlib.Path, pathlib.Path]]:
    """."""
    if arguments.to_version < V2_4_7:
        return []
    logger.debug(
        "rename_file_in_project(%s, %s, %s, ..., ...)",
        project_directory,
        from_files,
        to_files,
    )
    files_moved = []
    if isinstance(from_files, str):
        from_files = [from_files]
    if isinstance(to_files, str):
        to_files = [to_files]
    for from_file, to_file in zip(from_files, to_files, strict=True):
        for from_file_path in project_directory.glob(from_file):
            # Eval the to_file as a path
            try:
                to_file_path = eval(  # noqa: S307
                    to_file,
                    {},  # {"__builtins__": __builtins__},
                    {"file": from_file_path},
                )
            except Exception as e:  # noqa: BLE001
                logger.warning(
                    "Moving '%s' aborted as expression '%s' couldn't be parsed: %s",
                    from_file,
                    to_file,
                    e,
                )
                logger.warning(
                    "Note: Some files may have moved before this abort was called",
                )
                return []
            # Make all parents
            to_file_path.parent.mkdir(parents=True, exist_ok=True)
            # Then rename
            if not arguments.dry_run:
                from_file_path.rename(to_file_path)
            logger.info("Moved '%s' to '%s'", from_file_path, to_file_path)
            files_moved.append((from_file_path, to_file_path))
    return files_moved


def v2_4_7_owd_rename(
    worker_directory: pathlib.Path,
    arguments: Arguments,
    workers_with_proxies: list[str],
) -> bool:
    """
    Rename all OWD files to their v2.4.7 names.

    - Move all *.hdl/*.xml to *.hdl/*-hdl.xml
    - Move all *.rcc/*.xml to *.rcc/*-rcc.xml

    This isn't done for workers that are proxied when moving to v2.4.7 or
    earlier.

    See https://opencpi.dev/t/broken-hdl-worker-search-path-on-slave-attributes/105

    This function ignores OWDs that have already been migrated.
    """
    if arguments.to_version < V2_4_7:
        return False
    name = worker_directory.stem
    model = worker_directory.suffix[1:]
    old_owd_file = worker_directory / f"{name}.xml"
    logger.debug("Checking if '%s' requires a rename", old_owd_file)
    # Ignore already converted workers
    if not old_owd_file.exists():
        logger.debug(
            "File '%s' not found, assuming conversion already completed",
            old_owd_file,
        )
        return False
    # Ignore workers that have a proxy
    if arguments.to_version <= V2_4_7 and worker_directory.stem in workers_with_proxies:
        logger.debug(
            "'%s' is used in a proxy, can't convert in v2.4.7 or earlier",
            old_owd_file,
        )
        return False
    # Rename the file
    new_owd_file = worker_directory / f"{name}-{model}.xml"
    if not arguments.dry_run:
        old_owd_file.rename(new_owd_file)
    logger.info("Moved '%s' to '%s'", old_owd_file, new_owd_file)
    return True


def replace_text_in_file(
    file_path: pathlib.Path,
    text_from: list[str],
    text_to: str,
    arguments: Arguments,
) -> bool:
    """Replace any matching text in the file."""
    if arguments.to_version < V2_4_7:
        return False
    logger.debug("Scanning '%s' ... ", file_path)
    with file_path.open("r") as file:
        lines = file.readlines()
    changed_something = False
    for i, line in enumerate(lines):
        for case in text_from:
            if case in line:
                lines[i] = line.replace(case, text_to)
                logger.info(
                    "Replaced '%s' with '%s' on line %d of '%s'",
                    case,
                    text_to,
                    i,
                    file_path,
                )
                changed_something = True
                break
    if changed_something and not arguments.dry_run:
        with file_path.open("w") as file:
            file.writelines(lines)
    return changed_something


def parse_variables_from_makefiles(
    file_paths: list[pathlib.Path],
    file_identifier: str,
    config: Config,
) -> tuple[bool, dict[str, str]]:
    """Try to parse makefiles, returning a dictionary of their top level variables."""
    variables: dict[str, str] = {}
    node_fragments_to_ignore = config.get_list_setting_for_parse(
        "makefile",
        file_identifier,
        "node-fragments-to-ignore",
    )
    nodes_to_ignore = [
        treesitter.parser.MAKE.parse(fragment.encode("utf-8")).root_node.children[0]
        for fragment in node_fragments_to_ignore
    ]
    node_types_to_ignore = config.get_list_setting_for_parse(
        "makefile",
        file_identifier,
        "node-types-to-ignore",
    )
    for file_path in file_paths:
        if not file_path.exists():
            logger.debug(
                "File '%s' not found, assuming conversion already completed",
                file_path,
            )
            continue
        tree = treesitter.parser.MAKE.parse(file_path.read_bytes())
        for child in tree.root_node.children:
            # If node can be ignored, ignore it
            if child.type in node_types_to_ignore:
                logger.debug(
                    "Node ('%s') of type '%s' on line %d of '%s' is ignored "
                    "due to config",
                    treesitter.node.source_as_str(child),
                    child.type,
                    child.start_point[0],
                    file_path,
                )
                continue
            match_found = False
            for node in nodes_to_ignore:
                if treesitter.node.structural_equality(child, node):
                    logger.debug(
                        "Node ('%s') matches an ignored node",
                        treesitter.node.to_string(child),
                    )
                    match_found = True
                    break
            if match_found:
                continue
            # If variable is parsable, parse it. If not, fail
            if child.type == "variable_assignment":
                try:
                    treesitter.makefile.update_from_variable_assignments(
                        child,
                        variables,
                    )
                    continue
                except RuntimeError as err:
                    logger.warning(
                        "File '%s' not converted: %s",
                        file_path,
                        str(err),
                    )
                    return False, variables
            # Node hasn't been recognised or ignored, so fail
            logger.debug(
                "Node ('%s') of type '%s' not supported when parsing %s to %s in '%s'",
                treesitter.node.source_as_str(child),
                child.type,
                child.start_point,
                child.end_point,
                file_path,
            )
            logger.warning(
                "File '%s' not parsed due to unrecognised node at position %s",
                file_path,
                child.start_point,
            )
            return False, variables
    return True, variables


def check_variables_for_xml(
    variables: dict[str, str],
    file_paths: list[pathlib.Path],
    file_identifier: str,
    config: Config,
) -> bool:
    """Check a collection of variables for validity in a given XML document."""
    accepted_variables = config.get_list_setting_for_parse(
        "xml",
        file_identifier,
        "accepted-variables",
    )
    not_recommended_variables = config.get_dict_setting_for_parse(
        "xml",
        file_identifier,
        "not-recommended-variables",
    )
    recommended_variables = config.get_dict_setting_for_parse(
        "xml",
        file_identifier,
        "recommended-variables",
    )
    for k in variables:
        if k in accepted_variables:
            continue
        if k in not_recommended_variables:
            logger.warning(
                "Variable '%s' not recommended when converting '%s' (%s)",
                k,
                [str(file_path) for file_path in file_paths],
                not_recommended_variables[k],
            )
            continue
        # Variable not recognised
        logger.warning(
            "Files '%s' not converted due to unrecognised variable: %s",
            [str(file_path) for file_path in file_paths],
            k,
        )
        return False
    for k in recommended_variables:
        if k not in variables:
            logger.warning(
                "Variable '%s' recommended for inclusion when converting '%s' (%s)",
                k,
                [str(file_path) for file_path in file_paths],
                recommended_variables[k],
            )
            continue
    return True


def categorise_by_parent(
    paths: list[pathlib.Path],
) -> dict[pathlib.Path, list[pathlib.Path]]:
    """Categorise a list of paths by their parents."""
    ret: dict[pathlib.Path, list[pathlib.Path]] = {}
    for path in paths:
        if path.parent in ret:
            ret[path.parent].append(path)
        else:
            ret[path.parent] = [path]
    return ret


def translate_makefile_to_xml_in_project(  # noqa: PLR0912, PLR0914, PLR0915
    project_directory: pathlib.Path,
    from_file_identifier: str,
    to_file_identifier: str,
    arguments: Arguments,
    config: Config,
) -> bool:
    """Migrate a makefile to an xml file in a project."""
    if arguments.to_version < V2_4_7:
        return False
    logger.debug(
        "translate_makefile_to_xml_in_project(%s, %s, %s, ..., ...)",
        project_directory,
        from_file_identifier,
        to_file_identifier,
    )
    project_relative_old_file_paths = config.get_list_setting_for_parse(
        "makefile",
        from_file_identifier,
        "paths",
    )
    if len(project_relative_old_file_paths) == 0:
        logger.warning(
            "Setting 'ocpiupdate.makefile.%s.paths' not found or empty",
            from_file_identifier,
        )
        return False
    old_file_paths = [
        path
        for project_relative_old_file_path in project_relative_old_file_paths
        for path in project_directory.glob(project_relative_old_file_path)
    ]
    old_file_path_groups = categorise_by_parent(old_file_paths)
    any_converted = False
    for old_file_paths in old_file_path_groups.values():
        # Check that all the variables are acceptable, terminate if they aren't
        parsable, variables = parse_variables_from_makefiles(
            old_file_paths,
            from_file_identifier,
            config,
        )
        if not parsable:
            continue
        translated_from_makefile_variables = config.get_dict_setting_for_parse(
            "xml",
            to_file_identifier,
            "translated-from-makefile-variables",
        )
        xml_variables = {
            translated_from_makefile_variables.get(k, k): v
            for k, v in variables.items()
        }
        valid = check_variables_for_xml(
            xml_variables,
            old_file_paths,
            to_file_identifier,
            config,
        )
        if not valid:
            continue
        # Build the XML file
        root_tag = config.get_setting_for_parse(
            "xml",
            to_file_identifier,
            "tag",
        )
        if root_tag is None:
            logger.warning(
                "Setting 'ocpiupdate.xml.%s.tag' not found",
                to_file_identifier,
            )
            continue
        project_relative_new_file_path = config.get_setting_for_parse(
            "xml",
            to_file_identifier,
            "path",
        )
        if project_relative_new_file_path is not None:
            new_file_path = project_directory / project_relative_new_file_path
        else:
            makefile_relative_new_file_path = config.get_setting_for_parse(
                "xml",
                to_file_identifier,
                "path-relative-to-makefile",
            )
            if makefile_relative_new_file_path is None:
                logger.warning(
                    "Setting 'ocpiupdate.xml.%s.path' not found",
                    to_file_identifier,
                )
                logger.warning(
                    "Setting 'ocpiupdate.xml.%s.path-relative-to-makefile' not found",
                    to_file_identifier,
                )
                continue
            makefile_path = None
            for old_file_path in old_file_paths:
                if old_file_path.stem == "Makefile":
                    makefile_path = old_file_path
                    break
            if makefile_path is None:
                logger.warning(
                    "File '%s' does not define a 'Makefile'",
                    [str(old_file_path) for old_file_path in old_file_paths],
                )
                continue
            new_file_path = eval(  # noqa: S307
                makefile_relative_new_file_path,
                {},  # {"__builtins__": __builtins__},
                {"file": makefile_path},
            )
        existing_old_file_paths = [
            old_file_path for old_file_path in old_file_paths if old_file_path.exists()
        ]
        if len(existing_old_file_paths) == 0:
            logger.debug(
                "File '%s' not found; assuming nothing to convert",
                [str(old_file_path) for old_file_path in old_file_paths],
            )
            continue
        # Write new files
        if not new_file_path.exists():
            if not arguments.dry_run:
                et_root = etree.Element(root_tag, attrib=xml_variables)
                et_tree = etree.ElementTree(et_root)
                et_tree.write(new_file_path, encoding="utf-8", xml_declaration=True)
            logger.info(
                "Created '%s' from '%s' ('%s', %s)",
                new_file_path,
                [str(old_file_path) for old_file_path in existing_old_file_paths],
                root_tag,
                xml_variables,
            )
        # Modify existing files
        elif len(xml_variables) != 0:
            # Parse the existing XML
            treesitter_tree = treesitter.parser.XML.parse(new_file_path.read_bytes())
            root_node = treesitter_tree.root_node
            old_xml_source = treesitter.node.source_as_bytes(root_node)
            # Ensure no variable collision
            element = treesitter.xml.get_document_element_node_from_document_node(
                root_node,
            )
            if element is None:
                logger.warning(
                    "File '%s' does not contain a root node; aborting",
                    new_file_path,
                )
                continue
            attributes = treesitter.xml.get_attributes_from_document_element_node(
                element,
            )
            for attribute in attributes:
                if attribute in xml_variables:
                    logger.warning(
                        "File '%s' contains variables that are also set in '%s'; "
                        "aborting migration (xml {%s: %s}, makefile {%s: %s})",
                        new_file_path,
                        [
                            str(old_file_path)
                            for old_file_path in existing_old_file_paths
                        ],
                        attribute,
                        attributes[attribute],
                        attribute,
                        xml_variables[attribute],
                    )
                    continue
            # Add the new stuff
            indent = treesitter.xml.get_common_indent_from_document_element_node(
                old_xml_source,
                element,
            )
            new_xml_source = treesitter.xml.add_attributes(
                old_xml_source,
                element,
                xml_variables,
                indent.decode("utf-8") if indent is not None else " ",
            )
            if not arguments.dry_run:
                new_file_path.write_bytes(new_xml_source)
            logger.info(
                "Added content from '%s' to '%s' "
                "(current attributes: %s, added attributes: %s)",
                [str(old_file_path) for old_file_path in existing_old_file_paths],
                new_file_path,
                attributes,
                xml_variables,
            )
            logger.debug(
                "Old content:\n\n%s\nNew content:\n\n%s\n",
                old_xml_source,
                new_xml_source,
            )
        # Delete old files
        for old_file_path in existing_old_file_paths:
            if not arguments.dry_run:
                old_file_path.unlink()
            logger.info("Deleted '%s'", old_file_path)
        any_converted = True
    return any_converted


def directory_is_a_project(directory: pathlib.Path) -> bool:
    """Return True if the given directory is a project."""
    # It's a project if
    # - Contains Project.xml with tag `project`
    xml_file_path = directory / "Project.xml"
    if xml_file_path.exists():
        et_tree = etree.parse(xml_file_path, parser=XML_PARSER)
        root = et_tree.getroot()
        if root.tag == "project":
            return True
    # - Contains Project.mk
    file_path = directory / "Project.mk"
    if file_path.exists():
        return True
    # - Contains Makefile referencing project.mk
    file_path = directory / "Makefile"
    fragment = b"include $(OCPI_CDK_DIR)/include/project.mk"
    fragment_node = treesitter.parser.MAKE.parse(fragment).root_node.children[0]
    if file_path.exists():
        tree = treesitter.parser.MAKE.parse(file_path.read_bytes())
        for node in tree.root_node.children:
            if treesitter.node.structural_equality(node, fragment_node):
                return True
    return False


DEFAULT_CONFIG_PATH = pathlib.Path(__file__).parent / "ocpiupdate.toml"


def main(user_args: list[str] = sys.argv[1:]) -> None:  # noqa: PLR0912, PLR0914, PLR0915
    """Run the script."""
    # Argument parsing
    argparser = argparse.ArgumentParser()
    argparser.add_argument(
        "projects",
        nargs="*",
        help="The projects to update (defaults to the current directory)",
        type=pathlib.Path,
    )
    argparser.add_argument(
        "--config",
        action="append",
        type=pathlib.Path,
        default=[DEFAULT_CONFIG_PATH],
        help="Paths to config files to use. These are applied in order",
    )
    argparser.add_argument(
        "--config-string",
        action="append",
        type=str,
        default=[],
        help="Strings of TOML to use as config. These are applied after config files",
    )
    argparser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what the program would do, but don't write anything to disk",
    )
    argparser.add_argument(
        "--no-default-config",
        action="store_true",
        help="Prevent the loading of the default config file",
    )
    argparser.add_argument(
        "--to-version",
        type=Version,
        help="The OpenCPI version to migrate to (2.4.7 [default] or newer)",
        default=V2_4_7,
    )
    argparser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable printing debug messages to stdout",
    )
    argparser.add_argument(
        "--version",
        action="store_true",
        help="Print the version of the program and exit",
    )
    args, unknown_args = argparser.parse_known_args(user_args)
    if len(unknown_args) != 0:
        logger.error("Extra arguments not recognised: %s", unknown_args)
        sys.exit(1)

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    if args.version:
        print(importlib.metadata.version(__package__.split(".")[0]))  # noqa: T201
        sys.exit(0)

    try:  # noqa: PLR1702
        # Load configuration
        if args.no_default_config:
            args.config.remove(DEFAULT_CONFIG_PATH)
        logger.debug(
            "Attempting to parse '%s' and TOML '%s' ...",
            args.config,
            args.config_string,
        )
        config = Config.from_files_and_toml_strings(args.config, args.config_string)
        config.validate()
        logger.debug("Parsed config: %s", str(config))

        # Start of processing
        if len(args.projects) == 0:
            args.projects = [pathlib.Path.cwd()]
        arguments = Arguments(args)
        logger.debug("Running over projects '%s' ...", args.projects)
        for project in args.projects:
            if not directory_is_a_project(project):
                logger.error("Directory '%s' is not a project", project)
                sys.exit(1)

        # Get the names of every worker that has a proxy
        workers_with_proxies: list[str] = []
        if arguments.to_version <= V2_4_7:
            for project in args.projects:
                for library in yield_libraries_from_project(project):
                    for worker in yield_workers_from_library(library):
                        # Ignore everything but RCCs
                        if worker.suffix[1:] != "rcc":
                            continue
                        # Parse its XML
                        owd = owd_path_from_worker_directory(worker)
                        if not owd.exists():
                            logger.debug(
                                "Worker directory '%s' doesn't have an OWD. "
                                "File renaming could operate incorrectly",
                                worker,
                            )
                            continue
                        workers_with_proxies.extend(yield_slave_workers_from_proxy(owd))
        logger.debug("Workers that are proxied: %s", workers_with_proxies)

        # Do updates
        migrate_table = typing.cast("ConfigMigrateDict", config["migrate"])
        inplace_replaces_required: dict[str, list[tuple[list[str], str]]] = {}
        all_files_moved: list[tuple[pathlib.Path, pathlib.Path]] = []
        for project in args.projects:
            for library in yield_libraries_from_project(project):
                for worker in yield_workers_from_library(library):
                    v2_4_7_owd_rename(worker, arguments, workers_with_proxies)
            for strategy in migrate_table:
                for identifier in migrate_table[strategy]:  # type: ignore[literal-required]
                    if strategy == "translate":
                        translate_id_table = typing.cast(
                            "ConfigMigrateTranslateIdentifierDict",
                            config[f"migrate.translate.{identifier}"],
                        )
                        migrate_from = translate_id_table["from"]
                        migrate_to = translate_id_table["to"]
                        if migrate_from == "makefile" and migrate_to == "xml":
                            translate_makefile_to_xml_in_project(
                                project,
                                identifier,
                                identifier,
                                arguments,
                                config,
                            )
                    elif strategy == "rename":
                        rename_id_table = typing.cast(
                            "ConfigMigrateRenameIdentifierDict",
                            config[f"migrate.rename.{identifier}"],
                        )
                        rename_from = rename_id_table["from"]
                        rename_to = rename_id_table["to"]
                        rename_inplace_from = rename_id_table["inplace-from"]
                        rename_inplace_to = rename_id_table["inplace-to"]
                        files_moved = rename_file_in_project(
                            project,
                            rename_from,
                            rename_to,
                            arguments,
                        )
                        all_files_moved.extend(files_moved)
                        replaces_required = inplace_replaces_required.get(identifier)
                        if replaces_required is None:
                            inplace_replaces_required[identifier] = []
                            replaces_required = inplace_replaces_required[identifier]
                        for from_file, to_file in files_moved:
                            evaluated_inplace_from = [
                                eval(  # noqa: S307
                                    e,
                                    {},  # {"__builtins__": __builtins__},
                                    {"file": from_file},
                                )
                                for e in rename_inplace_from
                            ]
                            evaluated_inplace_to = eval(  # noqa: S307
                                rename_inplace_to,
                                {},  # {"__builtins__": __builtins__},
                                {"file": to_file},
                            )
                            replaces_required.append(
                                (
                                    typing.cast("list[str]", evaluated_inplace_from),
                                    typing.cast("str", evaluated_inplace_to),
                                ),
                            )
                    else:
                        logger.warning(
                            "Migration strategy '%s' isn't supported",
                            strategy,
                        )

            # Fix any links that we've accidentally broken
            logger.debug("Files moved: %s", all_files_moved)
            for orig, broken_link in (
                (orig, dest)
                for orig, dest in all_files_moved
                if dest.is_symlink() and not pathlib.Path.readlink(dest).exists()
            ):
                logger.debug(
                    "Found broken symlink: %s (%s)",
                    broken_link,
                    broken_link.readlink(),
                )
                try:
                    link_target = (
                        (orig.parent / broken_link.readlink()).resolve().absolute()
                    )
                except OSError as e:
                    logger.warning(
                        "Failed to read link target of '%s': %s",
                        broken_link,
                        e,
                    )
                    continue
                logger.debug("Broken link target: %s", link_target)

                for original, new in all_files_moved:
                    if original == link_target:
                        old_link_target = broken_link.readlink()
                        new_link_target = new.relative_to(
                            broken_link.parent,
                            walk_up=True,
                        )
                        logger.info(
                            "Fixing broken symlink '%s' (was '%s', now '%s')",
                            broken_link,
                            old_link_target,
                            new_link_target,
                        )
                        if not arguments.dry_run:
                            broken_link.unlink()
                            broken_link.symlink_to(new_link_target)
                        break

        for project in args.projects:
            for identifier, replaces in inplace_replaces_required.items():
                identifier_table = typing.cast(
                    "ConfigMigrateRenameIdentifierDict",
                    config[f"migrate.rename.{identifier}"],
                )
                categories = identifier_table["inplace-search"]
                models = []
                if "hdl-worker" in categories:
                    models.append("hdl")
                if "rcc-worker" in categories:
                    models.append("rcc")
                if len(models) != 0:
                    for owd in yield_owd_from_project(project, models=models):
                        for inplace_from, inplace_to in replaces:
                            replace_text_in_file(
                                owd,
                                inplace_from,
                                inplace_to,
                                arguments,
                            )
                if "component" in categories:
                    for component in yield_components_from_project(project):
                        for inplace_from, inplace_to in replaces:
                            replace_text_in_file(
                                component,
                                inplace_from,
                                inplace_to,
                                arguments,
                            )
    except Exception as err:
        logger.error(str(err))  # noqa: TRY400
        if args.verbose:
            raise
        sys.exit(1)


if __name__ == "__main__":
    main()
