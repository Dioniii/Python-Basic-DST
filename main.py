import pgzrun

WIDTH = 800
HEIGHT = 450

BUTTON_WIDTH = 240
BUTTON_HEIGHT = 55
BUTTON_GAP = 20
BUTTON_X = (WIDTH - BUTTON_WIDTH) // 2

menu_panel = Rect(190, 30, 420, 390)
startButton = Rect(BUTTON_X, 165, BUTTON_WIDTH, BUTTON_HEIGHT)
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

PANEL_BORDER = (224, 145, 56)
BUTTON_BORDER = (240, 181, 72)
BUTTON_NORMAL = (154, 60, 43)
BUTTON_HOVER = (204, 86, 45)
TEXT_COLOR = (255, 245, 216)
ACCENT_COLOR = (245, 177, 66)
SHADOW_COLOR = (18, 16, 25)


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
    screen.draw.text(label, center=button.center, color=text_color, fontsize=30)


def draw():
    screen.blit("menu_background", (0, 0))

    screen.draw.filled_rect(menu_panel, (12, 25, 42))
    screen.draw.rect(menu_panel, PANEL_BORDER)
    screen.draw.rect(menu_panel.inflate(-2, -2), PANEL_BORDER)

    screen.draw.text(
        "Industrial Warfare",
        center=(WIDTH // 2, 82),
        color=TEXT_COLOR,
        fontsize=40,
        shadow=(1, 1),
        scolor=(0, 0, 0),
    )
    screen.draw.text(
        "MAIN MENU",
        center=(WIDTH // 2, 125),
        color=ACCENT_COLOR,
        fontsize=20,
    )

    draw_button(startButton, "START GAME", "start")
    draw_button(soundButton, "SOUND: ON", "sound")
    draw_button(exitButton, "EXIT", "exit")


def on_mouse_move(pos):
    global hovered_button

    if startButton.collidepoint(pos):
        hovered_button = "start"
    elif soundButton.collidepoint(pos):
        hovered_button = "sound"
    elif exitButton.collidepoint(pos):
        hovered_button = "exit"
    else:
        hovered_button = None


def on_mouse_down(pos, button):
    if button != mouse.LEFT:
        return

    if startButton.collidepoint(pos):
        print("Start clicked")
    elif soundButton.collidepoint(pos):
        print("Sound clicked")
    elif exitButton.collidepoint(pos):
        print("Exit clicked")


pgzrun.go()
