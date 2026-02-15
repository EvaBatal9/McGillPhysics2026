import pygame
import sys
import math
import time
pygame.init()
#from signalscope import duck_amp, cat_amp, cow_amp, dog_amp, donkey_amp, kathy_amp, lion_amp, monkey_amp, pig_amp
import scipy.fft as sp
from jumblesignals import makeSignal, Time
from mazeTest import animals
import matplotlib.pyplot as plt
import numpy as np

from jumblesignals import makeSignal
pygame.init() 

LABEL_FONT = pygame.font.SysFont('arial', 9)
BASELINE = 520
MAXHEIGHT = 180
MENU = "menu"
GAME = "game"

YELLOW = (255, 237, 100)
PINK = (244, 165, 198)
ORANGE = (255, 165, 0)
GREEN = (0, 128, 0)
BEIGE = (252, 202, 82)


state = MENU     

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))


background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (screen_width, screen_height))

original_arrow = pygame.Surface((50, 20), pygame.SRCALPHA)
pygame.draw.polygon(original_arrow, YELLOW, [(0, 0), (50, 10), (0, 20)])
arrow_pos = pygame.Vector2(400, 500)
arrow_rect = original_arrow.get_rect(center=arrow_pos)


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

start_button = Button(300, 380, 150, 50, "Start Game", ORANGE)



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
         ['x', 'x', 'x', 0, 'x', 0, 0, 'x'],
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
"left": DirecionButton(0, 200, 400, 200, "Left", BEIGE, "left", "left"),
"right": DirecionButton(400, 200, 400, 200, "Right", BEIGE, "right", "right"),
"up": DirecionButton(300, 0, 200, 400, "Up", BEIGE, "up", "up"),
"down": DirecionButton(300, 250, 200, 500, "Down", BEIGE, "down", "down")
}

update_buttons()

def handle_game_events(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        for button in buttons.values():
            if button.is_clicked(event.pos):
                #this should be generated when you point the signalscope in a direction and use the coordinates of the pointed direction
                signal=makeSignal(player_pos)
                print(signal)
                print(amplitude_generator(player_pos,signal))
                move_player(button.direction)

def handle_menu_events(event):
    global state

    if event.type == pygame.MOUSEBUTTONDOWN:
        if start_button.is_hovered(event.pos):
            state = GAME
       
def draw_menu():

    screen.blit(background, (0, 0))
    start_button.draw(screen)

def draw_game():
    screen.fill((244, 165, 198))
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
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(20, 350, 310, 200))

    screen.blit(game_surface, (screen_width // 2 - game_surface.get_width() // 2, screen_height // 2 - game_surface.get_height() // 2))



time_step = int(len(Time) / 26.6)


duck_amp = []
cat_amp = []
cow_amp = []
dog_amp = []
donkey_amp = []
kathy_amp = []
lion_amp = []
monkey_amp = []
pig_amp = []

def amplitude_generator(position,signal):
        
    k = 0
    i = time_step

    while i <= len(Time):
        #everything from k = 0 to time_step is the first interval
        #then k += time step, i += timestep
        #then repeat until i = len(Time)
        
        current_time_array = Time[k:i]
        current_pressure_array = signal[k:i]

        N = len(current_pressure_array)
        dt = current_time_array[1] - current_time_array[0]
        freqs = sp.fftfreq(N, dt)

        fft_vals = sp.fft(current_pressure_array)
        magnitude = np.abs(fft_vals)

        positive = freqs > 0

        amplitudes = {}

        for animal in animals:
            target_freq = animal.ID
            idx = np.argmin(np.abs(freqs - target_freq))
            amplitudes[animal.name] = magnitude[idx]


        duck_amp.append(int(amplitudes["Duck"]))
        cat_amp.append(int(amplitudes["Cat"]))
        cow_amp.append(int(amplitudes["Cow"]))
        dog_amp.append(int(amplitudes["Dog"]))
        donkey_amp.append(int(amplitudes["Donkey"]))
        kathy_amp.append(int(amplitudes["Kathy"]))
        lion_amp.append(int(amplitudes["Lion"]))
        monkey_amp.append(int(amplitudes["Monkey"]))
        pig_amp.append(int(amplitudes["Pig"]))

        k += time_step
        i += time_step

    return duck_amp, cat_amp, cow_amp, dog_amp, donkey_amp, kathy_amp, lion_amp, monkey_amp, pig_amp

        #pseudo code for what's going on:
        #we have the amplitude per frequency graph for the active time interval we are in, 
        # we see what the amplitude is for each of the animals IDs, 
        # and then we associate an amplitude to each animal



def get_amplitude_at_index(animal_amp, index):
    if not animal_amp:
        return 0
    index = index % len(animal_amp)  # wrap around
    return animal_amp[index]

#duck_amp, cat_amp, cow_amp, dog_amp, donkey_amp, kathy_amp, lion_amp, monkey_amp, pig_amp = amplitude_generator(position)

running = True
clock = pygame.time.Clock()
#calling amplitude generator function

t = 0
last_update = pygame.time.get_ticks()
update_interval = 100  # 0.1 seconds in milliseconds

duck_height = 0
cat_height = 0
cow_height = 0
dog_height = 0
donkey_height = 0
kathy_height = 0
lion_height = 0
monkey_height = 0
pig_height = 0

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
        """duck_amp_at_t = getting_amplitude_at_index(duck_amp, t)
        cat_amp_at_t = getting_amplitude_per_time(cat_amp)
        cow_amp_at_t = getting_amplitude_per_time(cow_amp)
        dog_amp_at_t = getting_amplitude_per_time(dog_amp)
        donkey_amp_at_t = getting_amplitude_per_time(donkey_amp)
        kathy_amp_at_t = getting_amplitude_per_time(kathy_amp)
        lion_amp_at_t = getting_amplitude_per_time(lion_amp)
        monkey_amp_at_t = getting_amplitude_per_time(monkey_amp)
        pig_amp_at_t = getting_amplitude_per_time(pig_amp)
"""     
        current_time = pygame.time.get_ticks()

        while current_time - last_update >= update_interval:
            t += 1
            last_update += update_interval
        draw_game()

        # DUCK
        duck_amp_at_t = get_amplitude_at_index(duck_amp, t)
        if duck_amp_at_t != 0:
            duck_height = MAXHEIGHT * (duck_amp_at_t / PLACEHOLDER_MAX_POSSIBLE_AMPLITUDE)

        duck_rect = pygame.Rect(25, BASELINE - duck_height, 30, duck_height)
        pygame.draw.rect(screen, (255, 255, 224), duck_rect)
        duck_label = LABEL_FONT.render("Duck", True, (0,0,0))
        screen.blit(duck_label, duck_label.get_rect(center=(duck_rect.centerx, BASELINE + 20)))


        # CAT
        cat_amp_at_t = get_amplitude_at_index(cat_amp, t)
        if cat_amp_at_t != 0:
            cat_height = MAXHEIGHT * (cat_amp_at_t / PLACEHOLDER_MAX_POSSIBLE_AMPLITUDE)

        cat_rect = pygame.Rect(55, BASELINE - cat_height, 30, cat_height)
        pygame.draw.rect(screen, (211, 211, 211), cat_rect)
        cat_label = LABEL_FONT.render("Cat", True, (0,0,0))
        screen.blit(cat_label, cat_label.get_rect(center=(cat_rect.centerx, BASELINE + 20)))


        # COW
        cow_amp_at_t = get_amplitude_at_index(cow_amp, t)
        if cow_amp_at_t != 0:
            cow_height = MAXHEIGHT * (cow_amp_at_t / PLACEHOLDER_MAX_POSSIBLE_AMPLITUDE)

        cow_rect = pygame.Rect(85, BASELINE - cow_height, 30, cow_height)
        pygame.draw.rect(screen, (0, 0, 0), cow_rect)
        cow_label = LABEL_FONT.render("Cow", True, (0,0,0))
        screen.blit(cow_label, cow_label.get_rect(center=(cow_rect.centerx, BASELINE + 20)))


        # DOG
        dog_amp_at_t = get_amplitude_at_index(dog_amp, t)
        if dog_amp_at_t != 0:
            dog_height = MAXHEIGHT * (dog_amp_at_t / PLACEHOLDER_MAX_POSSIBLE_AMPLITUDE)

        dog_rect = pygame.Rect(115, BASELINE - dog_height, 30, dog_height)
        pygame.draw.rect(screen, (101, 67, 33), dog_rect)
        dog_label = LABEL_FONT.render("Dog", True, (0,0,0))
        screen.blit(dog_label, dog_label.get_rect(center=(dog_rect.centerx, BASELINE + 20)))


        # DONKEY
        donkey_amp_at_t = get_amplitude_at_index(donkey_amp, t)
        if donkey_amp_at_t != 0:
            donkey_height = MAXHEIGHT * (donkey_amp_at_t / PLACEHOLDER_MAX_POSSIBLE_AMPLITUDE)

        donkey_rect = pygame.Rect(145, BASELINE - donkey_height, 30, donkey_height)
        pygame.draw.rect(screen, (128, 128, 128), donkey_rect)
        donkey_label = LABEL_FONT.render("Donkey", True, (0,0,0))
        screen.blit(donkey_label, donkey_label.get_rect(center=(donkey_rect.centerx, BASELINE + 20)))


        # KATHY
        kathy_amp_at_t = get_amplitude_at_index(kathy_amp, t)
        if kathy_amp_at_t != 0:
            kathy_height = MAXHEIGHT * (kathy_amp_at_t / PLACEHOLDER_MAX_POSSIBLE_AMPLITUDE)

        kathy_rect = pygame.Rect(175, BASELINE - kathy_height, 30, kathy_height)
        pygame.draw.rect(screen, (216, 191, 216), kathy_rect)
        kathy_label = LABEL_FONT.render("Kathy", True, (0,0,0))
        screen.blit(kathy_label, kathy_label.get_rect(center=(kathy_rect.centerx, BASELINE + 20)))


        # LION
        lion_amp_at_t = get_amplitude_at_index(lion_amp, t)
        if lion_amp_at_t != 0:
            lion_height = MAXHEIGHT * (lion_amp_at_t / PLACEHOLDER_MAX_POSSIBLE_AMPLITUDE)

        lion_rect = pygame.Rect(205, BASELINE - lion_height, 30, lion_height)
        pygame.draw.rect(screen, (207, 185, 151), lion_rect)
        lion_label = LABEL_FONT.render("Lion", True, (0,0,0))
        screen.blit(lion_label, lion_label.get_rect(center=(lion_rect.centerx, BASELINE + 20)))


        # MONKEY
        monkey_amp_at_t = get_amplitude_at_index(monkey_amp, t)
        if monkey_amp_at_t != 0:
            monkey_height = MAXHEIGHT * (monkey_amp_at_t / PLACEHOLDER_MAX_POSSIBLE_AMPLITUDE)

        monkey_rect = pygame.Rect(235, BASELINE - monkey_height, 30, monkey_height)
        pygame.draw.rect(screen, (150, 75, 0), monkey_rect)
        monkey_label = LABEL_FONT.render("Monkey", True, (0,0,0))
        screen.blit(monkey_label, monkey_label.get_rect(center=(monkey_rect.centerx, BASELINE + 20)))


        # PIG
        pig_amp_at_t = get_amplitude_at_index(pig_amp, t)
        if pig_amp_at_t != 0:
            pig_height = MAXHEIGHT * (pig_amp_at_t / PLACEHOLDER_MAX_POSSIBLE_AMPLITUDE)

        pig_rect = pygame.Rect(265, BASELINE - pig_height, 30, pig_height)
        pygame.draw.rect(screen, (255, 182, 193), pig_rect)
        pig_label = LABEL_FONT.render("Pig", True, (0,0,0))
        screen.blit(pig_label, pig_label.get_rect(center=(pig_rect.centerx, BASELINE + 20)))


        # FOX (static)
        fox_rect = pygame.Rect(295, BASELINE-5, 30, 5)
        pygame.draw.rect(screen, (250, 200, 152), fox_rect) 
        fox_label = LABEL_FONT.render("Fox", True, (0, 0, 0))
        screen.blit(fox_label, fox_label.get_rect(center=(fox_rect.centerx, BASELINE+20)))



    pygame.display.flip()
    clock.tick(60)


pygame.quit()
sys.exit()