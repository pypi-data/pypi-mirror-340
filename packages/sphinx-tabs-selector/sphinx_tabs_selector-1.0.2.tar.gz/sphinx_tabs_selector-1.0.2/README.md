# sphinx_tabs_selector

This plugin is created based on the `sphinx_tabs` plugin and supports all formats supported by `sphinx_tabs`. 
In HTML displays, tabs can be switched by clicking. However, this switching functionality is not supported 
when generating certain specific formats, such as PDF. This plugin is designed to select the content of specified 
Sphinx tabs, facilitating Sphinx to generate non - HTML format content.

## Installation
```bash
pip install sphinx-tabs-selector
```

## Usage

Add the following configuration to `conf.py`:
```python
extensions = [
    ...
    'sphinx_tabs_selector.selector',
    ... 
]

# This is used to configure the tabs to be selected. If this item is not configured, the plugin will not work.
# The configuration item is a list. Each element in the list is a string, which is the name of the tab to be selected. 
# If the tab is nested, you need to write down all the names of the tabs in the nesting path.
tabs_selector = ["tab1_name","tab2_name","tab3_name"]
```

For the way of writing tabs in RST files, you can refer to the documentation of the `sphinx_tabs` plugin.

## Notes
1. You must add the `tabs_selector` configuration to `conf.py`; otherwise, the plugin will not take effect. 
   Therefore, you can use the `tabs_selector` configuration to control the activation of the plugin.
2. If both the `sphinx_tabs` plugin and the `sphinx_tabs_selector` plugin are added to the `extensions` in `conf.py`, 
   for the `sphinx_tabs_selector` plugin to work, it must be added after `sphinx_tabs`.
3. The `sphinx_tabs_selector` plugin can be used independently even if the `sphinx_tabs` plugin is not added to `conf.py`. 