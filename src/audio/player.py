import threading
import numpy as np
import soundfile as sf
import sounddevice as sd


class Player:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = None
        self._samplerate = 44100
        self._pos = 0
        self._playing = False
        self._stopping = False   # suppresses finished_callback on manual stop
        self._stream = None
        self.on_track_end = None  # callback

    # ------------------------------------------------------------------
    def load(self, path):
        self.stop()
        data, sr = sf.read(path, dtype="float32", always_2d=True)
        with self._lock:
            self._data = data
            self._samplerate = sr
            self._pos = 0

    def play(self):
        if self._data is None:
            return
        self._playing = True
        self._stream = sd.OutputStream(
            samplerate=self._samplerate,
            channels=self._data.shape[1],
            dtype="float32",
            callback=self._callback,
            finished_callback=self._finished,
        )
        self._stream.start()

    def pause(self):
        self._stopping = True
        self._playing = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        self._stopping = False

    def resume(self):
        if self._data is None or self._playing:
            return
        self.play()

    def stop(self):
        self._stopping = True
        self._playing = False
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None
        with self._lock:
            self._pos = 0
        self._stopping = False

    def toggle(self):
        if self._playing:
            self.pause()
        else:
            self.resume()

    # ------------------------------------------------------------------
    @property
    def is_playing(self):
        return self._playing

    @property
    def position(self):
        with self._lock:
            if self._data is None or self._samplerate == 0:
                return 0.0
            return self._pos / self._samplerate

    @property
    def duration(self):
        with self._lock:
            if self._data is None or self._samplerate == 0:
                return 0.0
            return len(self._data) / self._samplerate

    @property
    def progress(self):
        d = self.duration
        return self.position / d if d > 0 else 0.0

    def seek(self, seconds):
        with self._lock:
            if self._data is not None:
                self._pos = max(0, min(int(seconds * self._samplerate), len(self._data) - 1))

    # ------------------------------------------------------------------
    def _callback(self, outdata, frames, time, status):
        with self._lock:
            if self._data is None or not self._playing:
                outdata[:] = 0
                return
            end = self._pos + frames
            chunk = self._data[self._pos:end]
            if len(chunk) < frames:
                outdata[:len(chunk)] = chunk
                outdata[len(chunk):] = 0
                self._playing = False
            else:
                outdata[:] = chunk
            self._pos = min(end, len(self._data))

    def _finished(self):
        self._playing = False
        if self.on_track_end and not self._stopping:
            self.on_track_end()
