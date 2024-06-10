import Entity_Classes
from Entity_Classes import Wall
import random


class level_generation ():

    # fun initialization
    def __init__ (self, pygame_instance, screen, SCREEN_WIDTH,
                  SCREEN_HEIGHT, chest_open, chest_closed, powerups):
        self.width = SCREEN_WIDTH
        self.powerups = powerups
        self.height = SCREEN_HEIGHT
        self.chest_open = chest_open
        self.chest_closed = chest_closed
        self.screen = screen
        self.pygame = pygame_instance
        self.level = 0
        self.exit = None

    # creating rooms with walls and doors
    def create_room (self, x, y, prevdoor, door, iteration, numrooms):
        room = []
        if (iteration == numrooms - 1):
            door = -1
            self.exit = Entity_Classes.Level_End (x + 500, y + 500, 50, 50)
        # top wall
        topleft = Wall (x, y, 400, 10)
        topright = Wall (x + 600, y, 400, 10)
        room.append (topleft)
        room.append (topright)
        if (prevdoor != 0 and door != 2):
            topdoor = Wall (x + 400, y, 200, 10)
            room.append (topdoor)

        # left wall
        lefttop = Wall (x, y, 10, 400)
        leftbot = Wall (x, y + 600, 10, 400)
        room.append (lefttop)
        room.append (leftbot)
        if (prevdoor != 3 and door != 1):
            leftdoor = Wall (x, y + 400, 10, 200)
            room.append (leftdoor)

        # right wall
        righttop = Wall (x + 1000, y, 10, 400)
        rightbot = Wall (x + 1000, y + 600, 10, 400)
        room.append (righttop)
        room.append (rightbot)
        if (prevdoor != 1 and door != 3):
            rightdoor = Wall (x + 1000, y + 400, 10, 200)
            room.append (rightdoor)

        # bottom wall
        if (prevdoor != 2 and door != 0):
            botdoor = Wall (x + 400, y + 1000, 200, 10)
            room.append (botdoor)
        botleft = Wall (x, y + 1000, 400, 10)
        botright = Wall (x + 600, y + 1000, 410, 10)
        room.append (botright)
        room.append (botleft)

        return room

    # lets go we can draw stuff in classes
    def generate_level (self, numrooms, roomlist, iteration, prevx, prevy,
                        randomnum):
        iteration = iteration
        prevx = prevx
        prevy = prevy
        rooms = roomlist
        if (len(rooms) > 0):
            generating = True
            # maximum number of attempts to avoid infinite loop
            max_attempts = 100
            attempts = 0
            while (generating and attempts < max_attempts):
                attempts += 1
                nextrandomnum = random.randint (0, 3)

                # determine the new room position based on the random number
                if (randomnum == 0):  # up
                    newx = prevx [-1]
                    newy = prevy [-1] + 1000
                elif (randomnum == 1):  # left
                    newx = prevx [-1] - 1000
                    newy = prevy [-1]
                elif (randomnum == 2):  # down
                    newx = prevx [-1]
                    newy = prevy [-1] - 1000
                elif (randomnum == 3):  # right
                    newx = prevx [-1] + 1000
                    newy = prevy [-1]

                # check if the new position is occupied
                occupied = any (newx == x and newy == y for x,
                y in zip (prevx, prevy))

                if (not occupied):
                    # check nextrandomnum placement
                    if (nextrandomnum == 0):  # up
                        checkx = newx
                        checky = newy + 1000
                    elif (nextrandomnum == 1):  # left
                        checkx = newx - 1000
                        checky = newy
                    elif (nextrandomnum == 2):  # down
                        checkx = newx
                        checky = newy - 1000
                    elif (nextrandomnum == 3):  # right
                        checkx = newx + 1000
                        checky = newy

                    if any (checkx == x and checky == y for x,
                    y in zip (prevx, prevy)):
                        continue  # skip this iteration if the next
                                  # position is occupied

                    # create the new room and update positions
                    newroom = self.create_room (newx, newy, randomnum,
                                                nextrandomnum, iteration,
                                                numrooms)
                    prevx.append (newx)
                    prevy.append (newy)
                    rooms.append (newroom)
                    generating = False

            # this should only happen with a layout that cant make more rooms
            # if it does then we can end it early
            if (attempts == max_attempts):
                return rooms
        else:
            # first room
            nextrandomnum = random.randint (0, 3)
            x = -500
            y = -500
            rooms.append (self.create_room(x, y, 4,
                                          nextrandomnum, iteration, numrooms))
            prevx.append (x)
            prevy.append (y)

        # check if we're done or need more rooms
        if (iteration == numrooms - 1):
            return rooms
        else:
            return self.generate_level (numrooms, rooms,
                                        iteration + 1, prevx, prevy,
                                        nextrandomnum)

    # type, "enemy" for enemies, "loot" for upgrades and stuff
    def populate_room ( self, roomlist, objectlist, type):
        for room in roomlist:
            room_center_x = room [0].x + 500
            room_center_y = room [0].y + 500
            amount_to_spawn = random.randint (0, 2 + self.level)

            if (roomlist[0] == room):
                amount_to_spawn = -1

            for i in range (amount_to_spawn):
                randomx = random.randint(room_center_x - 400,
                                         room_center_x + 400)
                randomy = random.randint(room_center_y - 400,
                                         room_center_y + 400)
                if (type == "enemy"):
                    object_to_add = Entity_Classes.Enemy (100 +
                                                          (10 * self.level /2),
                                                          2 + (10 * self.level)
                                                          , 4 + (self.level *
                                                                 0.5),
                                                          True, randomx,
                                                          randomy, 50,50)
                elif (type == "loot"):

                    object_to_add = Entity_Classes.Chest(randomx, randomy, 4,
                                                         random.randint (6 + (4 * self.level),
                                                                         20 + (5 * self.level)),
                                                         self.chest_closed,
                                                         self.chest_open,
                                                         self.powerups)
                else:
                    print ("invalid type")
                objectlist.append (object_to_add)
        return objectlist
