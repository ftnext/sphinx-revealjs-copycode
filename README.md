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

You can specify the version of reveal.js-copycode plugin to use by setting `revealjs_copycode_tag` in your `conf.py`:

```python
revealjs_copycode_tag = "v1.2.0"  # Default is "v1.3.0"
```

This allows you to use a specific version of the plugin if needed.
