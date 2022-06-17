# Composition files

Composition files are YAML documents with layer configurations. They are used for generating new projects and recording how a current project was generated. The composition files used for generating new projects are usually minimal, compared to the `.composition.yaml` file `cookie-composer` writes in the project as a record of state.

For example, a basic composition file for generating new projects might look like:

```yaml
template: "/Users/oordcor/Documents/code/cookiecutter-templates/cookiecutter-boilerplate"
directory: ""
merge_strategies:
  '*.json': "comprehensive"
  '*.yaml': "comprehensive"
  '*.yml': "comprehensive"
---
template: "/Users/oordcor/Documents/code/cookiecutter-templates/cookiecutter-package"
directory: ""
merge_strategies:
  '*.json': "comprehensive"
  '*.yaml': "comprehensive"
  '*.yml': "comprehensive"
---
template: "/Users/oordcor/Documents/code/cookiecutter-templates/cookiecutter-docs"
directory: ""
merge_strategies:
  '*.json': "comprehensive"
  '*.yaml': "comprehensive"
  '*.yml': "comprehensive"
```
