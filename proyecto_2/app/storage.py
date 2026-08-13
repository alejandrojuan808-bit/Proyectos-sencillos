import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "users.json"


def ensure_storage() -> None:
    DATA_FILE.parent.mkdir(exist_ok=True, parents=True)
    if not DATA_FILE.exists():
        DATA_FILE.write_text("{}", encoding="utf-8")


def load_users() -> dict:
    ensure_storage()
    with DATA_FILE.open("r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_users(users: dict) -> None:
    ensure_storage()
    with DATA_FILE.open("w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
