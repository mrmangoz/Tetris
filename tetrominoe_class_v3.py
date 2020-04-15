import pygame as pg
import front_end
from copy import deepcopy


class Tetrominoe:
    def __init__(self, type):
        # these wallkick variables have all the data to be looped through and checked
        self.wall_kick_data = {"0->R": ((0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)),
                               "R->0": ((0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)),
                               "R->2": ((0, 0), (+1, 0), (+1, -1), (0, +2), (+1, +2)),
                               "2->R": ((0, 0), (-1, 0), (-1, +1), (0, -2), (-1, -2)),
                               "2->L": ((0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2)),
                               "L->2": ((0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)),
                               "L->0": ((0, 0), (-1, 0), (-1, -1), (0, +2), (-1, +2)),
                               "0->L": ((0, 0), (+1, 0), (+1, +1), (0, -2), (+1, -2))}
        self.wall_kick_data_I = {"0->R": ((0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)),
                                 "R->0": ((0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)),
                                 "R->2": ((0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1)),
                                 "2->R": ((0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)),
                                 "2->L": ((0, 0), (+2, 0), (-1, 0), (+2, +1), (-1, -2)),
                                 "L->2": ((0, 0), (-2, 0), (+1, 0), (-2, -1), (+1, +2)),
                                 "L->0": ((0, 0), (+1, 0), (-2, 0), (+1, -2), (-2, +1)),
                                 "0->L": ((0, 0), (-1, 0), (+2, 0), (-1, +2), (+2, -1))}
        # assigns variables to self.
        self.type = type # the type of tetrominoe
        self.coordinates = self.get_tetrominoe(self.type) # the current coords
        self.colour = self.get_colour(self.type) # current colour
        self.nrturn = 0 # number of right turns
        self.nlturn = 0 # number of left turns (not exactly "number of left turns" literally)
                        # but rather the position of the tetrominoe in relation to "right and left" turns
        self.nturn = 0 # overall turns
        self.state = None # state of the tetrominoe

    def addRotate(self, left_right):
        # function used in the wallkicks
        # is determines where the tetrominoe is in relation to it's number of turns
        # so if you turn right once, then left again, the tetrominoe would be back
        # at 0 and so on. Once it reaches 4 turns, it resets to 0.
        if left_right == "right": # if rotating right
            #self.state = "right" # changes the state to right
            if self.nrturn > 0 or self.nlturn == 0: # checks the right turns and left
                self.nrturn += 1 # if the previous rotate was right, then + 1 to right turns
                #print(self.nrturn)
            elif self.nlturn > 0: # else if left turns greater than 0
                self.nlturn -= 1 # if previous was left turn, -1 to left turns
        elif left_right == "left": # if rotating left
            self.state = "left" # changes the state to left
            if self.nlturn > 0 or self.nrturn == 0: # checks the left turns and right
                self.nlturn += 1 # if the previous rotate was left, then + 1 to left turns
            elif self.nrturn > 0: # else if the number of right turns is greater than 0
                self.nrturn -= 1 # if the prevous turn was right, -1 to right turns
        if (self.nrturn or self.nlturn) == 4: # if right or left turns are == to 4
            # reset the right and left turns
            self.nrturn = 0
            self.nlturn = 0



    def get_colour(self, type):
        # just gets the colour of the tetrominoe
        colours = {"I": (0, 255, 255),
                   "S": (0, 255, 0),
                   "Z": (255, 0, 0),
                   "J": (0, 0, 255),
                   "L": (255, 165, 0),
                   "T": (160, 32, 240),
                   "O": (255, 255, 0)}
        return colours[type]

    def get_tetrominoe(self, type):
        # gets the tetrominoe starting point
        tetrominoe = {"I": [[3, 18], [4, 18], [5, 18], [6, 18]],
                      "S": [[3, 18], [4, 18], [4, 17], [5, 17]],
                      "Z": [[5, 18], [4, 18], [4, 17], [3, 17]],
                      "J": [[3, 17], [3, 18], [4, 18], [5, 18]],
                      "L": [[5, 17], [5, 18], [4, 18], [3, 18]],
                      "T": [[3, 18], [4, 17], [4, 18], [5, 18]],
                      "O": [[3, 18], [4, 18], [3, 17], [4, 17]]}
        return tetrominoe[type]

    def repaint_background(self):
        # repaints the background that the tetrominoe was on after the tetrominoe has moved
        for x, y in self.coordinates: # loops through the x and y coords
            if x % 2 == 0: # if x divided by two has no remainder then paint grey
                pg.draw.rect(front_end.background, (211, 211, 211), [x*16,
                                                                     y*16 - 320, 16,
                                                                     16])
            else: # else paint white
                pg.draw.rect(front_end.background, (255, 255, 255), [x*16,
                                                                     y*16 - 320, 16,
                                                                     16])
            # pg.draw.rect(background, (211, 211, 211), [x*16, y*16, 16, 16])

    def draw(self):
        # draws the tetrominoe
        for x, y in self.coordinates: # loops through x y coordinates
            pg.draw.rect(front_end.background, self.colour, [x*16, y*16 - 320, 16,
                                                             16]) # draws the blocks
            front_end.background.convert()
            front_end.screen.blit(front_end.background, (0, 0)) #  blits the background onto the screen
            pg.display.flip() # updates the display

    def move(self):
        # moves the tetrmoninoe down
        self.repaint_background() # repaints over the tetrominoe
        for n in range(4): #loops for 4
            x = self.coordinates[n][0] # sets variables
            y = self.coordinates[n][1]
            if front_end.grid[y+1][x] != 1: # checks if there is a 1 underneath the tetrominoe
                self.coordinates[n][1] += 1 # pluses one to the coord
        self.draw() # draws the tetrominoe

    def move_side(self, lr):
        # moves the tetrominoe side to side
        self.repaint_background() # repaints over the tetrominoe
        if lr == "right": # if moving right
            for n in range(4):
                x = self.coordinates[n][0] # assigns x and y variables
                y = self.coordinates[n][1]
                if x < 9 and front_end.grid[y][x+1] != 1: # makes sure doesn't move off screen
                    result = True
                    continue
                else:
                    result = False
                    break
            if result:
                for n in range(4):
                    self.coordinates[n][0] += 1 # loops through and adds one to all x coords
        elif lr == "left": # if moving left
            for n in range(4):
                x = self.coordinates[n][0] # assigns variables to x and y
                y = self.coordinates[n][1]
                if x > 0 and front_end.grid[y][x-1] != 1: # makes sure doesn't move off screen
                    result = True
                    continue
                else:
                    result = False
                    break
            if result:
                for n in range(4):
                    self.coordinates[n][0] -= 1 # loops through and takes away one from all x coords
        self.draw() # draws the new tetrominoe at new position

    def end_game(self):
        # looping through second variable ... for y in [i[1] for i in self.coordinates]:
        for x, y in self.coordinates:
            #print(y)
            #print(front_end.grid)
            if y == 18 and front_end.grid[y + 1][x] == 1:
                print('!!!!!!!!!!!!!!!!!!!!!!!!!!test  ')
                return(True)
            else:
                return(False)

    def stop_tetrominoe(self):
        # function to stop the tetrominoe if it is at bottom of the screen or hits another tetrominoe
        result = False # assigns a result to false
        for x, y in self.coordinates:
            if y != 39: # if hits bottom of screen
                if front_end.grid[y+1][x] == 1: # if there is a block underneath
                    result = True
            else:
                result = True
        return(result) # returns the result

    def populate_ones(self):
        # populates the ones
        for n in range(4):
            x = self.coordinates[n][0]
            y = self.coordinates[n][1]
            front_end.grid[y][x] = 1 # fills a 1 in for every position of the tetrominoe blocks

    def shift_data(self, temp_coordinates, left_right):
        # this function determines whether the I is vertical or horizontal
        # and then determines how the coordinates must be shifted
        # does this by looking at the position of the 4th block in a
        # cartesian plane. Whether it is negative or positive determines
        # the shift needed for the desired rotation
        # This is needed since the I rotation doesn't focus around the 3rd block
        # as do all the other tetrominoes that rotate do. Depending on the position
        # of the 4th block, the coordinates need to be shifted up, down, left, or right
        # by 1 so as to output the desired rotation.
        if temp_coordinates[3][1] < 0: # if y coordinate of the 4th block < 0
            if left_right == "left": # if rotating left
                return 1, 0 # returns +1 to x and +0 to y
            elif left_right == "right": # if rotating right
                return 0, -1 # returns +0 to x and -1 to y
        elif temp_coordinates[3][1] > 0: # if y coordinate of the 4th block > 0
            if left_right == "left": # if rotating left
                return -1, 0 # returns -1 to x and +0 to y
            elif left_right == "right": # if rotating right
                return 0, 1 # returns +0 to x and +1 to y
        # if the y coordinate == 0 then it will bypass the first two if elif statments
        # and go and check the x coordinates of the 4th block.
        if temp_coordinates[3][0] < 0: # if the x coordinate of the 4th block <0
            if left_right == "left": # if rotating left
                return 0, -1 # returns +0 to x and -1 to y
            elif left_right == "right": # if rotating right
                return -1, 0 # returns -1 to x and +0 to y
        elif temp_coordinates[3][0] > 0: # if the x coordinate of the 4th block > 0
            if left_right == "left": # if rotating left
                return 0, 1 # returns +0 to x and +1 to y
            elif left_right == "right": # if rotating right
                return 1, 0 #returns +1 to x and +0 to y

    def rotate(self, left_right):
        if self.type != "O":
            temp_list = deepcopy(self.coordinates) # creates a temporary list of coordinates
            holder_x = temp_list[2][0] # assigns the x and y holder values that
                                       # that will be used to translate the grid coordinates
                                       # to cartesian plane coordinates, with the 3rd block
                                       # at the origin (0, 0)
            holder_y = temp_list[2][1]
            if self.type == "I":
                # makes a new list of the translated coordinates to cartesian
                shift_list = [[temp[0] -holder_x, (-1)*(temp[1]- holder_y)] for temp in temp_list]
                SHIFT_DATA = self.shift_data(shift_list, left_right[2])
                # assigns the rotation data for the I
            else:
                SHIFT_DATA = 0, 0 # if it's not an I then no need for shift data
            for n in range(4):
                # assigns variables to the translated and shifted x and y
                x = temp_list[n][0] - holder_x + SHIFT_DATA[0]
                y = (-1)*(temp_list[n][1] - holder_y) + SHIFT_DATA[1]
                # the (-1)* for the y is because the y values for the grid
                # are inverse to the y values on a cartesian plane
                x_rotated = int(left_right[0]*y) # rotates the x and y values
                y_rotated = int(left_right[1]*x)
                temp_list[n][0] = x_rotated + holder_x # adds the holder values back
                temp_list[n][1] = -1*(y_rotated) + holder_y
            #print(self.state)
            if self.wallkick(temp_list, left_right[2]):
                #print('wallkick')
                self.repaint_background()
                self.coordinates = temp_list
                self.draw()
                self.addRotate(left_right[2])
                #print("right #" + str(self.nrturn) + '\n')
                #print("left  #" + str(self.nlturn) + '\n')

            else:
                print("Nope \n")
                self.draw()


    def test(self, wn, type, x, y): # this function is used to test if the wallkick
                                    # position is true or false
        wallkickx = self.wall_kick_data[type][wn][0] # sets variables out of the
                                                     # wallkick data
        wallkicky = self.wall_kick_data[type][wn][1]
        if self.type == "I": # this is here because the data for I is different
            #print("I")
            wallkickx = self.wall_kick_data_I[type][wn][0]
            wallkicky = self.wall_kick_data_I[type][wn][1]
        x_transform = x + wallkickx
        y_transform = y + wallkicky
        if (y_transform <= 39) and (0 <= x_transform <= 9) and (front_end.grid[y_transform][x_transform] != 1): # checks if the transformation
                                                              # can be done
            return(True, wn) # returns true and the index
        else:
            return(False) # returns false


    def wallkick(self, list, left_right):
        # 0 : 0->R, 0->L
        # 1 : R->2, L->2, R->0, L->0
        # 2 : 2->R, 2->L
        #print("start of wallkick \n")
        #print()
        #print("right #" + str(self.nrturn) + '\n')
        #print("left  #" + str(self.nlturn) + '\n')
        for wn in range(5): # there a five wallkick states that must be checked
            for x, y in list: # loops for x, y in current tetrominoe
                if left_right == "right":
                    if self.nrturn == 0:
                        wallkick_type = "0->R"
                        state = "R"

                    if self.nrturn == 1 or self.nlturn == 3:
                        wallkick_type = "R->2"
                        state = "2"
                    elif self.nrturn or self.nlturn == 2:
                        wallkick_type = "2->L"
                        state = "L"
                    elif self.nrturn == 3 or self.nlturn == 1:
                        wallkick_type = "L->0"
                        state = "0"
                elif left_right == "left":
                    if self.nlturn == 0:
                        wallkick_type = "0->L"
                        state = "L"
                    if self.nlturn == 1 or self.nrturn == 3:
                        wallkick_type = "L->2"
                        state = "2"
                    elif self.nlturn == 2:
                        wallkick_type = "2->R"
                        state = "R"
                    elif self.nlturn == 3 or self.nrturn == 1:
                        wallkick_type = "R->0"
                        state = "0"
                print(state)
                print(wallkick_type)
                result = self.test(wn, wallkick_type, x, y)
                if result is False: break
            #print()
            #print(wallkick_type)
            #print(state + " after")
            #print()
            #print(result)
            if result:
                for n in range(4):
                    list[n][0] += self.wall_kick_data[wallkick_type][result[1]][0]
                    list[n][1] += self.wall_kick_data[wallkick_type][result[1]][1]
                return(result[0])
        if not result:
            return(result)
