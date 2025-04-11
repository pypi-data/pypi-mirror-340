import os

from .filter_empty import filter_empty


def dirname(path, indeks=-1, abs_path=None):
    """
    Mengembalikan nama folder dari path.
    Tanpa trailing slash di akhir.

    ```python
    print(dirname("/ini/nama/folder/ke/file.py"))
    ```
    """
    
    paths = path.split(os.sep)
    paths = list(filter_empty(paths))

    if indeks < 0:
        paths = paths[: len(paths) + indeks]
    path = os.sep.join(paths)

    if abs_path is None:
        return path

    path = os.path.abspath(path)
    if abs_path:
        return path
    return os.path.relpath(path, os.getcwd())

    return os.path.dirname(path)
