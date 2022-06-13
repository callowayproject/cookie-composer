# cookie-composer

## TODO

- requirements files and dependencies when layering?
  - Provide an "update requirements from file" command that reads the current set requirements and updates the config
  - Can things like that be put into a special context that each layer can add to
  - Can then render the files with the appropriate information (all composed)
- dealing with cookiecutter templates that try to initialize a git repo and make commits
- Figure out how to determine the correct commit to do a diff to (using something like updater)
  - Maybe track the parent (current) one per layer?

## Goals

- Create new projects from a composition of several templates
- Add new capabilities to an existing repository by applying a template
- Apply updates from the templates to generated repository


## Purpose

- Separate out parts to a repo into composable templates
  - Boilerplate
    - README, CONTRIBUTING, docs, Makefile, license, tooling configurations
  - Project-specific
    - Django
    - Flask
    - Library
    - Data science
  - CI/CD specific
    - Helm chart
    - GitHub Actions vs. Jenkins vs. ...
- Each composable template is managed and updated individually
- Each layer is update-able

- Now it is easy to manage shared information on template variations


## Use

### Create a base layer

```
cookie-composer https://github.com/coordt/cookiecutter-boilerplate.git
```

1. This takes all the arguments for `cookiecutter` and passes them along. 
2. Cookie cutter renders the template.
3. Cookie composer writes its config file into the rendered template.


### Add a layer

Now we need to add in a Fast API layer

```
cd <project-directory>
cookie-composer add https://github.com/coordt/cookiecutter-fastAPI.git
```

- This accepts the following cookie cutter flags:
  - `--no-input`
  - `-c/--checkout`
  - `--directory`
  - `-f/--overwrite-if-exists`
  - `-s/--skip-if-file-exists`
  - `--config-file`
  - `--default-config`
  - `--accept-hooks`


1. Cookie composer combines and de-duplicates the `cookiecutter.json` files
   - If the options are exactly the same, they are removed
   - If the new one is different from previous ones, it is kept.
2. This takes all the arguments for `cookiecutter` and passes them along. 
3. Cookie cutter renders the template.
4. Cookie composer updates its config file in the rendered template.


## Config file

.cookie-composer.[yml|yaml|json]
pyproject.toml -> [tool.cookie-composer]

This can be used to generate the project at the start, and is saved in the project to provide information regarding updates.

```yaml
templates:
- template: path/url
  checkout: # branch, tag or commit to checkout after git clone
  commit: hash # What git hash was (or should be) applied
  directory: # Directory within repo that holds cookiecutter.json file for advanced repositories with multi templates in it
  skip-hooks: false
  no-input: false
  skip-if-file-exists: true # 
  skip:  # paths or glob patterns to skip even attempting to use
    - tests/*
    - \{\{ cookiecutter.project_name \}\}/__init__.py
  overwrite:  # paths or glob patterns to overwrite
    - .pre-commit-config.yaml
  overwrite-exclude:  # paths or glob patterns to exclude from overwriting
    - "*.py"
  merge: # paths or glob patterns.
    "*.toml": nested-overwrite  # merge deeply nested structures and overwrite at the lowest level
    "*.yaml": overwrite  # Overwrite at the top level
    "*.json": merge-only  # Discard conflicting elements
  context:  # If not provided at creation, it is filled in with results from first run
      project_name: myproject
```


## References

- https://cookiecutter-hypermodern-python.readthedocs.io/en/2021.7.15/index.html
- https://cookiecutter.readthedocs.io/en/1.7.2/advanced/replay.html
- https://cookiecutter-project-upgrader.readthedocs.io/en/latest/readme.html
- https://github.com/cruft/cruft/
