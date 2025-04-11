# -*- coding: utf-8 -*-

"""
Automatic Table of Contents (TOC) generator for Sphinx documentation.

This module provides tools to automatically generate Sphinx
`toctree <https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-toctree>`_
directives based on your documentation's folder structure. Instead of manually maintaining
TOC entries when adding or removing documentation pages, this functionality
examines your directory structure and builds appropriate ``toctree`` directives
with correct titles extracted from each document.

The main workflow involves:

1. Finding directories containing index files (rst, md, or ipynb)
2. Extracting the title from each index file
3. Generating a properly formatted toctree directive linking to all child pages

This approach ensures your documentation navigation stays organized and up-to-date
with minimal manual intervention.
"""

import typing as T
import json
import dataclasses
from pathlib import Path
from functools import cached_property

from .template import TocTemplateParams, render_toc

T_INDEX_FILE_TYPE = T.Literal["rst", "md", "nb"]


class IndexFileNotFoundError(FileNotFoundError):
    pass


@dataclasses.dataclass
class PageFolder:
    """
    Represents a folder containing an index document with a title.

    A PageFolder typically maps to a documentation section with an index file
    (index.rst, index.md, or index.ipynb) that contains a title. This class
    provides methods to extract the title, find child page folders, and
    generate a toctree directive linking to those children.

    The index file is searched in this order:

    1. .rst (reStructuredText)
    2. .ipynb (Jupyter Notebook)
    3. .md (Markdown)

    :param dir: Path to the directory containing the index file
    :param index_filename: Base name of the index file without extension (default: "index")

    Example folder structure::

        docs/sources/
        docs/sources/index.rst
        docs/sources/document-1/index.rst
        docs/sources/document-2/index.ipynb
        docs/sources/document-3/index.md
        docs/sources/document-3/...

    Usage:

    .. code-block:: python

        # Create a PageFolder for the main docs directory
        main_folder = PageFolder.new(dir=Path("docs/sources"))

        # Generate toctree directive
        toc_content = main_folder.toc_directive()

        # Result will be:
        # .. toctree::
        #     :maxdepth: 1
        #
        #     Document 1 <document-1/index>
        #     Document 2 <document-2/index>
        #     Document 3 <document-3/index>
    """

    dir: Path = dataclasses.field()
    index_filename: str = dataclasses.field()
    path_index_file: Path = dataclasses.field(init=False)
    index_file_type: T_INDEX_FILE_TYPE = dataclasses.field(init=False)

    @classmethod
    def new(
        cls,
        dir: Path,
        index_filename: str = "index",
    ):
        """
        Create a new PageFolder instance with resolved index file.

        This factory method creates a PageFolder instance and resolves
        which type of index file exists (.rst, .ipynb, or .md).

        TODO: 现在有一个问题是作为包含 ``.. autotoctree:`` 的父节点必须要是 RST, 你不能在 Notebook 里包含这个.
        TODO: 我们需要将父节点的 index_filename 和 discover 阶段的子目录的 index_file 区分开来, 以后会实现.
        """
        index_filename = index_filename.split(".")[0]
        child_page_folder = cls(dir=dir, index_filename=index_filename)
        if child_page_folder.path_index_rst.exists():
            child_page_folder.path_index_file = child_page_folder.path_index_rst
            child_page_folder.index_file_type = "rst"
        # We check notebook before markdown, because sometime people have
        # converted markdown (from notebook) at the same location.
        elif child_page_folder.path_index_ipynb.exists():
            child_page_folder.path_index_file = child_page_folder.path_index_ipynb
            child_page_folder.index_file_type = "nb"
        elif child_page_folder.path_index_md.exists():  # pragma: no cover
            child_page_folder.path_index_file = child_page_folder.path_index_md
            child_page_folder.index_file_type = "md"
        else:  # pragma: no cover
            raise IndexFileNotFoundError(
                f"Cannot find index file in {child_page_folder.dir}"
            )
        return child_page_folder

    @property
    def path_index_rst(self) -> Path:
        """
        Get the absolute path to the potential reStructuredText index file.
        """
        return self.dir.joinpath(f"{self.index_filename}.rst")

    @property
    def path_index_ipynb(self) -> Path:
        """
        Get the absolute path to the potential Jupyter Notebook index file.
        """
        return self.dir.joinpath(f"{self.index_filename}.ipynb")

    @property
    def path_index_md(self) -> Path:
        """
        Get the absolute path to the potential Markdown index file.
        """
        return self.dir.joinpath(f"{self.index_filename}.md")

    @property
    def path_str(self):
        """
        Get the relative path string used in toctree entries.
        """
        return f"{self.dir.name}/{self.index_filename}"

    def get_title_from_rst(self) -> T.Optional[str]:
        """
        Extract title from a reStructuredText file.

        Finds the first section title by looking for underline patterns
        (====, ----, etc.) and returns the text line above it.

        Also handles .. include:: directives by replacing them with
        the content of the included file.

        :return: Extracted title or None if no title found
        """

        # replace ``.. include::`` with the content of the included file
        lines = list()
        with self.path_index_file.open("r", encoding="utf-8") as f:
            for cursor_line in f.readlines():
                cursor_line = cursor_line.strip()
                if cursor_line.startswith(".. include::"):
                    relpath_parts = cursor_line.split("::")[-1].strip().split("/")
                    path_included = self.path_index_file.parent.joinpath(*relpath_parts)
                    if path_included.exists():
                        cursor_line = path_included.read_text(encoding="utf-8")
                lines.append(cursor_line)
        rst_content = "\n".join(lines)

        # Identify the title line
        header_bar_char_list = "=-~+*#^"

        # please add more comments here
        cursor_previous_line = None
        for cursor_line in rst_content.split("\n"):
            for header_bar_char in header_bar_char_list:
                if cursor_line.startswith(header_bar_char):
                    flag_full_bar_char = cursor_line == header_bar_char * len(
                        cursor_line
                    )
                    flag_line_length_greather_than_1 = len(cursor_line) >= 1
                    flag_previous_line_not_empty = bool(cursor_previous_line)
                    if (
                        flag_full_bar_char
                        and flag_line_length_greather_than_1
                        and flag_previous_line_not_empty
                    ):
                        return cursor_previous_line.strip()
            cursor_previous_line = cursor_line

        return None

    def get_title_from_md(self) -> T.Optional[str]:
        """
        Extract title from a Markdown file.

        :return: Extracted title or None if no title found
        :raises NotImplementedError: This method is not implemented yet
        """
        raise NotImplementedError

    def get_title_from_ipynb(self) -> T.Optional[str]:
        """
        Extract title from a Jupyter Notebook file.

        Looks for a title in:

        1. The first markdown cell with a level 1 heading (# Title)
        2. A raw reStructuredText cell with a title and underline

        :return: Extracted title or None if no title found
        """
        header_bar_char_list = "=-~+*#^"

        data = json.loads(self.path_index_ipynb.read_text(encoding="utf-8"))
        for row in data["cells"]:
            if len(row["source"]):
                cell_type: str = row.get("cell_type", "unknown")
                raw_mimetype: str = row.get("metadata", {}).get(
                    "raw_mimetype", "unknown"
                )
                rst_mimetype = [
                    "text/restructuredtext",
                    "text/x-rst",
                ]
                if cell_type == "markdown":
                    content = row["source"][0]
                    line = content.split("\n")[0]
                    if "# " in line:
                        return line[2:].strip()
                elif cell_type == "raw" and raw_mimetype in rst_mimetype:
                    try:
                        line = row["source"][3].strip()
                    except IndexError:  # pragma: no cover
                        continue
                    try:
                        title_line = row["source"][2].strip()
                    except IndexError:  # pragma: no cover
                        continue
                    for header_bar_char in header_bar_char_list:
                        if line.startswith(header_bar_char):
                            flag_full_bar_char = line == header_bar_char * len(line)
                            flag_line_length_greather_than_1 = len(line) >= 1
                            flag_previous_line_not_empty = bool(title_line)
                            if (
                                flag_full_bar_char
                                and flag_line_length_greather_than_1
                                and flag_previous_line_not_empty
                            ):
                                return title_line
                else:  # pragma: no cover
                    pass
        return None

    @cached_property
    def title(self) -> T.Optional[str]:
        """
        Title for the first header in the index file
        """
        if self.index_file_type == "rst":
            return self.get_title_from_rst()
        elif self.index_file_type == "nb":
            return self.get_title_from_ipynb()
        elif self.index_file_type == "md":
            return self.get_title_from_md()
        else:  # pragma: no cover
            print("never gonna reach here")

    @cached_property
    def child_page_folders(self) -> T.List["PageFolder"]:
        """
        Find all valid child page folders.

        Searches for directories containing index files with valid titles
        and returns them as :class:`PageFolder` instances.
        """
        child_page_folders = list()
        dir_list = [path for path in self.dir.iterdir() if path.is_dir()]
        dir_list.sort()

        for dir in dir_list:
            try:
                child_page_folder = self.__class__.new(
                    dir=dir, index_filename=self.index_filename
                )
            # skip folders that cannot find index file
            except IndexFileNotFoundError:
                continue

            try:
                if child_page_folder.title is not None:
                    child_page_folders.append(child_page_folder)
                else:  # pragma: no cover
                    print(
                        f"Warning: cannot detect title in "
                        f"{child_page_folder.path_index_file} file"
                    )
            # skip folders that is failed to extract title
            except:  # pragma: no cover
                pass
        return child_page_folders

    def toc_directive(self, maxdepth=1):
        """
        Generate a ``toctree`` directive for the child page folders.

        Creates a properly formatted reStructuredText ``toctree`` directive
        that includes all child pages with their titles.

        :param maxdepth: Maximum depth for the toctree directive

        :return: Complete toctree directive as a string
        """
        params = TocTemplateParams(
            page_folders=self.child_page_folders,
            maxdepth=maxdepth,
        )
        articles_directive_content = render_toc(params)
        return articles_directive_content
