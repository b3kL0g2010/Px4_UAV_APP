from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def resource_path(relative_path):

    return str(
        BASE_DIR / relative_path
    )
