
import pygame
from pygame.locals import *
from math import *

# set colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)
BROWN = (139, 70, 19)


clock = pygame.time.Clock()

class branch():
    def __init__(self, name, pos_start, pos_end):
        self.name = name
        self.pos_start = pos_start
        self.pos_end = pos_end

    #def draw(self):


def getstring(iterations):
    s = ['X']

    for i in range(iterations):
        #X -> F-[[X]+X]+F[+FX]-X
        #X -> F[+X]F[-FX]FX (josh)
        #F-FF
        X_make = ['F', '[','+','X',']','F','[','-','F','X',']','F','X']
        F_make = ['F', 'F']
        j = 0
        while j<len(s):
            if s[j] == 'X':
                s.pop(j)#replace X with our X_make list
                for item in X_make[::-1]: s.insert(j,item)
                j+=17#bump j up to skip over added items
            elif s[j] == 'F':
                s.pop(j)
                for item in F_make[::-1]: s.insert(j,item)
                j+=1
            j+=1
    return s

def main():
    pygame.init()

    win_length = 600
    screen = pygame.display.set_mode((win_length, win_length))
    screen.fill(BLUE)

    #
    unit = 3
    angle = -90
    da = 20
    #

    t=pygame.time.get_ticks()
    s = getstring(7)
    print(pygame.time.get_ticks()-t)

    t = pygame.time.get_ticks()
    pos = win_length/2.,win_length

    saved_angles = []
    saved_poses = []
    for letter in s:
        if letter == 'F':
            dx = cos(radians(angle))*unit
            dy = sin(radians(angle))*unit

            a = abs(angle)
            pygame.draw.line(screen,BROWN,pos,(pos[0]+dx,pos[1]+dy), 2)
            pygame.display.update((pos[0]-1,pos[1]-1,pos[0]+dx+1,pos[1]+dy+1))

            pos = (pos[0]+dx, pos[1]+dy)

        elif letter == '+':
            angle += da
        elif letter == '-':
            angle -= da
        elif letter == '[':
            saved_poses.append(pos)
            saved_angles.append(angle)
        elif letter == ']':
            pos = saved_poses.pop()
            angle = saved_angles.pop()
    print(pygame.time.get_ticks()-t)

    try:
        while 1:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
            pygame.display.flip()
    finally:
        pygame.quit()

if __name__ == '__main__':
    main()
