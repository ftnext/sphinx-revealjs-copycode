from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from .helpers import (
    assert_html_has_script_tag_with_src,
    assert_revealjs_script_tag_with_code,
)

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
    assert_file_exists(expected_copycode_directory / "copycode.mjs")


@pytest.mark.sphinx("revealjs", testroot="single-plugin-copycode")
def test_arrange_copycode_plugin(
    app: SphinxTestApp,
) -> None:
    app.build()

    expected_copycode_directory = (
        app.outdir / "_static/revealjs/plugin/copycode"
    )
    assert_directory_exists(expected_copycode_directory)
    assert_copycode_static_files_exist(expected_copycode_directory)


@pytest.mark.sphinx("revealjs", testroot="single-plugin-copycode")
def test_script_src_copycode_plugin(app: SphinxTestApp) -> None:
    # ref: https://github.com/attakei/sphinx-revealjs/blob/v3.2.0/tests/test_configurations/test_scripts.py#L21  # noqa: E501
    app.build()

    contents = (app.outdir / "index.html").read_text()
    assert_html_has_script_tag_with_src(
        contents, "_static/revealjs/plugin/copycode/copycode.js"
    )


@pytest.mark.sphinx("revealjs", testroot="single-plugin-copycode")
def test_script_refer_copycode(app: SphinxTestApp) -> None:
    # ref: https://github.com/attakei/sphinx-revealjs/blob/v3.2.0/tests/test_configurations/test_scripts.py#L50  # noqa: E501
    app.build()

    contents = (app.outdir / "index.html").read_text()
    assert_revealjs_script_tag_with_code(contents, "CopyCode,")


@pytest.mark.sphinx("revealjs", testroot="with-other-revealjs-plugins")
def test_script_src_copycode_plugin_with_other_plugins(
    app: SphinxTestApp,
) -> None:
    app.build()

    contents = (app.outdir / "index.html").read_text()
    assert_html_has_script_tag_with_src(
        contents, "_static/revealjs/plugin/copycode/copycode.js"
    )


@pytest.mark.sphinx("revealjs", testroot="with-other-revealjs-plugins")
def test_script_refer_copycode_with_other_plugins(app: SphinxTestApp) -> None:
    app.build()

    contents = (app.outdir / "index.html").read_text()
    assert_revealjs_script_tag_with_code(contents, "CopyCode,")


@pytest.mark.sphinx("revealjs", testroot="custom-copycode-version")
def test_custom_copycode_version(app: SphinxTestApp) -> None:
    app.build()

    expected_copycode_directory = (
        app.outdir / "_static/revealjs/plugin/copycode"
    )
    assert_directory_exists(expected_copycode_directory)
    assert_file_exists(expected_copycode_directory / "copycode.js")
    assert_file_exists(expected_copycode_directory / "copycode.css")
    assert_file_exists(expected_copycode_directory / "copycode.esm.js")
