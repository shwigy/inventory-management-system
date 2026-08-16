"""In-memory/JSON-file backed inventory store used to simulate a database."""
import json
import os
from threading import Lock

DATA_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "data",
    "inventory.json",
)

_lock = Lock()


def _load():
    if not os.path.exists(DATA_FILE):
        return {"items": []}
    with open(DATA_FILE, "r") as f:
        content = f.read().strip()
        if not content:
            return {"items": []}
        return json.loads(content)


def _save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


def _next_id(items):
    if not items:
        return 1
    return max(item["id"] for item in items) + 1


def get_all_items():
    return _load()["items"]


def get_item(item_id):
    for item in get_all_items():
        if item["id"] == item_id:
            return item
    return None


def add_item(item):
    with _lock:
        data = _load()
        new_item = dict(item)
        new_item["id"] = _next_id(data["items"])
        data["items"].append(new_item)
        _save(data)
        return new_item


def update_item(item_id, updates):
    with _lock:
        data = _load()
        for item in data["items"]:
            if item["id"] == item_id:
                item.update(updates)
                item["id"] = item_id
                _save(data)
                return item
        return None


def delete_item(item_id):
    with _lock:
        data = _load()
        for item in data["items"]:
            if item["id"] == item_id:
                data["items"].remove(item)
                _save(data)
                return True
        return False
