from __future__ import annotations

from importlib.metadata import version
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.skipif(
    not version("sphinx-revealjs").startswith("2."),
    reason="requires sphinx-revealjs v2",
)
@pytest.mark.sphinx("revealjs", testroot="default")
def test_arrange_copycode_plugin_sphinx_revealjs_v2(
    app: SphinxTestApp,
) -> None:
    app.build()

    assert (app.outdir / "_static/revealjs4/plugin/copycode").exists()


@pytest.mark.skipif(
    not version("sphinx-revealjs").startswith("3."),
    reason="requires sphinx-revealjs v3",
)
@pytest.mark.sphinx("revealjs", testroot="default")
def test_arrange_copycode_plugin_sphinx_revealjs_v3(
    app: SphinxTestApp,
) -> None:
    app.build()

    assert (app.outdir / "_static/revealjs/plugin/copycode").exists()
