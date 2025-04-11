# -*- coding: utf-8 -*-

"""
Automatic API reference documentation generator for Sphinx.

While Sphinx's `autodoc extension <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_
lets you document Python modules, it still requires
manually including each module and defining members in your documentation. This module
automates that process by scanning your entire package structure and generating the
necessary .rst files with proper autodoc directives for all modules and packages. It supports
ignoring specific modules or packages through pattern matching, allowing you to exclude
internal, private, or third-party code from your documentation.
"""

import shutil
import dataclasses
from pathlib import Path
from functools import cached_property

from .template import (
    render_module,
    PackageTemplateParams,
    render_package,
)
from .vendor.picage import Package


def normalize_ignore_patterns(patterns: list[str]) -> list[str]:
    """
    Normalize ignore patterns by removing ``.py`` extensions.

    :param patterns: List of patterns to normalize

    :return: List of normalized patterns
    """
    normalized = []
    for pattern in patterns:
        if pattern.endswith(".py"):
            pattern = pattern[:-3]
        normalized.append(pattern)
    return normalized


def should_ignore(
    fullname: str,
    normalized_patterns: list[str],
) -> bool:
    """
    Determine if a module or package should be ignored based on its name.

    Checks if the module or package fullname matches any of the ignore patterns.
    A match occurs when the fullname starts with any pattern in the list.

    :param fullname: Full name of the module or package (e.g., "docfly.auto_api_doc")
    :param normalized_patterns: List of normalized ignore patterns

    :return: True if the module/package should be ignored, False otherwise

    Examples:
    >>> should_ignore("docfly.vendor", ["docfly.vendor"])
    True

    >>> should_ignore("docfly.vendor.picage", ["docfly.vendor"])
    True

    >>> should_ignore("docfly.auto_api_doc", ["docfly.vendor"])
    False

    >>> should_ignore("docfly.tests", ["docfly.tests", "docfly.vendor"])
    True

    >>> should_ignore("docfly._version", ["docfly._"])
    True
    """
    for pattern in normalized_patterns:
        if fullname.startswith(pattern):
            return True
    return False


def write_file(path: Path, text: str):
    """
    Write text to a file, creating parent directories if needed.
    """
    try:
        path.write_text(text, encoding="utf-8")
    except FileNotFoundError:
        path.parent.mkdir(parents=True)
        path.write_text(text, encoding="utf-8")


@dataclasses.dataclass
class ApiDocGenerator:
    """
    Generator for Sphinx API reference documentation.

    This class traverses a Python package structure and generates ``.rst`` files with
    appropriate autodoc directives for each module and package. The generated files
    maintain the package hierarchy and can be directly included in Sphinx documentation.

    Example generated autodoc code:

    .. code-block:: bash

        /path/to/dir_output/package
        /path/to/dir_output/package/subpackage1
        /path/to/dir_output/package/subpackage1/__init__.rst
        /path/to/dir_output/package/subpackage1/module.rst
        /path/to/dir_output/package/subpackage2/
        /path/to/dir_output/package/subpackage2/__init__.rst
        /path/to/dir_output/package/subpackage2/module.rst
        /path/to/dir_output/package/__init__.rst
        /path/to/dir_output/package/module1.rst
        /path/to/dir_output/package/module2.rst

    :param dir_output: Directory where generated ``.rst`` files will be written.
        Usually it is next to the sphinx doc ``conf.py`` file. For example,
        if your ``conf.py`` file is at ``docs/source/conf.py``, and your
        package name is ``docfly``, you should set ``dir_output`` to ``docs/source/api``.
        Then the autodoc code looks like::

            /docs/source/api/docfly
            /docs/source/api/docfly/__init__.rst
            /docs/source/api/docfly/module1.rst
            /docs/source/api/docfly/module2.rst
            /docs/source/api/docfly/...

    :param package_name: Name of the package to document.
    :param ignore_patterns: List of patterns for modules/packages to ignore.
        See :func:`should_ignore` for details on how patterns are matched.
    """

    dir_output: Path = dataclasses.field()
    package_name: str = dataclasses.field()
    ignore_patterns: list[str] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.ignore_patterns = normalize_ignore_patterns(self.ignore_patterns)

    @cached_property
    def package(self) -> Package:
        """
        Get the package object for the specified package name.
        """
        return Package(self.package_name)

    def fly(
        self,
        cleanup_before_fly: bool = True,
    ):
        """
        Generate the API documentation .rst files.

        Traverses the package structure and creates ``.rst`` files for each
        package and module. Each package gets an ``__init__.rst`` file that
        includes links to its sub-packages and modules.

        :param cleanup_before_fly: If True, remove existing output directory
            before generating new documentation
        """
        # clearn up existing api document
        if cleanup_before_fly:
            shutil.rmtree(self.dir_output, ignore_errors=True)

        # create .rst files
        for package, parent, sub_packages, sub_modules in self.package.walk():
            if should_ignore(package.fullname, self.ignore_patterns):
                continue
            filtered_sub_packages = [
                sub_package
                for sub_package in sub_packages
                if should_ignore(sub_package.fullname, self.ignore_patterns) is False
            ]
            filtered_sub_modules = [
                sub_module
                for sub_module in sub_modules
                if should_ignore(sub_module.fullname, self.ignore_patterns) is False
            ]
            package_template_params = PackageTemplateParams(
                package=package,
                sub_packages=filtered_sub_packages,
                sub_modules=filtered_sub_modules,
            )

            dir_package = self.dir_output.joinpath(*package.fullname.split("."))
            path_init_rst = dir_package.joinpath("__init__.rst")
            content = render_package(package_template_params)
            write_file(path_init_rst, content)

            for module in filtered_sub_modules:
                path_module = dir_package.joinpath(f"{module.shortname}.rst")
                content = render_module(module)
                write_file(path_module, content)
