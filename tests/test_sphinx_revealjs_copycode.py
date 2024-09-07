from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from sphinx.testing.util import SphinxTestApp


@pytest.mark.sphinx("revealjs", testroot="default")
def test_arrange_copycode_plugin(app: SphinxTestApp) -> None:
    app.build()

    assert (app.outdir / "_static/revealjs4/plugin/copycode").exists()
