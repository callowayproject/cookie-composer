# Changelog

## Unreleased (2022-05-31)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.1.0...HEAD)

### Fixes

- Fixed a bug when two templates have `_copy_without_render`. [9e89347](https://github.com/coordt/cookie-composer/commit/9e89347edd227332c50430c0bd8a26d2690fe182)
    
  `_copy_without_render` is template-specific and attempting to override it raises an error in cookiecutter. Now that key is deleted for the default context and full context when generating each layer.
- Fixed configurations. [df365df](https://github.com/coordt/cookie-composer/commit/df365dff8c522b6eb3fbc5efb4fef71162cd1f8b)
    
### New

- Added release tooling. [d0646d3](https://github.com/coordt/cookie-composer/commit/d0646d34e9af6159b08bca235687417cde18f1ee)
    
- Added code. [ccc4745](https://github.com/coordt/cookie-composer/commit/ccc47456bcb99407d60ce7f2b8ad9ac37572e126)
    
### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [63f2d7d](https://github.com/coordt/cookie-composer/commit/63f2d7d8c7e3a2f8a068dbc82411bd364fd5191e)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [8f6d661](https://github.com/coordt/cookie-composer/commit/8f6d66142a5c0950a9d8483133842944bd25f3b0)
    
  **updates:** - https://github.com/timothycrosley/isort → https://github.com/PyCQA/isort

- Migrated dependency management to pip-tools. [438c1a3](https://github.com/coordt/cookie-composer/commit/438c1a323d2663ef2823178782622d7d81dd342e)
    
- Vendored cookiecutter to use the latest version. [e6540e7](https://github.com/coordt/cookie-composer/commit/e6540e7239f58454d1412a06c23653566dbcc1cb)
    
### Updates

- Updated tests. [7c81df5](https://github.com/coordt/cookie-composer/commit/7c81df5b6978886c2939048808a3720c2bf3cb53)
    
## 0.1.0 (2022-02-28)

### Other

- Initial commit. [abdef79](https://github.com/coordt/cookie-composer/commit/abdef79ef9413faaa9602847f1f98317f58a74f3)
    
- Initial commit. [8965b8a](https://github.com/coordt/cookie-composer/commit/8965b8abb708212dbfe664a211989e6c5c81966a)
