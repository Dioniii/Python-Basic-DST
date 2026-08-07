from pgzero.builtins import Rect, keyboard, keys

from platformer import MAP_HEIGHT, MAP_ORIGIN, MAP_WIDTH, TILE_SIZE, TileMap


PLAYER_SIZE = (14, 28)
MOVE_SPEED = 3
GRAVITY = 1
MAX_FALL_SPEED = 12
JUMP_SPEED = -10

PLAYER_COLOR = (204, 86, 45)
PLAYER_BORDER = (255, 245, 216)
TEXT_COLOR = (255, 245, 216)

# Add another dictionary here after exporting its five CSV layers. The door
# advances through this list in order.
LEVELS = (
    {
        "name": "untitled",
        "spawn": (4, 11),
    },
)

player = Rect((0, 0), PLAYER_SIZE)
level = None
current_level_index = 0
velocity_y = 0
on_ground = False
has_key = False
state = "playing"


def reset_player():
    """Return the player to the map's starting platform."""

    global velocity_y, on_ground

    spawn_column, spawn_floor_row = LEVELS[current_level_index]["spawn"]
    player.x = MAP_ORIGIN[0] + spawn_column * TILE_SIZE
    player.bottom = MAP_ORIGIN[1] + spawn_floor_row * TILE_SIZE
    velocity_y = 0
    on_ground = False


def load_level(level_index):
    """Load one level and reset its player, key, and game state."""

    global level, current_level_index, has_key, state

    current_level_index = level_index
    level = TileMap(LEVELS[level_index]["name"])
    has_key = False
    state = "playing"
    reset_player()


def start():
    """Begin again from the first configured level."""

    load_level(0)


def advance_level():
    """Enter the next configured level, or finish after the final door."""

    global state

    next_level_index = current_level_index + 1

    if next_level_index < len(LEVELS):
        load_level(next_level_index)
    else:
        state = "won"


def move_horizontal(amount):
    player.x += amount

    for wall in level.solid_rects:
        if not player.colliderect(wall):
            continue

        if amount > 0:
            player.right = wall.left
        elif amount < 0:
            player.left = wall.right

    player.left = max(player.left, level.bounds.left)
    player.right = min(player.right, level.bounds.right)


def move_vertical():
    global velocity_y, on_ground

    velocity_y = min(velocity_y + GRAVITY, MAX_FALL_SPEED)
    player.y += velocity_y
    on_ground = False

    for wall in level.solid_rects:
        if not player.colliderect(wall):
            continue

        if velocity_y > 0:
            player.bottom = wall.top
            on_ground = True
        elif velocity_y < 0:
            player.top = wall.bottom

        velocity_y = 0


def update():
    global has_key, state, velocity_y

    if level is None or state != "playing":
        return

    horizontal_movement = 0

    if keyboard.left:
        horizontal_movement -= MOVE_SPEED
    if keyboard.right:
        horizontal_movement += MOVE_SPEED

    move_horizontal(horizontal_movement)
    move_vertical()

    if level.player_touches_hazard(player):
        state = "lost"
        velocity_y = 0
        return

    if level.collect_keys_at(player):
        has_key = True

    if has_key and level.player_is_at_exit(player):
        advance_level()
        return

    if player.top > level.bounds.bottom:
        state = "lost"
        velocity_y = 0


def on_key_down(key):
    global velocity_y

    if state == "playing" and on_ground and key in (keys.UP, keys.SPACE):
        velocity_y = JUMP_SPEED
    elif state == "lost" and key == keys.R:
        load_level(current_level_index)
    elif state == "won" and key == keys.R:
        start()


def draw_state_message(screen, title, instruction):
    message_panel = Rect(
        ((MAP_WIDTH - 370) // 2, (MAP_HEIGHT - 100) // 2),
        (370, 100),
    )
    screen.draw.filled_rect(message_panel, (12, 25, 42))
    screen.draw.rect(message_panel, PLAYER_BORDER)
    screen.draw.text(
        title,
        center=(MAP_WIDTH // 2, message_panel.y + 30),
        color=TEXT_COLOR,
        fontsize=34,
    )
    screen.draw.text(
        instruction,
        center=(MAP_WIDTH // 2, message_panel.y + 70),
        color=TEXT_COLOR,
        fontsize=20,
    )


def draw(screen):
    screen.fill((12, 25, 42))

    if level is None:
        return

    level.draw(screen)
    screen.draw.filled_rect(player, PLAYER_COLOR)
    screen.draw.rect(player, PLAYER_BORDER)

    objective = "KEY COLLECTED - FIND THE DOOR" if has_key else "FIND THE KEY"
    screen.draw.text(
        objective,
        midtop=(MAP_WIDTH // 2, 8),
        color=TEXT_COLOR,
        fontsize=18,
        shadow=(1, 1),
        scolor=(0, 0, 0),
    )

    if state == "lost":
        draw_state_message(screen, "YOU DIED", "Press R to restart")
    elif state == "won":
        draw_state_message(screen, "LEVEL COMPLETE", "Press R to play again")
