{{ params.package.shortname }}
{{ "=" * params.package.shortname|length }}

.. automodule:: {{ params.package.fullname }}
    :members:

sub packages and modules
------------------------

.. toctree::
    :maxdepth: 1

    {% for sub_package in params.sub_packages -%}
    {{ sub_package.shortname }} <{{ sub_package.shortname }}/__init__>
    {% endfor -%}
    {% for sub_module in params.sub_modules -%}
    {{ sub_module.shortname }} <{{ sub_module.shortname }}>
    {% endfor -%}