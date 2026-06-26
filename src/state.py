from src.audio.player import Player

# Shared player + library
player = Player()
tracks = []       # list[Track]
artists = {}      # artist -> list[Track]
albums = {}       # album  -> list[Track]
queue = []        # current playback queue
queue_index = 0

# Cart state
cart_inserted = None   # None | "music" | "games"
cart_playlist_id = None  # 1-9 for music carts
games_unlocked = False
