"""
Artificial Dance Party Simulation - Main Entry Point (Enhanced)
"""
import pygame
import random
import sys
import time
import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
import colorsys
from pygame.locals import *

from dancer import Dancer, DancePersonality, CelebrityDancer
from music_analyzer import MusicAnalyzer
from social_dynamics import SocialDynamics
from social_network import SocialNetwork
from visualization import Visualization
from control_panel import ControlPanel

# Constants
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
BG_COLOR = (20, 20, 40)
NUM_INITIAL_DANCERS = 30
DEFAULT_MUSIC = None  # No default music file

def create_random_dancer(x_range, y_range, default_creativity=0.5, default_sociability=0.5):
    """Create a dancer with random properties"""
    personality = DancePersonality(
        extroversion=random.uniform(0.1, 0.9) * default_sociability * 2,
        rhythm_sensitivity=random.uniform(0.1, 0.9),
        creativity=random.uniform(0.1, 0.9) * default_creativity * 2,
        trendsetter=random.uniform(0.1, 0.9),
        energy=random.uniform(0.1, 0.9)
    )
    
    position = (
        random.randint(x_range[0], x_range[1]),
        random.randint(y_range[0], y_range[1])
    )
    
    # Generate color based on personality
    hue = (personality.creativity * 0.7 + personality.rhythm_sensitivity * 0.3) % 1.0
    saturation = 0.7 + personality.extroversion * 0.3
    value = 0.7 + personality.energy * 0.3
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
    color = (int(r * 255), int(g * 255), int(b * 255))
    
    return Dancer(personality=personality, position=position, color=color)

def create_celebrity_dancer(x_range, y_range):
    """Create a celebrity dancer"""
    position = (
        random.randint(x_range[0], x_range[1]),
        random.randint(y_range[0], y_range[1])
    )
    
    # Celebrities get a golden color
    color = (255, 215, 0)  # Gold
    
    return CelebrityDancer(position=position, color=color)

def apply_floor_mood(dancers, mood):
    """Apply a floor mood to all dancers"""
    for dancer in dancers:
        if mood == "Energetic":
            # Boost energy
            dancer.energy = min(1.0, dancer.energy + 0.3)
            dancer.personality.energy = min(1.0, dancer.personality.energy + 0.2)
        elif mood == "Relaxed":
            # Lower energy, increase rhythm sensitivity
            dancer.energy = max(0.1, dancer.energy - 0.2)
            dancer.personality.energy = max(0.2, dancer.personality.energy - 0.1)
            dancer.personality.rhythm_sensitivity = min(1.0, dancer.personality.rhythm_sensitivity + 0.1)
        elif mood == "Experimental":
            # Boost creativity
            dancer.personality.creativity = min(1.0, dancer.personality.creativity + 0.2)

def select_music_file():
    """Open a file dialog to select a music file"""
    # Initialize tkinter without creating a visible window
    root = tk.Tk()
    root.withdraw()
    
    # Open file dialog
    file_path = filedialog.askopenfilename(
        title="Select Music File",
        filetypes=[
            ("Audio Files", "*.wav;*.mp3;*.ogg"),
            ("WAV Files", "*.wav"),
            ("MP3 Files", "*.mp3"),
            ("OGG Files", "*.ogg"),
            ("All Files", "*.*")
        ]
    )
    
    # Destroy the tkinter instance
    root.destroy()
    
    return file_path if file_path else None

def main():
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Artificial Dance Party Simulation")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    
    # Ask user if they want to select a music file
    print("Do you want to select a music file? (y/n)")
    user_input = input().lower()
    
    music_file = None
    if user_input.startswith('y'):
        music_file = select_music_file()
        if music_file:
            print(f"Using music file: {music_file}")
        else:
            print("No music file selected. Using simulated beats.")
    
    # Initialize components
    music = MusicAnalyzer(music_file)
    social = SocialDynamics()
    social_network = SocialNetwork()
    viz = Visualization(screen)
    
    # Create control panel
    panel_width = 200
    control_panel = ControlPanel(screen, (SCREEN_WIDTH - panel_width, 0), (panel_width, SCREEN_HEIGHT))
    
    # Global variables for settings
    global default_creativity, default_sociability, dancers, floor_size_factor
    default_creativity = 0.5
    default_sociability = 0.5
    floor_size_factor = 1.0
    
    # For reset functionality
    def reset_simulation():
        global dancers
        dancers = []
        for i in range(NUM_INITIAL_DANCERS):
            dancers.append(create_random_dancer((50, SCREEN_WIDTH-50), (50, SCREEN_HEIGHT-50)))
        social.dance_groups = []
        social.conga_lines = []
        social_network.relationships = {}
        social_network.dance_crews = []
        social_network.dancer_to_crew = {}
    
    # For changing music
    def change_music():
        new_music_file = select_music_file()
        if new_music_file:
            nonlocal music
            music.stop()
            music = MusicAnalyzer(new_music_file)
            music.play()
    
    # For adjusting floor size
    def update_floor_size(value):
        """Update the dance floor size"""
        global floor_size_factor
        floor_size_factor = value
        viz.set_floor_size(value)
        
        # Calculate new boundaries
        dancing_area_width = int(SCREEN_WIDTH * value)
        dancing_area_height = int(SCREEN_HEIGHT * value)
        offset_x = (SCREEN_WIDTH - dancing_area_width) // 2
        offset_y = (SCREEN_HEIGHT - dancing_area_height) // 2
        
        # Move dancers that are outside the new boundaries
        for dancer in dancers:
            if dancer.position[0] < offset_x:
                dancer.position = (offset_x + 10, dancer.position[1])
            elif dancer.position[0] > offset_x + dancing_area_width:
                dancer.position = (offset_x + dancing_area_width - 10, dancer.position[1])
                
            if dancer.position[1] < offset_y:
                dancer.position = (dancer.position[0], offset_y + 10)
            elif dancer.position[1] > offset_y + dancing_area_height:
                dancer.position = (dancer.position[0], offset_y + dancing_area_height - 10)

    # For group formation threshold
    def update_group_threshold(value):
        """Update the group formation threshold"""
        social.group_formation_factor = value
    
    # Create initial dancers
    dancers = []
    for i in range(NUM_INITIAL_DANCERS):
        dancers.append(create_random_dancer((50, SCREEN_WIDTH-50), (50, SCREEN_HEIGHT-50)))
    
    # Register control panel callbacks
    control_panel.register_callback("tempo_slider", lambda value: setattr(music, "simulated_tempo", value))
    control_panel.register_callback("creativity_slider", lambda value: globals().update({"default_creativity": value}))
    control_panel.register_callback("social_slider", lambda value: globals().update({"default_sociability": value}))
    control_panel.register_callback("floor_size_slider", update_floor_size)
    control_panel.register_callback("group_threshold_slider", update_group_threshold)
    control_panel.register_callback("mood_dropdown", lambda value: apply_floor_mood(dancers, value))
    control_panel.register_callback("theme_dropdown", lambda value: viz.set_theme(value))
    control_panel.register_callback("zoom_in_button", lambda: viz.zoom_in())
    control_panel.register_callback("zoom_out_button", lambda: viz.zoom_out())
    control_panel.register_callback("focus_button", lambda: viz.focus_on_random_dancer(dancers))
    control_panel.register_callback("reset_cam_button", lambda: viz.reset_camera())
    control_panel.register_callback("celebrity_button", lambda: dancers.append(create_celebrity_dancer((50, SCREEN_WIDTH-50), (50, SCREEN_HEIGHT-50))))
    control_panel.register_callback("music_button", change_music)
    control_panel.register_callback("reset_button", reset_simulation)
    
    # Start music
    music.play()
    
    # Main game loop
    running = True
    last_time = time.time()
    while running:
        # Calculate delta time
        current_time = time.time()
        delta_time = current_time - last_time
        last_time = current_time
        
        # Process events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                elif event.key == K_SPACE:
                    # Add a new dancer on spacebar
                    dancers.append(create_random_dancer(
                        (50, SCREEN_WIDTH-50), 
                        (50, SCREEN_HEIGHT-50),
                        default_creativity,
                        default_sociability
                    ))
                elif event.key == K_r:
                    # Randomize all dancer positions on 'r' key
                    for dancer in dancers:
                        dancer.position = (
                            random.randint(50, SCREEN_WIDTH-50),
                            random.randint(50, SCREEN_HEIGHT-50)
                        )
                elif event.key == K_c:
                    # Toggle control panel
                    control_panel.toggle_visibility()
                elif event.key == K_m:
                    # Change music
                    change_music()
            
            # Process UI events
            control_panel.process_events(event)
        
        # Get current music features
        beat_info = music.analyze_current_frame()
        
        # Update social dynamics
        social.update(dancers, beat_info)
        
        # Update social network
        social_network.update(dancers, delta_time)
        
        # Update dancers
        for dancer in dancers:
            dancer.update(dancers, beat_info, social, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Update UI
        control_panel.update(delta_time)
        
        # Draw everything
        viz.draw(dancers, beat_info, social, social_network)
        control_panel.draw()
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()