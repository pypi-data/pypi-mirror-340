"""
WiP.

Soon.
"""

# region [Imports]

# * Standard Library Imports ---------------------------------------------------------------------------->
from pathlib import Path
from threading import Lock, RLock
from weakref import WeakValueDictionary
from filelock import FileLock
# * Gid Imports ----------------------------------------------------------------------------------------->
from gidapptools.custom_types import LOCK_CLASS_TYPE, PATH_TYPE, LOCK_TYPE

# endregion [Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion [Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion [Constants]


class SingleProcessFileLocksManager:
    __slots__ = ("_lock_type",
                 "_interaction_lock",
                 "_file_locks")

    def __init__(self, lock_type: LOCK_CLASS_TYPE):
        self._lock_type = lock_type
        self._interaction_lock: Lock = Lock()
        self._file_locks: WeakValueDictionary[Path, LOCK_TYPE] = WeakValueDictionary()

    def _handle_file_path(self, file_path: PATH_TYPE) -> Path:
        return Path(file_path).resolve()

    def _get_or_create(self, file_path: PATH_TYPE) -> LOCK_CLASS_TYPE:
        file_path = self._handle_file_path(file_path=file_path)
        with self._interaction_lock:
            try:
                return self._file_locks[file_path]
            except KeyError:
                file_lock = self._lock_type()
                self._file_locks[file_path] = file_lock
                return file_lock

    def get_file_lock(self, file_path: PATH_TYPE) -> LOCK_CLASS_TYPE:
        return self._get_or_create(file_path=file_path)

    def __getitem__(self, file_path: PATH_TYPE) -> LOCK_CLASS_TYPE:
        return self.get_file_lock(file_path=file_path)

    def __len__(self) -> int:
        with self._interaction_lock:
            return len(self._file_locks)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(lock_type={self._lock_type!r})"


GLOBAL_LOCK_MANAGER = SingleProcessFileLocksManager(Lock)
GLOBAL_RLOCK_MANAGER = SingleProcessFileLocksManager(RLock)


# region [Main_Exec]
if __name__ == '__main__':
    pass
# endregion [Main_Exec]
