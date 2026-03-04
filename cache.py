import os
import json


def get_cache_dir():
    if os.name == "nt":
        base = os.path.join(os.environ.get("APPDATA", os.path.expanduser("~")),
                            "GameSupportTracker")
    else:
        base = os.path.join(os.path.expanduser("~"), ".config", "GameSupportTracker")
    os.makedirs(base, exist_ok=True)
    return base


def get_cache_path():
    return os.path.join(get_cache_dir(), "archipelago_cache.json")


def get_settings_path():
    return os.path.join(get_cache_dir(), "settings.json")


CACHE_FILE = get_cache_path()


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_cache(data):
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_settings():
    p = get_settings_path()
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_settings(data):
    with open(get_settings_path(), "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)