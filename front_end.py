import pygame as pg
import numpy

coords = []
grid = None # creates a global variable grid
test = None # creates global variable test
GREY = 211, 211, 211 # assigns RBG values to variables
WHITE = 255, 255, 255
screen = pg.display.set_mode((320, 320)) # creates the screen
background = pg.Surface((160, 320)) # creates the background image
background = background.convert()
menu = pg.Surface((160,320)) # creates the menu image
menu = menu.convert()
game_info = pg.Surface((160, 320)) # creates the game info image
game_info.fill((47, 79, 79)) # draws a colour onto game info
game_info = game_info.convert()
screen.blit(game_info, (160, 0)) # blits game info onto screen
pg.display.flip() # updates display

def create_menu():
    global menu
    menu.fill(WHITE)
    pg.draw.rect(menu, (0, 255, 100), [16, 16, 48, 16])
    pg.draw.rect(menu, (0, 255, 100), [32, 16, 16, 48])
    screen.blit(menu, (0, 0))
    pg.display.flip() # updates display

def draw_lines():
    global background
    global screen
    background.fill(WHITE) # fills background with white
    for n in (0, 2, 4, 6, 8): # loops for all pos of line
        pg.draw.rect(background, GREY, [n*16, 0, 16, 320]) # draws grey lines
        background.convert()
    if test == "y":
        for x, y in coords:
            pg.draw.rect(background, (0, 255, 255), [x*16, y*16 - 320,16,16])
    screen.blit(background, (0, 0)) # blits background to screen
    pg.display.flip() # updates display

def repaint():
    # repaints the game_info tetrominoe
    pg.draw.rect(game_info, (47, 79, 79), [0, 0, 160, 320]) # draws a colour onto game info
    # draws over the tetrominoe
    game_info.convert()
    screen.blit(game_info, (160, 0)) # blits game_info onto screen
    pg.display.flip() # updates display

def show_next(colour, coordinates):
    # this function shows the next tetrominoe to be played
    global game_info
    repaint()
    for x, y in coordinates: # loops through x y coordinates
        pg.draw.rect(game_info, colour, [16*x, y*16 - 272, 16, 16])
        # draws the tetrominoe onto game_info
        game_info.convert()
        screen.blit(game_info, (160, 0)) # blits game_info onto screen
        pg.display.flip() # updates display


def create_background():
    global grid
    global test
    global coords
    grid = numpy.zeros((400), dtype=int) # creates the grid of 0s
    grid = grid.reshape(40, 10) # reshapes it to a 2d grid
    test = input("test scenario, y/n?")
    if test == "y":
        count = 0
        y = 0
        with open("wallkick_test_scenario.txt", "r") as f:
            for line in f:

                for i in range(10):
                    grid[count][i] = line[i]
                    if line[i] == "1":
                        coords.append([i, y])
                y += 1
                count += 1

def load():
    create_background() # creates the background using the function
    draw_lines() # draws the grey and white lines on the screens

def start_up():
    create_menu()
