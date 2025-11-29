"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: [Your Name Here]

AI Usage: Loading quest and item data from text files.

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # 1. Try opening file
    try:
        with open(filename, "r") as f:
            try:
                content = f.read()
            except Exception:
                raise CorruptedDataError("Quest file is unreadable or corrupted.")
    except FileNotFoundError:
        raise MissingDataFileError(f"Quest file not found: {filename}")
    # 2. Split quests by blank lines
    blocks = [block.strip() for block in content.split("\n\n") if block.strip()]

    quests = {}

    required_fields = [
        "QUEST_ID", "TITLE", "DESCRIPTION",
        "REWARD_XP", "REWARD_GOLD", "REQUIRED_LEVEL",
        "PREREQUISITE"
    ]
    # 3. Parse each block
    for block in blocks:
        lines = block.split("\n")
        quest_data = {}

        for line in lines:
            if ":" not in line:
                raise InvalidDataFormatError(f"Invalid line: {line}")

            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()

            quest_data[key] = value
        # 4. Validate required fields
        for req in required_fields:
            if req not in quest_data:
                raise InvalidDataFormatError(f"Missing field {req} in quest block: {block}")

        # Convert numbers
        try:
            reward_xp = int(quest_data["REWARD_XP"])
            reward_gold = int(quest_data["REWARD_GOLD"])
            required_level = int(quest_data["REQUIRED_LEVEL"])
        except ValueError:
            raise InvalidDataFormatError("XP, gold, or level field is not a valid number.")
        prerequisite = quest_data["PREREQUISITE"]
        # Build final quest dict entry
        quests[quest_data["QUEST_ID"]] = {
            "title": quest_data["TITLE"],
            "description": quest_data["DESCRIPTION"],
            "reward_xp": reward_xp,
            "reward_gold": reward_gold,
            "required_level": required_level,
            "prerequisite": prerequisite
        }

    return quests
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    
    

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    with open(filename, "r") as f:
        try:
            content = f.read()
        except Exception:
            raise CorruptedDataError("Item file is unreadable or corrupted.")
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    pass

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    if not all (key in quest_dict for key in [
        "quest_id", "title", "description",
        "reward_xp", "reward_gold", "required_level",
        "prerequisite"
    ]):
        raise InvalidDataFormatError("Quest data missing required fields.")
    else:
        return True
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers


def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    if not all (key in item_dict for key in [
        "item_id", "name", "type",
        "effect", "cost", "description"
    ]):
        raise InvalidDataFormatError("Item data missing required fields.")
    if item_dict["type"] not in ["weapon", "armor", "consumable"]:
        raise InvalidDataFormatError(f"Invalid item type: {item_dict['type']}")
    return True
    # TODO: Implement validation
    pass

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    if not os.path.exists("data/"):
        os.makedirs("data/")
    quest_file = "data/quests.txt"
    item_file = "data/items.txt"
    if not os.path.exists(quest_file):
        with open(quest_file, "w") as f:
            f.write(
                "QUEST_ID: sample_quest\n"
                "TITLE: Sample Quest\n"
                "DESCRIPTION: This is a sample quest description.\n"
                "REWARD_XP: 100\n"
                "REWARD_GOLD: 50\n"
                "REQUIRED_LEVEL: 1\n"
                "PREREQUISITE: NONE\n"
            )
    if not os.path.exists(item_file):
        with open(item_file, "w") as f:
            f.write(
                "ITEM_ID: sample_item\n"
                "NAME: Sample Item\n"
                "TYPE: consumable\n"
                "EFFECT: health:20\n"
                "COST: 25\n"
                "DESCRIPTION: This is a sample item description.\n"
            )
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """

    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    pass

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    required = ["ITEM_ID", "NAME", "DESCRIPTION", "VALUE", "TYPE"]
    item = {}

    for line in lines:
        try:
            key, value = map(str.strip, line.split(":", 1))
        except ValueError:
            raise InvalidDataFormatError(f"Invalid line: {line}")
        item[key] = value

    missing = [f for f in required if f not in item]
    if missing:
        raise InvalidDataFormatError(f"Missing fields: {', '.join(missing)}")
    
    try:
        return {
            "item_id": item["ITEM_ID"],
            "name": item["NAME"],
            "description": item["DESCRIPTION"],
            "value": int(item["VALUE"]),
            "type": item["TYPE"].lower()
        }
    except ValueError:
        raise InvalidDataFormatError("VALUE must be an integer.")
    # TODO: Implement parsing logic
    pass

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    # create_default_data_files()
    
    # Test loading quests
    # try:
    #     quests = load_quests()
    #     print(f"Loaded {len(quests)} quests")
    # except MissingDataFileError:
    #     print("Quest file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid quest format: {e}")
    
    # Test loading items
    # try:
    #     items = load_items()
    #     print(f"Loaded {len(items)} items")
    # except MissingDataFileError:
    #     print("Item file not found")
    # except InvalidDataFormatError as e:
    #     print(f"Invalid item format: {e}")

