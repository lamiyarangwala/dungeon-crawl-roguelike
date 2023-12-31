# sets up initial vars like screen size and tileset
# creates entities
# Draws everything
# reacts to players input


#!/usr/bin/env python3

import traceback
import tcod
import color
# importing actions and key presses
from engine import Engine
from entity import Entity
from procgen import generate_dungeon
import copy
import entity_factories

def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30
    max_monsters_per_room = 2
    # keeping track of players position
    #player_x = int(screen_width / 2)
    #player_y = int(screen_height / 2)
    # Use move method from Entity instead!


    tileset = tcod.tileset.load_tilesheet(
        "dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
    )

    player = copy.deepcopy(entity_factories.player)
    engine = Engine(player=player)
    engine.game_map = generate_dungeon(
        max_rooms=max_rooms,
        room_max_size=room_max_size,
        room_min_size=room_min_size,
        map_width=map_width,
        map_height=map_height,
        max_monsters_per_room=max_monsters_per_room,
        engine=engine
    )

    engine.update_fov()
    engine.message_log.add_message(
        'Enter at your own risk, fellow adventurer!', color.welcome_text
    )

    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="MY ROGUELIKE",
        vsync=True,
    ) as context:
        root_console = tcod.Console(screen_width, screen_height, order="F")

        # Drawing function -- makes visual output
        while True:
            root_console.clear()
            engine.event_handler.on_render(console=root_console)
            context.present(root_console)

            try:
                for event in tcod.event.wait():
                    context.convert_event(event)
                    engine.event_handler.handle_events(event)
            except Exception:  # Handle exceptions in game.
                traceback.print_exc()  # Print error to stderr.
                # Then print the error to the message log.
                engine.message_log.add_message(traceback.format_exc(), color.error)

if __name__ == "__main__":
    main()