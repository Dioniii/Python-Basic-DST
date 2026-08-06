from pgzero.builtins import Rect, keyboard

GAME_WIDTH = 800
PLAYER_START = (80, 275)


player = Rect(PLAYER_START, (40, 50))


def start():
    """Reset everything when a new game begins."""
    player.topleft = PLAYER_START


def update():
    """Update the game every frame."""
    if keyboard.left:
        player.x -= 4

    if keyboard.right:
        player.x += 4

    player.x = max(0, min(player.x, GAME_WIDTH - player.width))


def draw(screen):
    """Draw the gameplay screen."""
    screen.fill((12, 25, 42))
    screen.blit("background", (30, 17))
    screen.draw.filled_rect(player, (204, 86, 45))
    screen.draw.rect(player, (255, 245, 216))
