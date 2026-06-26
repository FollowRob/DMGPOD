import os
import soundfile as sf
import mutagen
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
from mutagen.mp4 import MP4

from src.library.models import Track

SUPPORTED = {".flac", ".mp3", ".wav", ".m4a", ".ogg"}


def _tag(tags, *keys, fallback=""):
    for k in keys:
        v = tags.get(k)
        if v:
            return str(v[0]) if isinstance(v, list) else str(v)
    return fallback


def _art_bytes(mfile):
    try:
        if isinstance(mfile, FLAC):
            if mfile.pictures:
                return mfile.pictures[0].data
        elif isinstance(mfile, MP3):
            for key in mfile.tags.keys():
                if key.startswith("APIC"):
                    return mfile.tags[key].data
        elif isinstance(mfile, MP4):
            covers = mfile.tags.get("covr")
            if covers:
                return bytes(covers[0])
    except Exception:
        pass
    return None


def _duration(path):
    try:
        info = sf.info(path)
        return info.duration
    except Exception:
        return 0.0


def scan(music_dir):
    tracks = []
    for fname in sorted(os.listdir(music_dir)):
        ext = os.path.splitext(fname)[1].lower()
        if ext not in SUPPORTED:
            continue
        path = os.path.join(music_dir, fname)
        try:
            mfile = mutagen.File(path)
        except Exception:
            mfile = None

        tags = mfile.tags if mfile and mfile.tags else {}

        title = _tag(tags,
            "title", "TIT2", "\xa9nam",
            fallback=os.path.splitext(fname)[0])
        artist = _tag(tags,
            "artist", "TPE1", "\xa9ART",
            fallback="Unknown Artist")
        album = _tag(tags,
            "album", "TALB", "\xa9alb",
            fallback="Unknown Album")

        tnum_raw = _tag(tags, "tracknumber", "TRCK", "trkn", fallback="0")
        try:
            track_num = int(str(tnum_raw).split("/")[0])
        except ValueError:
            track_num = 0

        art = _art_bytes(mfile) if mfile else None
        duration = _duration(path)

        tracks.append(Track(
            path=path,
            title=title,
            artist=artist,
            album=album,
            track_num=track_num,
            duration=duration,
            art_data=art,
        ))

    return tracks


def build_index(tracks):
    artists = {}
    albums = {}
    for t in tracks:
        artists.setdefault(t.artist, []).append(t)
        albums.setdefault(t.album, []).append(t)
    return artists, albums
