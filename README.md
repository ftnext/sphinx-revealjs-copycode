# sphinx-revealjs-copycode

[attakei/sphinx-revealjs](https://github.com/attakei/sphinx-revealjs) meets [Martinomagnifico/reveal.js-copycode](https://github.com/Martinomagnifico/reveal.js-copycode)!

## Usage

Install in your sphinx-revealjs project.

```
$ pip install sphinx-revealjs-copycode
```

Create your presentation with sphinx-revealjs.

Then edit `conf.py` to use this extension.  
Just add one line!!

```diff
extensions = [
    "sphinx_revealjs",
+    "sphinx_revealjs_copycode",
]
```

## Configuration

### revealjs_copycode_tag

You can specify the version of the reveal.js-copycode plugin to use by setting the `revealjs_copycode_tag` in your `conf.py`:

```python
revealjs_copycode_tag = "v1.2.0"  # Example: Set a custom version. If not set, the default version "v1.3.0" will be used.
```

This allows you to use a specific version of the plugin if needed.

You can check available tags at [reveal.js-copycode tags](https://github.com/Martinomagnifico/reveal.js-copycode/tags).
