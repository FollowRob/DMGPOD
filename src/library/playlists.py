import json
import os
import uuid

PLAYLIST_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "playlists")


def _ensure_dir():
    os.makedirs(PLAYLIST_DIR, exist_ok=True)


def load_all():
    """Return list of playlist dicts sorted by name."""
    _ensure_dir()
    result = []
    for fname in sorted(os.listdir(PLAYLIST_DIR)):
        if fname.endswith(".json"):
            path = os.path.join(PLAYLIST_DIR, fname)
            try:
                with open(path) as f:
                    data = json.load(f)
                data["_file"] = path
                result.append(data)
            except Exception:
                pass
    return result


def save(playlist):
    """Save a playlist dict. Adds id and _file if missing."""
    _ensure_dir()
    if "id" not in playlist:
        playlist["id"] = str(uuid.uuid4())[:8]
    if "_file" not in playlist:
        safe = "".join(c if c.isalnum() or c in "-_ " else "_" for c in playlist["name"])
        playlist["_file"] = os.path.join(PLAYLIST_DIR, safe + ".json")
    data = {k: v for k, v in playlist.items() if not k.startswith("_")}
    with open(playlist["_file"], "w") as f:
        json.dump(data, f, indent=2)


def delete(playlist):
    if "_file" in playlist and os.path.exists(playlist["_file"]):
        os.remove(playlist["_file"])
