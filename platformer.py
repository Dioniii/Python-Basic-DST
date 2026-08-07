from pathlib import Path

from pgzero.builtins import Rect


TILE_SIZE = 18
MAP_COLUMNS = 30
MAP_ROWS = 20
MAP_WIDTH = MAP_COLUMNS * TILE_SIZE
MAP_HEIGHT = MAP_ROWS * TILE_SIZE

MAP_ORIGIN = (0, 0)

DRAW_ORDER = (
    "background",
    "platforms",
    "obstacles",
    "scaffolding",
    "doors",
    "collectibles",
)

ACID_TILE_IDS = {13, 29, 45, 94, 95}

EXIT_TILE_IDS = {12, 28}

PROJECT_DIR = Path(__file__).resolve().parent


class Tile:
    def __init__(self, tile_id, column, row, tile_size, origin):
        x = origin[0] + column * tile_size
        y = origin[1] + row * tile_size

        self.tile_id = tile_id
        self.image = f"tiles/tile_{tile_id:04d}"
        self.rect = Rect((x, y), (tile_size, tile_size))


def load_csv_layer(filename, tile_size=TILE_SIZE, origin=MAP_ORIGIN):
    path = PROJECT_DIR / filename
    tiles = []

    with path.open(encoding="utf-8") as map_file:
        rows = [line.strip() for line in map_file if line.strip()]

    if len(rows) != MAP_ROWS:
        raise ValueError(
            f"{filename} has {len(rows)} rows; expected {MAP_ROWS}."
        )

    for row_number, row in enumerate(rows):
        values = row.split(",")

        if len(values) != MAP_COLUMNS:
            raise ValueError(
                f"{filename} row {row_number + 1} has {len(values)} "
                f"columns; expected {MAP_COLUMNS}."
            )

        for column_number, value in enumerate(values):
            tile_id = int(value)

            if tile_id >= 0:
                tiles.append(
                    Tile(
                        tile_id,
                        column_number,
                        row_number,
                        tile_size,
                        origin,
                    )
                )

    return tiles


class TileMap:
    def __init__(self, layer_files):
        missing_layers = set(DRAW_ORDER) - set(layer_files)

        if missing_layers:
            missing_names = ", ".join(sorted(missing_layers))
            raise ValueError(f"Missing level layers: {missing_names}")

        self.layers = {
            layer_name: load_csv_layer(layer_files[layer_name])
            for layer_name in DRAW_ORDER
        }

        self.solid_rects = [
            tile.rect
            for layer_name in ("platforms", "scaffolding")
            for tile in self.layers[layer_name]
        ] + [
            tile.rect
            for tile in self.layers["obstacles"]
            if tile.tile_id not in ACID_TILE_IDS
        ]
        self.hazard_rects = [
            tile.rect
            for tile in self.layers["obstacles"]
            if tile.tile_id in ACID_TILE_IDS
        ]
        self.exit_rects = [
            tile.rect
            for tile in self.layers["doors"]
            if tile.tile_id in EXIT_TILE_IDS
        ]
        self.bounds = Rect(MAP_ORIGIN, (MAP_WIDTH, MAP_HEIGHT))

    def draw(self, screen):
        for layer_name in DRAW_ORDER:
            for tile in self.layers[layer_name]:
                screen.blit(tile.image, tile.rect.topleft)

    def collect_items_at(self, player_rect):
        remaining_items = []
        collected = False

        for tile in self.layers["collectibles"]:
            if player_rect.colliderect(tile.rect):
                collected = True
            else:
                remaining_items.append(tile)

        self.layers["collectibles"] = remaining_items
        return collected

    def player_is_at_exit(self, player_rect):
        return any(
            player_rect.colliderect(exit_rect)
            for exit_rect in self.exit_rects
        )

    def player_touches_hazard(self, player_rect):
        return any(
            player_rect.colliderect(hazard_rect)
            for hazard_rect in self.hazard_rects
        )
