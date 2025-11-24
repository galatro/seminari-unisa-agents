import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_json(name: str):
    with open(DATA_DIR / name, "r") as f:
        return json.load(f)

def save_json(name: str, data):
    with open(DATA_DIR / name, "w") as f:
        json.dump(data, f, indent=4)
