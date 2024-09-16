import numpy as np
import pyaudio
import pygame


class MicrophoneInput:
    def __init__(self):
        self.volume = 0
        self.is_above_threshold = False

        # PyAudio setup
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  channels=1,
                                  rate=44100,
                                  input=True,
                                  frames_per_buffer=1024)

    def update(self):
        data = np.frombuffer(self.stream.read(1024), dtype=np.int16)
        self.volume = np.abs(data).mean()

    def get_volume(self):
        return self.volume

    def cleanup(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
