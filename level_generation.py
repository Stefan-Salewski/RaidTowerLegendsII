#*************************************************
#level_generation.py
#Has all the code to generate each level
#Can be called from main to generate a list of rooms
# Stefan Salewski
#*************************************************

import random
class level_generation():

#fun initialization
    def __init__(self, pygame_instance, screen_instance, width, height):
        self.width = width
        self.height = height
        self.screen = screen_instance
        self.pygame = pygame_instance
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        print("HELLO WORLD")

#lets go we can draw stuff in classes
    def generate_level(self, numrooms, roomlist, iteration):
        iteration = iteration
        #0 of this list should always be the starting room and len(roomlist) is the end of the level
        rooms = roomlist
        if len(rooms) > 0:
            generating = True
            while generating:
                randomnum = random.randint(0, 3)
                previousroom = rooms[iteration - 1]

                # Determine the new room position based on the random number
                if randomnum == 0:  # up
                    newrect = self.pygame.Rect(previousroom.x, previousroom.y + 60, 50, 50)
                elif randomnum == 1:  # left
                    newrect = self.pygame.Rect(previousroom.x - 60, previousroom.y, 50, 50)
                elif randomnum == 2:  # down
                    newrect = self.pygame.Rect(previousroom.x, previousroom.y - 60, 50, 50)
                elif randomnum == 3:  # right
                    newrect = self.pygame.Rect(previousroom.x + 60, previousroom.y, 50, 50)

                # Check if the new room position is already occupied
                occupied = False
                for room in rooms:
                    if newrect.x == room.x and newrect.y == room.y:
                        occupied = True
                        break

                if not occupied:
                    rooms.append(newrect)
                    generating = False

        else:
            #first room in the list
            rooms.append(self.pygame.Rect((self.width / 2), (self.height / 2), 50, 50))

        #recursion
        if iteration == numrooms - 1:
            return rooms
        else:
            return self.generate_level(numrooms, rooms, iteration + 1)

