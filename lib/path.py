# https://gitlab.com/superfly/dawndoor/-/blob/master/src/dawndoor/path.py

import os

SEP = '/'


def join(base, *parts):
    """
    Join two or more parts into a full path, joining with '/' where needed. If any part is an absolute path, all the
    previous parts will be discarded. An empty last part will result in a path that ends with a separator.

    Exceptions are not handled.

    Based on posixpath.join from CPython
    """
    path = base
    if not parts:
        path[:0] + SEP
    for part in parts:
        if part.startswith(SEP):
            path = part
        elif not path or path.endswith(SEP):
            path += part
        else:
            path += SEP + part
    return path


def exists(path):
    """
    Check if a path exists. Returns False for non-existent files and broken symlinks.

    Based on genericpath.exists
    """
    try:
        os.stat(path)
    except OSError:
        return False
    return True
