import pgzrun
import gameplay
from platformer import MAP_HEIGHT, MAP_WIDTH

WIDTH = MAP_WIDTH
HEIGHT = MAP_HEIGHT

BUTTON_WIDTH = 240
BUTTON_HEIGHT = 48
BUTTON_GAP = 14
BUTTON_X = (WIDTH - BUTTON_WIDTH) // 2

menu_panel = Rect(55, 15, 430, 330)
startButton = Rect(BUTTON_X, 135, BUTTON_WIDTH, BUTTON_HEIGHT)
soundButton = Rect(
    BUTTON_X,
    startButton.bottom + BUTTON_GAP,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)
exitButton = Rect(
    BUTTON_X,
    soundButton.bottom + BUTTON_GAP,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
)

hovered_button = None
sound_on = True
current_screen = "menu"

PANEL_BORDER = (224, 145, 56)
BUTTON_BORDER = (240, 181, 72)
BUTTON_NORMAL = (154, 60, 43)
BUTTON_HOVER = (204, 86, 45)
TEXT_COLOR = (255, 245, 216)
ACCENT_COLOR = (245, 177, 66)
SHADOW_COLOR = (18, 16, 25)

background_sound = sounds.background
background_sound.set_volume(0.25)
background_sound.play(-1)


def draw_button(button, label, button_name):
    shadow = Rect(button.x + 5, button.y + 5, button.width, button.height)
    screen.draw.filled_rect(shadow, SHADOW_COLOR)

    if hovered_button == button_name:
        button_color = BUTTON_HOVER
        text_color = "white"
    else:
        button_color = BUTTON_NORMAL
        text_color = TEXT_COLOR

    screen.draw.filled_rect(button, BUTTON_BORDER)
    screen.draw.filled_rect(button.inflate(-4, -4), button_color)
    screen.draw.text(label, center=button.center, color=text_color, fontsize=26)


def draw_menu():
    # Centre-crop the existing 800 x 450 art without scaling it.
    screen.blit("menu_background", ((WIDTH - 800) // 2, (HEIGHT - 450) // 2))

    screen.draw.filled_rect(menu_panel, (12, 25, 42))
    screen.draw.rect(menu_panel, PANEL_BORDER)
    screen.draw.rect(menu_panel.inflate(-2, -2), PANEL_BORDER)

    screen.draw.text(
        "Industrial Warfare",
        center=(WIDTH // 2, 58),
        color=TEXT_COLOR,
        fontsize=36,
        shadow=(1, 1),
        scolor=(0, 0, 0),
    )
    screen.draw.text(
        "MAIN MENU",
        center=(WIDTH // 2, 100),
        color=ACCENT_COLOR,
        fontsize=20,
    )

    draw_button(startButton, "START GAME", "start")
    sound_label = "SOUND: ON" if sound_on else "SOUND: OFF"
    draw_button(soundButton, sound_label, "sound")
    draw_button(exitButton, "EXIT", "exit")


def draw_game():
    gameplay.draw(screen)
    screen.draw.text(
        "Press ESC to return to the menu",
        midbottom=(WIDTH // 2, HEIGHT - 7),
        color=TEXT_COLOR,
        fontsize=17,
        shadow=(1, 1),
        scolor=(0, 0, 0),
    )


def draw():
    if current_screen == "menu":
        draw_menu()
    else:
        draw_game()


def update():
    if current_screen == "game":
        gameplay.update()


def on_mouse_move(pos):
    global hovered_button

    if current_screen != "menu":
        hovered_button = None
        return

    if startButton.collidepoint(pos):
        hovered_button = "start"
    elif soundButton.collidepoint(pos):
        hovered_button = "sound"
    elif exitButton.collidepoint(pos):
        hovered_button = "exit"
    else:
        hovered_button = None

def on_mouse_down(pos, button):
    global current_screen, sound_on

    if button != mouse.LEFT or current_screen != "menu":
        return

    if startButton.collidepoint(pos):
        gameplay.start()
        current_screen = "game"

    elif soundButton.collidepoint(pos):
        sound_on = not sound_on
        background_sound.set_volume(0.25 if sound_on else 0)

    elif exitButton.collidepoint(pos):
        raise SystemExit


def on_key_down(key):
    global current_screen

    if key == keys.ESCAPE and current_screen == "game":
        current_screen = "menu"
    elif current_screen == "game":
        gameplay.on_key_down(key)


pgzrun.go()
