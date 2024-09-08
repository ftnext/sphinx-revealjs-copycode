# sphinx-revealjs-copycode

## Usage

Install in your sphinx-revealjs project.

```
$ pip install sphinx-revealjs-copycode
```

Create your presentation with sphinx-revealjs.

Then edit `conf.py` to use this extension.

```diff
extensions = [
    "sphinx_revealjs",
+    "sphinx_revealjs_copycode",
]

+revealjs_script_plugins = [
+    {
+        "name": "CopyCode",
+        "src": "revealjs4/plugin/copycode/copycode.js",
+    },
+]
```
