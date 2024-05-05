"""
Methods for merging data files.

The merging functions should look similar to the following:

```
def merge_generic_files(origin: Path, destination: Path, merge_strategy: str) -> None:
```

The function must write the file to destination.

The function must wrap any errors into a [MergeError][cookie_composer.exceptions.MergeError] and raise it.
"""

from pathlib import Path
from typing import Callable, Dict

from cookie_composer.merge_files.ini_file import merge_ini_files
from cookie_composer.merge_files.json_file import merge_json_files
from cookie_composer.merge_files.toml_file import merge_toml_files
from cookie_composer.merge_files.yaml_file import merge_yaml_files

merge_function = Callable[[Path, Path, str], None]

MERGE_FUNCTIONS: Dict[str, merge_function] = {
    ".json": merge_json_files,
    ".yaml": merge_yaml_files,
    ".yml": merge_yaml_files,
    ".ini": merge_ini_files,
    ".cfg": merge_ini_files,
    ".toml": merge_toml_files,
}
