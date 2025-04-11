# -*- coding: utf-8 -*-

import typing as T

from .autotoctree import AutoTocTree

if T.TYPE_CHECKING:  # pragma: no cover
    from sphinx.application import Sphinx


def setup(app: "Sphinx"):
    app.add_directive("autotoctree", AutoTocTree)
