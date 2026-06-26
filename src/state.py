from src.audio.player import Player

# Single shared instances — imported by any scene that needs them
player = Player()
tracks = []       # list[Track]
artists = {}      # artist -> list[Track]
albums = {}       # album  -> list[Track]
queue = []        # list[Track] — current playback queue
queue_index = 0   # position in queue
