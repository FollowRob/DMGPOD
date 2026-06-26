#!/usr/bin/env python3
"""
DMGPod Playlist Editor
Run: python3 tools/playlist_editor.py
Then open http://localhost:8765 in your browser.
"""

import json
import os
import sys
import uuid
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MUSIC_DIR = os.path.join(ROOT, "music")
PLAYLIST_DIR = os.path.join(ROOT, "playlists")
PORT = 8765

AUDIO_EXT = {".flac", ".mp3", ".wav", ".m4a", ".ogg"}


def scan_tracks():
    tracks = []
    for dirpath, _, filenames in os.walk(MUSIC_DIR):
        for fname in sorted(filenames):
            if os.path.splitext(fname)[1].lower() in AUDIO_EXT:
                full = os.path.join(dirpath, fname)
                rel = os.path.relpath(full, ROOT)
                parts = os.path.relpath(full, MUSIC_DIR).split(os.sep)
                artist = parts[0] if len(parts) > 2 else "Unknown Artist"
                album  = parts[1] if len(parts) > 2 else (parts[0] if len(parts) > 1 else "Unknown Album")
                title  = os.path.splitext(parts[-1])[0]
                tracks.append({"path": rel, "title": title, "artist": artist, "album": album})
    return tracks


def load_playlists():
    os.makedirs(PLAYLIST_DIR, exist_ok=True)
    result = []
    for fname in sorted(os.listdir(PLAYLIST_DIR)):
        if fname.endswith(".json"):
            try:
                with open(os.path.join(PLAYLIST_DIR, fname)) as f:
                    data = json.load(f)
                data["_file"] = fname
                result.append(data)
            except Exception:
                pass
    return result


def save_playlist(data):
    os.makedirs(PLAYLIST_DIR, exist_ok=True)
    pid = data.get("id") or str(uuid.uuid4())[:8]
    data["id"] = pid
    fname = data.get("_file") or (
        "".join(c if c.isalnum() or c in "-_ " else "_" for c in data["name"]) + ".json"
    )
    clean = {k: v for k, v in data.items() if not k.startswith("_")}
    with open(os.path.join(PLAYLIST_DIR, fname), "w") as f:
        json.dump(clean, f, indent=2)
    return fname


def delete_playlist(fname):
    path = os.path.join(PLAYLIST_DIR, fname)
    if os.path.exists(path):
        os.remove(path)


HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>DMGPod Playlist Editor</title>
<style>
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
         background: #1a1a1a; color: #e0e0e0; height: 100vh; display: flex; flex-direction: column; }
  header { background: #111; padding: 14px 20px; display: flex; align-items: center; gap: 16px;
           border-bottom: 1px solid #333; }
  header h1 { font-size: 16px; font-weight: 600; color: #fff; }
  header span { font-size: 12px; color: #666; }
  .layout { display: flex; flex: 1; overflow: hidden; }

  /* Left: track library */
  .library { width: 55%; border-right: 1px solid #2a2a2a; display: flex; flex-direction: column; }
  .library-header { padding: 10px 16px; background: #161616; border-bottom: 1px solid #2a2a2a;
                    display: flex; align-items: center; gap: 10px; }
  .library-header input { flex: 1; background: #2a2a2a; border: none; border-radius: 6px;
                          padding: 6px 10px; color: #e0e0e0; font-size: 13px; outline: none; }
  .library-header input::placeholder { color: #555; }
  .track-list { flex: 1; overflow-y: auto; }
  .track { display: flex; align-items: center; padding: 8px 16px; border-bottom: 1px solid #222;
           cursor: pointer; gap: 10px; }
  .track:hover { background: #222; }
  .track.selected { background: #1d3557; }
  .track-check { width: 16px; height: 16px; border: 1.5px solid #444; border-radius: 4px;
                 flex-shrink: 0; display: flex; align-items: center; justify-content: center; }
  .track.selected .track-check { background: #3b82f6; border-color: #3b82f6; }
  .track.selected .track-check::after { content: "✓"; font-size: 11px; color: #fff; }
  .track-info { flex: 1; min-width: 0; }
  .track-title { font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .track-meta  { font-size: 11px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

  /* Right: playlists */
  .playlists { width: 45%; display: flex; flex-direction: column; }
  .pl-header { padding: 10px 16px; background: #161616; border-bottom: 1px solid #2a2a2a;
               display: flex; align-items: center; justify-content: space-between; }
  .pl-header span { font-size: 13px; font-weight: 500; }
  .btn { background: #3b82f6; color: #fff; border: none; border-radius: 6px;
         padding: 6px 12px; font-size: 12px; cursor: pointer; }
  .btn:hover { background: #2563eb; }
  .btn.danger { background: #dc2626; }
  .btn.danger:hover { background: #b91c1c; }
  .btn.ghost { background: transparent; border: 1px solid #444; color: #aaa; }
  .btn.ghost:hover { border-color: #3b82f6; color: #3b82f6; }
  .pl-list { flex: 1; overflow-y: auto; }
  .pl-item { padding: 10px 16px; border-bottom: 1px solid #222; cursor: pointer; }
  .pl-item:hover { background: #1e1e1e; }
  .pl-item.active { background: #1d3557; border-left: 3px solid #3b82f6; }
  .pl-name { font-size: 13px; font-weight: 500; }
  .pl-count { font-size: 11px; color: #666; margin-top: 2px; }
  .pl-actions { display: flex; gap: 6px; margin-top: 6px; }

  /* Editor panel */
  .editor { border-top: 1px solid #2a2a2a; padding: 12px 16px; background: #111; }
  .editor input { width: 100%; background: #222; border: 1px solid #333; border-radius: 6px;
                  padding: 7px 10px; color: #e0e0e0; font-size: 13px; outline: none; margin-bottom: 8px; }
  .editor input:focus { border-color: #3b82f6; }
  .editor-buttons { display: flex; gap: 8px; }
  .track-count { font-size: 12px; color: #666; flex: 1; display: flex; align-items: center; }

  .empty { display: flex; align-items: center; justify-content: center; height: 100px;
           color: #444; font-size: 13px; }
  ::-webkit-scrollbar { width: 6px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: #333; border-radius: 3px; }
</style>
</head>
<body>
<header>
  <h1>DMGPod Playlist Editor</h1>
  <span id="status">Loading…</span>
</header>
<div class="layout">
  <div class="library">
    <div class="library-header">
      <input type="text" id="search" placeholder="Search tracks…" oninput="filterTracks()">
    </div>
    <div class="track-list" id="track-list"></div>
  </div>
  <div class="playlists">
    <div class="pl-header">
      <span>Playlists</span>
      <button class="btn" onclick="newPlaylist()">+ New</button>
    </div>
    <div class="pl-list" id="pl-list"></div>
    <div class="editor" id="editor" style="display:none">
      <input type="text" id="pl-name" placeholder="Playlist name…">
      <div class="editor-buttons">
        <span class="track-count" id="track-count"></span>
        <button class="btn ghost" onclick="cancelEdit()">Cancel</button>
        <button class="btn" onclick="savePlaylist()">Save</button>
      </div>
    </div>
  </div>
</div>

<script>
let allTracks = [];
let playlists = [];
let editing = null;   // playlist being edited (or {} for new)
let selected = new Set();  // paths in current editing session

async function init() {
  const [t, p] = await Promise.all([
    fetch("/api/tracks").then(r => r.json()),
    fetch("/api/playlists").then(r => r.json()),
  ]);
  allTracks = t;
  playlists = p;
  setStatus(`${allTracks.length} tracks  ·  ${playlists.length} playlists`);
  renderTracks();
  renderPlaylists();
}

function setStatus(msg) {
  document.getElementById("status").textContent = msg;
}

function filterTracks() {
  renderTracks();
}

function renderTracks() {
  const q = document.getElementById("search").value.toLowerCase();
  const list = document.getElementById("track-list");
  const filtered = allTracks.filter(t =>
    !q || t.title.toLowerCase().includes(q) ||
          t.artist.toLowerCase().includes(q) ||
          t.album.toLowerCase().includes(q)
  );
  if (!filtered.length) {
    list.innerHTML = '<div class="empty">No tracks found</div>';
    return;
  }
  list.innerHTML = filtered.map(t => `
    <div class="track ${selected.has(t.path) ? "selected" : ""}"
         onclick="toggleTrack('${CSS.escape(t.path)}')" data-path="${t.path}">
      <div class="track-check"></div>
      <div class="track-info">
        <div class="track-title">${esc(t.title)}</div>
        <div class="track-meta">${esc(t.artist)} · ${esc(t.album)}</div>
      </div>
    </div>
  `).join("");
}

function toggleTrack(path) {
  if (!editing) return;
  const realPath = document.querySelector(`[data-path="${path}"]`).dataset.path;
  if (selected.has(realPath)) selected.delete(realPath);
  else selected.add(realPath);
  updateCount();
  renderTracks();
}

function updateCount() {
  document.getElementById("track-count").textContent =
    selected.size ? `${selected.size} track${selected.size !== 1 ? "s" : ""} selected` : "No tracks selected";
}

function renderPlaylists() {
  const list = document.getElementById("pl-list");
  if (!playlists.length) {
    list.innerHTML = '<div class="empty">No playlists yet</div>';
    return;
  }
  list.innerHTML = playlists.map((p, i) => `
    <div class="pl-item ${editing && editing._file === p._file ? "active" : ""}" onclick="editPlaylist(${i})">
      <div class="pl-name">${esc(p.name)}</div>
      <div class="pl-count">${(p.tracks||[]).length} track${(p.tracks||[]).length !== 1 ? "s" : ""}</div>
      <div class="pl-actions">
        <button class="btn ghost" onclick="event.stopPropagation();editPlaylist(${i})">Edit</button>
        <button class="btn danger" onclick="event.stopPropagation();deletePlaylist(${i})">Delete</button>
      </div>
    </div>
  `).join("");
}

function newPlaylist() {
  editing = {};
  selected = new Set();
  document.getElementById("pl-name").value = "";
  document.getElementById("editor").style.display = "block";
  document.getElementById("pl-name").focus();
  updateCount();
  renderTracks();
  renderPlaylists();
}

function editPlaylist(i) {
  editing = playlists[i];
  selected = new Set(editing.tracks || []);
  document.getElementById("pl-name").value = editing.name || "";
  document.getElementById("editor").style.display = "block";
  document.getElementById("pl-name").focus();
  updateCount();
  renderTracks();
  renderPlaylists();
}

function cancelEdit() {
  editing = null;
  selected = new Set();
  document.getElementById("editor").style.display = "none";
  renderTracks();
  renderPlaylists();
}

async function savePlaylist() {
  const name = document.getElementById("pl-name").value.trim();
  if (!name) { alert("Please enter a playlist name."); return; }
  if (!selected.size) { alert("Please select at least one track."); return; }
  const ordered = allTracks.filter(t => selected.has(t.path)).map(t => t.path);
  const payload = { ...editing, name, tracks: ordered };
  const res = await fetch("/api/playlists", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const saved = await res.json();
  const idx = playlists.findIndex(p => p._file === saved._file);
  if (idx >= 0) playlists[idx] = saved;
  else playlists.push(saved);
  cancelEdit();
  setStatus(`Saved "${name}"`);
  renderPlaylists();
}

async function deletePlaylist(i) {
  const p = playlists[i];
  if (!confirm(`Delete "${p.name}"?`)) return;
  await fetch("/api/playlists/" + encodeURIComponent(p._file), { method: "DELETE" });
  playlists.splice(i, 1);
  if (editing && editing._file === p._file) cancelEdit();
  setStatus(`Deleted "${p.name}"`);
  renderPlaylists();
}

function esc(s) {
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
}

init();
</script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass  # silence request logs

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def send_html(self, html):
        body = html.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/" or path == "/index.html":
            self.send_html(HTML)
        elif path == "/api/tracks":
            self.send_json(scan_tracks())
        elif path == "/api/playlists":
            self.send_json(load_playlists())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/playlists":
            length = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(length))
            fname = save_playlist(data)
            data["_file"] = fname
            self.send_json(data)
        else:
            self.send_response(404)
            self.end_headers()

    def do_DELETE(self):
        path = urlparse(self.path).path
        if path.startswith("/api/playlists/"):
            from urllib.parse import unquote
            fname = unquote(path[len("/api/playlists/"):])
            delete_playlist(fname)
            self.send_json({"ok": True})
        else:
            self.send_response(404)
            self.end_headers()


def main():
    server = HTTPServer(("localhost", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"DMGPod Playlist Editor running at {url}")
    print("Press Ctrl+C to stop.\n")
    webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()
