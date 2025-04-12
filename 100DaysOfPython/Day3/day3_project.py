import json
import random
from abc import ABC, abstractmethod

class Displayable(ABC):
    @abstractmethod
    def display(self):
        pass

class GameObject(Displayable):
    def __init__(self, id, name, description, art):
        self.name = name
        self.description = description
        self.art = art
        self.id = id

    def display(self):
        ConsoleText.print_colorized(f"{self.art}", color="green", style="bold")
        ConsoleText.print_colorized(f"{self.name}: {self.description}", color="yellow", style="bold")

class UsableItem(GameObject):
    def __init__(self, id, name, description, art):
        super().__init__(id, name, description, art)

    def use_item(self, player):
        # Logic to use the item
        print(f"{self.name} used!")

class UserStats(Displayable):
    def __init__(self, health, strength, agility):
        self.health = health
        self.strength = strength
        self.agility = agility

    def display(self):
        print(f"Health: {self.health}, Strength: {self.strength}, Agility: {self.agility}")

class ItemStats(Displayable):
    def __init__(self, attack, defense, durability):
        self.attack = attack
        self.defense = defense
        self.durability = durability

    def display(self):
        print(f"Attack: {self.attack}, Defense: {self.defense}, Durability: {self.durability}")

# Assuming the game has items, we can create an Item class
# that inherits from GameObject.
# Items can be use only like a key or a book
# they can also be weapons and armor
class Item(GameObject, Displayable):
    def __init__(self, id, name, description, art, item_type):
        super().__init__(id, name, description, art)
        self.item_type = item_type
        
    def display(self):
        super().display()

#stats must be of type ItemStats
class EquipableItem(Item):
    def __init__(self, id, name, description, art, item_type, stats: ItemStats):
        super().__init__(id, name, description, art, item_type)
        self.stats = stats

    def equip(self, player):
        # Logic to equip the item to the player
        player.add_to_inventory(self)

    def display(self):
        super().display()
        self.stats.display()

class Player(GameObject):
    def __init__(self, name, description, stats: UserStats):
        super().__init__(id=random.randint, name=name, description=description, art="")
        self.user_stats = stats  # UserStats object
        self.inventory = [Item]

    def add_to_inventory(self, item: Item):
        self.inventory.append(item)

    def display_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            item.display()

class Enemy(GameObject):
    def __init__(self, id, name, description, art, stats: UserStats, item_stats: ItemStats):
        super().__init__(id, name, description, art)
        self.user_stats = stats
        self.item_stats = item_stats

    def display(self):
        super().display()
        print(f"Stats: {self.stats}")

# Choice can require an item to be used
# a choice can also give items to the player
class DialogueChoice(Displayable):
    def __init__(self, text, action=None, next_dialogue=None, item_required=None, item_given=None):
        self.item_given = item_given
        self.item_required = item_required
        self.text = text
        self.next_dialogue = next_dialogue
        self.action = action

    def display(self):
        ConsoleText.print_colorized(self.text, color="cyan", style="bold")
        
    def execute_action(self, game_controller):
        if self.action:
            # Here you can implement the action logic, e.g., updating inventory or game state
            game_controller.inventory.append(self.action)  # Example action: add to inventory
        else:
            print("No action associated with this choice.")

class Dialogue(Displayable):
    def __init__(self, text, choices:list[DialogueChoice], enemy:Enemy=None):
        self.enemy = enemy
        self.text = text
        self.choices = choices

    def display(self):
        if self.enemy:
            self.enemy.display()
            self.enemy.user_stats.display()
        else:
            ConsoleText.print_colorized(self.text, color="green", style="bold")
            ConsoleText.print_colorized("Choices:", color="green", style="bold")
            for i, choice in enumerate(self.choices, start=1):
                choice.display()

    def get_connections(self):
        return [choice.next_dialogue for choice in self.choices if choice.next_dialogue]

class attackDialogue(Dialogue):
    def __init__(self, text, choices, enemy:Enemy=None):
        super().__init__(text, choices, enemy)
        self.enemy = enemy

    def display(self):
        print(self.text)
        if self.enemy:
            print(f"Enemy: {self.enemy.name}")
            self.enemy.user_stats.display()

class GameController:
    def __init__(self, dialogues, items, start_key):
        self.dialogues = dialogues
        self.items = items
        self.current_dialogue = self.dialogues[start_key]
        self.player = Player("Player", "The main character of the game.", UserStats(100, 10, 5))

    def display_map(self):
        print("\nGame Map:")
        visited = set()
        self._display_map_recursive("start", visited, "")

    def _display_map_recursive(self, dialogue_key, visited, prefix):
        if dialogue_key in visited:
            print(f"{prefix}(Already visited)")
            return
        visited.add(dialogue_key)

        dialogue = self.dialogues.get(dialogue_key)
        if dialogue:
            print(f"{prefix}- {dialogue_key}: {dialogue.text}")
            for i, choice in enumerate(dialogue.choices):
                # Update the prefix for child nodes
                next_prefix = prefix + ("│   " if i < len(dialogue.choices) - 1 else "    ")
                branch = "├── " if i < len(dialogue.choices) - 1 else "└── "
                if choice.next_dialogue:
                    print(f"{prefix}{branch}{choice.text}")
                    self._display_map_recursive(choice.next_dialogue, visited, next_prefix)
                else:
                    print(f"{prefix}{branch}(End)")

    def display_global_options(self):
        ConsoleText.print_colorized("\nGlobal Options: [i. View Inventory] [m. View Map] [q. Quit Game]", color="blue", style="bold")

    def handle_global_option(self, option):
        if option == "i":
            print("\nInventory:", self.inventory if self.inventory else "Your inventory is empty.")
        elif option == "m":
            self.display_map()
        elif option == "q":
            print("\nThanks for playing!")
            exit()
        else:
            print("\nInvalid global option. Try again.")

    def play_game(self):
        while self.current_dialogue:
            self.current_dialogue.display()
            self.display_global_options()
            user_input = input("\nEnter the number of your choice or a global option: ").strip()
            if user_input.isdigit():
                choice = int(user_input) - 1
                if 0 <= choice < len(self.current_dialogue.choices):
                    next_key = self.current_dialogue.choices[choice].next_dialogue
                    self.current_dialogue = self.dialogues.get(next_key)
                    if self.current_dialogue is None:
                        ConsoleText.print_colorized("Game Over!", color="red", style="bold")
                else:
                    ConsoleText.print_colorized("Invalid choice. Try again.", color="yellow")
            else:
                self.handle_global_option(user_input)

def load_items_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    items = []
    for item_data in data:
        if item_data["item_type"] in ["weapon", "armor"]:
            items.append(EquipableItem(
                id=item_data["id"],
                name=item_data["name"],
                description=item_data["description"],
                art=item_data["art"],
                item_type=item_data["item_type"],
                stats=item_data.get("stats", {})
            ))
        else:
            items.append(Item(
                id=item_data["id"],
                name=item_data["name"],
                description=item_data["description"],
                art=item_data["art"],
                item_type=item_data["item_type"]
            ))
    return items

def load_dialogues_from_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    dialogues = {}
    for key, value in data.items():
        choices = [DialogueChoice(choice["text"], choice["next"]) for choice in value["choices"]]
        dialogues[key] = Dialogue(value["text"], choices)
    return dialogues

class ConsoleText:
    COLORS = {
        "black": "\033[30m",
        "red": "\033[31m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[34m",
        "magenta": "\033[35m",
        "cyan": "\033[36m",
        "white": "\033[37m",
        "reset": "\033[0m"
    }

    STYLES = {
        "bold": "\033[1m",
        "underline": "\033[4m",
        "reset": "\033[0m"
    }

    @staticmethod
    def colorize(text, color="reset", style=None):
        color_code = ConsoleText.COLORS.get(color, ConsoleText.COLORS["reset"])
        style_code = ConsoleText.STYLES.get(style, "")
        reset_code = ConsoleText.COLORS["reset"]
        return f"{color_code}{style_code}{text}{reset_code}"

    @staticmethod
    def print_colorized(text, color="reset", style=None):
        print(ConsoleText.colorize(text, color, style))

# Load dialogues from JSON
dialogues = load_dialogues_from_json("dialogues.json")
# Load items from JSON
items = load_items_from_json("items.json")

# Start the game
game_controller = GameController(dialogues, items, "start")
game_controller.play_game()
