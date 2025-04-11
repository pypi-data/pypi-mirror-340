.. toctree::
    :maxdepth: {{ params.maxdepth }}

    {% for page_folder in params.page_folders -%}
    {{ page_folder.title }} <{{ page_folder.path_str }}>
    {% endfor -%}
