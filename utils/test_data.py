import json
import os

def load_test_data(file_name: str) -> dict:
    file_path = os.path.join("testdata", file_name)
    with open(file_path, "r") as f:
        return json.load(f)