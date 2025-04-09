from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from bs4 import BeautifulSoup

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


def assert_html_not_have_script_tag_with_src(html: str, dont_src: str):
    soup = BeautifulSoup(html, "html.parser")
    elements = [e for e in soup.find_all("script") if e.get("src") == dont_src]
    assert len(elements) == 0


def assert_revealjs_script_tag_doesnot_have_code(html: str, dont_code: str):
    soup = BeautifulSoup(html, "html.parser")
    revealjs_script = soup.find_all("script")[-1]
    assert dont_code not in str(revealjs_script)


@pytest.mark.sphinx("revealjs", testroot="migrate-sphinx-revealjs-v2")
def test_script_src_no_revealjs4(app: SphinxTestApp) -> None:
    app.build()

    contents = (app.outdir / "index.html").read_text()
    assert_html_not_have_script_tag_with_src(
        contents, "_static/revealjs4/plugin/copycode/copycode.js"
    )


@pytest.mark.sphinx("revealjs", testroot="migrate-sphinx-revealjs-v2")
def test_copycode_should_not_duplicate_in_revealjs_script_tag(
    app: SphinxTestApp,
) -> None:
    app.build()

    contents = (app.outdir / "index.html").read_text()
    assert_revealjs_script_tag_doesnot_have_code(
        contents, "CopyCode,CopyCode,"
    )
