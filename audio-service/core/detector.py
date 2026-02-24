"""
Encapsulates the PyAudio logic to detect acoustic transients (pops/clicks).
"""
import os
import pyaudio
import numpy as np
import time
import logging
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
SENSITIVITY_MULTIPLIER = float(os.getenv("AUDIO_SENSITIVITY", 6.0))
COOLDOWN_SECONDS = float(os.getenv("AUDIO_COOLDOWN", 0.3))

class AcousticDetector:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.baseline_volume = 10.0
        self.last_click_time = 0.0
        
        try:
            self.stream = self.p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                                      input=True, frames_per_buffer=CHUNK)
            logging.info("Microphone initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to open microphone: {e}")
            raise SystemExit("CRITICAL: Microphone access required.")

    def process_chunk(self):
        """
        Reads a chunk of audio, updates the baseline, and checks for transients.
        Returns True if a valid 'pop' is detected.
        """
        try:
            data = self.stream.read(CHUNK, exception_on_overflow=False)
            audio_data = np.frombuffer(data, dtype=np.int16)
            
            # Calculate Root Mean Square (RMS) volume
            volume = np.sqrt(np.mean(np.square(audio_data.astype(np.float32)))) + 1e-6

            # Slowly adapt to room noise (Rolling Average)
            self.baseline_volume = (self.baseline_volume * 0.95) + (volume * 0.05)

            # Detect sharp spike
            if volume > (self.baseline_volume * SENSITIVITY_MULTIPLIER):
                current_time = time.time()
                if (current_time - self.last_click_time) > COOLDOWN_SECONDS:
                    self.last_click_time = current_time
                    logging.debug(f"Transient spike detected (Vol: {volume:.0f})")
                    return True
                    
        except Exception as e:
            logging.error(f"Error reading audio chunk: {e}")
            
        return False

    def close(self):
        """Cleans up the audio hardware locks."""
        if hasattr(self, 'stream'):
            self.stream.stop_stream()
            self.stream.close()
        self.p.terminate()