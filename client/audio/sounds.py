"""
Sound effects system for chess game
Uses pygame for audio playback
"""

import os
import pygame
from typing import Optional

# Initialize pygame mixer
pygame.mixer.init()

class SoundManager:
    """Manages all game sounds"""
    
    def __init__(self):
        self.enabled = True
        self.volume = 0.5
        self.sounds = {}
        self._load_sounds()
    
    def _load_sounds(self):
        """Load all sound effects"""
        sound_dir = os.path.join(os.path.dirname(__file__), 'files')
        
        # Create sound files directory if it doesn't exist
        os.makedirs(sound_dir, exist_ok=True)
        
        # Define sound files (will be created programmatically)
        sound_files = {
            'move': 'move.wav',
            'capture': 'capture.wav',
            'check': 'check.wav',
            'castle': 'castle.wav',
            'game_start': 'game_start.wav',
            'game_end': 'game_end.wav',
            'notify': 'notify.wav',
            'illegal': 'illegal.wav'
        }
        
        # Load sounds
        for sound_name, filename in sound_files.items():
            filepath = os.path.join(sound_dir, filename)
            if os.path.exists(filepath):
                try:
                    self.sounds[sound_name] = pygame.mixer.Sound(filepath)
                    self.sounds[sound_name].set_volume(self.volume)
                except Exception as e:
                    print(f"Could not load sound {sound_name}: {e}")
            else:
                # Create simple beep sounds programmatically
                self.sounds[sound_name] = self._create_beep_sound(sound_name)
    
    def _create_beep_sound(self, sound_type: str) -> Optional[pygame.mixer.Sound]:
        """Create a simple programmatic beep sound"""
        try:
            import numpy as np
            
            sample_rate = 22050
            duration = 0.1  # 100ms
            
            # Different frequencies for different sounds
            frequencies = {
                'move': 440,      # A4
                'capture': 523,   # C5
                'check': 659,     # E5
                'castle': 349,    # F4
                'game_start': 523, # C5
                'game_end': 329,  # E4
                'notify': 587,    # D5
                'illegal': 220    # A3
            }
            
            freq = frequencies.get(sound_type, 440)
            
            # Generate sine wave
            samples = np.sin(2 * np.pi * freq * np.linspace(0, duration, int(sample_rate * duration)))
            
            # Apply envelope to avoid clicks
            envelope = np.linspace(1, 0, len(samples))
            samples = samples * envelope
            
            # Convert to 16-bit integers
            samples = (samples * 32767).astype(np.int16)
            
            # Create stereo sound
            stereo_samples = np.column_stack((samples, samples))
            
            # Create pygame sound
            sound = pygame.sndarray.make_sound(stereo_samples)
            sound.set_volume(self.volume)
            
            return sound
            
        except Exception as e:
            print(f"Could not create beep sound: {e}")
            return None
    
    def play(self, sound_name: str):
        """Play a sound effect"""
        if not self.enabled:
            return
        
        if sound_name in self.sounds and self.sounds[sound_name]:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Error playing sound {sound_name}: {e}")
    
    def set_volume(self, volume: float):
        """Set volume (0.0 to 1.0)"""
        self.volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.volume)
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
        return self.enabled
    
    def stop_all(self):
        """Stop all playing sounds"""
        pygame.mixer.stop()


# Global sound manager instance
_sound_manager = None

def get_sound_manager() -> SoundManager:
    """Get global sound manager instance"""
    global _sound_manager
    if _sound_manager is None:
        _sound_manager = SoundManager()
    return _sound_manager
