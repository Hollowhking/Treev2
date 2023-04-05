import pygame
from pygame.locals import *
from math import *
import sys
import random
import math

# set colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)
BROWN = (139, 70, 19)

SYSRULES = {}  # generator system rules for l-system
X_RULES = []

#set up text:
class MyText():
    def __init__(self, color, background=WHITE, antialias=True, fontname="comicsansms", fontsize=24):
        pygame.font.init()
        self.font = pygame.font.SysFont(fontname, fontsize)
        self.color = color
        self.background = background
        self.antialias = antialias

    def draw(self, str1, screen, pos):
        text = self.font.render(str1, self.antialias, self.color, self.background)
        screen.blit(text, pos)

def derivation(axiom, steps):
    derived = [axiom]  # seed
    for _ in range(steps):
        next_seq = derived[-1]
        next_axiom = [rule(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived


def rule(cmd):
    #if (cmd == 'X'):
       #x = random.random()
    #   return random.choice(X_RULES)
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
        self.tempx = 0
        self.tempy = 0
    def drawbranch(self, screen, seg_thickness):
        pygame.draw.line(screen,BLACK,(self.startx,self.starty),(self.endx,self.endy),int(seg_thickness))

    def updatebranch(self, newstartx, newstarty, newendx, newendy):#FIX
        self.startx = newstartx
        self.starty = newstarty
        self.endx = newendx
        self.endy = newendy


def main():
    #-Init pygame stuff:----
    pygame.init()
    window_length = 700
    screen = pygame.display.set_mode((window_length, window_length))
    pygame.display.set_caption("Generating Trees")
    screen.fill(WHITE)
    text = MyText(BLACK)
    #-----------------------
    #-l systems set up string----
    # rule = "F->FF"
    # #rule = "F->F[+F][-F]"
    # #rule = "F->F[-FF]+[FFF]-FF[-F-F]"
    # key, value = rule.split("->")
    # SYSRULES[key] = value
    rule = "F->FF"
    key,value = rule.split("->")
    SYSRULES[key] = value
    #rule = "X->F[+XF]F[-X]+X"
    # rule = "X->F[+X]F[--FX]FX"
    rule = "X->F[+X]F[-FX]FX"
    key,value = rule.split("->")
    X_RULES.append(value)
    rule = "X->F[+FX]+[FX]-F[-FX]"
    key, value = rule.split("->")
    X_RULES.append(value)
    rule = "X->[+FX-FXFF][-FXX]"
    key, value = rule.split("->")
    X_RULES.append(value)
    #rule = "X->FF[+FFX][-FFX]"
    #rule = "X->F-[[X]+X]+F[+FX]-X"

    rule = "X->F[+X]F[-FX]FX"
    #rule = "X->[-FX]+FX"
    key, value = rule.split("->")
    X_RULES.append(value)

    SYSRULES[key] = value

    axiom = sys.argv[1]
    iterations = int(sys.argv[2])
    da = float(sys.argv[3])
    t=pygame.time.get_ticks()
    posx = window_length/2.
    posy = window_length

    model = derivation(axiom, iterations)  # axiom (initial string), nth iterations
    fullstring = []
    #print(model)
    for i in range(len(model)):
        for j in model[i]:
            fullstring.append(j)
    #-----------------------------------
    grow_angle = -90
    seg_length = 10
    seg_thickness = 1
    thickness_step = 0.1

    clock_ticks = pygame.time.get_ticks()

    saving_angle = []
    saving_endingofbraches = []
    listofbranches = []
    branchcount = 0

    #init update variables:
    clock = pygame.time.Clock()
    sway_angle = 0
    swap = False
    #-----------------
    print(fullstring)
    step = 0

    for cmd in fullstring:
        if cmd == 'F':
            seg_length = random.randint(15,25)
            grow_angle = random.randint(grow_angle-5,grow_angle+5)
            dx = cos(radians(grow_angle))*seg_length
            dy = sin(radians(grow_angle))*seg_length
            distance = math.sqrt((((posx+dx)-posx)**2)+(((posy+dy)-posy)**2))

            curbranch = branch(branchcount, distance, posx, posy, posx+dx, posy+dy)
            listofbranches.append(curbranch)
            curbranch.drawbranch(screen, int(seg_thickness))
            pygame.display.update((posx-1,posy-1,posx+dx+1,posy+dy+1))


            branchcount += 1
            #seg_thickness -= thickness_step
            posx = posx+dx
            posy = posy+dy

        elif cmd == '+':
            grow_angle += da
        elif cmd == '-':
            grow_angle -= da

        elif cmd == '[':
            saving_endingofbraches.append((posx,posy))
            saving_angle.append(grow_angle)
        elif cmd == ']':
            posx,posy = saving_endingofbraches.pop()
            grow_angle = saving_angle.pop()
        #print(pygame.time.get_ticks()-t)


    try:
        #note parents of all branches:


        # for i in listofbranches:
        #     print("branch num: ",i.id, " start location: ", i.startx,",",i.starty," end location: ",i.endx,",",i.endy)
        #     pygame.draw.circle(screen, RED, (int(i.endx),int(i.endy)), 2)
        # text.draw("Iterations = %f" % iterations, screen, (10,10))
        sway_angle = -90



        while step<200:
            clock.tick(30)
            #screen.fill(WHITE)
            #for i in listofbranches:
                #print("update branch: ",i.id," step num: ",step, " new end: ",i.endx,",",i.endy, " with angle: ",sway_angle)
                #updatebranch:
                #i.updatebranch(sway_angle) #<------THIS COMMAND LAGS THE SYSTEM!
                #i.drawbranch(screen, seg_thickness)
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                    break
            pygame.display.flip()
            #print(step)
            #update

            if (sway_angle == -95):
                #print("SWAP TO NEG")
                swap = True
            if (sway_angle == -120):
                #print("SWAP TO POS")
                swap = False
            if (swap):
                sway_angle = sway_angle-1
            else:
                sway_angle = sway_angle+1
            #----------------
            step += 1
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == '__main__':
    main()
