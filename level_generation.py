#*************************************************
#level_generation.py
#Has all the code to generate each level
#Can be called from main to generate a list of rooms
# Stefan Salewski
#*************************************************

import random
class level_generation():

#fun initialization :D
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
            randomnum = random.randint(0, 3)
            #up
            previousroom = rooms[iteration - 1]
            if randomnum == 0:
                rooms.append(self.pygame.Rect(previousroom.x, previousroom.y + 60, 50, 50))
            #left
            elif randomnum == 1:
                rooms.append(self.pygame.Rect(previousroom.x - 60, previousroom.y, 50, 50))
            #down
            elif randomnum == 2:
                rooms.append(self.pygame.Rect(previousroom.x, previousroom.y - 60, 50, 50))
            #right
            elif randomnum == 3:
                rooms.append(self.pygame.Rect(previousroom.x + 60, previousroom.y, 50, 50))

        else:
            #first room in the list
            rooms.append(self.pygame.Rect((self.width / 2), (self.height / 2), 50, 50))

        #recursion
        if iteration == numrooms:
            return rooms
        else:
            return self.generate_level(numrooms, rooms, iteration + 1)

