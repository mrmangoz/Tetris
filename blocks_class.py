import pygame as pg
import front_end


class Blocks:
    # class for handling/managing the individual blocks on screen/the line clears etc.
    def __init__(self):
        self.block_list = [] # creates a new list of blocks
        self.lines = [] # creates a new list of lines
        self.coords = [] # creates a new list of co ordinates
    def add_tetrominoe(self, tetrominoe):
        # function for adding a tetrominoe to the blocks list
        for x, y in tetrominoe.coordinates:
            # loops through the tetrominoes x and y coordinates
            self.block_list.append([x, y, tetrominoe.colour])
            # adds the coordinates to the list + the colour
        self.coords = [temp[:2] for temp in self.block_list]
        # updates the self.coords list from the blocks_list with just the coordinates

    def get_lowest_y(self):
        # this function just returns the lowest y of all the blocks in the class
        return(min(y[1] for y in self.block_list))

    def get_highest_y(self):
        # this function just returns the highest y of all the blocks in the class
        return(max(y[1] for y in self.block_list))

    def add_line(self):

        # this function counts all the lines (it is badly named, I know, it "adds" lines to
        # to the self.lines list xD)
        lowest_y = self.get_lowest_y() # assigns the lowest y to a variable using the function
        #print(lowest_y)
        for y in range(lowest_y, 40): # loops through the lowest y to 40
            count = 0 # assigns a count variable to 0
            for block in self.block_list: # loops through the self.block_list list
                if block[1] == y: # if the y of the current block in loop == the y of outer loop
                    count += 1 # increment count
                if count == 10: # if count == 10
                    count = 0 # set count to 0
                    self.lines.append(y) # add the y of the line to the lines list


    def check_line(self):
        # this function checks if there are any lines in the game
        return(True) if len(self.lines) != 0 else False

    def remove_line(self):
        # this function removes lines from the game
        #print('remove line prints')
        #print()
        num_rows = len(self.lines) # assigns the number of rows to a variable
        #print(str(num_rows) + ' ' + str(self.lines))
        #print()
        for y in self.lines: # loops through the y values in the lines
            for x in range(10): # loops x values through 0 -> 9
                front_end.grid[y][x] = 0 # assigns the grid value of the lines to 0
        #print(front_end.grid)
        # print(front_end.grid)
        self.repaint_background() # repaints over the blocks
        #print(self.block_list)
        #print()
        self.block_list = [temp for temp in self.block_list if temp[1] not in
                           self.lines] # updates the self.block_list

        #print(self.block_list)
        #print()
        for i in self.lines: # loops through the self.lines list
            #print("current testing scenario i: " + str(i))
            lowest_y = self.get_lowest_y() # assigns the lowest y to a variable with the function
            for y in range(i, lowest_y - 1, - 1): # loops through the y values from the 'i'
                                                  # (y value from self.lines) to the 'lowest y'
                #print("current testing scenario y " + str(y))
                for x in range(10): # loops through x values from 0 -> 9
                    # this loop will move all the lines down by performing a swop in relation
                    # to the y values e.g. y-1 with y etc.
                    swop = front_end.grid[y-1][x] # assigns the temp variable for the swop
                                                  # to take place
                    front_end.grid[y-1][x] = front_end.grid[y][x] # swaps coordinates
                    front_end.grid[y][x] = swop # assigns swop back to coordinates
            #print(front_end.grid)
        for j in range(num_rows): # loops through the number of rows
            self.block_list = [[temp[0], temp[1] + 1, temp[2]] if
                               temp[1] < max(self.lines) else temp for temp in
                               self.block_list] # updates the self.block_list so that all the
                                                # y values that are less than the maximun value
                                                # of the self.lines list are incremented by 1
        #print(self.block_list)
        #print()
        #print(front_end.grid)
        self.coords = [temp[:2] for temp in self.block_list] # updates the self.coords list
                                                             # with only numbers, leaves out
                                                             # the colour
        self.redraw() # redraws the blocks

        self.lines = [] # resets the self.lines list to empty
        #print('remove line end')

    def redraw(self):
        # this function redraws the blocks onto the screen
        for x, y, colour in self.block_list: # loops through the block_list variables
            pg.draw.rect(front_end.background, colour, [x*16, y*16 - 320, 16, 16]) # draws the blocks
            front_end.background.convert()
            front_end.screen.blit(front_end.background, (0, 0)) # blits the background onto the screen
            pg.display.flip() # updates the display

    def repaint_background(self):
        # repaints the lines and background
        for x, y in self.coords: # loops through x, y coords of all the blocks
            if x % 2 == 0: # if x divided by 2 has no remainder then draw a grey block
                pg.draw.rect(front_end.background, (211, 211, 211), [x*16,
                                                                     y*16 - 320, 16,
                                                                     16])
                #print('repaint test')
            else: # else draw a white block
                pg.draw.rect(front_end.background, (255, 255, 255), [x*16,
                                                                     y*16 - 320, 16,
                                                                     16])
