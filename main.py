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


def draw_button(button, label, button_name):
    shadow = Rect(button.x + 5, button.y + 5, button.width, button.height)
    screen.draw.filled_rect(shadow, (5, 15, 8))

    if hovered_button == button_name:
        button_color = (70, 155, 75)
        text_color = (255, 245, 180)
    else:
        button_color = (35, 105, 50)
        text_color = "white"

    screen.draw.filled_rect(button, button_color)
    screen.draw.rect(button, (180, 220, 120))
    screen.draw.text(label, center=button.center, color=text_color, fontsize=30)


def draw():
    screen.blit("background", (0, 0))

    screen.draw.filled_rect(menu_panel, (10, 38, 20))
    screen.draw.rect(menu_panel, (150, 205, 90))

    screen.draw.text(
        "WELCOME TO MY GAME",
        center=(WIDTH // 2, 82),
        color=(245, 245, 220),
        fontsize=40,
        shadow=(2, 2),
        scolor=(0, 0, 0),
    )
    screen.draw.text(
        "MAIN MENU",
        center=(WIDTH // 2, 125),
        color=(170, 215, 110),
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
