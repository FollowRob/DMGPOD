from dataclasses import dataclass, field


@dataclass
class Track:
    path: str
    title: str
    artist: str
    album: str
    track_num: int
    duration: float       # seconds
    art_data: bytes = field(default=None, repr=False)  # raw image bytes or None
