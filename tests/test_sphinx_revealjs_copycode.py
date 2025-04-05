from __future__ import annotations

from importlib.metadata import version
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pathlib import Path

    from sphinx.testing.util import SphinxTestApp


def assert_directory_exists(expected_directory: Path) -> None:
    assert expected_directory.exists()
    assert expected_directory.is_dir()


def assert_file_exists(expected_file: Path) -> None:
    assert expected_file.exists()
    assert expected_file.is_file()


def assert_copycode_static_files_exist(
    expected_copycode_directory: Path,
) -> None:
    assert_file_exists(expected_copycode_directory / "copycode.js")
    assert_file_exists(expected_copycode_directory / "copycode.css")
    assert_file_exists(expected_copycode_directory / "copycode.esm.js")


@pytest.mark.skipif(
    not version("sphinx-revealjs").startswith("2."),
    reason="requires sphinx-revealjs v2",
)
@pytest.mark.sphinx("revealjs", testroot="sphinx-revealjs-v2")
def test_arrange_copycode_plugin_sphinx_revealjs_v2(
    app: SphinxTestApp,
) -> None:
    app.build()

    expected_copycode_directory = (
        app.outdir / "_static/revealjs/plugin/copycode"
    )
    assert_directory_exists(expected_copycode_directory)
    assert_copycode_static_files_exist(expected_copycode_directory)


@pytest.mark.skipif(
    not version("sphinx-revealjs").startswith("3."),
    reason="requires sphinx-revealjs v3",
)
@pytest.mark.sphinx("revealjs", testroot="sphinx-revealjs-v3")
def test_arrange_copycode_plugin_sphinx_revealjs_v3(
    app: SphinxTestApp,
) -> None:
    app.build()

    expected_copycode_directory = (
        app.outdir / "_static/revealjs/plugin/copycode"
    )
    assert_directory_exists(expected_copycode_directory)
    assert_copycode_static_files_exist(expected_copycode_directory)
