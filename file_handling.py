import sys
from platformdirs import user_data_dir
from pathlib import Path
from contextlib import contextmanager


def appdata_path(rel_path):
    base_path = Path(user_data_dir('CardGenerator', 'BunkersBadasses'))

    return f"{base_path / rel_path}"


def resource_path(rel_path):
    # Path to bundled resource
    if getattr(sys, 'frozen', False):
        # When running as executable
        base_path = Path(sys._MEIPASS)
    else:
        # Running from source
        base_path = Path(__file__).parent

    return f"{base_path / rel_path}"


@contextmanager
def open_resourcefile(path, mode='r', *args, **kwargs):
    full_path = resource_path(path)
    with open (full_path, mode, *args, **kwargs) as file:
        yield file

@contextmanager
def open_appdatafile(path, mode='r', *args, **kwargs):
    full_path = appdata_path(path)

    # Create directories if not yet exists
    if 'w' in mode:
        full_path.parent.mkdir(parents=True, exist_ok=True)

    with open(full_path, mode, *args, **kwargs) as file:
        yield file
