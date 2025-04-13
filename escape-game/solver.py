from game import start_game, go_east, go_west, open_door, take_item, use_item, speak, pull_lever, get_room_content, get_room_type, get_room_description
def take_step():
    """
    This function takes a step in the game
    """
    print("Evaluating what to do next.")

    room_type = get_room_type()
    room_content = get_room_content()
    if room_type == "start":
        go_east()
        return True
    elif room_type == "end":
        return False
    elif room_content == "unlocked door":
        open_door()
        return True
    elif room_content == "open door":
        go_east()
        return True
    elif room_content == None:
        go_east()
        return True
    else:
        return False

def solve_game(difficulty):
    """
    This function automatically solves a game at the passed in difficulty
    """
    start_game(difficulty)

    is_running = True
    while is_running == True:
        is_running = take_step()

solve_game(0)