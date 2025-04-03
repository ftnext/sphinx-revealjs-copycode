from __future__ import annotations

import shutil
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import TYPE_CHECKING
from urllib.request import urlopen
from zipfile import ZipFile

from sphinx.util import logging
from sphinx.util.fileutil import copy_asset
from sphinx.util.typing import ExtensionMetadata

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = "0.2.0"
logger = logging.getLogger(__name__)


def copy_copycode_assets(app: Sphinx, exc):
    if exc is not None:  # Build failed
        return

    plugin_dir_path = Path(__file__).parent / "_static"
    plugin_dir_path.mkdir(parents=True, exist_ok=True)

    if (plugin_dir_path / "copycode").exists():
        logger.info("✅ Reveal.js CopyCode plugin is already installed")
    else:
        logger.info(
            "Reveal.js CopyCode plugin is not yet installed. "
            "Need to install it"
        )
        url = (
            "https://github.com/Martinomagnifico/reveal.js-copycode/"
            "archive/refs/tags/v1.2.0.zip"
        )
        with urlopen(url) as response:
            bytes_stream = BytesIO(response.read())
        with ZipFile(bytes_stream) as zf, TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            for plugin_file in [
                "copycode.css",
                "copycode.esm.js",
                "copycode.js",
            ]:
                zf.extract(
                    f"reveal.js-copycode-1.2.0/plugin/copycode/{plugin_file}",
                    path=tmpdir_path,
                )
            shutil.move(
                tmpdir_path / "reveal.js-copycode-1.2.0/plugin/copycode",
                plugin_dir_path,
            )
            logger.info("✅ Installed Reveal.js CopyCode plugin")

    for asset in ["copycode.css", "copycode.esm.js", "copycode.js"]:
        copy_asset(
            plugin_dir_path / "copycode" / asset,
            app.outdir
            / "_static"
            / "revealjs"
            / "plugin"
            / "copycode"
            / asset,
        )


def setup(app: Sphinx) -> ExtensionMetadata:
    metadata = ExtensionMetadata(
        version=__version__, parallel_read_safe=False, parallel_write_safe=True
    )

    app.connect("build-finished", copy_copycode_assets)

    return metadata
