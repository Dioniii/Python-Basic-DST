from pgzero.builtins import Rect, keyboard, keys

from enemy import (
    create_enemies,
    draw_enemies,
    player_touches_enemy,
    remove_bullet_hits,
    update_enemies,
)
from platformer import MAP_HEIGHT, MAP_ORIGIN, MAP_WIDTH, TILE_SIZE, TileMap


PLAYER_SIZE = (14, 28)
MOVE_SPEED = 3
GRAVITY = 1
MAX_FALL_SPEED = 12
JUMP_SPEED = -14
BULLET_SIZE = (6, 3)
BULLET_SPEED = 7

PLAYER_BORDER = (255, 245, 216)
TEXT_COLOR = (255, 245, 216)
BULLET_COLOR = (245, 177, 66)

PLAYER_SPRITE_SIZE = (40, 36)
PLAYER_IDLE_IMAGES = (
    "robot/robot_red_drive_1",
    "robot/robot_red_drive_1_left",
)
PLAYER_DRIVE_IMAGES = (
    (
        "robot/robot_red_drive_1",
        "robot/robot_red_drive_2",
    ),
    (
        "robot/robot_red_drive_1_left",
        "robot/robot_red_drive_2_left",
    ),
)
PLAYER_JUMP_IMAGES = (
    "robot/robot_red_jump",
    "robot/robot_red_jump_left",
)
PLAYER_HURT_IMAGES = (
    "robot/robot_red_hurt",
    "robot/robot_red_hurt_left",
)
ANIMATION_FRAME_LENGTH = 8

LEVELS = (
    {
        "name": "untitled",
        "spawn": (4, 11),
        "collectible_name": "KEY",
        "has_enemies": False,
        "layers": {
            "background": "levels/level1/untitled_background items.csv",
            "platforms": "levels/level1/untitled_platforms.csv",
            "obstacles": "levels/level1/untitled_obsticle.csv",
            "scaffolding": "levels/level1/untitled_scaffolding.csv",
            "doors": "levels/level1/untitled_door.csv",
            "collectibles": "levels/level1/untitled_key.csv",
        },
    },
    {
        "name": "level2",
        "spawn": (1, 19),
        "collectible_name": "CHEST",
        "has_enemies": True,
        "layers": {
            "background": "levels/level2/level2_background.csv",
            "platforms": "levels/level2/level2_platforms.csv",
            "obstacles": "levels/level2/level2_obsticle.csv",
            "scaffolding": "levels/level2/level2_scaffolding.csv",
            "doors": "levels/level2/level2_door.csv",
            "collectibles": "levels/level2/level2_chest.csv",
        },
    },
)

player = Rect((0, 0), PLAYER_SIZE)
level = None
current_level_index = 0
velocity_y = 0
on_ground = False
has_key = False
state = "playing"
animation_tick = 0
facing_left = False
bullets = []
enemies = []


class Bullet:
    def __init__(self, position, direction):
        self.rect = Rect(position, BULLET_SIZE)
        self.velocity_x = BULLET_SPEED * direction


def reset_player():
    """Return the player to the map's starting platform."""

    global velocity_y, on_ground, animation_tick, facing_left

    spawn_column, spawn_floor_row = LEVELS[current_level_index]["spawn"]
    player.x = MAP_ORIGIN[0] + spawn_column * TILE_SIZE
    player.bottom = MAP_ORIGIN[1] + spawn_floor_row * TILE_SIZE
    velocity_y = 0
    on_ground = True
    animation_tick = 0
    facing_left = False


def load_level(level_index):
    """Load one level and reset its player, key, and game state."""

    global level, current_level_index, has_key, state, bullets, enemies

    current_level_index = level_index
    level = TileMap(LEVELS[level_index]["layers"])
    has_key = False
    state = "playing"
    bullets = []
    enemies = (
        create_enemies(level.layers["platforms"], TILE_SIZE)
        if LEVELS[level_index]["has_enemies"]
        else []
    )
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
        state = "game_over"


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


def shoot_bullet():
    direction = -1 if facing_left else 1
    bullet_y = player.centery - BULLET_SIZE[1] // 2

    if facing_left:
        bullet_x = player.left - BULLET_SIZE[0]
    else:
        bullet_x = player.right

    bullets.append(Bullet((bullet_x, bullet_y), direction))


def update_bullets():
    active_bullets = []

    for bullet in bullets:
        bullet.rect.x += bullet.velocity_x

        outside_level = (
            bullet.rect.right < level.bounds.left
            or bullet.rect.left > level.bounds.right
        )
        hit_solid = bullet.rect.collidelist(level.solid_rects) != -1

        if not outside_level and not hit_solid:
            active_bullets.append(bullet)

    bullets[:] = active_bullets


def update():
    global has_key, state, velocity_y, animation_tick, facing_left

    if level is None or state != "playing":
        return

    horizontal_movement = 0

    if keyboard.left:
        horizontal_movement -= MOVE_SPEED
    if keyboard.right:
        horizontal_movement += MOVE_SPEED

    if horizontal_movement < 0:
        facing_left = True
    elif horizontal_movement > 0:
        facing_left = False

    move_horizontal(horizontal_movement)
    move_vertical()
    update_bullets()
    update_enemies(enemies)
    remove_bullet_hits(enemies, bullets)

    if horizontal_movement != 0 and on_ground:
        animation_tick += 1
    else:
        animation_tick = 0

    if level.player_touches_hazard(player):
        state = "lost"
        velocity_y = 0
        return

    if player_touches_enemy(player, enemies):
        state = "lost"
        velocity_y = 0
        return

    if level.collect_items_at(player):
        has_key = True

    if has_key and level.player_is_at_exit(player):
        advance_level()
        return

    if player.top > level.bounds.bottom:
        state = "lost"
        velocity_y = 0


def on_key_down(key):
    global velocity_y

    if state == "playing" and on_ground and key == keys.UP:
        velocity_y = JUMP_SPEED
    elif state == "playing" and key == keys.SPACE:
        shoot_bullet()
    elif state == "lost" and key == keys.R:
        load_level(current_level_index)
    elif state == "game_over" and key == keys.R:
        return "menu"

    return None


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


def get_player_image():
    if state == "lost":
        return PLAYER_HURT_IMAGES[facing_left]
    if not on_ground:
        return PLAYER_JUMP_IMAGES[facing_left]
    if keyboard.left or keyboard.right:
        frame_number = (animation_tick // ANIMATION_FRAME_LENGTH) % 2
        return PLAYER_DRIVE_IMAGES[facing_left][frame_number]
    return PLAYER_IDLE_IMAGES[facing_left]


def draw(screen):
    screen.fill((12, 25, 42))

    if level is None:
        return

    level.draw(screen)
    draw_enemies(screen, enemies)
    sprite_x = player.centerx - PLAYER_SPRITE_SIZE[0] // 2
    sprite_y = player.bottom - PLAYER_SPRITE_SIZE[1]
    screen.blit(get_player_image(), (sprite_x, sprite_y))

    for bullet in bullets:
        screen.draw.filled_rect(bullet.rect, BULLET_COLOR)

    collectible_name = LEVELS[current_level_index]["collectible_name"]
    objective = (
        "DOOR UNLOCKED - FIND THE DOOR"
        if has_key
        else f"FIND THE {collectible_name}"
    )
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
    elif state == "game_over":
        draw_state_message(screen, "GAME OVER", "Press R for main menu")
