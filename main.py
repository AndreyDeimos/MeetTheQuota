import pygame
import sys
from random import choice
from lib.dynamyc import find_cheapest_path, generate_random_table
pygame.init()
size = 1920, 1080

# code from pyautogui, thank you stackoverflow
if sys.platform == 'win32':
    # On Windows, the monitor scaling can be set to something besides normal 100%.
    # PyScreeze and Pillow needs to account for this to make accurate screenshots.
    # TODO - How does macOS and Linux handle monitor scaling?
    import ctypes
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except AttributeError:
        pass  # Windows XP doesn't support monitor scaling, so just do nothing.

fps = 60
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size, pygame.FULLSCREEN, pygame.HWSURFACE)
pygame.display.set_caption("Meet the quota")
running = True

table_size = 3
spread = 2
table = generate_random_table(table_size, spread)
table_surface = pygame.Surface((1000, 1000), pygame.HWSURFACE)
player_was = []
player_x = 0
player_y = table_size - 1
pressed_right = 0
pressed_up = 0
table_lines_surface = pygame.Surface((1000, 1000), pygame.HWSURFACE)
look_how_bad_are_you = 0
sumscore = 0

class Text:
    def __init__(self):
        self.font = pygame.font.SysFont('dubai', 72)
        self.currentfont = 'dubai'
        self.surface = self.font.render("example", False, "red")
        self.fontsize = 72

    def set_font(self, font, text_size):
        self.font = pygame.font.SysFont(font, text_size)
        self.currentfont = font
        self.fontsize = text_size

    def set_text(self, text, color):
        self.surface = self.font.render(text, False, color)

    def set_cords(self, x, y):
        self.text_rect = self.surface.get_rect(center=(x, y))

    def render_text(self, screen):
        screen.blit(self.surface, self.text_rect)


return_pressed = False

# return to tutorial when release
gamestate = "game"

button_state = 1

Welcome_text = Text()
Welcome_text.set_font("dubai", 120)
Welcome_text.set_text("Meet the quota", "red")

tutorial_text = Text()
tutorial_text.set_text("arrows to move, enter to select", "red")
tutorial_text.set_cords(960, 540)

continue_text = Text()
continue_text.set_font("dubai", 36)
continue_text.set_text("Press enter to continue", "red")
continue_text.set_cords(960, 945)

play_button = pygame.Surface((350, 100))
play_button.fill("red")
play_text = Text()
play_text.set_text("play", "black")
play_text.set_cords(175, 50)

exit_button = pygame.Surface((350, 100))
exit_button.fill("red")
exit_text = Text()
exit_text.set_cords(240, 50)
exit_text.set_text("exit", "black")

game_tutorial_state = 1


def render_game_tutorial():
    global game_tutorial_state, gamestate
    if game_tutorial_state == 2:
        gamestate = "game"
    elif game_tutorial_state == 1:
        continue_text.render_text(screen)


def render_play_button():
    global button_state
    if button_state == 1:
        play_button.fill("green")
    else:
        play_button.fill("red")
    play_text.render_text(play_button)
    screen.blit(play_button, (640 - 175, 810 - 50))


def render_exit_button():
    global button_state
    if button_state == 1:
        exit_button.fill("red")
    else:
        exit_button.fill("green")
    exit_text.render_text(exit_button)
    screen.blit(exit_button, (1280 - 175, 810 - 50))

def table_lines():
    global table_size, table_lines_surface
    table_lines_surface.fill("black")
    pygame.draw.line(table_lines_surface, "red", (0, 0), (999, 0), width=1)
    pygame.draw.line(table_lines_surface, "red", (999, 0), (999, 999), width=1)
    pygame.draw.line(table_lines_surface, "red", (0, 999), (999, 999), width=1)
    pygame.draw.line(table_lines_surface, "red", (0, 0), (0, 999), width=1)
    pos = 1000 // table_size
    for i in range(table_size):
        pygame.draw.line(table_lines_surface, "red", (0, pos * i),
                         (999, pos * i), width=1)
    for i in range(table_size):
        pygame.draw.line(table_lines_surface, "red", (pos * i, 0), (pos * i, 999), width=1)

def table_render():
    global table_size, table, table_surface, table_lines_surface
    table_surface.fill("black")
    table_surface.blit(table_lines_surface, (0, 0))
    pos = 1000 // table_size
    for i in range(table_size):
        for j in range(table_size):
            if (i, j) not in player_was:
                render_number(table[i][j], pos * (i + 0.5),
                              pos * (j + 0.5), pos - 1)
    pygame.draw.rect(table_surface, "red", [pos * player_x , pos * player_y, pos, pos], width=0)


def render_number(number, x, y, size):
    text = Text()
    text.set_font('dubai', size)
    text.set_text(str(number), "red")
    text.set_cords(x, y)
    text.render_text(table_surface)

score = Text()
level = Text()
quota = Text()
score.set_cords(1450, 1080 // 4)
level.set_cords(1450, (1080 // 4) * 2)
quota.set_cords(1450, (1080 // 4) * 3)
scorecounter = 0
quotascore = 0

def render_game():
    global table_surface
    table_render()
    score.set_text(f'your score: {scorecounter}', "red")
    score.render_text(screen)
    quota.set_text(f"{sumscore} / {quotascore}", "red")
    quota.render_text(screen)
    screen.blit(table_surface, (40, 40))


def render_tutorial():
    tutorial_text.render_text(screen)
    continue_text.render_text(screen)


def render_start_menu():
    text_x = size[0] // 2
    y = size[1] // 3
    Welcome_text.set_cords(text_x, y)
    Welcome_text.render_text(screen)
    render_play_button()
    render_exit_button()


def handle_event(event):
    global gamestate, button_state, running, game_tutorial_state, return_pressed, player_y, player_x, player_was, pressed_right, pressed_up, scorecounter
    if gamestate == "tutorial":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not return_pressed:
                gamestate = "start_menu"
                return_pressed = True
    if gamestate == "start_menu":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and button_state == 2:
                button_state = 1
            if event.key == pygame.K_RIGHT and button_state == 1:
                button_state = 2
            if event.key == pygame.K_RETURN:
                if button_state == 2:
                    running = False
                if button_state == 1 and not return_pressed:
                    gamestate = "game_tutorial"
                    return_pressed = True
    if gamestate == "game_tutorial":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not return_pressed:
                return_pressed = True
                game_tutorial_state += 1
    if gamestate == "game":
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                if player_x != table_size - 1 and not pressed_right:
                    pressed_right = 1
                    player_was.append((player_x, player_y))
                    player_x += 1
                    scorecounter += table[player_x][player_y]
                    print("pressed right")
            if event.key == pygame.K_UP:
                if player_y != 0 and not pressed_up:
                    pressed_up = 1
                    player_was.append((player_x, player_y))
                    player_y -= 1
                    scorecounter += table[player_x][player_y]
                    print("pressed up")

def new_table():
    global player_x, player_y, player_was, table, table_size, spread, scorecounter
    harder = choice((1, 2))
    if harder == 1:
        table_size += 1
    else:
        spread += 1
    table = generate_random_table(table_size, spread)
    table_lines()
    player_x = 0
    player_y = table_size - 1
    player_was = []
    scorecounter = 0

def update_scene():
    global player_x, player_y, table_size, gamestate, quotascore, sumscore, table, table_size, spread
    if player_x == table_size - 1 and player_y == 0:
        if look_how_bad_are_you == 0:
            ...
        cheapest_path = find_cheapest_path(table)
        sumscore += int(100 * (cheapest_path / scorecounter))
        print(cheapest_path, scorecounter)
        quotascore += 50    
        if quotascore > sumscore:
            gamestate = 'start_menu'
            sumscore = 0
            quotascore = 0
            table_size = 2
            spread = 2
        new_table()
def draw_scene():
    global gamestate
    screen.fill("black")
    if gamestate == "tutorial":
        render_tutorial()
    if gamestate == "start_menu":
        render_start_menu()
    if gamestate == "game_tutorial":
        render_game_tutorial()
    if gamestate == "game":
        render_game()

table_lines()

while running:
    return_pressed = False
    pressed_right = 0
    pressed_up = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        handle_event(event)
    update_scene()
    draw_scene()
    # print(gamestate)
    pygame.display.flip()
    clock.tick(fps)
pygame.quit()
sys.exit()
