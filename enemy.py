from pgzero.builtins import Rect


ENEMY_SIZE = (14, 28)
ENEMY_SPRITE_SIZE = (32, 36)
ENEMY_SPEED = 1
ANIMATION_FRAME_LENGTH = 6
MIN_PLATFORM_TILES = 2

RIGHT_WALK_IMAGES = tuple(
    f"enemy/enemy_robot_walk_{frame}" for frame in range(8)
)
LEFT_WALK_IMAGES = tuple(
    f"enemy/enemy_robot_walk_{frame}_left" for frame in range(8)
)


class Enemy:

    def __init__(self, patrol_left, patrol_right, platform_top, direction=1):
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.direction = direction
        self.animation_tick = 0

        self.rect = Rect((0, 0), ENEMY_SIZE)
        self.rect.centerx = (patrol_left + patrol_right) // 2
        self.rect.bottom = platform_top

    def update(self):
        self.rect.x += ENEMY_SPEED * self.direction

        if self.rect.left <= self.patrol_left:
            self.rect.left = self.patrol_left
            self.direction = 1
        elif self.rect.right >= self.patrol_right:
            self.rect.right = self.patrol_right
            self.direction = -1

        self.animation_tick += 1

    def draw(self, screen):
        frames = LEFT_WALK_IMAGES if self.direction < 0 else RIGHT_WALK_IMAGES
        frame_number = (
            self.animation_tick // ANIMATION_FRAME_LENGTH
        ) % len(frames)
        sprite_x = self.rect.centerx - ENEMY_SPRITE_SIZE[0] // 2
        sprite_y = self.rect.bottom - ENEMY_SPRITE_SIZE[1]
        screen.blit(frames[frame_number], (sprite_x, sprite_y))


def find_patrol_routes(platform_tiles, tile_size):

    platform_cells = {
        (tile.rect.x, tile.rect.y)
        for tile in platform_tiles
    }
    exposed_by_row = {}

    for x, y in platform_cells:
        if (x, y - tile_size) not in platform_cells:
            exposed_by_row.setdefault(y, []).append(x)

    routes = []

    for platform_top, columns in exposed_by_row.items():
        sorted_columns = sorted(columns)
        run_start = sorted_columns[0]
        previous_column = run_start

        for column in sorted_columns[1:] + [None]:
            run_ended = column is None or column != previous_column + tile_size

            if run_ended:
                run_width = previous_column - run_start + tile_size

                if run_width >= MIN_PLATFORM_TILES * tile_size:
                    routes.append(
                        (run_start, previous_column + tile_size, platform_top)
                    )

                if column is not None:
                    run_start = column

            if column is not None:
                previous_column = column

    return sorted(routes, key=lambda route: (route[2], route[0]))


def create_enemies(platform_tiles, tile_size):

    enemies = []

    for route_number, route in enumerate(
        find_patrol_routes(platform_tiles, tile_size)
    ):
        direction = -1 if route_number % 2 else 1
        enemies.append(Enemy(*route, direction=direction))

    return enemies


def update_enemies(enemies):
    for enemy in enemies:
        enemy.update()


def draw_enemies(screen, enemies):
    for enemy in enemies:
        enemy.draw(screen)


def player_touches_enemy(player_rect, enemies):
    return any(player_rect.colliderect(enemy.rect) for enemy in enemies)


def remove_bullet_hits(enemies, bullets):

    surviving_enemies = []
    hit_bullets = set()

    for enemy in enemies:
        enemy_was_hit = False

        for bullet in bullets:
            if id(bullet) in hit_bullets:
                continue

            if enemy.rect.colliderect(bullet.rect):
                hit_bullets.add(id(bullet))
                enemy_was_hit = True
                break

        if not enemy_was_hit:
            surviving_enemies.append(enemy)

    enemies[:] = surviving_enemies
    bullets[:] = [bullet for bullet in bullets if id(bullet) not in hit_bullets]
    return len(hit_bullets)
