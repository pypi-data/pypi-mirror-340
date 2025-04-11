import os


def dirname(path, indeks=-1):
    """
    Mengembalikan nama folder dari path.
    Tanpa trailing slash di akhir.

    ```python
    print(dirname("/ini/nama/folder/ke/file.py"))
    ```
    """
    paths = path.split(os.sep)
    if indeks < 0:
        paths = paths[: len(paths) + indeks]
    return os.sep.join(paths)
    return os.path.dirname(path)
