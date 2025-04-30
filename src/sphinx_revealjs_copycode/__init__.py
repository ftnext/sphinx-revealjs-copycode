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
    from sphinx.config import Config

__version__ = "0.4.0"
logger = logging.getLogger(__name__)


def get_plugin_dir() -> Path:
    return Path(__file__).parent / "_static"


def download_copycode_plugin(tag: str) -> None:
    plugin_dir_path = get_plugin_dir()
    plugin_dir_path.mkdir(parents=True, exist_ok=True)

    if (plugin_dir_path / "copycode").exists():
        logger.info("✅ Reveal.js CopyCode plugin is already installed")
    else:
        logger.info(
            "Reveal.js CopyCode plugin is not yet installed. "
            "Need to install it"
        )
        url = (
            f"https://github.com/Martinomagnifico/reveal.js-copycode/"
            f"archive/refs/tags/{tag}.zip"
        )
        with urlopen(url) as response:
            bytes_stream = BytesIO(response.read())
        with ZipFile(bytes_stream) as zf, TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            version_number = tag.removeprefix("v")
            for plugin_file in [
                "copycode.css",
                "copycode.esm.js",  # v1.2.0
                "copycode.js",
                "copycode.mjs",  # v1.3.0
            ]:
                base_path = f"reveal.js-copycode-{version_number}"
                plugin_path = f"{base_path}/plugin/copycode/{plugin_file}"
                try:
                    zf.extract(
                        plugin_path,
                        path=tmpdir_path,
                    )
                except KeyError:
                    pass
            shutil.move(
                tmpdir_path
                / f"reveal.js-copycode-{version_number}/plugin/copycode",
                plugin_dir_path,
            )
            logger.info("✅ Installed Reveal.js CopyCode plugin")


def tweak_builder_config(app: Sphinx, config: Config) -> None:
    revealjs_script_plugins = [
        plugin
        for plugin in config.revealjs_script_plugins
        if plugin["name"] != "CopyCode"
    ]
    revealjs_script_plugins.append(
        {
            "name": "CopyCode",
            "src": "revealjs/plugin/copycode/copycode.js",
        }
    )
    config.revealjs_script_plugins = revealjs_script_plugins


def copy_copycode_assets(app: Sphinx, exc):
    if app.builder.name != "revealjs":
        return
    if exc is not None:  # Build failed
        return

    copy_asset(
        get_plugin_dir() / "copycode",
        app.outdir / "_static" / "revealjs" / "plugin" / "copycode",
    )


def setup(app: Sphinx) -> ExtensionMetadata:
    metadata = ExtensionMetadata(
        version=__version__, parallel_read_safe=False, parallel_write_safe=True
    )

    app.add_config_value("revealjs_copycode_tag", "v1.2.0", "html")

    download_copycode_plugin(app.config.revealjs_copycode_tag)

    app.connect("config-inited", tweak_builder_config)
    app.connect("build-finished", copy_copycode_assets)

    return metadata
