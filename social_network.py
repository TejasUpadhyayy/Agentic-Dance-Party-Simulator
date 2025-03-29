"""
Social Network Module for Artificial Dance Party Simulation
Manages relationships between dancers and dance crews
"""
import random
import math
from typing import List, Dict, Set, Tuple, Any

class Relationship:
    """Represents a relationship between two dancers"""
    
    def __init__(self, dancer1_id, dancer2_id):
        self.dancer1_id = dancer1_id
        self.dancer2_id = dancer2_id
        self.strength = 0.0  # 0.0 to 1.0
        self.type = "neutral"  # "friend", "rival", "neutral"
        self.duration = 0  # How long this relationship has existed
    
    def update(self, compatibility: float, delta_time: float):
        """Update relationship based on dancer compatibility"""
        # Relationship strength grows or diminishes based on compatibility
        if compatibility > 0.7:  # Very compatible
            self.strength = min(1.0, self.strength + 0.01 * delta_time)
            if self.strength > 0.7 and self.type != "friend":
                self.type = "friend"
        elif compatibility < 0.3:  # Very incompatible
            if random.random() < 0.5:  # 50% chance of rivalry vs indifference
                self.strength = min(1.0, self.strength + 0.005 * delta_time)
                if self.strength > 0.5 and self.type != "rival":
                    self.type = "rival"
            else:
                self.strength = max(0.0, self.strength - 0.01 * delta_time)
                self.type = "neutral"
        else:  # Moderate compatibility
            self.strength = max(0.1, self.strength - 0.001 * delta_time)
            if self.strength < 0.3:
                self.type = "neutral"
        
        # Update duration
        self.duration += delta_time
    
    def get_color(self) -> Tuple[int, int, int, int]:
        """Get relationship line color based on type and strength"""
        alpha = int(self.strength * 255)
        
        if self.type == "friend":
            return (100, 200, 100, alpha)  # Green for friendship
        elif self.type == "rival":
            return (200, 100, 100, alpha)  # Red for rivalry
        else:
            return (150, 150, 150, alpha)  # Gray for neutral

class DanceCrew:
    """Represents a dance crew with a shared identity"""
    
    def __init__(self, name: str, founder_id):
        self.name = name
        self.members = {founder_id}
        self.formation_time = 0
        self.signature_moves = set()  # Moves associated with this crew
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
    
    def add_member(self, dancer_id):
        """Add a dancer to the crew"""
        self.members.add(dancer_id)
    
    def remove_member(self, dancer_id):
        """Remove a dancer from the crew"""
        if dancer_id in self.members:
            self.members.remove(dancer_id)
    
    def add_signature_move(self, move):
        """Add a signature move to the crew"""
        self.signature_moves.add(move)
    
    def member_count(self) -> int:
        """Get the number of members in the crew"""
        return len(self.members)
    
    def get_members_list(self) -> List:
        """Get a list of member IDs"""
        return list(self.members)

class SocialNetwork:
    """Manages the social relationships between dancers"""
    
    def __init__(self):
        self.relationships = {}  # (dancer1_id, dancer2_id) -> Relationship
        self.dance_crews = []  # List of dance crews
        self.dancer_to_crew = {}  # dancer_id -> crew
    
    def get_or_create_relationship(self, dancer1, dancer2):
        """Get an existing relationship or create a new one"""
        # Ensure consistent ordering of dancers
        dancer1_id = id(dancer1)
        dancer2_id = id(dancer2)
        
        if dancer1_id > dancer2_id:
            dancer1_id, dancer2_id = dancer2_id, dancer1_id
        
        key = (dancer1_id, dancer2_id)
        
        if key not in self.relationships:
            self.relationships[key] = Relationship(dancer1_id, dancer2_id)
        
        return self.relationships[key]
    
    def calculate_compatibility(self, dancer1, dancer2) -> float:
        """Calculate compatibility between two dancers"""
        # Personality similarity
        personality_diff = sum([
            abs(dancer1.personality.extroversion - dancer2.personality.extroversion),
            abs(dancer1.personality.rhythm_sensitivity - dancer2.personality.rhythm_sensitivity),
            abs(dancer1.personality.creativity - dancer2.personality.creativity),
            abs(dancer1.personality.energy - dancer2.personality.energy)
        ]) / 4
        
        personality_compat = 1.0 - personality_diff
        
        # Dance style compatibility (shared moves)
        dancer1_moves = set(dancer1.known_moves)
        dancer2_moves = set(dancer2.known_moves)
        
        shared_moves = len(dancer1_moves.intersection(dancer2_moves))
        total_moves = len(dancer1_moves.union(dancer2_moves))
        
        move_compat = shared_moves / max(1, total_moves)
        
        # Weigh and combine factors
        return 0.6 * personality_compat + 0.4 * move_compat
    
    def update_relationships(self, dancers: List, delta_time: float):
        """Update all relationships based on current dancer states"""
        # Update existing relationships
        for (dancer1_id, dancer2_id), relationship in list(self.relationships.items()):
            # Find the actual dancer objects
            dancer1 = None
            dancer2 = None
            
            for dancer in dancers:
                if id(dancer) == dancer1_id:
                    dancer1 = dancer
                elif id(dancer) == dancer2_id:
                    dancer2 = dancer
            
            # If both dancers still exist
            if dancer1 and dancer2:
                compatibility = self.calculate_compatibility(dancer1, dancer2)
                relationship.update(compatibility, delta_time)
                
                # Remove weak relationships that have existed for a while
                if relationship.strength < 0.1 and relationship.duration > 10:
                    del self.relationships[(dancer1_id, dancer2_id)]
            else:
                # One dancer was removed, delete the relationship
                del self.relationships[(dancer1_id, dancer2_id)]
        
        # Create new relationships between nearby dancers
        for i, dancer1 in enumerate(dancers):
            for dancer2 in dancers[i+1:]:
                # Check if they're close enough to interact
                dx = dancer1.position[0] - dancer2.position[0]
                dy = dancer1.position[1] - dancer2.position[1]
                distance = math.sqrt(dx*dx + dy*dy)
                
                # If dancers are near each other, they might form a relationship
                if distance < dancer1.social_radius:
                    # Get or create the relationship
                    self.get_or_create_relationship(dancer1, dancer2)
    
    def update_dance_crews(self, dancers: List, delta_time: float):
        """Update dance crews based on relationships"""
        # Remove dancers that no longer exist
        for crew in self.dance_crews:
            for dancer_id in list(crew.members):
                if not any(id(dancer) == dancer_id for dancer in dancers):
                    crew.remove_member(dancer_id)
                    if dancer_id in self.dancer_to_crew:
                        del self.dancer_to_crew[dancer_id]
        
        # Remove empty crews
        self.dance_crews = [crew for crew in self.dance_crews if crew.member_count() > 0]
        
        # Check for new crew formation
        self._create_new_crews(dancers)
        
        # Check for crew growth
        self._grow_existing_crews(dancers)
    
    def _create_new_crews(self, dancers: List):
        """Look for potential new dance crews to form"""
        # Don't create too many crews
        if len(self.dance_crews) >= 3:
            return
        
        # Find dancers not in crews with strong friendships
        for i, dancer1 in enumerate(dancers):
            # Skip dancers already in crews
            if id(dancer1) in self.dancer_to_crew:
                continue
            
            # Find dancers with strong friendly relationships
            strong_friends = []
            
            for dancer2 in dancers[i+1:]:
                # Skip dancers already in crews
                if id(dancer2) in self.dancer_to_crew:
                    continue
                
                relationship = self.get_or_create_relationship(dancer1, dancer2)
                
                if relationship.type == "friend" and relationship.strength > 0.7:
                    strong_friends.append(dancer2)
            
            # If enough strong friends, form a crew
            if len(strong_friends) >= 2:
                # Only form crew if the lead dancer is creative or a trendsetter
                if dancer1.personality.creativity > 0.6 or dancer1.personality.trendsetter > 0.6:
                    # Create a crew name
                    adjectives = ["Dynamic", "Rhythmic", "Smooth", "Electric", "Funky", "Wild", "Groove"]
                    nouns = ["Crew", "Squad", "Collective", "Posse", "Tribe", "Alliance", "Ensemble"]
                    crew_name = f"The {random.choice(adjectives)} {random.choice(nouns)}"
                    
                    # Create the crew
                    new_crew = DanceCrew(crew_name, id(dancer1))
                    
                    # Add friends to the crew
                    for friend in strong_friends[:3]:  # Limit initial size
                        new_crew.add_member(id(friend))
                    
                    # Add signature move
                    if dancer1.personality.creativity > 0.7:
                        new_move = dancer1.create_new_move()
                        new_move.name = f"{crew_name} {new_move.name}"
                        new_crew.add_signature_move(new_move)
                    
                    # Add the crew to the list
                    self.dance_crews.append(new_crew)
                    
                    # Update dancer_to_crew mapping
                    self.dancer_to_crew[id(dancer1)] = new_crew
                    for friend in strong_friends[:3]:
                        self.dancer_to_crew[id(friend)] = new_crew
                    
                    return  # Only create one crew per update
    
    def _grow_existing_crews(self, dancers: List):
        """Grow existing crews by recruiting new members"""
        for crew in self.dance_crews:
            # Skip very large crews
            if crew.member_count() >= 8:
                continue
            
            # Get current crew members
            crew_dancer_ids = crew.get_members_list()
            
            # Find potential recruits
            for dancer in dancers:
                dancer_id = id(dancer)
                
                # Skip dancers already in crews
                if dancer_id in self.dancer_to_crew:
                    continue
                
                # Check relationships with current crew members
                friend_count = 0
                for crew_dancer_id in crew_dancer_ids:
                    # Find the crew dancer object
                    crew_dancer = None
                    for d in dancers:
                        if id(d) == crew_dancer_id:
                            crew_dancer = d
                            break
                    
                    if crew_dancer:
                        relationship = self.get_or_create_relationship(dancer, crew_dancer)
                        if relationship.type == "friend" and relationship.strength > 0.5:
                            friend_count += 1
                
                # If enough friends in the crew, join it
                if friend_count >= 2 or (friend_count >= 1 and random.random() < 0.3):
                    crew.add_member(dancer_id)
                    self.dancer_to_crew[dancer_id] = crew
                    
                    # Learn crew's signature moves
                    for move in crew.signature_moves:
                        dancer.learn_move(move)
    
    def get_crew_for_dancer(self, dancer):
        """Get the crew a dancer belongs to, if any"""
        dancer_id = id(dancer)
        return self.dancer_to_crew.get(dancer_id, None)
    
    def get_visible_relationships(self) -> List[Tuple]:
        """Get relationships that are strong enough to be visible"""
        visible = []
        for key, relationship in self.relationships.items():
            if relationship.strength > 0.4:  # Only show reasonably strong relationships
                visible.append((key[0], key[1], relationship))
        return visible
    
    def update(self, dancers: List, delta_time: float):
        """Update the entire social network"""
        self.update_relationships(dancers, delta_time)
        self.update_dance_crews(dancers, delta_time)