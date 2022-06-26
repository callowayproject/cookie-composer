# Changelog

## 0.2.2 (2022-06-26)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.2.1...0.2.2)

### New

- Added badges to the readme. [9fdcad0](https://github.com/coordt/cookie-composer/commit/9fdcad099883c532f990acb2afbdd10118db4476)
    

## 0.2.1 (2022-06-26)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.2.0...0.2.1)

### Fixes

- Fixed minor issues with packaging tools. [d0f49d4](https://github.com/coordt/cookie-composer/commit/d0f49d42854410b86db38f019f4b2e287d260ccb)
    

## 0.2.0 (2022-06-26)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.1.0...0.2.0)

### Fixes

- Fixed add command requiring destination. [15cbd16](https://github.com/coordt/cookie-composer/commit/15cbd16b52659e198ea38d958adc071b14da2a35)
    
  The destination of the add command is now optional and defaults to the current working directory.
- Fixed error not writing commit to composition file. [8fd7bbe](https://github.com/coordt/cookie-composer/commit/8fd7bbe422dc60e7dab2dd48a26038d14f3db223)
    
- Fixed handling remote compositions and git clones. [ee142bd](https://github.com/coordt/cookie-composer/commit/ee142bd0cb0f06c568e76234615040898c75bde9)
    
- Fixed a bug when two templates have `_copy_without_render`. [9e89347](https://github.com/coordt/cookie-composer/commit/9e89347edd227332c50430c0bd8a26d2690fe182)
    
  `_copy_without_render` is template-specific and attempting to override it raises an error in cookiecutter. Now that key is deleted for the default context and full context when generating each layer.
- Fixed configurations. [df365df](https://github.com/coordt/cookie-composer/commit/df365dff8c522b6eb3fbc5efb4fef71162cd1f8b)
    
### New

- Added more github actions. [6bf5e54](https://github.com/coordt/cookie-composer/commit/6bf5e54abb108a7abcf320c9b95f4907ea2f9f6d)
    
- Added ability to use previous templatee contexts in rendering defaults. [fa6cb23](https://github.com/coordt/cookie-composer/commit/fa6cb2379a2889e2a6aa6cf05d1eb166164f464a)
    
- Added verbosity logging. [2081e30](https://github.com/coordt/cookie-composer/commit/2081e30346ea12d7b604ee16867ed15ae9212bd9)
    
- Added pip-compile to pre-commit config. [aae79f5](https://github.com/coordt/cookie-composer/commit/aae79f5494099c2cc45dcb17b984326868182752)
    
- Added the "add" command to add a layer to a rendered template. [86f17cd](https://github.com/coordt/cookie-composer/commit/86f17cdbe8e8ca19483eb180c1d6dd31e50619be)
    
- Added git commands. [291b9aa](https://github.com/coordt/cookie-composer/commit/291b9aa0cb0342a2db2a80ea5d3531dd9876be14)
    
  - gitpython added as a prod requirement
  - GitError raised when git command fails
  - added functions encompassing key functionality
- Added layer_name to RenderedLayer. [7f02db3](https://github.com/coordt/cookie-composer/commit/7f02db39e8a2da85e75d9d77b6f7d6aa54182c29)
    
  This allows for detection of multiple rendered directories, and proper writing of the composition file.
- Added release tooling. [d0646d3](https://github.com/coordt/cookie-composer/commit/d0646d34e9af6159b08bca235687417cde18f1ee)
    
- Added code. [ccc4745](https://github.com/coordt/cookie-composer/commit/ccc47456bcb99407d60ce7f2b8ad9ac37572e126)
    
### Other

- Create python-publish.yml. [62830a3](https://github.com/coordt/cookie-composer/commit/62830a35452b01648ca84c39d5fab221d6e3849d)
    
- [pre-commit.ci] auto fixes from pre-commit.com hooks. [2dae846](https://github.com/coordt/cookie-composer/commit/2dae84695df5c406fb7205789e66ab2e68ec787b)
    
  for more information, see https://pre-commit.ci
- Excluding test fixtures from requirement fixing. [40293a9](https://github.com/coordt/cookie-composer/commit/40293a99a734676cb006e1373246e6c7ca04be35)
    
- [pre-commit.ci] auto fixes from pre-commit.com hooks. [b774ad1](https://github.com/coordt/cookie-composer/commit/b774ad1eabf5bcd0fd891ad01ecd7ec54ab9887e)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [5098fde](https://github.com/coordt/cookie-composer/commit/5098fde4050ccc3df3965c90762fb30f36b38733)
    
  **updates:** - [github.com/pre-commit/pre-commit-hooks: v4.2.0 → v4.3.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.2.0...v4.3.0)

- Switched from typer to click. [d66f3f0](https://github.com/coordt/cookie-composer/commit/d66f3f0dda66256bbde70bdb531d768aa34371e3)
    
- [pre-commit.ci] auto fixes from pre-commit.com hooks. [63f2d7d](https://github.com/coordt/cookie-composer/commit/63f2d7d8c7e3a2f8a068dbc82411bd364fd5191e)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [8f6d661](https://github.com/coordt/cookie-composer/commit/8f6d66142a5c0950a9d8483133842944bd25f3b0)
    
  **updates:** - https://github.com/timothycrosley/isort → https://github.com/PyCQA/isort

- Migrated dependency management to pip-tools. [438c1a3](https://github.com/coordt/cookie-composer/commit/438c1a323d2663ef2823178782622d7d81dd342e)
    
- Vendored cookiecutter to use the latest version. [e6540e7](https://github.com/coordt/cookie-composer/commit/e6540e7239f58454d1412a06c23653566dbcc1cb)
    
### Updates

- Updated the readme. [e997618](https://github.com/coordt/cookie-composer/commit/e997618c4e6a27b2704de7a65117d93ec3a8e686)
    
- Updated the documentation. [8b59661](https://github.com/coordt/cookie-composer/commit/8b596616f008c048b0b6012c0d5c11ff4b51b816)
    
- Updated pre-commit to allow multiple documents in YAML files. [3a3e578](https://github.com/coordt/cookie-composer/commit/3a3e5780ced76675f6942b371d6767c8f1964cf1)
    
- Removed vendored cookiecutter and switched to released version. [f5cd36a](https://github.com/coordt/cookie-composer/commit/f5cd36a74657db6c8003e92088bf7a5f322ba3ce)
    
- Updated the error text when missing a git repo. [78507e9](https://github.com/coordt/cookie-composer/commit/78507e96692cf9d8c9bdbd7e4dc3df0c91c25d81)
    
- Updated formatting for composition output. [9df7856](https://github.com/coordt/cookie-composer/commit/9df78568a6b603382a08c2b12091e31eeade8bd3)
    
- Updated the documentation to a new theme. [5f68737](https://github.com/coordt/cookie-composer/commit/5f68737655256c1e6c3ede7721774a31f5a75b07)
    
- Renamed _commands to commands. [da6d4f5](https://github.com/coordt/cookie-composer/commit/da6d4f5143acc0cc7b9ffacfe4daa21b3e7aea61)
    
- Changed MergeStrategy from an Enum to constants. [ef8b828](https://github.com/coordt/cookie-composer/commit/ef8b82804566a613ac1631efa52752441ff56700)
    
- Changed dependency management. [4cf52ba](https://github.com/coordt/cookie-composer/commit/4cf52ba2d90c2aaff2d0c9d2e52f7390587090ff)
    
  Uses pip-tools to compile and maintain dependency information.
- Updated tests. [7c81df5](https://github.com/coordt/cookie-composer/commit/7c81df5b6978886c2939048808a3720c2bf3cb53)
    

## 0.1.0 (2022-02-28)

### Other

- Initial commit. [abdef79](https://github.com/coordt/cookie-composer/commit/abdef79ef9413faaa9602847f1f98317f58a74f3)
    
- Initial commit. [8965b8a](https://github.com/coordt/cookie-composer/commit/8965b8abb708212dbfe664a211989e6c5c81966a)
