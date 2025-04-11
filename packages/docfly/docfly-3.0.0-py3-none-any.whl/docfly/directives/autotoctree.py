# -*- coding: utf-8 -*-

"""
AutoTocTree Sphinx Directive Implementation

This module implements a custom Sphinx directive ``.. autotoctree::`` that automatically
generates a ``toctree`` based on your documentation folder structure. It eliminates the need
to manually update ``toctree`` entries when you add or modify documentation sections.
"""

from pathlib import Path

import sphinx.util
from sphinx.directives.other import TocTree

from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import StringList

from ..autotoctree import IndexFileNotFoundError, PageFolder


class AutoTocTree(Directive):
    """
    Custom Sphinx directive that automatically includes subdirectory index files in a ``toctree``.

    This directive works by:

    1. Determining the current document's location
    2. Finding all subdirectories containing index files
    3. Extracting titles from those index files
    4. Generating a properly formatted toctree directive

    The directive supports all standard
    `toctree <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree>`_
    options (inherited from TocTree) plus additional custom options:

    :param append_ahead: Flag to append manual entries before the auto-detected entries
    :param index_file: Base name of index files to look for (default: "index")

    Example::

        .. autotoctree::
           :maxdepth: 1
           :index_file: index
    """

    # Define custom option names as class constants for clarity and maintainability
    _opt_append_ahead = "append_ahead"
    _opt_index_file = "index_file"
    _opt_index_file_default = "index"

    # Directive configuration
    has_content = True  # override default behavior of TocTree class

    option_spec = TocTree.option_spec.copy()
    option_spec[_opt_append_ahead] = directives.flag
    option_spec[_opt_index_file] = str

    def run(self):
        """
        Execute the directive to generate the ``toctree``.

        This method is called by Sphinx when processing the directive.
        It creates a docutils node tree representing the ``toctree``.

        :return: List of nodes to be inserted into the document
        """
        # Create an empty element node to hold our generated content
        node = nodes.Element()
        node.document = self.state.document
        # print(f"[DEBUG] {node.document = }") # for debug only

        # Get the path of the current file containing this directive
        current_file = self.state.document.current_source
        print(f"[DEBUG] {current_file = }")  # for debug only

        # Generate the RST content for the toctree
        output_rst = self.derive_toctree_rst(current_file)
        print(f"[DEBUG] {output_rst = }")  # for debug only

        # Convert the RST string into a list of lines with source information
        view_list = StringList(output_rst.splitlines(), source="")

        # Parse our generated RST content into docutils nodes
        sphinx.util.nested_parse_with_titles(self.state, view_list, node)

        # Return the children of our node (the parsed toctree nodes)
        return node.children

    def derive_toctree_rst(self, current_file: str):
        """
        Generate the RST content for the ``toctree`` directive.

        This method creates a string containing a complete ``toctree`` directive
        with entries for all subdirectories with index files.

        :param current_file: Path to the file containing this directive
        :return: String containing RST ``toctree`` directive

        Generate the rst content::

            .. toctree::
                args ...

                example.rst
                ...

        :param current_file:
        :return:
        """
        TAB = " " * 4  # Standard indentation
        lines = list()

        # Create the toctree directive header
        lines.append(".. toctree::")

        # Add all options from the original directive (like maxdepth, etc.)
        for opt in TocTree.option_spec:
            value = self.options.get(opt)
            if value is not None:
                line = "{indent}:{option}: {value}".format(
                    indent=TAB,
                    option=opt,
                    value=value,
                ).rstrip()
                lines.append(line)

        # Add a blank line after options (required by RST syntax)
        lines.append("")

        # If append_ahead option is set, add manual entries first
        if self._opt_append_ahead in self.options:
            for line in list(self.content):
                lines.append(TAB + line)

        # Get the index file name from options or use default
        index_file = self.options.get(
            self._opt_index_file,
            self._opt_index_file_default,
        )
        print(f"[DEBUG] {index_file = }")  # for debug only

        # Create ArticleFolder to scan the directory structure
        try:
            page_folder = PageFolder.new(
                dir=Path(current_file).parent,
                index_filename=index_file,
            )
        except IndexFileNotFoundError as e:
            print(
                f"You set index_file = {index_file} in an `.. autotoctree::` directive"
                f"in {current_file}, but cannot locate the right index_file in the current directory!"
            )
            raise e

        # Add each subdirectory with index file to the toctree
        for child_page_folder in page_folder.child_page_folders:
            line = f"{TAB}{child_page_folder.title} <{child_page_folder.path_str}>"
            lines.append(line)

        # If append_ahead option is not set, add manual entries after auto entries
        if self._opt_append_ahead not in self.options:
            for line in list(self.content):
                lines.append(TAB + line)

        # Add final blank line
        lines.append("")

        # Join all lines into a single string
        toctree = "\n".join(lines)
        return toctree
