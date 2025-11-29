"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from random import random
from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    if enemy_type.lower() == "goblin":
        return {
            'name': 'Goblin',
            'health': 50,
            'max_health': 50,
            'strength': 8,
            'magic': 2,
            'xp_reward': 25,
            'gold_reward': 10
        }
    elif enemy_type.lower() == "orc":
        return {
            'name': 'Orc',
            'health': 80,
            'max_health': 80,
            'strength': 12,
            'magic': 5,
            'xp_reward': 50,
            'gold_reward': 25
        }
    elif enemy_type.lower() == "dragon":
        return {
            'name': 'Dragon',
            'health': 200,
            'max_health': 200,
            'strength': 25,
            'magic': 15,
            'xp_reward': 200,
            'gold_reward': 100
        }
    else:
        raise InvalidTargetError(f"Unknown enemy type: {enemy_type}")
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    

def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    if 1 <= character_level <= 2:
        return create_enemy("goblin")
    elif 3 <= character_level <= 5:
        return create_enemy("orc")
    elif character_level >= 6:
        return create_enemy("dragon")
    else:
        raise InvalidTargetError(f"Invalid character level: {character_level}")
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        self.character = character
        self.enemy = enemy
        self.combat_active = True
        self.turn_counter = 0
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        if self.character['health'] <= 0:
            raise CharacterDeadError("Cannot start battle: Character is dead.")
        
        while self.combat_active:
            self.turn_counter += 1
            # Player's turn
            self.player_turn()
            if not self.combat_active:
                break
            # Enemy's turn
            self.enemy_turn()
            if not self.combat_active:
                break

        winner = self.check_battle_end()
        if winner == 'player':
            xp_gained = self.enemy['xp_reward']
            gold_gained = self.enemy['gold_reward']
            return {'winner': 'player', 'xp_gained': xp_gained, 'gold_gained': gold_gained}
        else:
            raise CharacterDeadError("Character has been defeated in battle.")
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        pass
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take player turn: Combat is not active.")
        
        display_combat_stats(self.character, self.enemy)
        print("\nChoose your action:")
        print("1. Basic Attack")
        print("2. Special Ability")
        print("3. Try to Run")
        choice = input("Enter choice (1-3): ")
        if choice == '1':
            damage = self.calculate_damage(self.character, self.enemy)
            self.apply_damage(self.enemy, damage)
            display_battle_log(f"You attack the {self.enemy['name']} for {damage} damage!")
        elif choice == '2':
            result = use_special_ability(self.character, self.enemy)
            display_battle_log(result)
        elif choice == '3':
            escaped = self.attempt_escape()
            if escaped:
                display_battle_log("You successfully escaped the battle!")
                self.combat_active = False
            else:
                display_battle_log("Escape failed! The battle continues.")
        else:
            display_battle_log("Invalid choice! You lose your turn.")
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        
    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        if not self.combat_active:
            raise CombatNotActiveError("Cannot take enemy turn: Combat is not active.")
        damage = self.calculate_damage(self.enemy, self.character)
        self.apply_damage(self.character, damage)
        display_battle_log(f"The {self.enemy['name']} attacks you for {damage} damage!")
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        base_damage = attacker['strength'] - (defender['strength'] // 4)
        if base_damage < 1:
            base_damage = 1
        return base_damage
        # TODO: Implement damage calculation
        
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        target['health'] -= damage
        if target['health'] < 0:
            target['health'] = 0
        # TODO: Implement damage application
        
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        if self.enemy['health'] <= 0:
            self.combat_active = False
            return 'player'
        elif self.character['health'] <= 0:
            self.combat_active = False
            return 'enemy'
        else:
            return None
        # TODO: Implement battle end check
        pass
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        success = random.random() < 0.5
        if success:
            self.combat_active = False
        return success
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    character_class = character['class'].lower()
    if character_class == "warrior":
        warrior_power_strike(character, enemy)
        return "Warrior uses Power Strike!"
    elif character_class == "mage":
        mage_fireball(character, enemy)
        return "Mage casts Fireball!"
    elif character_class == "rogue":
        rogue_critical_strike(character, enemy)
        return "Rogue attempts Critical Strike!"
    elif character_class == "cleric":
        cleric_heal(character)
        return "Cleric casts Heal!"
    else:
        return "No special ability available."
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    damage = character['strength'] * 2
    enemy['health'] -= damage
    if enemy['health'] < 0:
        enemy['health'] = 0

    # TODO: Implement power strike
    # Double strength damage

def mage_fireball(character, enemy):
    """Mage special ability"""
    damage = character['magic'] * 2
    enemy['health'] -= damage
    if enemy['health'] < 0:
        enemy['health'] = 0

    # TODO: Implement fireball
    # Double magic damage

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    if random.random() < 0.5:
        damage = character['strength'] * 3
    else:
        damage = character['strength']
    enemy['health'] -= damage
    if enemy['health'] < 0:
        enemy['health'] = 0
    # TODO: Implement critical strike
    # 50% chance for triple damage


def cleric_heal(character):
    """Cleric special ability"""
    character['health'] += 30
    if character['health'] > character['max_health']:
        character['health'] = character['max_health']
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    if character['health'] > 0:
        return True
    return False
    # TODO: Implement fight check
    

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    return {'xp': enemy['xp_reward'], 'gold': enemy['gold_reward']}
    # TODO: Implement reward calculation


def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']}")
    

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f">>> {message}")
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    # try:
    #     goblin = create_enemy("goblin")
    #     print(f"Created {goblin['name']}")
    # except InvalidTargetError as e:
    #     print(f"Invalid enemy: {e}")
    
    # Test battle
    # test_char = {
    #     'name': 'Hero',
    #     'class': 'Warrior',
    #     'health': 120,
    #     'max_health': 120,
    #     'strength': 15,
    #     'magic': 5
    # }
    #
    # battle = SimpleBattle(test_char, goblin)
    # try:
    #     result = battle.start_battle()
    #     print(f"Battle result: {result}")
    # except CharacterDeadError:
    #     print("Character is dead!")

