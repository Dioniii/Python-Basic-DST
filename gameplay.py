"""Gameplay state and movement for the tile-map level."""

from pgzero.builtins import Rect, keyboard, keys

from platformer import MAP_ORIGIN, TILE_SIZE, TileMap


PLAYER_SIZE = (14, 28)
PLAYER_START_COLUMN = 7
PLAYER_START_FLOOR_ROW = 16
MOVE_SPEED = 3
GRAVITY = 1
MAX_FALL_SPEED = 12
JUMP_SPEED = -10

PLAYER_COLOR = (204, 86, 45)
PLAYER_BORDER = (255, 245, 216)
TEXT_COLOR = (255, 245, 216)

player = Rect((0, 0), PLAYER_SIZE)
level = None
velocity_y = 0
on_ground = False
has_key = False
state = "playing"


def reset_player():
    """Return the player to the map's starting platform."""

    global velocity_y, on_ground

    player.x = MAP_ORIGIN[0] + PLAYER_START_COLUMN * TILE_SIZE
    player.bottom = MAP_ORIGIN[1] + PLAYER_START_FLOOR_ROW * TILE_SIZE
    velocity_y = 0
    on_ground = False


def start():
    """Load a fresh copy of the level whenever Start Game is selected."""

    global level, has_key, state

    level = TileMap()
    has_key = False
    state = "playing"
    reset_player()


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
    global has_key, state

    if level is None or state != "playing":
        return

    horizontal_movement = 0

    if keyboard.left:
        horizontal_movement -= MOVE_SPEED
    if keyboard.right:
        horizontal_movement += MOVE_SPEED

    move_horizontal(horizontal_movement)
    move_vertical()

    if level.collect_keys_at(player):
        has_key = True

    if has_key and level.player_is_at_exit(player):
        state = "won"

    if player.top > level.bounds.bottom:
        reset_player()


def on_key_down(key):
    global velocity_y

    if state == "playing" and on_ground and key in (keys.UP, keys.SPACE):
        velocity_y = JUMP_SPEED
    elif state == "won" and key == keys.R:
        start()


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
        midtop=(400, 8),
        color=TEXT_COLOR,
        fontsize=18,
        shadow=(1, 1),
        scolor=(0, 0, 0),
    )

    if state == "won":
        screen.draw.filled_rect(Rect((215, 170), (370, 100)), (12, 25, 42))
        screen.draw.text(
            "LEVEL COMPLETE",
            center=(400, 200),
            color=TEXT_COLOR,
            fontsize=34,
        )
        screen.draw.text(
            "Press R to play again",
            center=(400, 240),
            color=TEXT_COLOR,
            fontsize=20,
        )
