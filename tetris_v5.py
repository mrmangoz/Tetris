import pygame as pg
import random
import front_end
from tetrominoe_class_v3 import Tetrominoe
from blocks_class import Blocks
# from points_class import Points
# from points_class import points

pg.init()  # iniates pygame


def init():  # sets up variables etc.
    global sequence
    global tetrominoe
    global blocks
    global points
    global end_game
    global time
    global timer
    global shift_left
    global shift_right
    global tetrominoe_tick
    global game_tick
    global pause
    global resume
    global speed
    speed = 100  # increases the tetrominoe speed
    timer = None
    sequence = generate_sequence() # initiates a starting sequence
    tetrominoe = Tetrominoe(sequence[0]) # initiates the first Tetrominoe class
    # points = Points()
    del sequence[0] # deletes the selected tetrominoe from the sequence
    front_end.show_next(tetrominoe.get_colour(sequence[0]), # updates the "next" tetrominoe indicator
                        tetrominoe.get_tetrominoe(sequence[0]))
    blocks = Blocks() # initiates a Blocks class
    tetrominoe.draw() # draws the tetrominoe
    end_game = False # boolean variable used to break the game loop
    time = 500 # assigns the time each tick takes to a variable
    #game_time = 1000
    shift_left = -1, 1, "left" # assigns the data needed to complete a rotation to a variable
    shift_right = 1, -1, "right"
    tetrominoe_tick = pg.USEREVENT + 1 # creates a new event called "tetrominoe_tick"
    #game_tick = pg.USEREVENT + 2 # creates a new event called "game_tick"
    pause = 0
    resume = time
    front_end.create_menu()
    print(get_pos()) # this was a work in progress to only click on the "T" to load
                     # but I gave up on that, so the function is just used to call
                     # front_end.load()
    # if input("start") == 'y':
        # front_end.load()
    control(time)
    #game_control(game_time)
    #print(front_end.grid)

def get_pos():
    while True:
        for event in pg.event.get():
            if event.type == pg.MOUSEBUTTONDOWN:
                front_end.load()
                return(pg.mouse.get_pos())
            else:
                continue

def generate_sequence():
    # generates the sequence of tetrominoes by "picking them out of a hat"
    sequence = [] # creates new sequence list
    new_sequence = [] # creates a "new sequence" list
    sequence = ["I", "S", "Z", "J", "L", "T", "O"]
    # creates a stock list of the shapes
    while len(sequence) > 0: # runs while sequence has stuff in it
        r = random.randint(0, len(sequence) - 1)
        # gets a random number based on the length of the list
        new_sequence.append(sequence[r])
        # adds the corresponding shape to the new list
        del sequence[r] # deletes the letter from the list
    if front_end.test == "y":
        return(["I","I","I","I","I","I","I"])
    else:
        return(new_sequence)

def control(state):
    global tetrominoe_timer
    tetrominoe_timer = pg.time.set_timer(tetrominoe_tick, state) # creates a timer for the event "tick"

def game_control(state):
    global game_timer
    game_timer = pg.time.set_timer(game_tick, state)

init()
pg.key.set_repeat(100, 100) # manages holding down keys (I think, not sure though lol)
while not end_game:  # main game loop
    key = pg.key.get_pressed()  # gets the key pressed
    for event in pg.event.get():  # deteremines which key is pressed
        if event.type == pg.QUIT:  # if you click the quit :(
            end_game = True # breaks the while loop
        if event.type == pg.KEYDOWN: # determines if a key is pressed
            if event.key == pg.K_LEFT: # left key
                tetrominoe.move_side("left")  # moves the tetrominoe left
            if event.key == pg.K_RIGHT: # right key
                tetrominoe.move_side("right")  # moves the tetrominoe left
            if event.key == pg.K_z: # Z key
                tetrominoe.rotate(shift_left)  # rotates anticlockwise/left
            if event.key == pg.K_x: # X key
                tetrominoe.rotate(shift_right)  # rotates clockwise/right
            if event.key == pg.K_c: # C key
                control(pause)
            if event.key == pg.K_v: # V key
                control(resume)
            if event.key == pg.K_DOWN: # down key
                control(speed)
        elif event.type == pg.KEYUP:
            if event.key == pg.K_DOWN: # down key
                control(resume)


        if event.type == tetrominoe_tick: # on tick
            if tetrominoe.end_game():
                control(pause)
                #time = pause
                #t = 0
                restart_quit = input("restart or quit? type r/q" )
                if restart_quit == "r":
                    #print(front_end.grid)
                    init()
                    #time = resume
                    #t = 0
                    #print(blocks.block_list)
                    control(resume)
                    continue
                elif restart_quit == "q":
                    end_game == True
            else:
                if tetrominoe.stop_tetrominoe() is False:  # determines if there is a collision
                    tetrominoe.move()  # moves the tetrominoe
                else:
                    # what happens if there is a collision
                    #print(sequence)
                    tetrominoe.populate_ones() # populates the 1s into the grid
                    #print(front_end.grid)
                    blocks.add_tetrominoe(tetrominoe) # adds the coordinates to the blocks class
                    blocks.add_line() # if there are any lines calls the blocks function
                    #print(blocks.block_list)
                    if blocks.check_line(): # if there are lines
                        #print("there's a line")
                        blocks.remove_line() # remove them and move the blocks down
                    tetrominoe = Tetrominoe(sequence[0])  # new tetrominoe
                    del sequence[0] # removes tetrominoe from the sequence
                    if len(sequence) == 0: # checks the length of the sequence
                        sequence = generate_sequence() # creates a new sequence
                    front_end.show_next(tetrominoe.get_colour(sequence[0]), # indicates the next tetrominoe on screen
                                        tetrominoe.get_tetrominoe(sequence[0]))
                    tetrominoe.draw()  # draws the new tetrominoe at spawn location
