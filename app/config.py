import json
from typing import Optional
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


def get_sercet(
    key: str,
    default_value: Optional[str] = None,
    json_path: str = str(BASE_DIR / "secrets.json")
):
    with open(json_path) as f:
        secrets = json.loads(f.read())
    try:
        return secrets[key]
    except KeyError:
        if default_value:
            return default_value
        raise EnvironmentError(f"Set the {key} enviroment variable.")


if __name__ == "__main__":
    world = get_sercet("Hello")
    print(world)