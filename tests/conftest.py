import json
from pathlib import Path

import pytest

DATA_DIR = Path(__file__).parent / ".data"


@pytest.fixture()
def load_data():
    """
    Provides a callable that retrieves JSON objects from tests/.data.
    """

    def _fetch_json(filename: str) -> dict:
        file_path = DATA_DIR / filename
        if not file_path.exists():
            raise FileNotFoundError(f"Unable to locate: {file_path}")
        with open(file_path, "r") as f:
            return json.loads(f.read())

    return _fetch_json
