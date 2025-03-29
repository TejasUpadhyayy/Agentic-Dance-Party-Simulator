"""
Visualization Module for Artificial Dance Party Simulation
Handles rendering dancers, effects, and UI elements
"""
import pygame
import math
import random
import colorsys
from typing import List, Dict, Any, Tuple

class Visualization:
    """Handles all visualization for the dance party simulation"""
    
    # Color theme definitions
    COLOR_THEMES = {
        "Default": {
            "background": (20, 20, 40),
            "grid": (40, 40, 80),
            "pulse": (220, 220, 255),
            "energy_zone": (200, 100, 255),
            "ui_text": (255, 255, 255),
            "ui_background": (0, 0, 0, 150)
        },
        "Neon": {
            "background": (0, 0, 0),
            "grid": (0, 80, 80),
            "pulse": (0, 255, 255),
            "energy_zone": (255, 0, 255),
            "ui_text": (0, 255, 0),
            "ui_background": (20, 0, 20, 150)
        },
        "Pastel": {
            "background": (230, 230, 250),
            "grid": (180, 180, 220),
            "pulse": (255, 182, 193),
            "energy_zone": (173, 216, 230),
            "ui_text": (148, 0, 211),
            "ui_background": (230, 230, 250, 150)
        },
        "Monochrome": {
            "background": (0, 0, 0),
            "grid": (50, 50, 50),
            "pulse": (150, 150, 150),
            "energy_zone": (200, 200, 200),
            "ui_text": (255, 255, 255),
            "ui_background": (50, 50, 50, 150)
        }
    }
    
    def __init__(self, screen):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.font = pygame.font.SysFont('Arial', 14)
        self.title_font = pygame.font.SysFont('Arial', 24)
        
        # Trail effects
        self.trails = {}  # dancer id -> list of positions
        self.trail_length = 15
        
        # Beat visualization
        self.beat_pulse = 0
        self.beat_color = (255, 255, 255)
        
        # Dance move display
        self.show_dance_moves = True
        self.show_stats = True
        
        # Theme and camera settings
        self.current_theme = "Default"
        self.camera_zoom = 1.0
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.focused_dancer = None
        
        # Dance floor sizing
        self.floor_size_factor = 1.0
    
    def set_theme(self, theme_name):
        """Set the color theme"""
        if theme_name in self.COLOR_THEMES:
            self.current_theme = theme_name
    
    def zoom_in(self):
        """Zoom in the camera view"""
        self.camera_zoom = min(2.5, self.camera_zoom + 0.1)
    
    def zoom_out(self):
        """Zoom out the camera view"""
        self.camera_zoom = max(0.5, self.camera_zoom - 0.1)
    
    def reset_camera(self):
        """Reset camera to default view"""
        self.camera_zoom = 1.0
        self.camera_offset_x = 0
        self.camera_offset_y = 0
        self.focused_dancer = None
    
    def focus_on_random_dancer(self, dancers):
        """Focus the camera on a random dancer"""
        if dancers:
            self.focused_dancer = random.choice(dancers)
    
    def set_floor_size(self, size_factor):
        """Set the dance floor size factor"""
        self.floor_size_factor = size_factor
    
    def get_dance_floor_area(self):
        """Get the current dance floor area"""
        dancing_area_width = int(self.width * self.floor_size_factor)
        dancing_area_height = int(self.height * self.floor_size_factor)
        offset_x = (self.width - dancing_area_width) // 2
        offset_y = (self.height - dancing_area_height) // 2
        
        return (offset_x, offset_y, dancing_area_width, dancing_area_height)
    
    def generate_dancer_color(self, personality):
        """Generate a color based on dancer personality"""
        # Use HSV color space for more vibrant colors
        # Hue based on dancer creativity and rhythm
        hue = (personality.creativity * 0.7 + personality.rhythm_sensitivity * 0.3) % 1.0
        
        # Saturation based on extroversion (more extroverted = more vibrant)
        saturation = 0.7 + personality.extroversion * 0.3
        
        # Value (brightness) based on energy
        value = 0.7 + personality.energy * 0.3
        
        # Convert to RGB
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)
        return (int(r * 255), int(g * 255), int(b * 255))
    
    def update_beat_visualization(self, beat_info):
        """Update visual elements that respond to the beat"""
        # Create a pulse effect on beats
        if beat_info.get("just_beat", False):
            self.beat_pulse = 1.0
            
            # Change color based on beat pattern
            pattern_pos = beat_info.get("pattern_position", 0)
            theme = self.COLOR_THEMES[self.current_theme]
            
            if pattern_pos == 0:  # Downbeat
                # Use theme-appropriate pulse colors
                if self.current_theme == "Monochrome":
                    self.beat_color = (200, 200, 200)
                else:
                    # Add a slight red tint to the pulse color
                    pulse_color = theme["pulse"]
                    r = min(255, pulse_color[0] + 35)
                    g = max(0, pulse_color[1] - 35)
                    b = max(0, pulse_color[2] - 35)
                    self.beat_color = (r, g, b)
            else:
                self.beat_color = theme["pulse"]
        else:
            # Decay the pulse
            self.beat_pulse *= 0.9
    
    def update_trails(self, dancers):
        """Update position trails for each dancer"""
        for dancer in dancers:
            # Create new entry if needed
            if id(dancer) not in self.trails:
                self.trails[id(dancer)] = []
            
            # Add current position
            trail = self.trails[id(dancer)]
            trail.append(dancer.position)
            
            # Limit trail length
            if len(trail) > self.trail_length:
                del trail[0]
            
            # Remove trails for dancers that no longer exist
            dancer_ids = [id(d) for d in dancers]
            for trail_id in list(self.trails.keys()):
                if trail_id not in dancer_ids:
                    del self.trails[trail_id]
    
    def apply_camera_transform(self, x, y):
        """Apply camera transformation to coordinates"""
        # Center the view on the focused dancer if needed
        cam_x, cam_y = self.camera_offset_x, self.camera_offset_y
        
        # Apply zoom
        transformed_x = (x - self.width/2) * self.camera_zoom + self.width/2 + cam_x
        transformed_y = (y - self.height/2) * self.camera_zoom + self.height/2 + cam_y
        
        return transformed_x, transformed_y
    
    def draw_background(self, beat_info):
        """Draw the dance floor background with beat-reactive elements"""
        theme = self.COLOR_THEMES[self.current_theme]
        
        # Base background
        bg_color = theme["background"]
        self.screen.fill(bg_color)
        
        # Beat-reactive elements
        if self.beat_pulse > 0.05:
            # Draw a subtle pulse expanding from center
            pulse_radius = (1.0 - self.beat_pulse) * self.width * 0.8
            pulse_width = int(5 + self.beat_pulse * 10)
            
            pulse_color = self.beat_color
            pulse_alpha = int(self.beat_pulse * 40)
            
            # Create a surface with per-pixel alpha
            pulse_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # Draw the pulse circle with alpha
            pygame.draw.circle(
                pulse_surface,
                (*pulse_color, pulse_alpha),
                (self.width // 2, self.height // 2),
                pulse_radius,
                pulse_width
            )
            
            # Blit to main screen
            self.screen.blit(pulse_surface, (0, 0))
        
        # Draw a subtle grid on the floor
        grid_color = theme["grid"]
        grid_spacing = 50
        
        # Dance floor boundary
        offset_x, offset_y, dancing_area_width, dancing_area_height = self.get_dance_floor_area()
        
        # Draw grid lines
        for x in range(offset_x, offset_x + dancing_area_width, grid_spacing):
            x_pos, _ = self.apply_camera_transform(x, 0)
            pygame.draw.line(self.screen, grid_color, 
                            (x_pos, offset_y), 
                            (x_pos, offset_y + dancing_area_height))
        
        for y in range(offset_y, offset_y + dancing_area_height, grid_spacing):
            _, y_pos = self.apply_camera_transform(0, y)
            pygame.draw.line(self.screen, grid_color, 
                            (offset_x, y_pos), 
                            (offset_x + dancing_area_width, y_pos))
        
        # Draw a border around the dance area
        if self.floor_size_factor != 1.0:
            border_rect = pygame.Rect(offset_x, offset_y, dancing_area_width, dancing_area_height)
            border_color = grid_color
            pygame.draw.rect(self.screen, border_color, border_rect, 2)
    
    def draw_music_reactive_floor(self, beat_info):
        """Draw a floor that reacts to the music"""
        # Base background already drawn in draw_background
        theme = self.COLOR_THEMES[self.current_theme]
        
        # Create a surface for the reactive floor elements
        floor_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Get current music info
        beat_strength = beat_info.get("beat_strength", 0.5)
        energy = beat_info.get("energy", 0.5)
        is_buildup = beat_info.get("is_buildup", False)
        is_breakdown = beat_info.get("is_breakdown", False)
        phase = beat_info.get("phase", 0)
        tempo = beat_info.get("tempo", 120)
        
        # Get dance floor area
        offset_x, offset_y, dancing_area_width, dancing_area_height = self.get_dance_floor_area()
        
        # Floor grid that pulses with the beat
        grid_base = theme["grid"]
        grid_color = (
            grid_base[0] + int(20 * beat_strength), 
            grid_base[1] + int(20 * beat_strength),
            grid_base[2] + int(40 * beat_strength)
        )
        grid_spacing = int(50 - 10 * beat_strength)
        
        # Draw grid lines with varying intensity
        for x in range(offset_x, offset_x + dancing_area_width, grid_spacing):
            intensity = 0.5 + 0.5 * math.sin(x / 100 + beat_info.get("time", 0))
            line_color = (
                int(grid_color[0] * intensity),
                int(grid_color[1] * intensity),
                int(grid_color[2] * intensity),
                100
            )
            
            x_pos, _ = self.apply_camera_transform(x, 0)
            pygame.draw.line(floor_surface, line_color, 
                           (x_pos, offset_y), 
                           (x_pos, offset_y + dancing_area_height))
        
        for y in range(offset_y, offset_y + dancing_area_height, grid_spacing):
            intensity = 0.5 + 0.5 * math.sin(y / 100 + beat_info.get("time", 0))
            line_color = (
                int(grid_color[0] * intensity),
                int(grid_color[1] * intensity),
                int(grid_color[2] * intensity),
                100
            )
            
            _, y_pos = self.apply_camera_transform(0, y)
            pygame.draw.line(floor_surface, line_color, 
                           (offset_x, y_pos), 
                           (offset_x + dancing_area_width, y_pos))
        
        # Energy zones during high energy sections
        if energy > 0.7 or is_buildup:
            # Create 1-3 energy zones
            zone_count = random.randint(1, 3)
            
            for _ in range(zone_count):
                # Random position within dance floor boundaries
                x = random.randint(offset_x + 100, offset_x + dancing_area_width - 100)
                y = random.randint(offset_y + 100, offset_y + dancing_area_height - 100)
                
                # Size based on energy
                radius = int(30 + 40 * energy)
                
                # Color with alpha
                energy_base = theme["energy_zone"]
                zone_color = (*energy_base, int(50 + 40 * energy))
                
                # Apply camera transform
                x_pos, y_pos = self.apply_camera_transform(x, y)
                
                # Draw the zone
                pygame.draw.circle(floor_surface, zone_color, (int(x_pos), int(y_pos)), radius)
                
                # Inner highlight
                inner_radius = int(radius * 0.7)
                # Lighter version of energy zone color
                r, g, b = energy_base
                inner_color = (min(255, r + 20), min(255, g + 60), min(255, b + 60), int(30 + 20 * energy))
                pygame.draw.circle(floor_surface, inner_color, (int(x_pos), int(y_pos)), inner_radius)
        
        # Special effects during breakdown
        if is_breakdown:
            # Radial pattern emanating from center
            center_x = offset_x + dancing_area_width // 2
            center_y = offset_y + dancing_area_height // 2
            max_radius = math.sqrt(dancing_area_width**2 + dancing_area_height**2) / 2
            
            # Transform center
            center_x, center_y = self.apply_camera_transform(center_x, center_y)
            
            # Draw multiple rings
            ring_count = int(5 + 5 * energy)
            for i in range(ring_count):
                # Calculate ring properties
                progress = i / ring_count
                ring_phase = (phase + progress) % 1.0
                radius = ring_phase * max_radius
                
                # Ring color with alpha
                alpha = int(150 * (1 - ring_phase))
                pulse_base = theme["pulse"]
                ring_color = (*pulse_base, alpha)
                
                # Draw the ring
                pygame.draw.circle(
                    floor_surface, 
                    ring_color, 
                    (int(center_x), int(center_y)), 
                    int(radius),
                    max(1, int(3 * (1 - ring_phase)))
                )
        
        # Blit the floor surface to the main screen
        self.screen.blit(floor_surface, (0, 0))
    
    def draw_audio_waveform(self, beat_info):
        """Draw audio waveform/spectrum visualization at the bottom of the screen"""
        theme = self.COLOR_THEMES[self.current_theme]
        
        # Create a surface for the waveform
        waveform_height = 60
        waveform_rect = pygame.Rect(0, self.height - waveform_height, self.width, waveform_height)
        waveform_surface = pygame.Surface((waveform_rect.width, waveform_rect.height), pygame.SRCALPHA)
        
        # Fill with semi-transparent background
        bg_color = theme["ui_background"]
        if len(bg_color) == 3:
            bg_color = (*bg_color, 150)  # Add alpha if needed
        waveform_surface.fill(bg_color)
        
        # Get current time for animation
        time = beat_info.get("time", 0)
        energy = beat_info.get("energy", 0.5)
        beat_phase = beat_info.get("phase", 0)
        
        # Generate a simple waveform visualization
        # In a real implementation, you would analyze the actual audio spectrum
        bar_count = 64
        bar_width = waveform_rect.width // bar_count
        
        for i in range(bar_count):
            # Calculate bar height based on simulated spectrum
            # This creates a wave pattern that responds to the beat
            normalized_pos = i / bar_count
            
            # Multiple frequencies combined
            height_factor = (
                0.4 * math.sin(normalized_pos * 10 + time * 2) +
                0.3 * math.sin(normalized_pos * 20 + time * 3) +
                0.2 * math.sin(normalized_pos * 5 - time) +
                0.1 * math.cos(normalized_pos * 15 + time * 5)
            )
            
            # Apply beat emphasis
            if beat_phase < 0.2:
                beat_emphasis = 1.0 - beat_phase * 5  # Strongest right on the beat
            else:
                beat_emphasis = 0.0
            
            height_factor += beat_emphasis * 0.3
            
            # Clamp and scale
            height_factor = max(0.1, min(1.0, height_factor)) * energy
            bar_height = int(height_factor * (waveform_rect.height - 10))
            
            # Calculate color based on frequency (position) and energy
            if self.current_theme == "Monochrome":
                # Grayscale for monochrome theme
                value = int(100 + 155 * height_factor)
                color = (value, value, value)
            else:
                # Use HSV color space for other themes
                hue = (normalized_pos * 240) % 360  # Blue to red spectrum
                saturation = int(50 + 50 * energy)
                value = int(70 + 30 * height_factor)
                
                # Convert HSV to RGB
                r, g, b = colorsys.hsv_to_rgb(hue/360, saturation/100, value/100)
                color = (int(r * 255), int(g * 255), int(b * 255))
            
            # Draw the bar
            bar_x = i * bar_width
            bar_rect = pygame.Rect(
                bar_x, 
                waveform_rect.height - bar_height - 5,  # 5px padding
                bar_width - 1, 
                bar_height
            )
            pygame.draw.rect(waveform_surface, color, bar_rect)
        
        # Blit the waveform surface to the main screen
        self.screen.blit(waveform_surface, waveform_rect)
    
    def draw_dance_groups(self, social_dynamics):
        """Draw visualization for dance groups"""
        theme = self.COLOR_THEMES[self.current_theme]
        
        # Get dance floor area
        offset_x, offset_y, dancing_area_width, dancing_area_height = self.get_dance_floor_area()
        
        for group in social_dynamics.dance_groups:
            # Draw group area
            color = (*theme["grid"], 30)  # Semi-transparent
            
            # Create a surface with per-pixel alpha
            group_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            
            # Apply camera transform
            x, y = self.apply_camera_transform(group.center[0], group.center[1])
            
            # Draw the group circle with alpha
            pygame.draw.circle(
                group_surface,
                color,
                (int(x), int(y)),
                int(group.radius * self.camera_zoom)  # Scale radius with zoom
            )
            
            # Blit to main screen
            self.screen.blit(group_surface, (0, 0))
    
    def draw_conga_lines(self, social_dynamics):
        """Draw connections for conga lines"""
        for line in social_dynamics.conga_lines:
            if not line.followers:
                continue
            
            # Draw line from leader to first follower
            if line.followers:
                start_x, start_y = self.apply_camera_transform(*line.leader.position)
                end_x, end_y = self.apply_camera_transform(*line.followers[0].position)
                
                pygame.draw.line(
                    self.screen, 
                    (200, 200, 50), 
                    (start_x, start_y), 
                    (end_x, end_y), 
                    2
                )
            
            # Draw lines between followers
            for i in range(len(line.followers) - 1):
                start_x, start_y = self.apply_camera_transform(*line.followers[i].position)
                end_x, end_y = self.apply_camera_transform(*line.followers[i + 1].position)
                
                pygame.draw.line(
                    self.screen, 
                    (200, 200, 50), 
                    (start_x, start_y), 
                    (end_x, end_y), 
                    2
                )
    
    def draw_relationships(self, dancers, social_network):
        """Draw relationship lines between dancers"""
        # Get visible relationships
        visible_relationships = social_network.get_visible_relationships()
        
        # Create a surface for relationships
        rel_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Draw each relationship
        for dancer1_id, dancer2_id, relationship in visible_relationships:
            # Find the actual dancer objects
            dancer1 = None
            dancer2 = None
            
            for dancer in dancers:
                if id(dancer) == dancer1_id:
                    dancer1 = dancer
                elif id(dancer) == dancer2_id:
                    dancer2 = dancer
            
            # If both dancers exist, draw the relationship
            if dancer1 and dancer2:
                # Get positions with camera transform
                pos1_x, pos1_y = self.apply_camera_transform(*dancer1.position)
                pos2_x, pos2_y = self.apply_camera_transform(*dancer2.position)
                
                # Get relationship color
                color = relationship.get_color()
                
                # Draw the line with appropriate width based on strength
                width = int(1 + 2 * relationship.strength)
                pygame.draw.line(rel_surface, color, (pos1_x, pos1_y), (pos2_x, pos2_y), width)
                
                # For very strong relationships, add a glow effect
                if relationship.strength > 0.7:
                    # Draw a wider, more transparent line underneath
                    glow_color = (color[0], color[1], color[2], int(color[3] * 0.5))
                    pygame.draw.line(rel_surface, glow_color, (pos1_x, pos1_y), (pos2_x, pos2_y), width + 2)
        
        # Blit the relationship surface to the main screen
        self.screen.blit(rel_surface, (0, 0))
    
    def draw_dancer(self, dancer, beat_info):
        """Draw a single dancer with their current state"""
        # Draw position trail
        if id(dancer) in self.trails:
            trail = self.trails[id(dancer)]
            if len(trail) > 1:
                for i in range(len(trail) - 1):
                    start = trail[i]
                    end = trail[i + 1]
                    
                    # Fade alpha based on position in trail
                    alpha = int(255 * (i / len(trail)))
                    
                    # Adjust color based on dancer's color
                    r, g, b = dancer.color
                    trail_color = (r//2, g//2, b//2, alpha)
                    
                    # Apply camera transform
                    start_x, start_y = self.apply_camera_transform(*start)
                    end_x, end_y = self.apply_camera_transform(*end)
                    
                    # Draw trail segment
                    if i > 0:  # Skip the oldest segment
                        # Create a surface with per-pixel alpha
                        trail_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
                        pygame.draw.line(trail_surface, trail_color, (start_x, start_y), (end_x, end_y), 2)
                        self.screen.blit(trail_surface, (0, 0))
        
        # Draw dancer
        x, y = dancer.position
        
        # Apply camera transform
        x, y = self.apply_camera_transform(x, y)
        
        # Base radius and adjustments for beat and energy
        base_radius = 10
        beat_boost = 0
        
        # Pulse on beat if dancer is rhythm sensitive
        if beat_info.get("just_beat", False) and random.random() < dancer.personality.rhythm_sensitivity:
            beat_boost = 3
        
        # Energy affects size slightly
        energy_factor = 0.8 + 0.4 * dancer.energy
        
        # Scale radius with camera zoom
        radius = (base_radius + beat_boost) * energy_factor * self.camera_zoom
        
        # Draw dancer body
        pygame.draw.circle(self.screen, dancer.color, (int(x), int(y)), int(radius))
        
        # Draw dancer outline - use slightly different color based on theme
        outline_color = (255, 255, 255)  # Default white outline
        if self.current_theme == "Neon":
            outline_color = (0, 255, 255)  # Cyan for neon
        elif self.current_theme == "Pastel":
            outline_color = (230, 230, 250)  # Light lavender for pastel
        
        pygame.draw.circle(self.screen, outline_color, (int(x), int(y)), int(radius), 1)
        
        # Show dance move name if enabled
        if self.show_dance_moves:
            # Use theme-specific text color
            text_color = self.COLOR_THEMES[self.current_theme]["ui_text"]
            
            move_text = self.font.render(dancer.current_move.name, True, text_color)
            text_rect = move_text.get_rect(center=(int(x), int(y) - 20 * self.camera_zoom))
            self.screen.blit(move_text, text_rect)
        
        # Highlight focused dancer
        if dancer == self.focused_dancer:
            highlight_radius = radius + 4
            pygame.draw.circle(self.screen, (255, 215, 0), (int(x), int(y)), int(highlight_radius), 2)
        
        # Visualize movement for current dance move
        self.visualize_dance_move(dancer, beat_info, x, y)
    
    def visualize_dance_move(self, dancer, beat_info, x, y):
        """Add visual effects based on dancer's current move"""
        move = dancer.current_move
        theme = self.COLOR_THEMES[self.current_theme]
        
        # Create a surface with per-pixel alpha
        effect_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Different effects based on move complexity and energy
        if move.complexity > 0.7:  # Complex moves
            # Spinning effect
            spin_radius = (15 + 5 * dancer.energy) * self.camera_zoom
            angle = beat_info.get("time", 0) * 5 + hash(move.name) % 360
            
            for i in range(3):
                point_angle = angle + i * 120
                px = x + math.cos(math.radians(point_angle)) * spin_radius
                py = y + math.sin(math.radians(point_angle)) * spin_radius
                
                pygame.draw.circle(
                    effect_surface,
                    (*dancer.color, 100),
                    (int(px), int(py)),
                    int(3 * self.camera_zoom)
                )
        
        elif move.energy_required > 0.7:  # High energy moves
            # Burst effect
            if random.random() < 0.2:
                burst_count = random.randint(3, 6)
                burst_range = 20 * self.camera_zoom
                
                for _ in range(burst_count):
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(5, burst_range)
                    px = x + math.cos(angle) * distance
                    py = y + math.sin(angle) * distance
                    
                    pygame.draw.circle(
                        effect_surface,
                        (*dancer.color, 100),
                        (int(px), int(py)),
                        int(2 * self.camera_zoom)
                    )
        
        elif "Wave" in move.name or move.name.startswith("Smooth"):
            # Wave effect
            wave_points = 8
            wave_radius = 12 * self.camera_zoom
            base_angle = beat_info.get("time", 0) * 3
            
            for i in range(wave_points):
                angle = base_angle + i * (360 / wave_points)
                offset = math.sin(math.radians(angle * 2)) * 3 * self.camera_zoom
                
                px = x + math.cos(math.radians(angle)) * (wave_radius + offset)
                py = y + math.sin(math.radians(angle)) * (wave_radius + offset)
                
                pygame.draw.circle(
                    effect_surface,
                    (*dancer.color, 100),
                    (int(px), int(py)),
                    int(2 * self.camera_zoom)
                )
        
        # Blit effect to main screen
        self.screen.blit(effect_surface, (0, 0))
    
    def draw_stats(self, dancers, social_dynamics, beat_info):
        """Draw statistics and trend information"""
        if not self.show_stats:
            return
        
        theme = self.COLOR_THEMES[self.current_theme]
        text_color = theme["ui_text"]
        bg_color = theme["ui_background"]
        
        # Background panel
        panel_rect = pygame.Rect(10, 10, 200, 120)
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel_surface.fill(bg_color)
        self.screen.blit(panel_surface, panel_rect)
        
        # Title
        title_text = self.title_font.render("Dance Stats", True, text_color)
        self.screen.blit(title_text, (20, 15))
        
        # Stats
        y_pos = 50
        stats = [
            f"Dancers: {len(dancers)}",
            f"Groups: {len(social_dynamics.dance_groups)}",
            f"Conga Lines: {len(social_dynamics.conga_lines)}",
            f"Unique Moves: {len(social_dynamics.dance_trends)}",
            f"BPM: {int(beat_info.get('tempo', 120))}"
        ]
        
        for stat in stats:
            stat_text = self.font.render(stat, True, text_color)
            self.screen.blit(stat_text, (20, y_pos))
            y_pos += 20
        
        # Top trends
        trend_data = social_dynamics.get_trend_data()
        top_trends = trend_data["current"][:3]  # Top 3 trends
        
        if top_trends:
            # Trending panel
            trend_rect = pygame.Rect(self.width - 210, 10, 200, 100)
            trend_surface = pygame.Surface((trend_rect.width, trend_rect.height), pygame.SRCALPHA)
            trend_surface.fill(bg_color)
            self.screen.blit(trend_surface, trend_rect)
            
            # Title
            trend_title = self.title_font.render("Trending Moves", True, text_color)
            self.screen.blit(trend_title, (self.width - 200, 15))
            
            # Trend list
            y_pos = 50
            for i, (move_name, popularity) in enumerate(top_trends):
                # Create color based on ranking and theme
                if self.current_theme == "Monochrome":
                    colors = [(255, 255, 255), (200, 200, 200), (150, 150, 150)]  # Grayscale
                else:
                    colors = [(255, 215, 0), (192, 192, 192), (205, 127, 50)]  # Gold, Silver, Bronze
                
                color = colors[min(i, 2)]
                
                trend_text = self.font.render(f"{move_name}", True, color)
                self.screen.blit(trend_text, (self.width - 200, y_pos))
                
                # Popularity bar
                bar_width = int(popularity * 100)
                pygame.draw.rect(
                    self.screen,
                    color,
                    (self.width - 200, y_pos + 15, bar_width, 5)
                )
                
                y_pos += 25
    
    def draw_controls(self):
        """Draw control information"""
        theme = self.COLOR_THEMES[self.current_theme]
        
        controls = [
            "SPACE: Add Dancer",
            "R: Randomize Positions",
            "C: Controls Panel",
            "M: Change Music",
            "ESC: Quit"
        ]
        
        # Background panel
        panel_rect = pygame.Rect(10, self.height - 40, 380, 30)
        panel_surface = pygame.Surface((panel_rect.width, panel_rect.height), pygame.SRCALPHA)
        panel_surface.fill(theme["ui_background"])
        self.screen.blit(panel_surface, panel_rect)
        
        # Control text
        control_text = self.font.render(" | ".join(controls), True, theme["ui_text"])
        self.screen.blit(control_text, (15, self.height - 35))
    
    def draw(self, dancers, beat_info, social_dynamics, social_network=None):
        """Main draw function that renders everything"""
        # Update visualization state
        self.update_beat_visualization(beat_info)
        self.update_trails(dancers)
        
        # Update camera if following a dancer
        if self.focused_dancer in dancers:
            target_x = self.width/2 - self.focused_dancer.position[0]
            target_y = self.height/2 - self.focused_dancer.position[1]
            # Smooth camera movement
            self.camera_offset_x = target_x
            self.camera_offset_y = target_y
        
        # Draw layers from back to front
        self.draw_background(beat_info)
        
        # Draw music-reactive floor elements
        self.draw_music_reactive_floor(beat_info)
        
        # Draw social structures
        self.draw_dance_groups(social_dynamics)
        self.draw_conga_lines(social_dynamics)
        
        # Draw social network relationships if available
        if social_network:
            self.draw_relationships(dancers, social_network)
        
        # Draw all dancers
        for dancer in dancers:
            self.draw_dancer(dancer, beat_info)
        
        # Draw audio visualization at bottom
        self.draw_audio_waveform(beat_info)
        
        # Draw UI elements on top
        self.draw_stats(dancers, social_dynamics, beat_info)
        self.draw_controls()