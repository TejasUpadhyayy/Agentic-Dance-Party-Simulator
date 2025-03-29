"""
Dancer Agent Module for Artificial Dance Party Simulation
"""
import random
import math
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List, Dict, Any

@dataclass
class DancePersonality:
    """Defines the personality traits of a dancer"""
    extroversion: float       # 0-1: how social the dancer is
    rhythm_sensitivity: float # 0-1: how well they follow the beat
    creativity: float         # 0-1: tendency to create new moves vs copy
    trendsetter: float        # 0-1: influence on others
    energy: float             # 0-1: how energetically they move

class DanceMove:
    """Represents a specific dance move pattern"""
    def __init__(self, name: str, complexity: float, energy_required: float):
        self.name = name
        self.complexity = complexity    # 0-1: how difficult the move is
        self.energy_required = energy_required  # 0-1: energy needed to perform
        self.popularity = 0.0           # 0-1: how popular the move is currently
        self.originators = []           # dancers who created/use this move
    
    def __repr__(self):
        return f"DanceMove({self.name}, pop:{self.popularity:.2f})"

class Dancer:
    """Represents a dancing agent in the simulation"""
    
    # Class variables for shared dance moves
    BASIC_MOVES = [
        DanceMove("Shuffle", 0.2, 0.3),
        DanceMove("Twist", 0.3, 0.4),
        DanceMove("Jump", 0.1, 0.7),
        DanceMove("Spin", 0.4, 0.5),
        DanceMove("Wave", 0.2, 0.3),
    ]
    
    # All known moves in the simulation
    ALL_MOVES = BASIC_MOVES.copy()
    
    def __init__(self, personality: DancePersonality, position: Tuple[float, float], color: Tuple[int, int, int]):
        self.personality = personality
        self.position = position
        self.color = color
        self.velocity = (0.0, 0.0)
        self.target_position = None
        
        # Dancing state
        self.current_move = random.choice(self.BASIC_MOVES)
        self.move_progress = 0.0  # 0-1: progress through current move
        self.energy = 1.0  # current energy level
        self.last_beat_response = 0
        
        # Social state
        self.group = None  # current dance group
        self.following = None  # dancer being followed
        self.followers = []  # dancers following this one
        self.social_radius = 30 + 70 * personality.extroversion
        
        # Movement patterns
        self.move_timer = 0
        self.move_change_threshold = random.uniform(1.0, 3.0)  # seconds between move changes
        self.movement_offset = random.uniform(0, 2 * math.pi)  # individual rhythm variation
        
        # Dance repertoire (moves this dancer knows)
        self.known_moves = self.BASIC_MOVES.copy()
        
        # Create a personal move if creative enough
        if personality.creativity > 0.7:
            self.create_new_move()
    
    def create_new_move(self) -> DanceMove:
        """Create a new unique dance move based on personality"""
        complexity = 0.5 + 0.5 * self.personality.creativity
        energy_req = 0.3 + 0.7 * self.personality.energy
        
        # Generate a fun name for the move
        adjectives = ["Funky", "Smooth", "Wild", "Chill", "Electric", "Bouncy", "Groovy"]
        nouns = ["Slide", "Hop", "Twist", "Wave", "Shake", "Bounce", "Glide", "Sway"]
        name = f"{random.choice(adjectives)} {random.choice(nouns)}"
        
        # Ensure name uniqueness
        existing_names = [move.name for move in self.ALL_MOVES]
        if name in existing_names:
            name = name + " " + str(random.randint(1, 99))
        
        # Create the move
        new_move = DanceMove(name, complexity, energy_req)
        new_move.originators.append(self)
        
        # Add to personal repertoire and global catalog
        self.known_moves.append(new_move)
        self.ALL_MOVES.append(new_move)
        
        # Start using it
        self.current_move = new_move
        
        return new_move
    
    def learn_move(self, move: DanceMove) -> bool:
        """Learn a move from another dancer"""
        # Can't learn if already known
        if move in self.known_moves:
            return False
        
        # Learning probability based on complexity and rhythm_sensitivity
        learn_chance = self.personality.rhythm_sensitivity * (1 - move.complexity)
        if random.random() < learn_chance:
            self.known_moves.append(move)
            return True
        return False
    
    def select_new_move(self, beat_info: Dict[str, Any]):
        """Select a new dance move based on personality and music"""
        # Get move options based on current energy
        valid_moves = [m for m in self.known_moves if m.energy_required <= self.energy]
        if not valid_moves:
            valid_moves = [m for m in self.BASIC_MOVES if m.energy_required <= self.energy]
        
        # If there are no valid moves available, return early
        if not valid_moves:
            # Default to the lowest energy basic move if nothing else works
            self.current_move = min(self.BASIC_MOVES, key=lambda m: m.energy_required)
            return
        
        # Different selection strategies based on personality
        if self.personality.trendsetter > 0.8 and random.random() < 0.2:
            # Creative trend-setters occasionally make new moves
            if random.random() < self.personality.creativity * 0.3:
                self.create_new_move()
                return
        elif self.personality.trendsetter < 0.3 and random.random() < 0.7:
            # Followers prefer popular moves
            move_weights = [0.5 + m.popularity for m in valid_moves]
            self.current_move = random.choices(valid_moves, weights=move_weights, k=1)[0]
            return
        
        # Default: random selection weighted by move-personality match
        move_weights = []
        for move in valid_moves:
            # Match move complexity with rhythm skill
            rhythm_match = 1 - abs(move.complexity - self.personality.rhythm_sensitivity)
            # Match move energy with dancer energy personality
            energy_match = 1 - abs(move.energy_required - self.personality.energy)
            weight = 0.5 + rhythm_match * 0.3 + energy_match * 0.2
            move_weights.append(weight)
        
        # Make sure we have valid weights before making a selection
        if move_weights:
            self.current_move = random.choices(valid_moves, weights=move_weights, k=1)[0]
        else:
            # Default to a random valid move if we can't calculate weights
            self.current_move = random.choice(valid_moves)
    
    def respond_to_beat(self, beat_info: Dict[str, Any]):
        """React to the current music beat"""
        current_beat = beat_info.get("beat_count", 0)
        beat_strength = beat_info.get("beat_strength", 0.5)
        tempo = beat_info.get("tempo", 120)
        
        # Only respond on actual beats if rhythm-sensitive
        if (current_beat > self.last_beat_response and 
            random.random() < self.personality.rhythm_sensitivity):
            
            # Calculate movement impulse based on beat and personality
            beat_response = beat_strength * self.personality.rhythm_sensitivity
            angle = self.movement_offset + beat_info.get("phase", 0) * 2 * math.pi
            
            # Movement vector
            dx = math.cos(angle) * beat_response * self.personality.energy * 5
            dy = math.sin(angle) * beat_response * self.personality.energy * 5
            
            # Apply movement impulse
            self.velocity = (
                self.velocity[0] + dx,
                self.velocity[1] + dy
            )
            
            # Occasionally change moves on the beat
            self.move_timer += 1/tempo * 60
            if self.move_timer >= self.move_change_threshold:
                self.select_new_move(beat_info)
                self.move_timer = 0
                self.move_change_threshold = random.uniform(1.0, 4.0)
            
            # Update beat response tracking
            self.last_beat_response = current_beat
    
    def move_toward_point(self, target: Tuple[float, float], speed_factor: float = 0.05):
        """Move toward a specific point"""
        dx = target[0] - self.position[0]
        dy = target[1] - self.position[1]
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 5:  # Only move if we're not already there
            # Calculate movement impulse
            scale = speed_factor * self.personality.energy
            self.velocity = (
                self.velocity[0] + dx * scale / distance,
                self.velocity[1] + dy * scale / distance
            )
    
    def join_group(self, group_center: Tuple[float, float], group_radius: float):
        """Move to join a dance group"""
        # Find a spot in the group
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, group_radius * 0.8)
        target_x = group_center[0] + math.cos(angle) * distance
        target_y = group_center[1] + math.sin(angle) * distance
        
        self.target_position = (target_x, target_y)
        self.move_toward_point(self.target_position, 0.1)
    
    def start_conga(self, dancers: List['Dancer']):
        """Try to start a conga line"""
        # Only extroverted, energetic dancers start congas
        if (self.personality.extroversion < 0.7 or 
            self.personality.energy < 0.6 or
            random.random() > 0.005):  # Very rare event
            return
        
        # Find nearby dancers to join the conga
        nearby = []
        for dancer in dancers:
            if dancer is not self:
                dx = dancer.position[0] - self.position[0]
                dy = dancer.position[1] - self.position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < self.social_radius:
                    nearby.append((dancer, distance))
        
        # Sort by distance
        nearby.sort(key=lambda x: x[1])
        
        # Try to recruit followers based on influence
        potential_followers = nearby[:5]  # Try the closest 5
        for dancer, _ in potential_followers:
            join_chance = self.personality.trendsetter * dancer.personality.extroversion
            if random.random() < join_chance:
                dancer.following = self
                self.followers.append(dancer)
    
    def follow_conga(self):
        """Follow the dancer ahead in a conga line"""
        if self.following:
            # Target position is behind the followed dancer
            dx = self.following.position[0] - self.position[0] 
            dy = self.following.position[1] - self.position[1]
            distance = math.sqrt(dx*dx + dy*dy)
            
            # Stay at a set distance
            target_distance = 30
            if distance > target_distance + 5:
                # Need to catch up
                self.move_toward_point(self.following.position, 0.2)
            elif distance < target_distance - 5:
                # Too close, back off slightly
                self.velocity = (
                    self.velocity[0] - dx * 0.01,
                    self.velocity[1] - dy * 0.01
                )
            
            # Copy the move of the leader after a slight delay
            if random.random() < 0.1:  # Occasional move sync
                self.current_move = self.following.current_move
    
    def update(self, dancers: List['Dancer'], beat_info: Dict[str, Any], social_dynamics, width: int, height: int):
        """Update dancer state for the current frame"""
        # Respond to music
        self.respond_to_beat(beat_info)
        
        # Social behaviors
        if self.following:
            # In a conga line
            self.follow_conga()
        elif random.random() < 0.01:  # Occasionally try to start a conga
            self.start_conga(dancers)
        
        # Learning from others
        for dancer in dancers:
            if dancer is not self:
                dx = dancer.position[0] - self.position[0]
                dy = dancer.position[1] - self.position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Close enough to observe and potentially learn
                if distance < self.social_radius:
                    # May learn move if seen
                    if dancer.current_move not in self.known_moves:
                        self.learn_move(dancer.current_move)
                    
                    # Influence (repel or attract) based on personalities
                    similarity = sum([
                        abs(self.personality.extroversion - dancer.personality.extroversion),
                        abs(self.personality.energy - dancer.personality.energy),
                        abs(self.personality.rhythm_sensitivity - dancer.personality.rhythm_sensitivity)
                    ]) / 3
                    
                    # Similar dancers attract, different repel
                    if similarity < 0.3:  # Very similar
                        self.move_toward_point(dancer.position, 0.01)
                    elif similarity > 0.7:  # Very different
                        # Move away
                        self.velocity = (
                            self.velocity[0] - dx * 0.01,
                            self.velocity[1] - dy * 0.01
                        )
        
        # Random movement if not otherwise directed
        if random.random() < 0.05 and not self.following and not self.target_position:
            # Occasionally pick a new random direction
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2.0) * self.personality.energy
            self.velocity = (
                math.cos(angle) * speed,
                math.sin(angle) * speed
            )
        
        # Update position based on velocity
        self.position = (
            self.position[0] + self.velocity[0],
            self.position[1] + self.velocity[1]
        )
        
        # Friction - slow down over time
        friction = 0.9
        self.velocity = (
            self.velocity[0] * friction,
            self.velocity[1] * friction
        )
        
        # Boundary handling - bounce off walls
        if self.position[0] < 10:
            self.position = (10, self.position[1])
            self.velocity = (-self.velocity[0] * 0.8, self.velocity[1])
        elif self.position[0] > width - 10:
            self.position = (width - 10, self.position[1])
            self.velocity = (-self.velocity[0] * 0.8, self.velocity[1])
            
        if self.position[1] < 10:
            self.position = (self.position[0], 10)
            self.velocity = (self.velocity[0], -self.velocity[1] * 0.8)
        elif self.position[1] > height - 10:
            self.position = (self.position[0], height - 10)
            self.velocity = (self.velocity[0], -self.velocity[1] * 0.8)
        
        # Energy management
        # Recover energy slowly
        self.energy = min(1.0, self.energy + 0.001)
        # Use energy based on current move and activity
        energy_use = self.current_move.energy_required * 0.01
        velocity_magnitude = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
        energy_use += velocity_magnitude * 0.001
        self.energy = max(0.1, self.energy - energy_use)
        
        # Reset target if reached
        if self.target_position:
            dx = self.target_position[0] - self.position[0]
            dy = self.target_position[1] - self.position[1]
            if dx*dx + dy*dy < 25:  # Within 5 pixels
                self.target_position = None

class CelebrityDancer(Dancer):
    """A special dancer with high influence and unique abilities"""
    
    def __init__(self, position: Tuple[float, float], color: Tuple[int, int, int]):
        # Create an exceptional personality
        personality = DancePersonality(
            extroversion=0.9,
            rhythm_sensitivity=0.9,
            creativity=0.95,
            trendsetter=0.95,
            energy=0.9
        )
        
        # Initialize with this personality
        super().__init__(personality, position, color)
        
        # Special celebrity properties
        self.influence_radius = 150  # Much larger influence radius
        self.social_radius = 150
        self.move_change_threshold = 0.5  # Changes moves more frequently
        
        # Create a special move
        self.signature_move = self.create_new_move()
        self.signature_move.name = "Celebrity " + self.signature_move.name
        
        # Start with the signature move
        self.current_move = self.signature_move
    
    def update(self, dancers: List['Dancer'], beat_info: Dict[str, Any], social_dynamics, width: int, height: int):
        """Update celebrity dancer with special behaviors"""
        # Normal dancer update
        super().update(dancers, beat_info, social_dynamics, width, height)
        
        # Special celebrity influence: higher chance to make others learn moves
        for dancer in dancers:
            if dancer is not self:
                dx = dancer.position[0] - self.position[0]
                dy = dancer.position[1] - self.position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                # Influence dancers within the influence radius
                if distance < self.influence_radius:
                    # Higher chance to teach moves
                    if random.random() < 0.2:  # 20% chance each update
                        dancer.learn_move(self.current_move)
                    
                    # Attraction effect - dancers are drawn to celebrities
                    attraction_factor = 0.01 * (1 - distance/self.influence_radius)
                    dancer.move_toward_point(self.position, attraction_factor)
        
        # Celebrities occasionally return to their signature move
        if random.random() < 0.05 and self.current_move != self.signature_move:
            self.current_move = self.signature_move