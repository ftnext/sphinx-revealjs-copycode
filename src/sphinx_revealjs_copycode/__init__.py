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

__version__ = "0.4.2"
logger = logging.getLogger(__name__)


def get_plugin_dir() -> Path:
    return Path(__file__).parent / "_static"


def download_copycode_plugin(tag: str) -> None:
    plugin_dir_path = get_plugin_dir()
    copycode_path = plugin_dir_path / "copycode"
    copycode_path.mkdir(parents=True, exist_ok=True)

    version_dir = copycode_path / tag
    if version_dir.exists():
        logger.info(
            "✅ Reveal.js CopyCode plugin version %s is already installed",
            tag,
        )
    else:
        logger.info(
            "Reveal.js CopyCode plugin version %s is not yet installed. "
            "Need to install it",
            tag,
        )
        url = (
            "https://github.com/Martinomagnifico/reveal.js-copycode/"
            f"archive/refs/tags/{tag}.zip"
        )
        with urlopen(url) as response:
            bytes_stream = BytesIO(response.read())
        with ZipFile(bytes_stream) as zf, TemporaryDirectory() as tmpdir:
            version_number = tag.removeprefix("v")
            copycode_files = [
                member
                for member in zf.namelist()
                if member.startswith(
                    f"reveal.js-copycode-{version_number}/plugin/copycode"
                )
            ]

            tmpdir_path = Path(tmpdir)
            zf.extractall(tmpdir_path, copycode_files)

            version_dir.mkdir(exist_ok=True)
            src_dir = (
                tmpdir_path
                / f"reveal.js-copycode-{version_number}/plugin/copycode"
            )
            for file in src_dir.iterdir():
                shutil.move(file, version_dir)

            logger.info(
                "✅ Installed Reveal.js CopyCode plugin version %s", tag
            )


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

    tag = app.config.revealjs_copycode_tag

    src_dir = get_plugin_dir() / "copycode" / tag

    dest_dir = app.outdir / "_static" / "revealjs" / "plugin" / "copycode"
    dest_dir.mkdir(parents=True, exist_ok=True)

    copy_asset(src_dir, dest_dir)


def setup(app: Sphinx) -> ExtensionMetadata:
    metadata = ExtensionMetadata(
        version=__version__, parallel_read_safe=False, parallel_write_safe=True
    )

    app.add_config_value("revealjs_copycode_tag", "v1.3.0", "html")

    download_copycode_plugin(app.config.revealjs_copycode_tag)

    app.connect("config-inited", tweak_builder_config)
    app.connect("build-finished", copy_copycode_assets)

    return metadata
