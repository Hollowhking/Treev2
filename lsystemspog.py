import pygame
from pygame.locals import *
from math import *
import sys
import random
import math
import time

# set colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)
BROWN = (139, 70, 19)

SYSRULES = {}  # generator system rules for l-system
X_RULES = []
listofbranches = []

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
    if (cmd == 'X'):
      #x = random.random()
      return random.choice(X_RULES)
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

def drawtree(screen, fullstring, posx, posy, seg_thickness, da, iterations):
    #Add to drawtree
    saving_angle = []
    saving_endingofbraches = []
    branchcount = 0

    max_seg_thickness = seg_thickness
    grow_angle = -90
    text = MyText(BLACK)

    for cmd in fullstring:
        if cmd == 'F':
            seg_length = random.randint(15,25)
            grow_angle = random.randint(grow_angle-5,grow_angle+5)
            dx = cos(radians(grow_angle))*seg_length
            dy = sin(radians(grow_angle))*seg_length
            distance = math.sqrt((((posx+dx)-posx)**2)+(((posy+dy)-posy)**2))

            curbranch = branch(branchcount, distance, posx, posy, posx+dx, posy+dy)
            listofbranches.append(curbranch)


            if (seg_thickness <= 1):
                curbranch.drawbranch(screen, 2)
            else:
                curbranch.drawbranch(screen, int(seg_thickness))

            #pygame.display.update((posx-1,posy-1,posx+dx+1,posy+dy+1))
            #print (grow_angle)
            pygame.display.update()

            if (branchcount*iterations < iterations*5):
                grow_angle = -90

            branchcount += 1
            posx = posx+dx
            posy = posy+dy
            time.sleep(0.05)
            print(seg_thickness,"/",max_seg_thickness)

        elif cmd == '+':
            grow_angle += da
        elif cmd == '-':
            grow_angle -= da

        elif cmd == '[':
            if (branchcount*iterations > iterations*5):
                seg_thickness = seg_thickness-3
            saving_endingofbraches.append((posx,posy))
            saving_angle.append(grow_angle)
        elif cmd == ']':
            if (branchcount*iterations > iterations*5):
                seg_thickness = seg_thickness + 2
                #seg_thickness = max_seg_thickness
                #print(seg_thickness)
            posx,posy = saving_endingofbraches.pop()
            grow_angle = saving_angle.pop()

        text.draw("Iterations = %f" % iterations, screen, (10,10))
        text.draw("branch thickness = %f" % seg_thickness, screen, (10,40))

def maketree(axiom, iterations):
    model = derivation(axiom, iterations)  # axiom (initial string), nth iterations
    fullstringx = []
    #print(model)
    for i in range(len(model)):
        for j in model[i]:
            fullstringx.append(j)
    return fullstringx
#-MAIN-------------------
# def main():
def drawying(curimg):
    #-Init pygame stuff:----
    pygame.init()
    if (int(sys.argv[3]) == 1):
        window_length = 1224
        window_height = 720
    else:
        window_length = 800
        window_height = 800
    screen = pygame.display.set_mode((window_length, window_height))
    pygame.display.set_caption("Generating Trees")

    backgroundimg = pygame.image.load('a-banner-with-a-simple-spring-landscape-a-meadow-with-green-grass-and-a-blue-sky-with-clouds.png')

    screen.fill(WHITE)
    if (int(sys.argv[3]) == 1):
        screen.blit(backgroundimg, (0,0))
    #-----------------------
    #-l systems set up string----
    rule = "F->FF"
    key,value = rule.split("->")
    SYSRULES[key] = value

    rule = "X->F[-X]F[+FX]FX"
    key,value = rule.split("->")
    X_RULES.append(value)

    rule = "X->F-[[-X]+X]+F[+FX]-X"
    key, value = rule.split("->")
    X_RULES.append(value)

    rule = "X->F[-FX+FXF-F][+FXX]"
    key, value = rule.split("->")
    X_RULES.append(value)

    rule = "X->F[+X]F[-FX]FX"
    key, value = rule.split("->")
    X_RULES.append(value)

    SYSRULES[key] = value

    axiom = "X"
    iterations = 2
    da = 20
    t=pygame.time.get_ticks()
    posix = window_length/2.
    posiy = window_height

    clock_ticks = pygame.time.get_ticks()

    seg_thickness = int(sys.argv[1])

    #init update variables:
    clock = pygame.time.Clock()
    sway_angle = 0
    swap = False
    #-----------------
    step = 0

    #make tree:
    screen.fill(WHITE)
    if (int(sys.argv[3]) == 1):
        screen.blit(backgroundimg,(0,0))
    for i in range(int(sys.argv[2])):
        posix = random.randint(20,window_length)
        fullstring = maketree(axiom, iterations)
        drawtree(screen, fullstring, posix, posiy, seg_thickness, da, iterations)



    # for i in listofbranches:
    #     print("branch num: ",i.id, " start location: ", i.startx,",",i.starty," end location: ",i.endx,",",i.endy)
    #     pygame.draw.circle(screen, RED, (int(i.endx),int(i.endy)), 2)

    while step<80:
        clock.tick(30)
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.unicode == 'q':
                break
        pygame.display.flip()
        #print(step)
        step += 1

    pygame.image.save(screen, ("Tree"+str(curimg)+".jpeg"))
    pygame.quit()

def main():
    curimag = 1
    for i in range(1):
        drawying(curimag)
        curimag += 1
    sys.exit(0)



if __name__ == '__main__':
    main()
