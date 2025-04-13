"""Script to check basic config functionality."""

# ruff: noqa: S101

import pytest

from .util import ocpiupdate


def test_no_migrate() -> None:
    """Check that extra arguments cause an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_no_from() -> None:
    """Check that `migrate.rename.id` with no `from` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id = {}",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_from_invalid() -> None:
    """Check that `migrate.rename.id` with invalid `from` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = ''",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_no_to() -> None:
    """Check that `migrate.rename.id` with no `to` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_to_empty() -> None:
    """Check that `migrate.rename.id` with empty `to` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = ''",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_to_invalid() -> None:
    """Check that `migrate.rename.id` with invalid `to` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = '\"\"'",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_no_inplace_search() -> None:
    """Check that `migrate.rename.id` with no `inplace-search` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_inplace_search_empty() -> None:
    """Check that `migrate.rename.id` with empty `inplace-search` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
                "--config-string",
                "migrate.rename.id.inplace-search = []",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_inplace_search_invalid() -> None:
    """Check that `migrate.rename.id` with invalid `inplace-search` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
                "--config-string",
                "migrate.rename.id.inplace-search = ['project']",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_no_inplace_from() -> None:
    """Check that `migrate.rename.id` with no `inplace-from` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
                "--config-string",
                "migrate.rename.id.inplace-search = ['hdl-worker']",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_inplace_from_empty() -> None:
    """Check that `migrate.rename.id` with empty `inplace-from` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
                "--config-string",
                "migrate.rename.id.inplace-search = ['hdl-worker']",
                "--config-string",
                "migrate.rename.id.inplace-from = []",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_inplace_from_empty_element() -> None:
    """Check that `migrate.rename.id` with invalid `inplace-from` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
                "--config-string",
                "migrate.rename.id.inplace-search = ['hdl-worker']",
                "--config-string",
                "migrate.rename.id.inplace-from = ['']",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_inplace_from_invalid() -> None:
    """Check that `migrate.rename.id` with invalid `inplace-from` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
                "--config-string",
                "migrate.rename.id.inplace-search = ['hdl-worker']",
                "--config-string",
                "migrate.rename.id.inplace-from = ['file']",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_no_inplace_to() -> None:
    """Check that `migrate.rename.id` with no `inplace-to` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
                "--config-string",
                "migrate.rename.id.inplace-search = ['hdl-worker']",
                "--config-string",
                "migrate.rename.id.inplace-from = ['file.name']",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_inplace_to_empty() -> None:
    """Check that `migrate.rename.id` with invalid `inplace-to` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
                "--config-string",
                "migrate.rename.id.inplace-search = ['hdl-worker']",
                "--config-string",
                "migrate.rename.id.inplace-from = ['file.name']",
                "--config-string",
                "migrate.rename.id.inplace-to = ''",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_rename_inplace_to_invalid() -> None:
    """Check that `migrate.rename.id` with invalid `inplace-to` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.rename.id.from = '*'",
                "--config-string",
                "migrate.rename.id.to = 'file'",
                "--config-string",
                "migrate.rename.id.inplace-search = ['hdl-worker']",
                "--config-string",
                "migrate.rename.id.inplace-from = ['file.name']",
                "--config-string",
                "migrate.rename.id.inplace-to = 'file'",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_translate_no_from() -> None:
    """Check that `migrate.translate.id` with no `from` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.translate.id = {}",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_translate_from_invalid() -> None:
    """Check that `migrate.translate.id` with invalid `from` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.translate.id.from = 'toml'",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_translate_no_to() -> None:
    """Check that `migrate.translate.id` with no `to` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.translate.id.from = 'makefile'",
            ],
        )
    assert excinfo.value.code == 1


def test_migrate_translate_to_invalid() -> None:
    """Check that `migrate.translate.id` with invalid `to` causes an error."""
    with pytest.raises(SystemExit) as excinfo:
        ocpiupdate(
            [
                "--dry-run",
                "--no-default-config",
                "--config-string",
                "migrate.translate.id.from = 'makefile'",
                "--config-string",
                "migrate.translate.id.to = 'toml'",
            ],
        )
    assert excinfo.value.code == 1
