# Define an enum for all the possible room content
from enum import Enum
from random import randint

class RoomContent(Enum):
    BRONZE_KEY = "bronze key"
    SILVER_KEY = "silver key"
    GOLD_KEY = "gold key"
    UNPULLED_LEVER = "unpulled lever"
    PULLED_LEVER = "pulled lever"
    UNLOCKED_DOOR = "unlocked door"
    OPEN_DOOR = "open door"
    LOCKED_DOOR_WITH_BRONZE_KEY = "locked door with bronze key"
    LOCKED_DOOR_WITH_SILVER_KEY = "locked door with silver key"
    LOCKED_DOOR_WITH_GOLD_KEY = "locked door with gold key"
    GHOST_SISTER_A = "ghost sister A",
    GHOST_SISTER_B = "ghost sister B",
    BLOCKING_GARGOYLE = "blocking gargoyle",
    COOPERATIVE_GARGOYLE = "cooperative gargoyle"


def get_text_for_content(content):
    """
    Returns the text for the given content
    """
    global game_state

    if content == RoomContent.BRONZE_KEY.value:
        return "You see a bronze key on a pedestal."
    elif content == RoomContent.SILVER_KEY.value:
        return "You see a silver key lying on a table ."
    elif content == RoomContent.GOLD_KEY.value:
        prefix = "You see a gold key in a glass case. "
        if game_state.is_lever_pulled:
            return prefix + "The case appears to be open."
        else:
            return prefix + "The case is locked and can not be opened from this room."
    elif content == RoomContent.UNPULLED_LEVER.value:
        return "You see a lever on the wall. It looks like it can be pulled."
    elif content == RoomContent.PULLED_LEVER.value:
        return "You see a lever on the wall. It looks like it has been pulled."
    elif content == RoomContent.UNLOCKED_DOOR.value:
        return "You see a closed door to the east. It is unlocked."
    elif content == RoomContent.OPEN_DOOR.value:
        return "You see an open door to the east."
    elif content == RoomContent.LOCKED_DOOR_WITH_BRONZE_KEY.value:
        return "You see a closed door to the east. It is locked. It's lock has a bronze hue."
    elif content == RoomContent.LOCKED_DOOR_WITH_SILVER_KEY.value:
        return "You see a closed door to the east. It is locked. It's lock has a silver hue."
    elif content == RoomContent.LOCKED_DOOR_WITH_GOLD_KEY.value:
        return "You see a closed door to the east. It is locked. It's lock has a golden hue."
    elif content == RoomContent.GHOST_SISTER_A.value:
        if game_state.difficulty <= 5 or game_state.steps_since_sister_a >= 3:
            return "A ghost appears in the room. She says \"My sister " + game_state.sister_b_name + " must be around here somewhere.\""
        else:
            return "A ghost appears in the room. She says \"I'm not in the mood to talk right now. Come back later.\""
    elif content == RoomContent.GHOST_SISTER_B.value:
        if game_state.difficulty <= 5 or game_state.steps_since_sister_b >= 3:
            return "A ghost appears in the room. She says \"My sister " + game_state.sister_a_name + " must be around here somewhere.\""
        else:
            return "A ghost appears in the room. She says \"I'm not in the mood to talk right now. Come back later.\""
    elif content == RoomContent.BLOCKING_GARGOYLE.value:
        if game_state.gargoyle_sister_question == 0:
            return "A gargoyle blocks your passage to the east. It asks \"What is the name of " + game_state.sister_a_name + "'s sister?\""
        elif game_state.gargoyle_sister_question == 1:
            return "A gargoyle blocks your passage to the east. It asks \"What is the name of " + game_state.sister_b_name + "'s sister?\""
        elif game_state.gargoyle_sister_question == 2:
            return "A gargoyle blocks your passage to the east. It asks \"What are the names of the two sisters who used to live here?\""

    elif content == RoomContent.COOPERATIVE_GARGOYLE.value:
        return "A gargoyle stands to the side, you can continue eastwards."
    else:
        return ""

class Room:
    """
    Represents a room in the game
    """

    def __init__(self, room_type, description, description_postfix, content):
        self.room_type = room_type
        self.description = description
        self.description_postfix = description_postfix
        self.content = content

    def __str__(self):
        return f"Room: {self.room_type}, Description: {self.description}, Description Postfix: {self.description_postfix}, Content: {self.content}"

    def __repr__(self):
        return str(self)
    
    def get_description(self):
        """
        Returns a description of the room
        """
        full_text = self.description
        if self.content:
            full_text += f" {get_text_for_content(self.content)}"
        if self.description_postfix:
            full_text += f" {self.description_postfix}"
        return full_text


sister_a_names = ["Lilith", "Laila", "Luna"]
sister_b_names = ["Mercedes", "Melinoe", "Melissa"]

class GameState:
    """
    Represents the current state of the game including flags for what has been picked up etc
    """

    def __init__(self):
        self.has_bronze_key = False
        self.has_silver_key = False
        self.has_gold_key = False
        self.is_lever_pulled = False
        self.has_lost = False
        self.has_won = False
        self.rooms = []
        self.current_room = 0
        self.sister_a_name = sister_a_names[randint(0, len(sister_a_names)-1)]
        self.sister_b_name = sister_b_names[randint(0, len(sister_b_names)-1)]
        self.steps_since_sister_a = -9999
        self.steps_since_sister_b = -9999
        self.gargoyle_sister_question = randint(0, 1)
        self.difficulty = 0
        self.used_room_fluff_texts = []

    def __str__(self):
        return f"Bronze key: {self.has_bronze_key}, Silver key: {self.has_silver_key}, Gold key: {self.has_gold_key}, Lever: {self.is_lever_pulled}"

    def __repr__(self):
        return str(self)
    
game_state = None

def place_before(current_layout, groups):
    """
    Replaces empty slots in the current layout with entries from groups, respecting order of
    occurrence of items in groups
    """

    open_indexes = []
    index = 0
    for entry in current_layout:
        if entry.room_type == "open slot":
            open_indexes.append(index)
        index = index +1

    for group in groups:
        last_used_index = -1
        entry_number = 0
        assigned_indexes = []
        for entry in group:
            last_possible_index = len(open_indexes)-len(group)+entry_number+1
            possible_indexes = open_indexes[last_used_index+1:last_possible_index]
            meta_index = randint(0, len(possible_indexes)-1)
            last_used_index = (last_used_index + 1) + meta_index
            assigned_indexes.append(possible_indexes[meta_index])
            entry_number = entry_number + 1


        current_entry_index = 0
        for entry in group:
            index_to_remove = assigned_indexes[current_entry_index]
            open_indexes.remove(index_to_remove)
            current_layout[index_to_remove] = entry
            current_entry_index = current_entry_index + 1

    return current_layout

def get_room_fluff_text(difficulty):
    """
    Returns a random text for a given room and index. Makes sure to not re-use options.
    """
    options = [
        "You find yourself in a library. Bookshelfs span all walls from the floor to the ceiling.",
        "The room you are in seems to be a large storage closet, brooms and cleaning material is neatly organized.",
        "You're in a wine cellar of sorts. You notice a subtle musky smell. Barrels are stacked in rows of 5.",
        "This one is a bedroom, with bunks to one side. A closet covers the opposite side.",
        "You enter a study. A desk, stacked with books and papers, seems to have been left untouched for a while. Dust covers most areas.",
        "Now you're in a kitchen, the smell of freshly baked bread fills the room.",
        "You find yourself in a corridor of sorts, checkerboard tiles covers the floor.",
        "A large panorama window is the highlight of this room. Outside you see rolling hills of green. A storm seems to be brewing over there.",
        "Your eyes are drawn to the paintings covering the walls of this room. It seems to be an artists workshop.",
        "This room is clearly the master bedroom. A luxurious double takes up most of the space.",
        "You enter an underground pool area. The room is large. There's no water in the pool.",
        "You're in an attic now. The walls are slanted and you see wooden panels covering both sides and the floor.",
    ]

    global game_state

    available_options = []
    for option_index in range(0, len(options)):
        if not option_index in game_state.used_room_fluff_texts:
            available_options.append(option_index)

    picked_option_index = randint(0, len(available_options)-1)
    picked_option = available_options[picked_option_index]
    game_state.used_room_fluff_texts.append(picked_option)
    return options[picked_option]


def build_room_layout(difficulty):
    """
    Returns a dictionary representing the layout of the rooms in the game
    """

    if difficulty == 0:
        return [
            Room("start", "You are in a dark room. You can see a passage to the east.", "", ""),
            Room("end", "You are in a room with a large treasure chest. You have won the game.", "", "")
        ]

    if difficulty == 1:
        return [
            Room("start", "You are in a dark room. You can see a passage to the east.", "", ""),
            Room("unlocked door", get_room_fluff_text(difficulty), "", RoomContent.UNLOCKED_DOOR.value),
            Room("end", "You are in a room with a large treasure chest. You have won the game.", "", "")
        ]
    
    if difficulty == 2:
        return [
            Room("start", "You are in a dark room. You can see a passage to the east.", "", ""),
            Room("bronze key", get_room_fluff_text(difficulty), "", RoomContent.BRONZE_KEY.value),
            Room("bronze door", "You are in a room with a small fireplace in the corner.", "", RoomContent.LOCKED_DOOR_WITH_BRONZE_KEY.value),
            Room("end", "You are in a room with a large treasure chest. You have won the game.", "", "")
        ]
        
    if difficulty == 3:
        layout = [
            Room("start", "You are in a dark room. You can see a passage to the east.", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("end", "You are in a room with a large treasure chest. You have won the game.", "", "")
        ]
        layout = place_before(layout, [
            [
            Room("bronze key", get_room_fluff_text(difficulty), "", RoomContent.BRONZE_KEY.value),
            Room("bronze door", "You are in a room with a small fireplace in the corner.", "", RoomContent.LOCKED_DOOR_WITH_BRONZE_KEY.value),
            ],
            [
            Room("silver key", get_room_fluff_text(difficulty), "", RoomContent.SILVER_KEY.value),
            Room("silver door", "You are in a room with a small fireplace in the corner.", "", RoomContent.LOCKED_DOOR_WITH_SILVER_KEY.value),
            ],
        ])
        return layout
    
    if difficulty == 4:
        layout = [
            Room("start", "You are in a dark room. You can see a passage to the east.", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("end", "You are in a room with a large treasure chest. You have won the game.", "", "")
        ]
        layout = place_before(layout, [
            [
            Room("bronze key", get_room_fluff_text(difficulty), "", RoomContent.BRONZE_KEY.value),
            Room("bronze door", get_room_fluff_text(difficulty), "", RoomContent.LOCKED_DOOR_WITH_BRONZE_KEY.value),
            ],
            [
            Room("silver key", get_room_fluff_text(difficulty), "", RoomContent.SILVER_KEY.value),
            Room("silver door", get_room_fluff_text(difficulty), "", RoomContent.LOCKED_DOOR_WITH_SILVER_KEY.value),
            ],
            [
            Room("gold key", get_room_fluff_text(difficulty), "", RoomContent.GOLD_KEY.value),
            Room("lever", get_room_fluff_text(difficulty), "", RoomContent.UNPULLED_LEVER.value),
            Room("gold door", get_room_fluff_text(difficulty), "", RoomContent.LOCKED_DOOR_WITH_GOLD_KEY.value),
            ]
        ])
        return layout
    
    if difficulty == 5:
        layout = [
            Room("start", "You are in a dark room. You can see a passage to the east.", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("end", "You are in a room with a large treasure chest. You have won the game.", "", "")
        ]
        layout = place_before(layout, [
            [
            Room("bronze key", get_room_fluff_text(difficulty), "", RoomContent.BRONZE_KEY.value),
            Room("bronze door", get_room_fluff_text(difficulty), "", RoomContent.LOCKED_DOOR_WITH_BRONZE_KEY.value),
            ],
            [
            Room("silver key", get_room_fluff_text(difficulty), "", RoomContent.SILVER_KEY.value),
            Room("silver door", get_room_fluff_text(difficulty), "", RoomContent.LOCKED_DOOR_WITH_SILVER_KEY.value),
            ],
            [
            Room("gold key", get_room_fluff_text(difficulty), "", RoomContent.GOLD_KEY.value),
            Room("lever", get_room_fluff_text(difficulty), "", RoomContent.UNPULLED_LEVER.value),
            Room("gold door", get_room_fluff_text(difficulty), "", RoomContent.LOCKED_DOOR_WITH_GOLD_KEY.value),
            ],
            [
            Room("ghost sister a", get_room_fluff_text(difficulty), "", RoomContent.GHOST_SISTER_A.value),
            Room("ghost sister b", get_room_fluff_text(difficulty), "", RoomContent.GHOST_SISTER_B.value),
            Room("gargoyle", get_room_fluff_text(difficulty), "", RoomContent.BLOCKING_GARGOYLE.value),
            ]
        ])
        return layout

    if difficulty == 6:
        layout = [
            Room("start", "You are in a dark room. You can see a passage to the east.", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("open slot", "", "", ""),
            Room("end", "You are in a room with a large treasure chest. You have won the game.", "", "")
        ]
        layout = place_before(layout, [
            [
            Room("gold key", get_room_fluff_text(difficulty), "", RoomContent.GOLD_KEY.value),
            Room("lever", get_room_fluff_text(difficulty), "", RoomContent.UNPULLED_LEVER.value),
            Room("gold door", get_room_fluff_text(difficulty), "", RoomContent.LOCKED_DOOR_WITH_GOLD_KEY.value),
            ],
            [
            Room("silver key", get_room_fluff_text(difficulty), "", RoomContent.SILVER_KEY.value),
            Room("silver door", get_room_fluff_text(difficulty), "", RoomContent.LOCKED_DOOR_WITH_SILVER_KEY.value),
            ],
            [
            Room("ghost sister a", get_room_fluff_text(difficulty), "", RoomContent.GHOST_SISTER_A.value),
            Room("bronze key", get_room_fluff_text(difficulty), "", RoomContent.BRONZE_KEY.value),
            Room("bronze door", get_room_fluff_text(difficulty), "", RoomContent.LOCKED_DOOR_WITH_BRONZE_KEY.value),
            Room("ghost sister b", get_room_fluff_text(difficulty), "", RoomContent.GHOST_SISTER_B.value),
            Room("gargoyle", get_room_fluff_text(difficulty), "", RoomContent.BLOCKING_GARGOYLE.value),
            ]
        ])
        game_state.gargoyle_sister_question = 2
        return layout

def loose_game():
    """
    Sets the game to lost
    """
    global game_state
    game_state.has_lost = True
    print("You have lost the game")

def win_game():
    """
    Sets the game to won
    """
    global game_state
    game_state.has_won = True
    print("You have won the game")

def enter_room(room_index):
    """
    Enters the room with the given index
    """
    global game_state

    if room_index < 0 or room_index >= len(game_state.rooms):
        print("Action is not possible")
        loose_game()
        return
    
    if room_index == len(game_state.rooms) - 1:
        win_game()
        return
    
    room = game_state.rooms[room_index]
    if room.content == RoomContent.GHOST_SISTER_A.value:
        if game_state.steps_since_sister_a < 0:
            game_state.steps_since_sister_a = 0
    else:
        game_state.steps_since_sister_a = game_state.steps_since_sister_a + 1
    
    if room.content == RoomContent.GHOST_SISTER_B.value:
        if game_state.steps_since_sister_b < 0:
            game_state.steps_since_sister_b = 0
    else:
        game_state.steps_since_sister_b = game_state.steps_since_sister_b + 1
    
    
    game_state.current_room = room_index
    print(room.get_description())


def start_game(difficulty):
    """
    Starts the game with the given difficulty
    """

    global game_state

    game_state = GameState()
    game_state.difficulty = difficulty
    room_layout = build_room_layout(difficulty)
    game_state.rooms = room_layout

    print("Game has started in difficulty", difficulty)
    enter_room(0)

def go_east():
    """
    Moves the player to the room to the east
    """
    global game_state

    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return
    
    room = game_state.rooms[game_state.current_room]
    # Check if there is an unopened door anywhere in the content of the current room
    # content is a list, so we need to see if we find a matching index
    content = room.content
    blocking_doors = [
        RoomContent.UNLOCKED_DOOR.value, 
        RoomContent.LOCKED_DOOR_WITH_BRONZE_KEY.value, 
        RoomContent.LOCKED_DOOR_WITH_SILVER_KEY.value,
        RoomContent.LOCKED_DOOR_WITH_GOLD_KEY.value
    ]
    if content in blocking_doors:
        print("You can't go east. There is an unopened door to the east.")
        loose_game()
        return
    elif content == RoomContent.BLOCKING_GARGOYLE:
        print("You can't go east. The gargoyle blocks your way.")
        loose_game()
        return

    enter_room(game_state.current_room + 1)

def go_west():
    """
    Moves the player to the room to the west
    """
    global game_state

    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return    


    enter_room(game_state.current_room - 1)

def open_door():
    """
    Opens a door in the current room, if possible.
    """

    global game_state
    
    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return
    
    room = game_state.rooms[game_state.current_room]
    # Check if there is an unopened door anywhere in the content of the current room
    content = room.content
    if content == RoomContent.UNLOCKED_DOOR.value:
        print("You open the door.")
        # Remove the door from the room content
        room.content = RoomContent.OPEN_DOOR.value
        print(room.get_description())
    else:
        print("There is no door here.")
        loose_game()
    return

def pull_lever():
    """
    Pulls a lever in the current room, if possible.
    """

    global game_state
    
    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return
    
    room = game_state.rooms[game_state.current_room]
    # Check if there is an unopened door anywhere in the content of the current room
    content = room.content
    if content == RoomContent.UNPULLED_LEVER.value:
        print("You pull the lever.")
        game_state.is_lever_pulled = True
        room.content = RoomContent.PULLED_LEVER.value
        print(room.get_description())
    else:
        print("There is no lever here.")
        loose_game()
    return

def speak(text):
    """
    Speaks some words. This is always possible.
    """

    global game_state
    
    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return
    
    room = game_state.rooms[game_state.current_room]
    if room.content == RoomContent.BLOCKING_GARGOYLE.value:
        if game_state.gargoyle_sister_question == 0:
            if text == game_state.sister_b_name:
                print("The gargoyle nods. \"Correct.\". It moves to the side.")
                room.content = RoomContent.COOPERATIVE_GARGOYLE
            else:
                print("The gargoyle shakes it's head. \"That's wrong.\".")
                loose_game()
        elif game_state.gargoyle_sister_question == 1:
            if text == game_state.sister_a_name:
                print("The gargoyle nods. \"Correct.\". It moves to the side.")
                room.content = RoomContent.COOPERATIVE_GARGOYLE
            else:
                print("The gargoyle shakes it's head. \"That's wrong.\".")
                loose_game()
        elif game_state.gargoyle_sister_question == 2:
            if text == game_state.sister_a_name + " and " + game_state.sister_b_name or \
            text == game_state.sister_b_name + " and " + game_state.sister_a_name:
                print("The gargoyle nods. \"Correct.\". It moves to the side.")
                room.content = RoomContent.COOPERATIVE_GARGOYLE
            else:
                print("The gargoyle shakes it's head. \"That's wrong.\".")
                loose_game()


def get_room_type():
    """
    Returns what type of room you are currently in. Does not work in difficulties 7+.
    """

    global game_state
        
    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return

    if game_state.difficulty >= 7:
        print("getRoomType can not be used in difficulty 7+.")
        loose_game()
        return
    
    room = game_state.rooms[game_state.current_room]
    return room.room_type


def get_room_content():
    """
    Returns what is in the current room. Does not work in difficulties 7+.
    """

    global game_state
    
    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return
    
    if game_state.difficulty >= 7:
        print("getRoomType can not be used in difficulty 7+.")
        loose_game()
        return
    
    
    room = game_state.rooms[game_state.current_room]
    return room.content

def get_room_description():
    """
    Returns a text description of the current room. This is always allowed.
    """
    
    global game_state

    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return
    
    room = game_state.rooms[game_state.current_room]
    return room.get_description()

def take_item(item_name):
    """
    Picks up an item from the current room.
    """

    global game_state
    
    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return

    room = game_state.rooms[game_state.current_room]
    if room.content != item_name:
        print("There is no item called", item_name, "in the current room.")
        loose_game()
        return
    
    if item_name == RoomContent.BRONZE_KEY.value:
        game_state.has_bronze_key = True
    elif item_name == RoomContent.SILVER_KEY.value:
        game_state.has_silver_key = True
    elif item_name == RoomContent.GOLD_KEY.value:
        game_state.has_gold_key = True
    room.content = None
    print("You have picked up a", item_name)

def use_item(item_name):
    """
    Uses an item in the current room.
    """

    global game_state
        
    if game_state.has_lost or game_state.has_won:
        print("Game is over")
        return
    
    room = game_state.rooms[game_state.current_room]

    has_item = False
    if item_name == RoomContent.BRONZE_KEY.value:
        has_item = game_state.has_bronze_key
    elif item_name == RoomContent.SILVER_KEY.value:
        has_item = game_state.has_silver_key
    elif item_name == RoomContent.GOLD_KEY.value:
        has_item = game_state.has_gold_key

    if not has_item:
        print("You do not have ", item_name)
        loose_game()
        return

    if item_name == RoomContent.BRONZE_KEY.value:
        game_state.has_bronze_key = False
    elif item_name == RoomContent.SILVER_KEY.value:
        game_state.has_silver_key = False
    elif item_name == RoomContent.GOLD_KEY.value:
        game_state.has_gold_key = False

    room.content = RoomContent.UNLOCKED_DOOR.value
    print("You have used your", item_name, "to unlock the door")
    print(room.get_description())