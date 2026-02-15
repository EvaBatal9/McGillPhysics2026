import pygame
import sys
import math
import time
pygame.init()
from signalscope import duck_amp, cat_amp, cow_amp, dog_amp, donkey_amp, kathy_amp, lion_amp, monkey_amp, pig_amp



MENU = "menu"
GAME = "game"

YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)

state = MENU     

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

original_arrow = pygame.Surface((50, 20), pygame.SRCALPHA)
pygame.draw.polygon(original_arrow, YELLOW, [(0, 0), (50, 10), (0, 20)])
arrow_pos = pygame.Vector2(400, 500)
arrow_rect = original_arrow.get_rect(center=arrow_pos)
hover_imgl1 = pygame.image.load("hover_image.png").convert_alpha()


TITLE_FONT = pygame.font.SysFont("freesansbold.ttf", 48)
BUTTON_FONT = pygame.font.SysFont('freesansbold.ttf', 32)


class Button:
    def __init__(self, x,y, width, height, text, color, action=None, hover_image=None):
        self.rect = pygame.Rect(x,y,width, height)
        self.text = text
        self.color = color
        self.action = action
        self.hover_image = hover_image

    def draw (self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = BUTTON_FONT.render (self.text, True, (255,255,255))
        surface.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height -text_surface.get_height()) // 2 ))
        if self.hover_image and self.is_hovered(pygame.mouse.get_pos()):
            hover_rect = self.hover_image.get_rect(topleft=(self.rect.x, self.rect.y))
            surface.blit(self.hover_image, hover_rect)
        
    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)
    
    def click(self):
        if self.action:
            self.action()

start_button = Button(300, 500, 200, 50, "Start Game", ORANGE)



class DirecionButton:
    def __init__(self, x,y, width, height, text, color, direction, label):
        self.rect = pygame.Rect(x,y,width, height)
        self.text = text
        self.color = color
        self.direction = direction
        self.label = label
        self.visible = False 

    def draw (self, screen):
        if not self.visible:
            return
        pygame.draw.rect(screen, self.color, self.rect)
        text_surface = BUTTON_FONT.render (self.text, True, (255,255,255))
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                    self.rect.y + (self.rect.height -text_surface.get_height()) // 2 ))

    def is_clicked(self,pos):
        return self.visible and self.rect.collidepoint(pos)
    

player_pos = None

maze=[['x', 'duck', 'x', 'x', 'x', 'lion', 'x', 'x'],
         ['x', 0, 'x', 0, 0, 0, 0, 'x'],
         ['cow', 0, 'fox', 0, 'pig', 'x', 0, 'dog'],
         ['x', 0, 'x', 0, 'x', 0, 0, 'x'],
         ['donkey', 0, 'x', 0, 'x', 0, 'x', 'monkey'],
         ['x', 0, 0, 'start', 0, 0, 0, 0],
         ['x', 0, 'x', 'x', 0, 'x', 'x', 'x'],
         ['kathy', 0, 'x', 'x', 'cat', 'x', 'x', 'x']]

for y in range(len(maze)):
    for x in range (len(maze[y])):
        if maze[y][x] == 'start':
            player_pos = (x, y)
            break
    if player_pos:
        break

def get_valid_directions(maze, x, y):
    valid = []

    if y - 1 >= 0 and maze[y - 1][x] != 'x':
        valid.append("up")

    if y + 1 < len(maze) and maze[y + 1][x] != 'x':
        valid.append("down")

    if x - 1 >= 0 and maze[y][x - 1] != 'x':
        valid.append("left")

    if x + 1 < len(maze[0]) and maze[y][x + 1] != 'x':
        valid.append("right")

    return valid


def update_buttons():
    global player_pos
    x,y = player_pos 
    valid_directions = get_valid_directions(maze, x, y)

    for direction, button in buttons.items():
        button.visible = direction in valid_directions
            
    
def move_player(direction):
        global player_pos

        dx, dy = {
            "up": (0, -1), 
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }[direction]

        x, y = player_pos
        player_pos = (x + dx, y + dy)
        update_buttons()


buttons = {
"left": DirecionButton(50, 300, 100, 50, "Left", PINK, "left", "left"),
"right": DirecionButton(650, 300, 100, 50, "Right", PINK, "right", "right"),
"up": DirecionButton(375, 250, 50, 100, "Up", PINK, "up", "up"),
"down": DirecionButton(375, 350, 50, 100, "Down", PINK, "down", "down")
}

update_buttons()

def handle_game_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        for button in buttons.values():
            if button.is_clicked(event.pos):
                move_player(button.direction)

def handle_menu_events(event):
    global state

    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_button.is_hovered(event.pos):
            state = GAME
       
def draw_menu():
    screen.fill(YELLOW)
    title_surface = TITLE_FONT.render("Love, Duck, and FFT", True, PINK)
    screen.blit(title_surface, (screen_width // 2 - title_surface.get_width() // 2, 100))
    start_button.draw(screen)

def draw_game():
    screen.fill((0, 0, 0))
    game_surface = TITLE_FONT.render("", True, (255, 255, 255))
    for button in buttons.values():
        button.draw(screen)

    mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
    direction = mouse_pos - arrow_pos
    if direction.length() != 0:  
        angle = math.degrees(math.atan2(-direction.y, direction.x))
        rotated_arrow = pygame.transform.rotate(original_arrow, angle)
        rotated_rect = rotated_arrow.get_rect(center=arrow_pos)
        screen.blit(rotated_arrow, rotated_rect)

    screen.blit(game_surface, (screen_width // 2 - game_surface.get_width() // 2, screen_height // 2 - game_surface.get_height() // 2))

k = 0

def getting_amplitude_per_time(animal_amp):
    while k <= len(animal_amp):
        current_amp = animal_amp[k]
        time.sleep(0.1)
        k += 1
    


running = True
clock = pygame.time.Clock()
#calling amplitude generator function


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == MENU:
            handle_menu_events(event)
            
        elif state == GAME:
            handle_game_events(event)
    
    if state == MENU:
        draw_menu()
    elif state == GAME:
        
            


        draw_game()
        

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()