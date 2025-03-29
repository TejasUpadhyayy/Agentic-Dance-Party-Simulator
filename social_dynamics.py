"""
Social Dynamics Module for Artificial Dance Party Simulation
Handles social interactions, trend propagation, and group formations
"""
import random
import math
from typing import List, Dict, Set, Tuple, Any
from collections import Counter

class DanceGroup:
    """Represents a group of dancers dancing together"""
    
    def __init__(self, center: Tuple[float, float], initial_members=None):
        self.center = center
        self.members = set(initial_members) if initial_members else set()
        self.radius = 50  # Initial radius
        self.formation_time = 0  # How long the group has existed
        self.lifespan = random.uniform(10, 30)  # How long the group will last
        self.energy = 0.5  # Group energy level
        self.dominant_move = None  # Most popular move in the group
    
    def add_member(self, dancer):
        """Add a dancer to the group"""
        self.members.add(dancer)
        # Increase radius with more members
        self.radius = max(50, 20 * math.sqrt(len(self.members)))
    
    def remove_member(self, dancer):
        """Remove a dancer from the group"""
        if dancer in self.members:
            self.members.remove(dancer)
    
    def update_center(self):
        """Update the group's center based on member positions"""
        if not self.members:
            return
        
        # Calculate the average position of all members
        x_sum = sum(dancer.position[0] for dancer in self.members)
        y_sum = sum(dancer.position[1] for dancer in self.members)
        
        self.center = (x_sum / len(self.members), y_sum / len(self.members))
    
    def update_dominant_move(self):
        """Determine the most popular move in the group"""
        if not self.members:
            return
        
        # Count the occurrences of each move
        move_counter = Counter(dancer.current_move for dancer in self.members)
        
        # Find the most common move
        self.dominant_move, _ = move_counter.most_common(1)[0]
    
    def update(self, delta_time: float):
        """Update the state of the group"""
        self.formation_time += delta_time
        
        # Update center position based on member positions
        self.update_center()
        
        # Update the dominant move
        self.update_dominant_move()
        
        # Calculate group energy based on member energy
        if self.members:
            avg_energy = sum(dancer.personality.energy for dancer in self.members) / len(self.members)
            self.energy = 0.3 * self.energy + 0.7 * avg_energy  # Smooth transition
        
        # Return whether the group should disband
        return self.formation_time >= self.lifespan or len(self.members) < 3

class CongaLine:
    """Represents a conga line of dancers"""
    
    def __init__(self, leader):
        self.leader = leader
        self.followers = []
        self.formation_time = 0
        self.lifespan = random.uniform(15, 40)
    
    def add_follower(self, dancer):
        """Add a dancer to the end of the conga line"""
        self.followers.append(dancer)
        dancer.following = self.followers[-2] if len(self.followers) > 1 else self.leader
    
    def remove_follower(self, dancer):
        """Remove a dancer from the conga line"""
        if dancer in self.followers:
            index = self.followers.index(dancer)
            
            # Update following references
            if index < len(self.followers) - 1:
                next_dancer = self.followers[index + 1]
                if index > 0:
                    next_dancer.following = self.followers[index - 1]
                else:
                    next_dancer.following = self.leader
            
            # Remove the dancer
            self.followers.remove(dancer)
            dancer.following = None
    
    def update(self, delta_time: float):
        """Update the state of the conga line"""
        self.formation_time += delta_time
        
        # Return whether the conga line should disband
        return self.formation_time >= self.lifespan or not self.followers

class SocialDynamics:
    """Manages social dynamics between dancers"""
    
    def __init__(self):
        self.dance_groups = []
        self.conga_lines = []
        self.dance_trends = {}  # Move name -> popularity
        self.trend_decay_rate = 0.995  # How quickly trends fade
        self.last_update_time = 0
        
        # Group formation factor (adjustable by UI)
        self.group_formation_factor = 0.1  # Default value
        
        # Store historical data for visualization
        self.trend_history = {}  # Move name -> [popularity values over time]
    
    def update_dance_groups(self, dancers: List, delta_time: float):
        """Update existing dance groups and create new ones"""
        # Update existing groups
        groups_to_remove = []
        for group in self.dance_groups:
            # Update the group state
            should_disband = group.update(delta_time)
            
            # Check if the group should disband
            if should_disband or len(group.members) < 2:
                groups_to_remove.append(group)
        
        # Remove disbanded groups
        for group in groups_to_remove:
            for dancer in list(group.members):
                group.remove_member(dancer)
            self.dance_groups.remove(group)
        
        # Potentially create new groups
        self._create_new_groups(dancers)
    
    def _create_new_groups(self, dancers: List):
        """Look for potential new dance groups to form"""
        # Don't create too many groups
        if len(self.dance_groups) >= 3:
            return
        
        # Find dancers that aren't in groups or conga lines
        available_dancers = []
        for dancer in dancers:
            in_group = any(dancer in group.members for group in self.dance_groups)
            in_conga = any(dancer == line.leader or dancer in line.followers for line in self.conga_lines)
            
            if not in_group and not in_conga:
                available_dancers.append(dancer)
        
        # Need at least 3 dancers for a group
        if len(available_dancers) < 3:
            return
        
        # Look for clusters of dancers
        for dancer in available_dancers:
            nearby_dancers = []
            
            # Find dancers within social radius
            for other in available_dancers:
                if dancer is not other:
                    dx = dancer.position[0] - other.position[0]
                    dy = dancer.position[1] - other.position[1]
                    distance = math.sqrt(dx*dx + dy*dy)
                    
                    if distance < dancer.social_radius:
                        nearby_dancers.append(other)
            
            # If enough dancers are nearby and at least one is extroverted
            if len(nearby_dancers) >= 2:
                # Check if any dancer is extroverted enough to start a group
                extroversion_sum = dancer.personality.extroversion + sum(d.personality.extroversion for d in nearby_dancers)
                avg_extroversion = extroversion_sum / (1 + len(nearby_dancers))
                
                # Higher chance with more extroverted dancers
                # Use the group_formation_factor here to make it adjustable
                formation_chance = avg_extroversion * self.group_formation_factor
                
                if random.random() < formation_chance:
                    # Create a new group
                    initial_members = [dancer] + nearby_dancers
                    center = (dancer.position[0], dancer.position[1])
                    new_group = DanceGroup(center, initial_members)
                    self.dance_groups.append(new_group)
                    return  # Only create one group per update
    
    def update_conga_lines(self, dancers: List, delta_time: float):
        """Update existing conga lines and create new ones"""
        # Update existing conga lines
        lines_to_remove = []
        for line in self.conga_lines:
            # Update the line state
            should_disband = line.update(delta_time)
            
            # Check if the line should disband
            if should_disband:
                lines_to_remove.append(line)
        
        # Remove disbanded lines
        for line in lines_to_remove:
            # Clear following references
            for follower in line.followers:
                follower.following = None
            line.leader.followers = []
            self.conga_lines.remove(line)
        
        # Conga lines are created directly by dancers calling start_conga()
    
    def update_dance_trends(self, dancers: List, beat_info: Dict[str, Any]):
        """Update the popularity of dance moves"""
        # Collect all moves currently being used
        active_moves = [dancer.current_move for dancer in dancers]
        
        # Count occurrences
        move_counter = Counter(active_moves)
        
        # Update trend scores
        for move, count in move_counter.items():
            # Initial popularity boost based on count and trendsetter values
            boost = count * 0.1
            
            # Additional boost from trendsetters
            for dancer in dancers:
                if dancer.current_move == move:
                    boost += dancer.personality.trendsetter * 0.05
            
            # Update existing trend or create new one
            if move.name in self.dance_trends:
                # Existing trends decay slightly but can be boosted
                self.dance_trends[move.name] *= self.trend_decay_rate
                self.dance_trends[move.name] += boost
            else:
                # New trends start with initial boost
                self.dance_trends[move.name] = boost
            
            # Cap popularity at 1.0
            self.dance_trends[move.name] = min(1.0, self.dance_trends[move.name])
            
            # Update the move's popularity score
            move.popularity = self.dance_trends[move.name]
        
        # Record history for visualization (sample every few beats)
        if beat_info.get("just_beat", False) and beat_info.get("beat_count", 0) % 4 == 0:
            for move_name, popularity in self.dance_trends.items():
                if move_name not in self.trend_history:
                    self.trend_history[move_name] = []
                self.trend_history[move_name].append(popularity)
    
    def update(self, dancers: List, beat_info: Dict[str, Any]):
        """Update all social dynamics for the current frame"""
        current_time = beat_info.get("time", 0)
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Update groups and conga lines
        self.update_dance_groups(dancers, delta_time)
        self.update_conga_lines(dancers, delta_time)
        
        # Update dance trends
        self.update_dance_trends(dancers, beat_info)
        
        # Assign dancers to groups if they're in range
        self._update_group_membership(dancers)
    
    def _update_group_membership(self, dancers: List):
        """Update which dancers are part of which groups"""
        # Check each dancer against each group
        for dancer in dancers:
            # Skip dancers in conga lines
            if dancer.following or any(dancer == line.leader for line in self.conga_lines):
                continue
            
            # Check if dancer is in any group
            current_group = None
            for group in self.dance_groups:
                if dancer in group.members:
                    current_group = group
                    break
            
            # Find the closest group
            closest_group = None
            closest_distance = float('inf')
            
            for group in self.dance_groups:
                dx = group.center[0] - dancer.position[0]
                dy = group.center[1] - dancer.position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                if distance < group.radius and distance < closest_distance:
                    closest_group = group
                    closest_distance = distance
            
            # Update group membership
            if closest_group != current_group:
                # Remove from current group
                if current_group:
                    current_group.remove_member(dancer)
                
                # Add to new group
                if closest_group:
                    closest_group.add_member(dancer)
                    
                    # Dancers in groups may adopt the dominant move
                    if closest_group.dominant_move and random.random() < 0.3:
                        dancer.current_move = closest_group.dominant_move
                    
                    # Set target position within group
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(0, closest_group.radius * 0.8)
                    
                    target_x = closest_group.center[0] + math.cos(angle) * distance
                    target_y = closest_group.center[1] + math.sin(angle) * distance
                    dancer.target_position = (target_x, target_y)
    
    def get_trend_data(self):
        """Get current trend data for visualization"""
        # Sort by popularity
        sorted_trends = sorted(
            self.dance_trends.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return {
            "current": sorted_trends[:5],  # Top 5 trends
            "history": self.trend_history
        }
    
    def get_social_structures(self):
        """Get all social structures for visualization"""
        return {
            "groups": self.dance_groups,
            "conga_lines": self.conga_lines
        }