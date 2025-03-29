"""
Music Analysis Module for Artificial Dance Party Simulation
A simplified beat detector using pygame's audio capabilities
"""
import pygame
import numpy as np
import time
from typing import Dict, Any

class MusicAnalyzer:
    """Analyzes music to extract beat information for the dancers to respond to"""
    
    def __init__(self, music_file: str = None):
        """Initialize the music analyzer"""
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
        
        self.music_file = music_file
        self.beat_count = 0
        self.last_beat_time = 0
        self.beat_interval = 0.5  # Default: 120 BPM
        self.beat_pattern = [1.0, 0.5, 0.7, 0.5]  # Basic 4/4 pattern
        self.beat_position = 0
        self.is_playing = False
        self.start_time = 0
        
        # Fallback for when no music file is provided
        self.simulated_tempo = 120  # BPM
        self.simulated_start_time = 0
        
        # Load music if file provided
        if music_file:
            try:
                pygame.mixer.music.load(music_file)
                # Analyze BPM (simplified for demo)
                self.detect_tempo()
                print(f"Successfully loaded music file: {music_file}")
            except Exception as e:
                print(f"Could not load music file: {e}")
                self.music_file = None
                print("Using simulated beats instead.")
        else:
            print("No music file provided. Using simulated beats.")
    
    def detect_tempo(self):
        """
        Simple tempo detection based on onset strength
        Note: In a real implementation, you would use a library like librosa
        for proper beat detection. This is a simplified version.
        """
        # For demonstration, we're using a fixed tempo
        # In a real implementation, analyze the audio file
        self.simulated_tempo = 128  # Example fixed BPM
        self.beat_interval = 60 / self.simulated_tempo
        
        # Simple pattern for a 4/4 beat (stronger on 1, weaker on 3)
        self.beat_pattern = [1.0, 0.4, 0.7, 0.4]
    
    def play(self):
        """Start playing the music"""
        self.start_time = time.time()
        self.simulated_start_time = time.time()
        self.is_playing = True
        
        if self.music_file:
            pygame.mixer.music.play(-1)  # Loop indefinitely
        else:
            print("No music file loaded. Using simulated beats.")
    
    def stop(self):
        """Stop playing the music"""
        self.is_playing = False
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
    
    def get_current_time(self):
        """Get the current playback time in seconds"""
        if self.music_file:
            return pygame.mixer.music.get_pos() / 1000.0
        else:
            return time.time() - self.simulated_start_time
    
    def analyze_current_frame(self) -> Dict[str, Any]:
        """
        Analyze the current music frame and return beat information
        Returns a dictionary with beat information
        """

        if not self.music_file or not pygame.mixer.music.get_busy():
        # If no music is playing, use simulated beats
            return self.generate_beat_without_audio()

        current_time = time.time()
        elapsed_time = current_time - self.start_time
        
        # Calculate beat timing based on tempo
        beat_phase = (elapsed_time % self.beat_interval) / self.beat_interval
        is_on_beat = beat_phase < 0.1 or beat_phase > 0.9
        
        # Detect beats in pattern
        pattern_position = int((elapsed_time / self.beat_interval) % len(self.beat_pattern))
        beat_strength = self.beat_pattern[pattern_position]
        
        # Check if we've moved to a new beat
        beats_elapsed = elapsed_time / self.beat_interval
        current_beat = int(beats_elapsed)
        
        if current_beat > self.beat_count:
            self.beat_count = current_beat
            self.last_beat_time = current_time
            just_beat = True
        else:
            just_beat = False
        
        # For demonstration purposes, add some variation over time
        # In a real implementation, you would analyze the actual audio
        time_variation = 0.1 * np.sin(elapsed_time / 10)  # Slow variation
        energy_variation = 0.2 * np.sin(elapsed_time / 5)  # Energy variation
        
        # Detect breakdown/buildup sections (simplified)
        section_length = 32  # beats per section
        section_position = (current_beat % section_length) / section_length
        is_buildup = section_position > 0.75  # Last quarter is buildup
        is_breakdown = section_position < 0.25  # First quarter is breakdown
        
        # Create result dictionary
        result = {
            "beat_count": self.beat_count,
            "beat_strength": beat_strength + energy_variation,
            "is_on_beat": is_on_beat,
            "tempo": self.simulated_tempo + time_variation * 5,
            "phase": beat_phase,
            "pattern_position": pattern_position,
            "energy": 0.5 + energy_variation,
            "is_buildup": is_buildup,
            "is_breakdown": is_breakdown,
            "just_beat": just_beat,
            "time": elapsed_time
        }
        
        return result
    
    def generate_beat_without_audio(self) -> Dict[str, Any]:
        """Generate simulated beat information when no audio file is available"""
        current_time = time.time()
        elapsed_time = current_time - self.simulated_start_time
        
        # Calculate beat information from elapsed time and simulated tempo
        beats_elapsed = elapsed_time / (60 / self.simulated_tempo)
        current_beat = int(beats_elapsed)
        beat_phase = beats_elapsed - current_beat
        is_on_beat = beat_phase < 0.1 or beat_phase > 0.9
        
        # Use the beat pattern for strength
        pattern_position = current_beat % len(self.beat_pattern)
        beat_strength = self.beat_pattern[pattern_position]
        
        # Add some variation to make it interesting
        time_variation = 0.1 * np.sin(elapsed_time / 10)
        energy_variation = 0.2 * np.sin(elapsed_time / 5)
        
        # Create result dictionary
        result = {
            "beat_count": current_beat,
            "beat_strength": beat_strength + energy_variation,
            "is_on_beat": is_on_beat,
            "tempo": self.simulated_tempo + time_variation * 5,
            "phase": beat_phase,
            "pattern_position": pattern_position,
            "energy": 0.5 + energy_variation,
            "is_buildup": (current_beat % 32) > 24,  # Last 8 beats of 32
            "is_breakdown": (current_beat % 32) < 8,  # First 8 beats of 32
            "just_beat": current_beat > self.beat_count,
            "time": elapsed_time
        }
        
        # Update state
        if current_beat > self.beat_count:
            self.beat_count = current_beat
            self.last_beat_time = current_time
        
        return result