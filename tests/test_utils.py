import os
import sys
import pytest

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(myPath, "..", "code"))

from utils import load_json, validate_json


def test_load_json():
    """
    Unit test to check the load_json function
    """
    file_path = os.path.join(".cloud", ".azure", "workspace.json")
    json_object = load_json(
        file_path=file_path
    )
    assert type(json_object) == dict

    with pytest.raises(FileNotFoundError):
        assert load_json(
            file_path=""
        )
