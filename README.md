# Cookie Composer

<!-- start-badges -->

[![PyPI](https://img.shields.io/pypi/v/cookie-composer)][pypi_]
[![Status](https://img.shields.io/pypi/status/cookie-composer)][status]
[![Python Version](https://img.shields.io/pypi/pyversions/cookie-composer)][python version]
[![License](https://img.shields.io/pypi/l/cookie-composer)][license]
[![codecov](https://codecov.io/gh/callowayproject/cookie-composer/branch/master/graph/badge.svg?token=YO2JQLV1OB)](https://codecov.io/gh/callowayproject/cookie-composer)

[pypi_]: https://pypi.org/project/cookie-composer/
[status]: https://pypi.org/project/cookie-composer/
[python version]: https://pypi.org/project/cookie-composer
[license]: https://github.com/callowayproject/cookie-composer/blob/master/LICENSE

Documentation: https://callowayproject.github.io/cookie-composer/

<!-- end-badges -->

Cookie composer builds on the [cookie cutter](https://github.com/cookiecutter/cookiecutter) project to generate projects based on one or more cookiecutter templates.

## Goals

- Create new projects from a composition of several templates
- Add new capabilities to an existing repository by applying a template
- Apply template updates to the generated project

## Introduction

Cookie Cutter treats templates like sandwiches. There are templates for hamburgers, clubs, and any other kind of sandwich you can dream up. You might have options and defaults on a template, like `Hold the mustard?[False]:` or `Mustard type [dijon]:`, but those are decided by the template author. 


<img src="https://raw.githubusercontent.com/coordt/cookie-composer/master/docs/assets/img/sandwiches.png" alt="Templates are treated like finished sandwiches" style="zoom:50%;" />

If you look closely at the sandwiches (templates), there is usually many things in common. What if we treated the templates as compositions of other templates:

<img src="https://raw.githubusercontent.com/coordt/cookie-composer/master/docs/assets/img/compositions.png" alt="Sandwiches as a composition of layers" style="zoom:50%;" />

You now can manage several smaller and specialized templates that provide functionality. Each template's options will be specific to what that template needs.

<img src="https://raw.githubusercontent.com/coordt/cookie-composer/master/docs/assets/img/layers.png" alt="Templates broken out as layers on a sandwich" style="zoom:50%;" />

Cookie Composer uses a composition file to describe the layers required, and even override a template's default answers.

```yaml
template: bottom-bun
context:
  toasting_level: light
  buttered: False
---
template: burger
---
template: cheese
context:
  kind: swiss
---
template: bacon
context:
  cooking_level: crispy
---
template: ketchup
---
template: mustard
context:
  type: yellow
---
template: top-bun
context:
  toasting_level: light
  buttered: False
```

We have created [a repo of highly composable templates](https://github.com/coordt/cookiecomposer-templates) as examples or reference. However, Cookie Composer is designed to handle any Cookie Cutter template.

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
  - Documentation specific
    - Sphinx
    - MkDocs
- Each composable template is managed and updated individually
- A project can update itself based on chages in layers


## Please contribute

- Documentation critiques
- Documentation suggestions
- Feature suggestions
- Feature improvements
- Edge case identification
- Code improvements
