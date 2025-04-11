from pathlib import Path
import sys

SOURCE = Path.cwd().parent.parent / "src"
sys.path.insert(0, str(SOURCE))

with (SOURCE / "phystool" / "__about__.py").open() as about:
    key, val = about.readline().split("=")
    if key.strip() == "__version__":
        release = val.strip()
        version = ".".join(release.split(".")[:2])
    else:
        raise ValueError(f"Version not found in {about}")


project = 'phystool'
author = 'Jérome Dufour'

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinxarg.ext',
]

html_theme = "sphinx_rtd_theme"
language = "fr"
