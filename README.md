# useblocks-theme
This repository contains the theme for all Useblock documentation sites.

> **NOTE:** Useblocks uses the Sphinx-Immaterial theme so ensure that the theme is already installed and applied.

## Installation
To install the files from this repository, you must have [Git](https://git-scm.com) installed.

* Change directory to your preferred docs working directory
  ```bash
  cd docs
  ```
* Download the files from the repository:
  ```bash
  git clone https://github.com/useblocks/useblocks-theme.git 
  ```

## Configuration

You must configure the following in the **conf.py** file of the Sphinx documentation project.

* Add the `html_theme_options` to your **conf.py**:
    * Import the theme options for Useblocks.
      ```python
      from ub_theme.conf import html_theme_options
        ```
    * Set it as the value for the `html_theme_options` variable.
      ```python
      html_theme_options = html_theme_options
        ```
* Add the custom template changes folder to the `templates_path` variable.
  ```python
  templates_path = ['ub_theme/templates']
  ```
* Add custom CSS changes:
    * Add the folder containing the CSS files to the `html_static_path` variable.
      ```python
      html_static_path = ["ub_theme/css"]
        ```
    * Add the custom CSS files to the `html_css_files` variable.
      ```python
      html_css_files = ['ub-theme.css']
        ```
* Add custom JS changes:
    * Add the folder containing the JS files to the `html_static_path` variable.
      ```python
      html_static_path = ["ub_theme/js"]
        ```
    * Add the custom JS files to the `html_js_files` variable.
      ```python
      html_js_files = ['ub-theme.js']
        ```
  
The final configuration should look like below:
```python
from ub_theme.conf import html_theme_options

extensions = [
    "sphinx_immaterial",
]

templates_path = ['ub_theme/templates']

html_theme = "sphinx_immaterial"
html_theme_options = html_theme_options

# You can add other Sphinx-Immaterial theme options like below
other_options = {
    "repo_url": "https://github.com/useblocks/useblocks-theme",
    "repo_name": "useblocks-theme",
    "repo_type": "github",
}
html_theme_options.update(other_options)

html_static_path = ["ub_theme/css", "ub_theme/js"]
html_css_files = ['ub-theme.css']
html_js_files = ['ub-theme.js']

```

## Changelog

* 28.12.2022 - Setup and added the initial Useblocks theme codes 
