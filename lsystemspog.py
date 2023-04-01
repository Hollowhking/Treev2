import pygame
from pygame.locals import *
from math import *
import sys
import random

# set colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)
BROWN = (139, 70, 19)

SYSRULES = {}  # generator system rules for l-system



def derivation(axiom, steps):
    derived = [axiom]  # seed
    for _ in range(steps):
        next_seq = derived[-1]
        next_axiom = [rule(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived


def rule(cmd):
    if cmd in SYSRULES:
        return SYSRULES[cmd]
    return cmd

clock = pygame.time.Clock()

class branch:
    def __init__(self, id, seg_length, startx, starty, endx, endy):
        self.id = id
        self.seg_length = seg_length
        self.startx = startx
        self.starty = starty
        self.endx = endx
        self.endy = endy
    def drawbranch(self, screen, seg_thickness):
        pygame.draw.line(screen,BROWN,(self.startx,self.starty),(self.endx,self.endy),int(seg_thickness))
    def updatebranch(self, angle):
        x2 = (self.seg_length*2)/2.0*sin(radians(angle))
        y2 = (self.seg_length*2)/2.0*cos(radians(angle))
        self.endx = self.endx - x2
        self.endy = self.endy - y2


def main():
    #-Init pygame stuff:----
    pygame.init()
    window_length = 600
    screen = pygame.display.set_mode((window_length, window_length))
    screen.fill(BLUE)
    #-----------------------
    #-l systems set up string----
    #rule = "F->FF"
    #rule = "F->F[+F][-F]"
    rule = "F->FF"
    key, value = rule.split("->")
    SYSRULES[key] = value
    #rule = "X->F[+X]F[-X]+X"
    #rule = "X->F[+X]F[--FX]FX"
    #rule = "X->FF+[-F-XF-X][XXX][+FF][--XF[+X]][+++F-X]"
    #rule = "X->F[+FX]+[FX]-F[-FX]"
    #rule = "X->[+FX--FXFF]"
    rule = "X->FF[+FFX][-FFX]"
    key, value = rule.split("->")
    SYSRULES[key] = value

    axiom = sys.argv[1]
    iterations = int(sys.argv[2])
    angle = float(sys.argv[3])
    t=pygame.time.get_ticks()
    posx = window_length/2.
    posy = window_length

    model = derivation(axiom, iterations)  # axiom (initial string), nth iterations
    fullstring = []
    for i in range(len(model)):
        for j in model[i]:
            fullstring.append(j)
    #-----------------------------------
    grow_angle = -90
    seg_length = 10
    seg_thickness = 1
    thickness_step = 0.2

    clock_ticks = pygame.time.get_ticks()

    saving_angle = []
    saving_endingofbraches = []
    listofbranches = []
    branchcount = 0
    step = 0

    #init update variables:
    clock = pygame.time.Clock()
    sway_angle = 0
    swap = False
    #-----------------
    for cmd in fullstring:
        if cmd == 'F':
            seg_length = random.randint(15,25)

            dx = int(cos(radians(grow_angle))*seg_length)
            dy = int(sin(radians(grow_angle))*seg_length)

            ang = abs(grow_angle)
            curbranch = branch(branchcount, seg_length, posx, posy, posx+dx, posy+dy)
            listofbranches.append(curbranch)
            curbranch.drawbranch(screen, seg_thickness)
            pygame.display.update((posx-1,posy-1,posx+dx+1,posy+dy+1))
            branchcount += 1
            #seg_thickness -= thickness_step
            posx = posx+dx
            posy = posy+dy

        elif cmd == '+':
            grow_angle += angle
        elif cmd == '-':
            grow_angle -= angle

        elif cmd == '[':
            saving_endingofbraches.append((posx,posy))
            saving_angle.append(grow_angle)
        elif cmd == ']':
            posx,posy = saving_endingofbraches.pop()
            grow_angle = saving_angle.pop()
        print(pygame.time.get_ticks()-t)

    try:
        for i in listofbranches:
            print("branch num: ",i.id, " start location: ", i.startx,",",i.starty," end location: ",i.endx,",",i.endy)
            pygame.draw.circle(screen, RED, (int(i.endx),int(i.endy)), 2)

        while step<200:
            clock.tick(30)
            for i in listofbranches:
                print("update branch: ",i.id," step num: ",step)
                #updatebranch:
                i.updatebranch(angle)
                i.drawbranch(screen, seg_thickness)
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
            pygame.display.flip()
            #print(step)
            #update
            if (sway_angle == 20):
                swap = True
            if (sway_angle == -5):
                swap = False
            if (swap):
                angle = sway_angle-1
            else:
                angle = sway_angle+1
            screen.fill(BLUE)
            #----------------
            step += 1
    finally:
        pygame.quit()
        system.exit(0)

if __name__ == '__main__':
    main()
