"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: [Your Name Here]

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    print("\n=== MAIN MENU ===")
    print("1. New Game")
    print("2. Load Game")
    print("3. Exit")
    choice = input("Enter your choice (1-3): ")
    try:
        choice_int = int(choice)
        if choice_int in [1, 2, 3]:
            return choice_int
        else:
            print("Invalid choice. Please select 1-3.")
            return main_menu()
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 3.")
        return main_menu()


def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    global current_character
    input_name = input("Enter your character's name: ")
    print("Choose your character class:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    class_choice = input("Enter the number of your choice: ")
    class_dict = {'1': 'Warrior', '2': 'Mage', '3': 'Rogue'}
    if class_choice in class_dict:
        input_class = class_dict[class_choice]
        try:
            current_character = character_manager.create_character(input_name, input_class)
            character_manager.save_character(current_character)
            print(f"Character {input_name} the {input_class} created successfully!")
            game_loop()
        except InvalidCharacterClassError as e:
            print(f"Error: {e}")
    else:
        print("Invalid class choice. Please try again.")
        new_game()



def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    print("\n=== LOAD GAME ===")
    saved_characters = character_manager.list_saved_characters()
    if not saved_characters:
        print("No saved characters found.")
        return
    print("Saved Characters:")
    for idx, name in enumerate(saved_characters, 1):
        print(f"{idx}. {name}")
    input_name = input("Enter the name of the character to load: ")
    try:
        current_character = character_manager.load_character(input_name)
        print(f"Character {input_name} loaded successfully!")
        game_loop()
    except CharacterNotFoundError:
        print(f"Error: Character '{input_name}' not found.")
    except SaveFileCorruptedError:
        print(f"Error: Save file for '{input_name}' is corrupted.")
        load_game()
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    while game_running:
        game_menu()
        choice = input("Enter your choice (1-6): ")
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    print("\n=== GAME MENU ===")
    print("1. View Character Stats")
    print("2. View Inventory")
    print("3. Quest Menu")
    print("4. Explore (Find Battles)")
    print("5. Shop")
    print("6. Save and Quit")
    
    choice = input("Enter your choice (1-6): ")
    try:
        choice_int = int(choice)
        if choice_int in [1, 2, 3, 4, 5, 6]:
            if choice_int == 1:
                view_character_stats()
            elif choice_int == 2:
                view_inventory()
            elif choice_int == 3:
                quest_menu()
            elif choice_int == 4:
                explore()
            elif choice_int == 5:
                shop()
            elif choice_int == 6:
                save_game()
                global game_running
                game_running = False
                print("Exiting to main menu...")
            return choice_int
        else:
            print("Invalid choice. Please select 1-6.")
            return game_menu()
    except ValueError:
        print("Invalid input. Please enter a number between 1 and 6.")
        return game_menu()
    
    

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    print("\n=== CHARACTER STATS ===")
    character_manager.display_character_stats(current_character)
def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    print("\n=== INVENTORY ===")

    if not inventory_system.display_inventory(current_character, all_items):
        print("Your inventory is empty.")
        return
    
    unique_items = list(set(inventory_system.display_inventory(current_character, all_items)))
    for i, item_id in enumerate(unique_items, 1):
        item_name = all_items[item_id]["name"]
        count = current_character.inventory.count(item_id)
        print(f"{i}. {item_name}  (x{count})")

    print("\nOptions:")
    print("1. Use Item")
    print("2. Equip Weapon")
    print("3. Equip Armor")
    print("4. Drop Item")
    print("5. Exit Inventory")

    choice = input("Choose an option: ")

    if choice == "1":
        inventory_system.use_item(unique_items)
    elif choice == "2":
        inventory_system.equip_weapon(unique_items)
    elif choice == "3":
        inventory_system.equip_armor(unique_items)
    elif choice == "4":
        inventory_system.remove_item_from_inventory(unique_items)
    else:
        print("Leaving inventory...")
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system


def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    while True:
        print("\n=== QUEST MENU ===")
        print("1. View Active Quests")
        print("2. View Available Quests")
        print("3. View Completed Quests")
        print("4. Accept Quest")
        print("5. Abandon Quest")
        print("6. Complete Quest (for testing)")
        print("7. Back to Game Menu")

        try:
            choice = int(input("Choose an option: "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 7.")
            

        if choice == 1:
            # Get active quests safely
            active_quests = quest_handler.get_active_quests(current_character, all_quests)
            if active_quests:
                quest_handler.display_quest_list(active_quests)
            else:
                print("You have no active quests.")

        elif choice == 2:
            # Get available quests safely
            available_quests = quest_handler.get_available_quests(current_character, all_quests)
            if available_quests:
                quest_handler.display_quest_list(available_quests)
            else:
                print("No quests are currently available to accept.")

        elif choice == 3:
            # Get completed quests safely
            completed_quests = quest_handler.get_completed_quests(current_character, all_quests)
            if completed_quests:
                quest_handler.display_quest_list(completed_quests)
            else:
                print("You have not completed any quests yet.")

        elif choice == 4:
            quest_id = input("Enter the Quest ID to accept: ")
            try:
                quest_handler.accept_quest(current_character, quest_id, all_quests)
                character_manager.save_character(current_character)
                print(f"Quest '{quest_id}' accepted!")
            except (QuestNotFoundError, InsufficientLevelError, QuestRequirementsNotMetError, QuestAlreadyCompletedError) as e:
                print(f"Cannot accept quest: {e}")

        elif choice == 5:
            quest_id = input("Enter the Quest ID to abandon: ")
            try:
                quest_handler.abandon_quest(current_character, quest_id)
                character_manager.save_character(current_character)
                print(f"Quest '{quest_id}' abandoned.")
            except QuestNotActiveError as e:
                print(f"Cannot abandon quest: {e}")

        elif choice == 6:
            quest_id = input("Enter the Quest ID to complete (testing only): ")
            try:
                rewards = quest_handler.complete_quest(current_character, quest_id, all_quests)
                character_manager.save_character(current_character)
                print(f"Quest '{quest_id}' completed! Rewards: {rewards['reward_xp']} XP, {rewards['reward_gold']} Gold")
            except (QuestNotFoundError, QuestNotActiveError) as e:
                print(f"Cannot complete quest: {e}")

        elif choice == 7:
            # Back to game menu
            break

        else:
            print("Invalid choice. Please select 1-7.")
    

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    enemy = combat_system.get_random_enemy_for_level(current_character['level'])
    battle = combat_system.SimpleBattle(current_character, enemy)
    result = battle.start_battle()
    if result == "victory":
        print(f"You defeated the {enemy['name']}!")
        current_character.gold += enemy['gold_reward']
        current_character.gain_xp(enemy['xp_reward'])
        character_manager.save_character(current_character)
        print(f"You earned {enemy['xp_reward']} XP and {enemy['gold_reward']} gold.")
    elif result == "defeat":
        print("You have been defeated...")
        handle_character_death()

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    print("\n=== SHOP ===")
    print("1. Buy items")
    print("2. Sell items")
    print(f"\nYour Gold: {current_character['gold']}")
    choice = input("Choose an option: ")
    if choice == "1":
        print("What would you like to buy?")
        item = input("Enter the item name: ")
        if item not in all_items:
            print("Item not found in shop.")
            return
        try:
            inventory_system.purchase_item(current_character, item, item_data=all_items[item])
            print(f"You purchased {all_items[item]['name']}!")
        except (InsufficientResourcesError, InventoryFullError) as e:
            print(f"Cannot purchase item: {e}")    
    elif choice == "2":
        print("What would you like to sell?")
        item = input("Enter the item name: ")
        try:
            inventory_system.sell_item(current_character, item)
            print(f"You sold {all_items[item]['name']}!")
        except ItemNotFoundError as e:
            print(f"Cannot sell item: {e}")
    else:
        print("Leaving shop...")
        return
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    try:
        character_manager.save_character(current_character)
        print("Game saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions


def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    try:
        all_quests = game_data.load_quests("quests.json")
        all_items = game_data.load_items("items.json")
    except MissingDataFileError as e:
        print(f"Data file missing: {e}")
        game_data.create_default_data_files()
    except InvalidDataFormatError as e:
        print(f"Data file format error: {e}")
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()


def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    print("\n=== YOU HAVE DIED ===")
    print("Revive costs 50 gold.")
    choice = input("Do you want to revive? (y/n): ")
    if choice.lower() == 'y':
        if current_character.gold >= 50:
            current_character.gold -= 50
            character_manager.revive_character(current_character)
            character_manager.save_character(current_character)
            print("You have been revived!")
        else:
            print("Game over.")
            game_running = False
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False


def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

