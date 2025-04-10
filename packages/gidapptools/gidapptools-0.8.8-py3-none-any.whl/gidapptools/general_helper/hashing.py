"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
from typing import TYPE_CHECKING, Callable
from hashlib import sha1, blake2b
from pathlib import Path

# * Type-Checking Imports --------------------------------------------------------------------------------->
if TYPE_CHECKING:
    from gidapptools.custom_types import PATH_TYPE
    from hashlib import _Hash

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


# FILE_HASH_INCREMENTAL_THRESHOLD: int = 104857600  # 100mb
FILE_HASH_INCREMENTAL_THRESHOLD: int = 52428800  # 50mb


def _actual_hash_file(in_file: Path, hash_algo: Callable = blake2b) -> "_Hash":
    if in_file.stat().st_size > FILE_HASH_INCREMENTAL_THRESHOLD:
        _hash = hash_algo(usedforsecurity=False)
        with in_file.open("rb", buffering=FILE_HASH_INCREMENTAL_THRESHOLD // 4) as f:
            for chunk in f:
                _hash.update(chunk)
        return _hash

    return hash_algo(in_file.read_bytes(), usedforsecurity=False)


def file_hash(in_file: "PATH_TYPE", hash_algo: Callable = blake2b) -> str:
    in_file = Path(in_file)
    if not in_file.is_file():
        raise OSError(f"The path {in_file.as_posix()!r} either does not exist or is a Folder.")
    return _actual_hash_file(in_file=in_file, hash_algo=hash_algo).hexdigest()


def hash_to_int(in_hash: str) -> int:
    return int(in_hash, base=16)

# region [Main_Exec]


if __name__ == '__main__':
    pass
# endregion [Main_Exec]
