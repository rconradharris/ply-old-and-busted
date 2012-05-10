import contextlib
import os


def fixup_path(path):
    path = os.path.expanduser(path)
    path = os.path.abspath(path)
    return path


def slugify(text):
    # TODO: use Django's slugify routine
    text = text.replace(' ', '-')
    return text


@contextlib.contextmanager
def temporary_chdir(path):
    if not os.path.exists(path):
        raise PathNotFound(path)

    orig_path = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(orig_path)


def walk_up_path(path):
    """Walk up a given path towards the root directory.

    For example, path '/a/b/c' would yield:
        /a/b/c
        /a/b
        /a
        /
    """
    prev_path = None
    while True:
        yield path
        prev_path = path
        path, _ = os.path.split(path)
        if prev_path == path:
            raise StopIteration


def write_empty_file(filename):
    return write_file(filename, '')


def write_file(filename, data):
    with open(filename, 'w') as f:
        f.write(data)
