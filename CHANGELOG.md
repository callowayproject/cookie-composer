# Changelog

## 0.13.0 (2024-02-10)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.11.0...HEAD)

### Fixes

- Fixed linting. [94a4b7a](https://github.com/coordt/cookie-composer/commit/94a4b7aa5a5d22d17b8f82fbfbabc0155b0d7516)
    
- Fixed doc generation. [ce88c23](https://github.com/coordt/cookie-composer/commit/ce88c23229d1850e7a81b114832616d3f4deb548)
    
- Fixed local git repo resolution. [115ed5f](https://github.com/coordt/cookie-composer/commit/115ed5f51594349182d4ebe50b88f1cd3d8b5d47)
    
- Fixed dev versioning config. [6299c11](https://github.com/coordt/cookie-composer/commit/6299c1153626e793ae581306a07f4a9a329ab319)
    
- Fixed git worktree issue. [e27636c](https://github.com/coordt/cookie-composer/commit/e27636c5e2bd6c75ded8fe077a5095133a019205)
    
  - uses the correct git command depending on the parameters passed.
- Fixed missing commit sha in test. [c9997be](https://github.com/coordt/cookie-composer/commit/c9997beaa26858e32e3abbae8627941208731c3a)
    
- Fixed error handling with patching. [f35864d](https://github.com/coordt/cookie-composer/commit/f35864d8d02189eafe545a16e8857e6c2d052fc1)
    
- Fixed Exception handling for click. [c481ad7](https://github.com/coordt/cookie-composer/commit/c481ad7afc642ef402add996ba7fe54fb6400281)
    
- Fixed _copy_without_render bug. [4edc4bf](https://github.com/coordt/cookie-composer/commit/4edc4bf1306a3931b44ddfebe191a50eca3ada20)
    
- Fixed test type annotation. [4a4a7c0](https://github.com/coordt/cookie-composer/commit/4a4a7c06d9a73680d4aece212c9b0bb7fbafb07e)
    
- Fixed rendering layers from previous commits. [0fefdbc](https://github.com/coordt/cookie-composer/commit/0fefdbc578ec5545447a81f6925a7419276a8811)
    
- Fixed issue with generate_prompt_context. [4756660](https://github.com/coordt/cookie-composer/commit/475666052f1ba555c054e779537ef93c0742a3d7)
    
- Fixed issue with determining rendered layer names. [06bad39](https://github.com/coordt/cookie-composer/commit/06bad3913a4a899f37acdcd2342bd2053c1419e6)
    
  Added `get_template_rendered_name` to proactively determine the name of the rendered template.
- Fixed resiliency issue with git template repos. [a9bb80d](https://github.com/coordt/cookie-composer/commit/a9bb80df0657008bb5bda157cda7aa96ff0004a1)
    
  Provided better error checking for bad cached repos.
- Fixed issue with relative paths in local files. [7f1b354](https://github.com/coordt/cookie-composer/commit/7f1b354d416515ef44126853827174914a5c54cb)
    
  You can pass a local_path to use to resolve relative local paths for I/O and template determination.
- Fixed data merge organization. [4bba0f4](https://github.com/coordt/cookie-composer/commit/4bba0f4de123d11624fc96ec5f49f8341d958108)
    
  - Moved data merge constants and functions from composition.py to data_merge.py
### New

- Added new workflow for versioning. [2232682](https://github.com/coordt/cookie-composer/commit/2232682391e491b8511e532ef270bb2a24d56a8f)
    
- Added context managers for temporary copies. [90fa24c](https://github.com/coordt/cookie-composer/commit/90fa24cb6e5d4b03e74cca3c1df9891780e2cdcf)
    
- Added convenience functions to the template classes. [0b62c44](https://github.com/coordt/cookie-composer/commit/0b62c440ec481356f283bc62fbaca27c0ec1cdf6)
    
- Added interface to get template repositories. [cf9ff4a](https://github.com/coordt/cookie-composer/commit/cf9ff4a412d19eeba47919deb0387b57380ccb4a)
    
- Added git template repositories. [02bf112](https://github.com/coordt/cookie-composer/commit/02bf112dcd1d951b3ac5c0d38a6295ce5aa72848)
    
- Added zipfile template repositories. [8190cb6](https://github.com/coordt/cookie-composer/commit/8190cb64f808c9ad2229c8c503b3e0125501b7f6)
    
- Added git shortcuts for cloning. [6ad76a3](https://github.com/coordt/cookie-composer/commit/6ad76a3c32a90cfbaeee72b7ab5688c7b0377ed0)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [86a2c04](https://github.com/coordt/cookie-composer/commit/86a2c045f5e2d445868a8bb3db62b06e4adc9eb9)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.1.3 → v0.2.0](https://github.com/astral-sh/ruff-pre-commit/compare/v0.1.3...v0.2.0)

- Bump gitpython from 3.1.40 to 3.1.41 in /requirements. [119c786](https://github.com/coordt/cookie-composer/commit/119c7868f2427a06f212f8a395869e001c078619)
    
  Bumps [gitpython](https://github.com/gitpython-developers/GitPython) from 3.1.40 to 3.1.41.
  - [Release notes](https://github.com/gitpython-developers/GitPython/releases)
  - [Changelog](https://github.com/gitpython-developers/GitPython/blob/main/CHANGES)
  - [Commits](https://github.com/gitpython-developers/GitPython/compare/3.1.40...3.1.41)

  ---
  **updated-dependencies:** - dependency-name: gitpython
dependency-type: direct:production

  **signed-off-by:** dependabot[bot] <support@github.com>

- Bump jinja2 from 3.1.2 to 3.1.3 in /requirements. [100a239](https://github.com/coordt/cookie-composer/commit/100a239c5bfeae3df7f8f53e6d0051d98100a87c)
    
  Bumps [jinja2](https://github.com/pallets/jinja) from 3.1.2 to 3.1.3.
  - [Release notes](https://github.com/pallets/jinja/releases)
  - [Changelog](https://github.com/pallets/jinja/blob/main/CHANGES.rst)
  - [Commits](https://github.com/pallets/jinja/compare/3.1.2...3.1.3)

  ---
  **updated-dependencies:** - dependency-name: jinja2
dependency-type: direct:production

  **signed-off-by:** dependabot[bot] <support@github.com>

- Bump aiohttp from 3.8.6 to 3.9.2 in /requirements. [4b2a9df](https://github.com/coordt/cookie-composer/commit/4b2a9dfc6be29e429e359b8de0fc61983abdc270)
    
  Bumps [aiohttp](https://github.com/aio-libs/aiohttp) from 3.8.6 to 3.9.2.
  - [Release notes](https://github.com/aio-libs/aiohttp/releases)
  - [Changelog](https://github.com/aio-libs/aiohttp/blob/master/CHANGES.rst)
  - [Commits](https://github.com/aio-libs/aiohttp/compare/v3.8.6...v3.9.2)

  ---
  **updated-dependencies:** - dependency-name: aiohttp
dependency-type: direct:production

  **signed-off-by:** dependabot[bot] <support@github.com>

- Moved `get_context_for_layer` from utils.py to composition.py. [6641a91](https://github.com/coordt/cookie-composer/commit/6641a9102ac0fce22df4b30fee3dd141a3fb6c9b)
    
- Moved `get_template_name` tests. [1c0c054](https://github.com/coordt/cookie-composer/commit/1c0c05454f97068414a7e1155de126ad65aa1878)
    
- [pre-commit.ci] pre-commit autoupdate. [db151ef](https://github.com/coordt/cookie-composer/commit/db151ef49453ade797eb1437de9ff98e6b186b08)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.287 → v0.0.290](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.287...v0.0.290)

- [pre-commit.ci] pre-commit autoupdate. [7335d97](https://github.com/coordt/cookie-composer/commit/7335d9722973db509fa2636999c724d361a488b7)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.287 → v0.0.292](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.287...v0.0.292)

- Bump urllib3 from 2.0.4 to 2.0.7 in /requirements. [6f5dd07](https://github.com/coordt/cookie-composer/commit/6f5dd07ae6576ce65c1c0e4a27f527491d74d71a)
    
  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.4 to 2.0.7.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.0.4...2.0.7)

  ---
  **updated-dependencies:** - dependency-name: urllib3
dependency-type: direct:production

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [94b1833](https://github.com/coordt/cookie-composer/commit/94b18336a59d7495ed2dd9055e9d8013e72eb927)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.287 → v0.1.3](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.287...v0.1.3)

- [pre-commit.ci] pre-commit autoupdate. [bc33fbd](https://github.com/coordt/cookie-composer/commit/bc33fbd383107379b00c7a9932f83a62442b872f)
    
  **updates:** - https://github.com/charliermarsh/ruff-pre-commit → https://github.com/astral-sh/ruff-pre-commit

### Updates

- Updated requirement lock files. [026cd2d](https://github.com/coordt/cookie-composer/commit/026cd2dcbd045b2e88031abda0a9b75190ad300d)
    
- Updated pre-commit config. [57d6cff](https://github.com/coordt/cookie-composer/commit/57d6cff1f362ff1ba04ce34b2128913eff9bf92f)
    
- Updated requirements. [8d83ba0](https://github.com/coordt/cookie-composer/commit/8d83ba0be0edd4013cdb7e42064156310589eb41)
    
- Updated tests. [5d3c51f](https://github.com/coordt/cookie-composer/commit/5d3c51f18d1d3833563a6d5062960994130f30d8)
    
- Renamed `zipfile_repo.unzip` to `cache_source`. [60a2393](https://github.com/coordt/cookie-composer/commit/60a23939fa462a599a3a0eaee52ff0b2337fb6d6)
    
- Updated commands to use refactored methods. [14d2781](https://github.com/coordt/cookie-composer/commit/14d27811f04062ad0f720fa536102ba3874d78d5)
    
- Refactored (de)serialization and I/O methods into `io` module. [3c64a3e](https://github.com/coordt/cookie-composer/commit/3c64a3e2aae7efc54cf87caf16d96bfe06900b65)
    
- Refactored `layers`. [e8af7d5](https://github.com/coordt/cookie-composer/commit/e8af7d5279f7c6be9af163f2d8ac008b6e34cc5f)
    
  - Integrated `Template` with `LayerConfig`
      - `template` attribute is now a `Template` instance
      - removed `directory`, `checkout`, `password`, and `commit`
      - renamed `context` to `initial_context` to distiguish it from the `Template`'s context
  - Updated `RenderedLayer` to use templates
      - renamed `new_context` to `rendered_context` to better describe it.
      - renamed `latest_commit` to `rendered_commit` for better clarity
      - added `latest_commit` convenience function
  - Simplified `render_layer` using the new template functions
- Removed get_latest_template_commit from git_commands. [af84ff4](https://github.com/coordt/cookie-composer/commit/af84ff404a62cf1c36329f9211c4370795230792)
    
  It is now part of the template repo
- Updated requirements to use Pydantic 2. [b24a158](https://github.com/coordt/cookie-composer/commit/b24a15818aec12f622b60caa456d8e67d7445078)
    
- Refactored layer context to fix #39. [300578f](https://github.com/coordt/cookie-composer/commit/300578f067df5582bc8041f1eaf2fec3bc3761f6)
    
## 0.11.0 (2023-07-27)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.10.3...0.11.0)

### Fixes

- Fix test coverage matrix. [5ef8815](https://github.com/coordt/cookie-composer/commit/5ef8815aac62f874b5d130e82d7b8ba4320ec49b)
    
- Fix pre-commit from autofixing templates. [99e7dfb](https://github.com/coordt/cookie-composer/commit/99e7dfb6d71ece01d1c74d6d61b9cc135b124b31)
    
- Fixed typing hints. [ff695e3](https://github.com/coordt/cookie-composer/commit/ff695e38e864cf052bb15dc3a4278e782ce7a784)
    
### New

- Added support for local extensions. [838f25c](https://github.com/coordt/cookie-composer/commit/838f25c67c91b39be137b93bd64191bd78ae8d08)
    
- Added `-o` and `--output-dir` as an alias. [04f063d](https://github.com/coordt/cookie-composer/commit/04f063d702279731e54a578fd5c82f7f59426798)
    
  It is now an alias for `-d` and `--destination`
### Other

- Revert "[pre-commit.ci] auto fixes from pre-commit.com hooks". [42d8704](https://github.com/coordt/cookie-composer/commit/42d8704565d1927647e1692b29bd3e62e149a37a)
    
  This reverts commit 52772f1352d6130b2d6189bf632b26fb9732c13f.
- [pre-commit.ci] auto fixes from pre-commit.com hooks. [52772f1](https://github.com/coordt/cookie-composer/commit/52772f1352d6130b2d6189bf632b26fb9732c13f)
    
  for more information, see https://pre-commit.ci
- Migrated from setup.cfg to pyproject.toml. [b3a39f0](https://github.com/coordt/cookie-composer/commit/b3a39f0845a0dcd66177b3fbfaf5cac0369c18e1)
    
- Bump aiohttp from 3.8.3 to 3.8.5 in /requirements. [0392ef7](https://github.com/coordt/cookie-composer/commit/0392ef74feda8f0e2080967fa4ced8a62b1b9166)
    
  Bumps [aiohttp](https://github.com/aio-libs/aiohttp) from 3.8.3 to 3.8.5.
  - [Release notes](https://github.com/aio-libs/aiohttp/releases)
  - [Changelog](https://github.com/aio-libs/aiohttp/blob/v3.8.5/CHANGES.rst)
  - [Commits](https://github.com/aio-libs/aiohttp/compare/v3.8.3...v3.8.5)

  ---
  **updated-dependencies:** - dependency-name: aiohttp
dependency-type: direct:production

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [83d1217](https://github.com/coordt/cookie-composer/commit/83d121798ff502a6aa95caff731b5f39d698485b)
    
  **updates:** - [github.com/psf/black: 23.3.0 → 23.7.0](https://github.com/psf/black/compare/23.3.0...23.7.0)

- [pre-commit.ci] pre-commit autoupdate. [c58fe42](https://github.com/coordt/cookie-composer/commit/c58fe42786a5c73e82a57ae8aab7f9fef5e94c14)
    
  **updates:** - [github.com/psf/black: 23.3.0 → 23.7.0](https://github.com/psf/black/compare/23.3.0...23.7.0)

## 0.10.3 (2023-05-15)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.10.2...0.10.3)

### New

- Added support for accepting hooks. [096dfcc](https://github.com/coordt/cookie-composer/commit/096dfcc79ce19a732b93c4f6d00b5e733dc0a597)
    
## 0.10.2 (2023-05-11)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.10.1...0.10.2)

### Fixes

- Fixed a bug that reformatted files that should be overwritten. [3f0f7b5](https://github.com/coordt/cookie-composer/commit/3f0f7b5f54ec227ade3b49b411e4324c889a0b7e)
    
## 0.10.1 (2023-05-10)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.10.0...0.10.1)

### Fixes

- Fixed a bug where additional context wasn't passed to the composition. [bd8b571](https://github.com/coordt/cookie-composer/commit/bd8b57140ec29a7b6ec6542086660c012c43b428)
    
### Other

- Bump markdown-it-py from 2.1.0 to 2.2.0 in /requirements. [65a4863](https://github.com/coordt/cookie-composer/commit/65a4863b1baab6c2f6062806874c2e8946b857ff)
    
  Bumps [markdown-it-py](https://github.com/executablebooks/markdown-it-py) from 2.1.0 to 2.2.0.
  - [Release notes](https://github.com/executablebooks/markdown-it-py/releases)
  - [Changelog](https://github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/executablebooks/markdown-it-py/compare/v2.1.0...v2.2.0)

  ---
  **updated-dependencies:** - dependency-name: markdown-it-py
dependency-type: indirect

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [21eca93](https://github.com/coordt/cookie-composer/commit/21eca9331691b355b322119fca002384eb827fb4)
    
  **updates:** - [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)

## 0.10.0 (2023-03-24)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.9.2...0.10.0)

### New

- Added relative directory support for compositions. [02fa5b8](https://github.com/coordt/cookie-composer/commit/02fa5b8b591c25fef7bbd6c2aec20532f16541b5)
    
  - Template paths or URLs are resolved using the path to the composition file.
  - Using an absolute path or URL as a template works as before
  - `.`, `..`, and relative paths (non-`/` prefixed) are resolved with `urllib.parse.urljoin`
## 0.9.2 (2023-02-13)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.9.1...0.9.2)

### New

- Added test for validate_context_params. [a52d28d](https://github.com/coordt/cookie-composer/commit/a52d28d97445c426f02cb8399883ad8a9052928c)
    
- Added ability to pass initial contexts. [9e3cdf3](https://github.com/coordt/cookie-composer/commit/9e3cdf34480f9bfafd5f4750d48b78cc6ac294e1)
    
### Updates

- Modified CLI options and arguments. [02a4bf3](https://github.com/coordt/cookie-composer/commit/02a4bf3a9378f2788be53cfa769bbc5a9bb3eae3)
    
  - The `output_dir` argument was moved to the `--destination` option.
  - Added `CONTEXT_PARAMS` argument for initial context
- Removed checkout from first commit when linking. [f2725ef](https://github.com/coordt/cookie-composer/commit/f2725ef3464f932914e3393e5883792a8f93d0ca)
    
  - The first commit was causing confusing issues and now a normal checkout is performed.
## 0.9.1 (2023-02-08)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.9.0...0.9.1)

### New

- Added `--version` option. [4b1b9e1](https://github.com/coordt/cookie-composer/commit/4b1b9e1fd84f976f590dcc1ad803dea4808fe643)
    
## 0.9.0 (2023-01-25)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.8.1...0.9.0)

### Fixes

- Fixed license and documentation badges. [37289c9](https://github.com/coordt/cookie-composer/commit/37289c96e4bebcd25b2df0f90a797f2753494d07)
    
- Fixed the coveralls badge in README. [a4eaf73](https://github.com/coordt/cookie-composer/commit/a4eaf7313e534e71942335a8cce18b8348658159)
    
### New

- Added testing for authentication.py. [73c8335](https://github.com/coordt/cookie-composer/commit/73c83351529a834c219ffb4e8aa22fad84108802)
    
- Added authentication capability. [19b5a8d](https://github.com/coordt/cookie-composer/commit/19b5a8d60e1c12f361ff0d08d9809b310dede40d)
    
### Other

- Switched to Codecov. [c2fb125](https://github.com/coordt/cookie-composer/commit/c2fb125712b24c98ac450f206fb31048cb06dc5f)
    
- [pre-commit.ci] pre-commit autoupdate. [1f5320a](https://github.com/coordt/cookie-composer/commit/1f5320a8f9d45c0c9bc68290d43dec76c5230ce3)
    
  **updates:** - [github.com/pycqa/pydocstyle: 6.1.1 → 6.2.3](https://github.com/pycqa/pydocstyle/compare/6.1.1...6.2.3)

### Updates

- Updated documentation. [1a1c1f6](https://github.com/coordt/cookie-composer/commit/1a1c1f6166328dd627fdf5a0de7d9c17da684740)
    
- Update README.md coveralls badge. [b105133](https://github.com/coordt/cookie-composer/commit/b105133dc5046b55d6b486eaa2715a671c1c661a)
    
- Update README.md. [a55a257](https://github.com/coordt/cookie-composer/commit/a55a2579edafd49541b50de994d9ddcd203dd8ea)
    
## 0.8.1 (2023-01-04)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.8.0...0.8.1)

### Fixes

- Fixed YAML merge formatting. [7259919](https://github.com/coordt/cookie-composer/commit/7259919a851e7d5d4d1d59e7eb38b51eca7ed91a)
    
### Other

- Bump wheel from 0.37.1 to 0.38.1 in /requirements. [cab9b8e](https://github.com/coordt/cookie-composer/commit/cab9b8e1ce86c4a3dd38182320a9e64d016f849e)
    
  Bumps [wheel](https://github.com/pypa/wheel) from 0.37.1 to 0.38.1.
  - [Release notes](https://github.com/pypa/wheel/releases)
  - [Changelog](https://github.com/pypa/wheel/blob/main/docs/news.rst)
  - [Commits](https://github.com/pypa/wheel/compare/0.37.1...0.38.1)

  ---
  **updated-dependencies:** - dependency-name: wheel
dependency-type: indirect

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [45e8596](https://github.com/coordt/cookie-composer/commit/45e859622a82cd023f7ca02bfcd9a8e79f249508)
    
  **updates:** - [github.com/PyCQA/isort: v5.11.3 → 5.11.4](https://github.com/PyCQA/isort/compare/v5.11.3...5.11.4)

- [pre-commit.ci] pre-commit autoupdate. [550e0cb](https://github.com/coordt/cookie-composer/commit/550e0cb1e788dd0c800e502862f236f8bf3e9bfe)
    
  **updates:** - [github.com/PyCQA/isort: 5.10.1 → v5.11.3](https://github.com/PyCQA/isort/compare/5.10.1...v5.11.3)

## 0.8.0 (2022-12-16)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.7.1...0.8.0)

### Fixes

- Fixed ability to merge a list of dicts in YAML. [f3698ef](https://github.com/coordt/cookie-composer/commit/f3698ef7588fbac64cc14a9699ee4c2a4fca7f4d)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [5b21a40](https://github.com/coordt/cookie-composer/commit/5b21a4070ae643adaa5be564de2e9a171abe6b3d)
    
  **updates:** - [github.com/psf/black: 22.10.0 → 22.12.0](https://github.com/psf/black/compare/22.10.0...22.12.0)

- [pre-commit.ci] pre-commit autoupdate. [0f5c7a5](https://github.com/coordt/cookie-composer/commit/0f5c7a5fcb16b5557cf6453ad02d119b3edf8852)
    
  **updates:** - [github.com/pre-commit/pre-commit-hooks: v4.3.0 → v4.4.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.3.0...v4.4.0)

### Updates

- Change frozendict to immutabledict. [8edf699](https://github.com/coordt/cookie-composer/commit/8edf69920e37032c27ceea1545c51e11e86892e8)
    
- Changed JSON library to orjson. [c857a2f](https://github.com/coordt/cookie-composer/commit/c857a2f694d131a44ce863a743d8bbceb5146095)
    
  - has better serialization capability and performance.
## 0.7.1 (2022-11-07)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.7.0...0.7.1)

### Fixes

- Fixed ability to merge a list of dicts. [21b9033](https://github.com/coordt/cookie-composer/commit/21b9033d922ac83b31ebc1c1f65d6fec7d4582aa)
    
- Fixed chrobinson email to me. [7f2bf8e](https://github.com/coordt/cookie-composer/commit/7f2bf8e5d84c0777f19d321b216ca437050e1559)
    
## 0.7.0 (2022-10-31)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.6.0...0.7.0)

### New

- Added ability to merge .toml files. [2e36b40](https://github.com/coordt/cookie-composer/commit/2e36b407feadd58f6aac418504ea6e9274175afe)
    
- Added ability to merge .ini and .cfg files. [31ff1e0](https://github.com/coordt/cookie-composer/commit/31ff1e033f10bef3067b4811aaa61607fa6c5b14)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [a31eeef](https://github.com/coordt/cookie-composer/commit/a31eeef0dff2d826d68d6138667b5ab971eefa7a)
    
  **updates:** - [github.com/psf/black: 22.8.0 → 22.10.0](https://github.com/psf/black/compare/22.8.0...22.10.0)

## 0.6.0 (2022-10-09)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.5.0...0.6.0)

### Fixes

- Fixed a typo in the docs. [986f0d8](https://github.com/coordt/cookie-composer/commit/986f0d8c229689c77f6a9814b20386c0280124bc)
    
- Fixed dependency conflict between flake8 and virtualenv. [6925b05](https://github.com/coordt/cookie-composer/commit/6925b059c2be253b15375319c3f6fc51518995c9)
    
### New

- Added the link command to apply a composition to an existing project. [03f723e](https://github.com/coordt/cookie-composer/commit/03f723e20d9063f233513526ac46047f9efeb37c)
    
### Updates

- Updated the update command to use `git diff` and `git apply`. [d4bc14f](https://github.com/coordt/cookie-composer/commit/d4bc14f2765ad4cf9ee0bd10077a61d1b4f40353)
    
- Updated the project requirements. [0834e0b](https://github.com/coordt/cookie-composer/commit/0834e0bcb89f6dcc45a10afe298b5b2b197f8807)
    
- Refactored getting a composition from an input. [2f8edfe](https://github.com/coordt/cookie-composer/commit/2f8edfecdf17f2b1440a096e4d2fd853a75d1d2f)
    
## 0.5.0 (2022-09-22)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.4.0...0.5.0)

### New

- Added the update subcommand. [6696589](https://github.com/coordt/cookie-composer/commit/66965899d5c7c5d701c70d97e77f304904531bcf)
    
  - Made the existing implementation idempotent
  - Connected the update_cmd to the command line
- Add very basic cli tests. [c6482d4](https://github.com/coordt/cookie-composer/commit/c6482d46c11e70b354851a9c431634d0d4a6c51f)
    
### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [e5425d5](https://github.com/coordt/cookie-composer/commit/e5425d5bebb847be59b48ad5c9ac3cfb11fa5a92)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [dbfde0a](https://github.com/coordt/cookie-composer/commit/dbfde0ae58ca2d7fb0f537388091a74607a8fcdc)
    
  **updates:** - [github.com/psf/black: 22.6.0 → 22.8.0](https://github.com/psf/black/compare/22.6.0...22.8.0)

### Updates

- Update cli.py. [5a50f14](https://github.com/coordt/cookie-composer/commit/5a50f14c0affbfee66a795d9df5bfe6ecb905e7c)
    
## 0.4.0 (2022-09-06)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.3.0...0.4.0)

### New

- Added subset of cookiecutter options to CLI. [a66f17a](https://github.com/coordt/cookie-composer/commit/a66f17a0471f7178742f9d8d80010bb8d6628cac)
    
- Added documentation images. [86113dc](https://github.com/coordt/cookie-composer/commit/86113dcb19588ede45cfedcebda7f6e840c3b652)
    
- Added template layer updating. [20c6fe3](https://github.com/coordt/cookie-composer/commit/20c6fe326955deb3514420abb12d2bfaef7353a7)
    
- Added layer naming convention. [5e61312](https://github.com/coordt/cookie-composer/commit/5e613121130a640ff6721fec322a9a948cfa7a1e)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [e516a18](https://github.com/coordt/cookie-composer/commit/e516a181e4a3ebe3d3c93800ef8a059125494d82)
    
  **updates:** - [github.com/PyCQA/flake8: 4.0.1 → 5.0.4](https://github.com/PyCQA/flake8/compare/4.0.1...5.0.4)

- [pre-commit.ci] pre-commit autoupdate. [3e6f695](https://github.com/coordt/cookie-composer/commit/3e6f695a3126c52beec1a1bcd3f39e4df09cc2ee)
    
  **updates:** - [github.com/psf/black: 22.3.0 → 22.6.0](https://github.com/psf/black/compare/22.3.0...22.6.0)

### Updates

- Updated documentation configuration. [a4c9652](https://github.com/coordt/cookie-composer/commit/a4c9652625f8e42df722f046f13a2f4e74f7c4bf)
    
- Updated README.md. [a7ead0d](https://github.com/coordt/cookie-composer/commit/a7ead0d745aae637948661e3bb6ac7a978b0d4a3)
    
## 0.3.0 (2022-06-29)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.2.2...0.3.0)

### Fixes

- Fixed metadata's long description content type. [99470e9](https://github.com/coordt/cookie-composer/commit/99470e936dc440012d8542cd590853836a6454b6)
    
### Other

- Created tests for the add command. [358e189](https://github.com/coordt/cookie-composer/commit/358e189020fead21646397e56399e920e85a7ac2)
    
### Updates

- Updated cc_override's tests. [5388df7](https://github.com/coordt/cookie-composer/commit/5388df7cb4abe6f460a6f4ddd71f24cb9b02012f)
    
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
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.12.0...0.1.0)

### Other

- Initial commit. [abdef79](https://github.com/coordt/cookie-composer/commit/abdef79ef9413faaa9602847f1f98317f58a74f3)
    
- Initial commit. [8965b8a](https://github.com/coordt/cookie-composer/commit/8965b8abb708212dbfe664a211989e6c5c81966a)
    

## 0.12.0 (2023-11-04)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.11.0...0.12.0)

### Fixes

- Fixed git worktree issue. [e27636c](https://github.com/coordt/cookie-composer/commit/e27636c5e2bd6c75ded8fe077a5095133a019205)
    
  - uses the correct git command depending on the parameters passed.
- Fixed missing commit sha in test. [c9997be](https://github.com/coordt/cookie-composer/commit/c9997beaa26858e32e3abbae8627941208731c3a)
    
- Fixed error handling with patching. [f35864d](https://github.com/coordt/cookie-composer/commit/f35864d8d02189eafe545a16e8857e6c2d052fc1)
    
- Fixed Exception handling for click. [c481ad7](https://github.com/coordt/cookie-composer/commit/c481ad7afc642ef402add996ba7fe54fb6400281)
    
- Fixed _copy_without_render bug. [4edc4bf](https://github.com/coordt/cookie-composer/commit/4edc4bf1306a3931b44ddfebe191a50eca3ada20)
    
- Fixed test type annotation. [4a4a7c0](https://github.com/coordt/cookie-composer/commit/4a4a7c06d9a73680d4aece212c9b0bb7fbafb07e)
    
- Fixed rendering layers from previous commits. [0fefdbc](https://github.com/coordt/cookie-composer/commit/0fefdbc578ec5545447a81f6925a7419276a8811)
    
- Fixed issue with generate_prompt_context. [4756660](https://github.com/coordt/cookie-composer/commit/475666052f1ba555c054e779537ef93c0742a3d7)
    
- Fixed issue with determining rendered layer names. [06bad39](https://github.com/coordt/cookie-composer/commit/06bad3913a4a899f37acdcd2342bd2053c1419e6)
    
  Added `get_template_rendered_name` to proactively determine the name of the rendered template.
- Fixed resiliency issue with git template repos. [a9bb80d](https://github.com/coordt/cookie-composer/commit/a9bb80df0657008bb5bda157cda7aa96ff0004a1)
    
  Provided better error checking for bad cached repos.
- Fixed issue with relative paths in local files. [7f1b354](https://github.com/coordt/cookie-composer/commit/7f1b354d416515ef44126853827174914a5c54cb)
    
  You can pass a local_path to use to resolve relative local paths for I/O and template determination.
- Fixed data merge organization. [4bba0f4](https://github.com/coordt/cookie-composer/commit/4bba0f4de123d11624fc96ec5f49f8341d958108)
    
  - Moved data merge constants and functions from composition.py to data_merge.py
### New

- Added new workflow for versioning. [2232682](https://github.com/coordt/cookie-composer/commit/2232682391e491b8511e532ef270bb2a24d56a8f)
    
- Added context managers for temporary copies. [90fa24c](https://github.com/coordt/cookie-composer/commit/90fa24cb6e5d4b03e74cca3c1df9891780e2cdcf)
    
- Added convenience functions to the template classes. [0b62c44](https://github.com/coordt/cookie-composer/commit/0b62c440ec481356f283bc62fbaca27c0ec1cdf6)
    
- Added interface to get template repositories. [cf9ff4a](https://github.com/coordt/cookie-composer/commit/cf9ff4a412d19eeba47919deb0387b57380ccb4a)
    
- Added git template repositories. [02bf112](https://github.com/coordt/cookie-composer/commit/02bf112dcd1d951b3ac5c0d38a6295ce5aa72848)
    
- Added zipfile template repositories. [8190cb6](https://github.com/coordt/cookie-composer/commit/8190cb64f808c9ad2229c8c503b3e0125501b7f6)
    
- Added git shortcuts for cloning. [6ad76a3](https://github.com/coordt/cookie-composer/commit/6ad76a3c32a90cfbaeee72b7ab5688c7b0377ed0)
    
### Other

- Moved `get_context_for_layer` from utils.py to composition.py. [6641a91](https://github.com/coordt/cookie-composer/commit/6641a9102ac0fce22df4b30fee3dd141a3fb6c9b)
    
- Moved `get_template_name` tests. [1c0c054](https://github.com/coordt/cookie-composer/commit/1c0c05454f97068414a7e1155de126ad65aa1878)
    
- [pre-commit.ci] pre-commit autoupdate. [db151ef](https://github.com/coordt/cookie-composer/commit/db151ef49453ade797eb1437de9ff98e6b186b08)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.287 → v0.0.290](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.287...v0.0.290)

- [pre-commit.ci] pre-commit autoupdate. [7335d97](https://github.com/coordt/cookie-composer/commit/7335d9722973db509fa2636999c724d361a488b7)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.287 → v0.0.292](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.287...v0.0.292)

- Bump urllib3 from 2.0.4 to 2.0.7 in /requirements. [6f5dd07](https://github.com/coordt/cookie-composer/commit/6f5dd07ae6576ce65c1c0e4a27f527491d74d71a)
    
  Bumps [urllib3](https://github.com/urllib3/urllib3) from 2.0.4 to 2.0.7.
  - [Release notes](https://github.com/urllib3/urllib3/releases)
  - [Changelog](https://github.com/urllib3/urllib3/blob/main/CHANGES.rst)
  - [Commits](https://github.com/urllib3/urllib3/compare/2.0.4...2.0.7)

  ---
  **updated-dependencies:** - dependency-name: urllib3
dependency-type: direct:production

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [94b1833](https://github.com/coordt/cookie-composer/commit/94b18336a59d7495ed2dd9055e9d8013e72eb927)
    
  **updates:** - [github.com/astral-sh/ruff-pre-commit: v0.0.287 → v0.1.3](https://github.com/astral-sh/ruff-pre-commit/compare/v0.0.287...v0.1.3)

- [pre-commit.ci] pre-commit autoupdate. [bc33fbd](https://github.com/coordt/cookie-composer/commit/bc33fbd383107379b00c7a9932f83a62442b872f)
    
  **updates:** - https://github.com/charliermarsh/ruff-pre-commit → https://github.com/astral-sh/ruff-pre-commit

### Updates

- Updated requirement lock files. [026cd2d](https://github.com/coordt/cookie-composer/commit/026cd2dcbd045b2e88031abda0a9b75190ad300d)
    
- Updated pre-commit config. [57d6cff](https://github.com/coordt/cookie-composer/commit/57d6cff1f362ff1ba04ce34b2128913eff9bf92f)
    
- Updated requirements. [8d83ba0](https://github.com/coordt/cookie-composer/commit/8d83ba0be0edd4013cdb7e42064156310589eb41)
    
- Updated tests. [5d3c51f](https://github.com/coordt/cookie-composer/commit/5d3c51f18d1d3833563a6d5062960994130f30d8)
    
- Renamed `zipfile_repo.unzip` to `cache_source`. [60a2393](https://github.com/coordt/cookie-composer/commit/60a23939fa462a599a3a0eaee52ff0b2337fb6d6)
    
- Updated commands to use refactored methods. [14d2781](https://github.com/coordt/cookie-composer/commit/14d27811f04062ad0f720fa536102ba3874d78d5)
    
- Refactored (de)serialization and I/O methods into `io` module. [3c64a3e](https://github.com/coordt/cookie-composer/commit/3c64a3e2aae7efc54cf87caf16d96bfe06900b65)
    
- Refactored `layers`. [e8af7d5](https://github.com/coordt/cookie-composer/commit/e8af7d5279f7c6be9af163f2d8ac008b6e34cc5f)
    
  - Integrated `Template` with `LayerConfig`
      - `template` attribute is now a `Template` instance
      - removed `directory`, `checkout`, `password`, and `commit`
      - renamed `context` to `initial_context` to distiguish it from the `Template`'s context
  - Updated `RenderedLayer` to use templates
      - renamed `new_context` to `rendered_context` to better describe it.
      - renamed `latest_commit` to `rendered_commit` for better clarity
      - added `latest_commit` convenience function
  - Simplified `render_layer` using the new template functions
- Removed get_latest_template_commit from git_commands. [af84ff4](https://github.com/coordt/cookie-composer/commit/af84ff404a62cf1c36329f9211c4370795230792)
    
  It is now part of the template repo
- Updated requirements to use Pydantic 2. [b24a158](https://github.com/coordt/cookie-composer/commit/b24a15818aec12f622b60caa456d8e67d7445078)
    
- Refactored layer context to fix #39. [300578f](https://github.com/coordt/cookie-composer/commit/300578f067df5582bc8041f1eaf2fec3bc3761f6)
    

## 0.11.0 (2023-07-27)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.10.3...0.11.0)

### Fixes

- Fix test coverage matrix. [5ef8815](https://github.com/coordt/cookie-composer/commit/5ef8815aac62f874b5d130e82d7b8ba4320ec49b)
    
- Fix pre-commit from autofixing templates. [99e7dfb](https://github.com/coordt/cookie-composer/commit/99e7dfb6d71ece01d1c74d6d61b9cc135b124b31)
    
- Fixed typing hints. [ff695e3](https://github.com/coordt/cookie-composer/commit/ff695e38e864cf052bb15dc3a4278e782ce7a784)
    
### New

- Added support for local extensions. [838f25c](https://github.com/coordt/cookie-composer/commit/838f25c67c91b39be137b93bd64191bd78ae8d08)
    
- Added `-o` and `--output-dir` as an alias. [04f063d](https://github.com/coordt/cookie-composer/commit/04f063d702279731e54a578fd5c82f7f59426798)
    
  It is now an alias for `-d` and `--destination`
### Other

- Revert "[pre-commit.ci] auto fixes from pre-commit.com hooks". [42d8704](https://github.com/coordt/cookie-composer/commit/42d8704565d1927647e1692b29bd3e62e149a37a)
    
  This reverts commit 52772f1352d6130b2d6189bf632b26fb9732c13f.
- [pre-commit.ci] auto fixes from pre-commit.com hooks. [52772f1](https://github.com/coordt/cookie-composer/commit/52772f1352d6130b2d6189bf632b26fb9732c13f)
    
  for more information, see https://pre-commit.ci
- Migrated from setup.cfg to pyproject.toml. [b3a39f0](https://github.com/coordt/cookie-composer/commit/b3a39f0845a0dcd66177b3fbfaf5cac0369c18e1)
    
- Bump aiohttp from 3.8.3 to 3.8.5 in /requirements. [0392ef7](https://github.com/coordt/cookie-composer/commit/0392ef74feda8f0e2080967fa4ced8a62b1b9166)
    
  Bumps [aiohttp](https://github.com/aio-libs/aiohttp) from 3.8.3 to 3.8.5.
  - [Release notes](https://github.com/aio-libs/aiohttp/releases)
  - [Changelog](https://github.com/aio-libs/aiohttp/blob/v3.8.5/CHANGES.rst)
  - [Commits](https://github.com/aio-libs/aiohttp/compare/v3.8.3...v3.8.5)

  ---
  **updated-dependencies:** - dependency-name: aiohttp
dependency-type: direct:production

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [83d1217](https://github.com/coordt/cookie-composer/commit/83d121798ff502a6aa95caff731b5f39d698485b)
    
  **updates:** - [github.com/psf/black: 23.3.0 → 23.7.0](https://github.com/psf/black/compare/23.3.0...23.7.0)

- [pre-commit.ci] pre-commit autoupdate. [c58fe42](https://github.com/coordt/cookie-composer/commit/c58fe42786a5c73e82a57ae8aab7f9fef5e94c14)
    
  **updates:** - [github.com/psf/black: 23.3.0 → 23.7.0](https://github.com/psf/black/compare/23.3.0...23.7.0)


## 0.10.3 (2023-05-15)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.10.2...0.10.3)

### New

- Added support for accepting hooks. [096dfcc](https://github.com/coordt/cookie-composer/commit/096dfcc79ce19a732b93c4f6d00b5e733dc0a597)
    


## 0.10.2 (2023-05-11)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.10.1...0.10.2)

### Fixes

- Fixed a bug that reformatted files that should be overwritten. [3f0f7b5](https://github.com/coordt/cookie-composer/commit/3f0f7b5f54ec227ade3b49b411e4324c889a0b7e)
    


## 0.10.1 (2023-05-10)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.10.0...0.10.1)

### Fixes

- Fixed a bug where additional context wasn't passed to the composition. [bd8b571](https://github.com/coordt/cookie-composer/commit/bd8b57140ec29a7b6ec6542086660c012c43b428)
    
### Other

- Bump markdown-it-py from 2.1.0 to 2.2.0 in /requirements. [65a4863](https://github.com/coordt/cookie-composer/commit/65a4863b1baab6c2f6062806874c2e8946b857ff)
    
  Bumps [markdown-it-py](https://github.com/executablebooks/markdown-it-py) from 2.1.0 to 2.2.0.
  - [Release notes](https://github.com/executablebooks/markdown-it-py/releases)
  - [Changelog](https://github.com/executablebooks/markdown-it-py/blob/master/CHANGELOG.md)
  - [Commits](https://github.com/executablebooks/markdown-it-py/compare/v2.1.0...v2.2.0)

  ---
  **updated-dependencies:** - dependency-name: markdown-it-py
dependency-type: indirect

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [21eca93](https://github.com/coordt/cookie-composer/commit/21eca9331691b355b322119fca002384eb827fb4)
    
  **updates:** - [github.com/psf/black: 23.1.0 → 23.3.0](https://github.com/psf/black/compare/23.1.0...23.3.0)



## 0.10.0 (2023-03-24)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.9.2...0.10.0)

### New

- Added relative directory support for compositions. [02fa5b8](https://github.com/coordt/cookie-composer/commit/02fa5b8b591c25fef7bbd6c2aec20532f16541b5)
    
  - Template paths or URLs are resolved using the path to the composition file.
  - Using an absolute path or URL as a template works as before
  - `.`, `..`, and relative paths (non-`/` prefixed) are resolved with `urllib.parse.urljoin`


## 0.9.2 (2023-02-13)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.9.1...0.9.2)

### New

- Added test for validate_context_params. [a52d28d](https://github.com/coordt/cookie-composer/commit/a52d28d97445c426f02cb8399883ad8a9052928c)
    
- Added ability to pass initial contexts. [9e3cdf3](https://github.com/coordt/cookie-composer/commit/9e3cdf34480f9bfafd5f4750d48b78cc6ac294e1)
    
### Updates

- Modified CLI options and arguments. [02a4bf3](https://github.com/coordt/cookie-composer/commit/02a4bf3a9378f2788be53cfa769bbc5a9bb3eae3)
    
  - The `output_dir` argument was moved to the `--destination` option.
  - Added `CONTEXT_PARAMS` argument for initial context
- Removed checkout from first commit when linking. [f2725ef](https://github.com/coordt/cookie-composer/commit/f2725ef3464f932914e3393e5883792a8f93d0ca)
    
  - The first commit was causing confusing issues and now a normal checkout is performed.


## 0.9.1 (2023-02-08)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.9.0...0.9.1)

### New

- Added `--version` option. [4b1b9e1](https://github.com/coordt/cookie-composer/commit/4b1b9e1fd84f976f590dcc1ad803dea4808fe643)
    


## 0.9.0 (2023-01-25)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.8.1...0.9.0)

### Fixes

- Fixed license and documentation badges. [37289c9](https://github.com/coordt/cookie-composer/commit/37289c96e4bebcd25b2df0f90a797f2753494d07)
    
- Fixed the coveralls badge in README. [a4eaf73](https://github.com/coordt/cookie-composer/commit/a4eaf7313e534e71942335a8cce18b8348658159)
    
### New

- Added testing for authentication.py. [73c8335](https://github.com/coordt/cookie-composer/commit/73c83351529a834c219ffb4e8aa22fad84108802)
    
- Added authentication capability. [19b5a8d](https://github.com/coordt/cookie-composer/commit/19b5a8d60e1c12f361ff0d08d9809b310dede40d)
    
### Other

- Switched to Codecov. [c2fb125](https://github.com/coordt/cookie-composer/commit/c2fb125712b24c98ac450f206fb31048cb06dc5f)
    
- [pre-commit.ci] pre-commit autoupdate. [1f5320a](https://github.com/coordt/cookie-composer/commit/1f5320a8f9d45c0c9bc68290d43dec76c5230ce3)
    
  **updates:** - [github.com/pycqa/pydocstyle: 6.1.1 → 6.2.3](https://github.com/pycqa/pydocstyle/compare/6.1.1...6.2.3)

### Updates

- Updated documentation. [1a1c1f6](https://github.com/coordt/cookie-composer/commit/1a1c1f6166328dd627fdf5a0de7d9c17da684740)
    
- Update README.md coveralls badge. [b105133](https://github.com/coordt/cookie-composer/commit/b105133dc5046b55d6b486eaa2715a671c1c661a)
    
- Update README.md. [a55a257](https://github.com/coordt/cookie-composer/commit/a55a2579edafd49541b50de994d9ddcd203dd8ea)
    


## 0.8.1 (2023-01-04)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.8.0...0.8.1)

### Fixes

- Fixed YAML merge formatting. [7259919](https://github.com/coordt/cookie-composer/commit/7259919a851e7d5d4d1d59e7eb38b51eca7ed91a)
    
### Other

- Bump wheel from 0.37.1 to 0.38.1 in /requirements. [cab9b8e](https://github.com/coordt/cookie-composer/commit/cab9b8e1ce86c4a3dd38182320a9e64d016f849e)
    
  Bumps [wheel](https://github.com/pypa/wheel) from 0.37.1 to 0.38.1.
  - [Release notes](https://github.com/pypa/wheel/releases)
  - [Changelog](https://github.com/pypa/wheel/blob/main/docs/news.rst)
  - [Commits](https://github.com/pypa/wheel/compare/0.37.1...0.38.1)

  ---
  **updated-dependencies:** - dependency-name: wheel
dependency-type: indirect

  **signed-off-by:** dependabot[bot] <support@github.com>

- [pre-commit.ci] pre-commit autoupdate. [45e8596](https://github.com/coordt/cookie-composer/commit/45e859622a82cd023f7ca02bfcd9a8e79f249508)
    
  **updates:** - [github.com/PyCQA/isort: v5.11.3 → 5.11.4](https://github.com/PyCQA/isort/compare/v5.11.3...5.11.4)

- [pre-commit.ci] pre-commit autoupdate. [550e0cb](https://github.com/coordt/cookie-composer/commit/550e0cb1e788dd0c800e502862f236f8bf3e9bfe)
    
  **updates:** - [github.com/PyCQA/isort: 5.10.1 → v5.11.3](https://github.com/PyCQA/isort/compare/5.10.1...v5.11.3)



## 0.8.0 (2022-12-16)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.7.1...0.8.0)

### Fixes

- Fixed ability to merge a list of dicts in YAML. [f3698ef](https://github.com/coordt/cookie-composer/commit/f3698ef7588fbac64cc14a9699ee4c2a4fca7f4d)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [5b21a40](https://github.com/coordt/cookie-composer/commit/5b21a4070ae643adaa5be564de2e9a171abe6b3d)
    
  **updates:** - [github.com/psf/black: 22.10.0 → 22.12.0](https://github.com/psf/black/compare/22.10.0...22.12.0)

- [pre-commit.ci] pre-commit autoupdate. [0f5c7a5](https://github.com/coordt/cookie-composer/commit/0f5c7a5fcb16b5557cf6453ad02d119b3edf8852)
    
  **updates:** - [github.com/pre-commit/pre-commit-hooks: v4.3.0 → v4.4.0](https://github.com/pre-commit/pre-commit-hooks/compare/v4.3.0...v4.4.0)

### Updates

- Change frozendict to immutabledict. [8edf699](https://github.com/coordt/cookie-composer/commit/8edf69920e37032c27ceea1545c51e11e86892e8)
    
- Changed JSON library to orjson. [c857a2f](https://github.com/coordt/cookie-composer/commit/c857a2f694d131a44ce863a743d8bbceb5146095)
    
  - has better serialization capability and performance.


## 0.7.1 (2022-11-07)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.7.0...0.7.1)

### Fixes

- Fixed ability to merge a list of dicts. [21b9033](https://github.com/coordt/cookie-composer/commit/21b9033d922ac83b31ebc1c1f65d6fec7d4582aa)
    
- Fixed chrobinson email to me. [7f2bf8e](https://github.com/coordt/cookie-composer/commit/7f2bf8e5d84c0777f19d321b216ca437050e1559)
    


## 0.7.0 (2022-10-31)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.6.0...0.7.0)

### New

- Added ability to merge .toml files. [2e36b40](https://github.com/coordt/cookie-composer/commit/2e36b407feadd58f6aac418504ea6e9274175afe)
    
- Added ability to merge .ini and .cfg files. [31ff1e0](https://github.com/coordt/cookie-composer/commit/31ff1e033f10bef3067b4811aaa61607fa6c5b14)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [a31eeef](https://github.com/coordt/cookie-composer/commit/a31eeef0dff2d826d68d6138667b5ab971eefa7a)
    
  **updates:** - [github.com/psf/black: 22.8.0 → 22.10.0](https://github.com/psf/black/compare/22.8.0...22.10.0)



## 0.6.0 (2022-10-09)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.5.0...0.6.0)

### Fixes

- Fixed a typo in the docs. [986f0d8](https://github.com/coordt/cookie-composer/commit/986f0d8c229689c77f6a9814b20386c0280124bc)
    
- Fixed dependency conflict between flake8 and virtualenv. [6925b05](https://github.com/coordt/cookie-composer/commit/6925b059c2be253b15375319c3f6fc51518995c9)
    
### New

- Added the link command to apply a composition to an existing project. [03f723e](https://github.com/coordt/cookie-composer/commit/03f723e20d9063f233513526ac46047f9efeb37c)
    
### Updates

- Updated the update command to use `git diff` and `git apply`. [d4bc14f](https://github.com/coordt/cookie-composer/commit/d4bc14f2765ad4cf9ee0bd10077a61d1b4f40353)
    
- Updated the project requirements. [0834e0b](https://github.com/coordt/cookie-composer/commit/0834e0bcb89f6dcc45a10afe298b5b2b197f8807)
    
- Refactored getting a composition from an input. [2f8edfe](https://github.com/coordt/cookie-composer/commit/2f8edfecdf17f2b1440a096e4d2fd853a75d1d2f)
    


## 0.5.0 (2022-09-22)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.4.0...0.5.0)

### New

- Added the update subcommand. [6696589](https://github.com/coordt/cookie-composer/commit/66965899d5c7c5d701c70d97e77f304904531bcf)
    
  - Made the existing implementation idempotent
  - Connected the update_cmd to the command line
- Add very basic cli tests. [c6482d4](https://github.com/coordt/cookie-composer/commit/c6482d46c11e70b354851a9c431634d0d4a6c51f)
    
### Other

- [pre-commit.ci] auto fixes from pre-commit.com hooks. [e5425d5](https://github.com/coordt/cookie-composer/commit/e5425d5bebb847be59b48ad5c9ac3cfb11fa5a92)
    
  for more information, see https://pre-commit.ci
- [pre-commit.ci] pre-commit autoupdate. [dbfde0a](https://github.com/coordt/cookie-composer/commit/dbfde0ae58ca2d7fb0f537388091a74607a8fcdc)
    
  **updates:** - [github.com/psf/black: 22.6.0 → 22.8.0](https://github.com/psf/black/compare/22.6.0...22.8.0)

### Updates

- Update cli.py. [5a50f14](https://github.com/coordt/cookie-composer/commit/5a50f14c0affbfee66a795d9df5bfe6ecb905e7c)
    

## 0.4.0 (2022-09-06)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.3.0...0.4.0)

### New

- Added subset of cookiecutter options to CLI. [a66f17a](https://github.com/coordt/cookie-composer/commit/a66f17a0471f7178742f9d8d80010bb8d6628cac)
    
- Added documentation images. [86113dc](https://github.com/coordt/cookie-composer/commit/86113dcb19588ede45cfedcebda7f6e840c3b652)
    
- Added template layer updating. [20c6fe3](https://github.com/coordt/cookie-composer/commit/20c6fe326955deb3514420abb12d2bfaef7353a7)
    
- Added layer naming convention. [5e61312](https://github.com/coordt/cookie-composer/commit/5e613121130a640ff6721fec322a9a948cfa7a1e)
    
### Other

- [pre-commit.ci] pre-commit autoupdate. [e516a18](https://github.com/coordt/cookie-composer/commit/e516a181e4a3ebe3d3c93800ef8a059125494d82)
    
  **updates:** - [github.com/PyCQA/flake8: 4.0.1 → 5.0.4](https://github.com/PyCQA/flake8/compare/4.0.1...5.0.4)

- [pre-commit.ci] pre-commit autoupdate. [3e6f695](https://github.com/coordt/cookie-composer/commit/3e6f695a3126c52beec1a1bcd3f39e4df09cc2ee)
    
  **updates:** - [github.com/psf/black: 22.3.0 → 22.6.0](https://github.com/psf/black/compare/22.3.0...22.6.0)

### Updates

- Updated documentation configuration. [a4c9652](https://github.com/coordt/cookie-composer/commit/a4c9652625f8e42df722f046f13a2f4e74f7c4bf)
    
- Updated README.md. [a7ead0d](https://github.com/coordt/cookie-composer/commit/a7ead0d745aae637948661e3bb6ac7a978b0d4a3)
    

## 0.3.0 (2022-06-29)
[Compare the full difference.](https://github.com/coordt/cookie-composer/compare/0.2.2...0.3.0)

### Fixes

- Fixed metadata's long description content type. [99470e9](https://github.com/coordt/cookie-composer/commit/99470e936dc440012d8542cd590853836a6454b6)
    
### Other

- Created tests for the add command. [358e189](https://github.com/coordt/cookie-composer/commit/358e189020fead21646397e56399e920e85a7ac2)
    
### Updates

- Updated cc_override's tests. [5388df7](https://github.com/coordt/cookie-composer/commit/5388df7cb4abe6f460a6f4ddd71f24cb9b02012f)
    

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
