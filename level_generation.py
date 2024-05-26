#*************************************************
#level_generation.py
#Has all the code to generate each level
#Can be called from main to generate a list of rooms
#Stefan Salewski
#*************************************************
import pygame.math

from Entity_Classes import Wall
import random
class level_generation():

#fun initialization
    def __init__(self, pygame_instance, screen, SCREEN_WIDTH, SCREEN_HEIGHT):
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.screen = screen
        self.pygame = pygame_instance
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        print("HELLO WORLD")

    def create_room(self, x, y):
        room = []

        #top wall
        topleft = Wall(x, y, 400, 10)
        topmid = Wall(x + 400, y, 200, 10)
        topright = Wall(x + 600, y + 200, 400, 10)

        room.append(topleft)
        room.append(topmid)
        room.append(topright)

        #left wall
        lefttop = Wall(x, y, 10, 400)
        leftdoor = Wall(x, y + 400, 10, 200)
        leftbot = Wall(x, y + 600, 10, 400)

        room.append(lefttop)
        room.append(leftdoor)
        room.append(leftbot)

        #bottom wall
        botleft = Wall(x, y + 1000, 400, 10)
        botdoor = Wall(x + 400, y + 1000, 200, 10)
        botright = Wall(x + 600, y + 1000, 400, 10)

        room.append(botleft)
        room.append(botdoor)
        room.append(botright)

        #right wall
        righttop = Wall(x + 1000, y, 10, 400)
        rightdoor = Wall(x + 1000, y + 400, 10, 200)
        rightbot = Wall(x + 1000, y + 600, 10, 400)

        room.append(righttop)
        room.append(rightdoor)
        room.append(rightbot)

        return room
    def edit_room(self, room):

        return

#lets go we can draw stuff in classes
    def generate_level(self, numrooms, roomlist, iteration, prevx, prevy):
        iteration = iteration
        prevx = prevx
        prevy = prevy

        #0 of this list should always be the starting room and len(roomlist) is the end of the level
        rooms = roomlist
        if len(rooms) > 0:
            generating = True
            while generating:
                randomnum = random.randint(0, 3)
                #previousroom = rooms[iteration - 1]

                # Determine the new room position based on the random number
                if randomnum == 0:  # up
                    newroom = self.create_room(prevx[len(prevx) - 1], prevy[len(prevy) - 1] + 1000)
                    newx = prevx[len(prevx) - 1]
                    newy = prevy[len(prevy) - 1] + 1000
                elif randomnum == 1:  # left
                    newroom = self.create_room(prevx[len(prevx) - 1] - 1000, prevy[len(prevy) - 1])
                    newx = prevx[len(prevx) - 1] - 1000
                    newy = prevy[len(prevy) - 1]
                elif randomnum == 2:  # down
                    newroom = self.create_room(prevx[len(prevx) - 1], prevy[len(prevy) - 1] - 1000)
                    newx = prevx[len(prevx) - 1]
                    newy = prevy[len(prevy) - 1] - 1000
                elif randomnum == 3:  # right
                    newroom = self.create_room(prevx[len(prevx) - 1] + 1000, prevy[len(prevy) - 1])
                    newx = prevx[len(prevx) - 1] + 1000
                    newy = prevy[len(prevy) - 1]

                occupied = False

                for i in range(len(prevx)):
                    if newx == prevx[i] and newy == prevy[i]:
                        occupied = True
                        break

                if not occupied:
                    prevx.append(newx)
                    prevy.append(newy)
                    rooms.append(newroom)
                    generating = False

        else:
            rooms.append(self.create_room(0, 0))
            prevx.append(0)
            prevy.append(0)

        #recursion
        if iteration == numrooms - 1:
            return rooms
        else:
            return self.generate_level(numrooms, rooms, iteration + 1, prevx, prevy)

