import pygame
from pygame.locals import *
from math import *
import sys
import random
import math
import time

# set colours for sim
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)
BROWN = (139, 70, 19)

SYSRULES = {}  # generator system rules for l-system
X_RULES = []
listofbranches = []

clock = pygame.time.Clock()

"""
Class: MyText
The MyText class is used to store the text information for the simulation.
"""
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

"""
Class: Branch
The Branch class is used to store branch data.
"""
class Branch:
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
        # draw branch based on updated state variables
        pygame.draw.line(screen,BLACK,(self.startx,self.starty),(self.endx,self.endy),int(seg_thickness))

# function: derivation
    # parameters: string axiom, int steps
    # returns: string[] derived
    # desc: takes the axiom and # of steps and converts it to a list of chars for the commands
def derivation(axiom, steps):
    derived = [axiom]  # seed
    for _ in range(steps):
        next_seq = derived[-1]
        next_axiom = [rule(char) for char in next_seq]
        derived.append(''.join(next_axiom))
    return derived

# function: rule
    # parameters: string cmd
    # returns: string X_rules
    # desc: takes the turtle command and returns a random production rule
def rule(cmd):
    if (cmd == 'X'):
      # return random production rule for iteration
      return random.choice(X_RULES)
    if cmd in SYSRULES:
        return SYSRULES[cmd]
    return cmd

# function: drawtree
    # parameters: screen, fullstring, posx, posy, seg_thickness, da, iterations
    # returns: none
    # desc: takes the screen, state of branch and angle, # of iterations and draws the tree
def drawtree(screen, fullstring, posx, posy, seg_thickness, da, iterations):
    # store the state in array
    state_endofbranch = []
    state_angle = []
    state_thickness = []

    # set initial variables
    branchcount = 0
    grow_angle = -90
    text = MyText(BLACK)

    # loop through symbols in string
    for symbol in fullstring:
        if symbol == 'F':
            seg_length = 10
            grow_angle = random.randint(grow_angle - 2, grow_angle + 2)

            # calculate state of turtle using update rule of equations (1) and (2)
            dx = cos(radians(grow_angle)) * seg_length
            dy = sin(radians(grow_angle)) * seg_length

            # calculate length of line with pythagorean therom
            distance = math.sqrt((((posx + dx) - posx)**2)+(((posy + dy) - posy)**2))

            # save current branch and append to list
            curbranch = Branch(branchcount, distance, posx, posy, posx+dx, posy+dy)
            listofbranches.append(curbranch)

            # functionality for differing branch thickness based on current thickness
            if (seg_thickness <= 1):
                curbranch.drawbranch(screen, 2)
            else:
                curbranch.drawbranch(screen, int(seg_thickness))

            # update display so tree growth drawn
            pygame.display.update()

            # functionality to reduce chance tree grows sideways
            if ((branchcount * iterations) < (iterations * 5)):
                grow_angle = -90

            # increment branch count
            branchcount += 1

            # update position state
            posx = posx + dx
            posy = posy + dy

            # sleep simulation so change to tree can be observed while growing
            time.sleep(0.05)

        elif symbol == '+':
            # if symbol '+', turn left by change in angle
            grow_angle += da

        elif symbol == '-':
            # if symbol '-', turn right by change in angle
            grow_angle -= da

        elif symbol == '[':
            # if symbol '[', change thickness and append state of branch

            # decrease thickness for new branch
            seg_thickness -= 1

            # state of branch stored as x and y of end of branches and angle
            state_endofbranch.append((posx,posy))
            state_angle.append(grow_angle)
            state_thickness.append(seg_thickness)

        elif symbol == ']':
            # if symbol ']', pop state of branch from list
            # replace current state of turtle with state removed
            posx, posy = state_endofbranch.pop()
            grow_angle = state_angle.pop()
            seg_thickness = state_thickness.pop()

        text.draw("Iterations = %f" % iterations, screen, (10,10))
        text.draw("Branch Thickness = %f" % seg_thickness, screen, (10,40))

# function: maketree
    # parameters: string axiom, int iterations
    # returns: string fullstringx
    # desc: takes the screen, state of branch and angle, # of iterations and draws the tree
def maketree(axiom, iterations):
    # get list of symbols for number of iterations
    model = derivation(axiom, iterations)  # axiom (initial string), nth iterations
    fullstringx = []

    # loop through elements in model
    for i in range(len(model)):
        # loop through symbols
        for j in model[i]:
            # append to list
            fullstringx.append(j)
    return fullstringx

# function: draw_landscape
    # parameters: int current_run
    # returns: none
    # desc: generates the window for the simulation
def draw_landscape(current_run):
    # create pygame window
    pygame.init()

    # change the background size if background image included
    if (int(sys.argv[3]) == 1):
        window_length = 800
        window_height = 793
    else:
        window_length = 800
        window_height = 800

    # set up pygame screen and caption window
    screen = pygame.display.set_mode((window_length, window_height))
    pygame.display.set_caption("Generating Trees")
    backgroundimg = pygame.image.load('background_size.png')
    screen.fill(WHITE)

    # add background image if cmd-line arg 3 is equal to 1
    if (int(sys.argv[3]) == 1):
        screen.blit(backgroundimg, (0,0))

    # initial rule
    rule = "F->FF"
    key,value = rule.split("->")
    SYSRULES[key] = value

    # four predefined rules to generate random tree
    rule = "X->F[-X]F[+FX]FX"
    key,value = rule.split("->")
    X_RULES.append(value)

    # rule commented out since it produced unsatisfactory results
    # rule = "X->F-[[-X]+X]+F[+FX]-X"
    # key, value = rule.split("->")
    # X_RULES.append(value)

    rule = "X->F[-FX+FXF-F][+FXX]"
    key, value = rule.split("->")
    X_RULES.append(value)

    rule = "X->F[+X]F[-FX]FX"
    key, value = rule.split("->")
    X_RULES.append(value)

    SYSRULES[key] = value

    # define l-system parameters for sim
    axiom = "X"
    iterations = int(sys.argv[1])
    da = 20

    # set available area for tree to be drawn with floor operation for int
    posix = window_length // 2
    posiy = window_height

    # init update variables
    clock = pygame.time.Clock()
    clock_ticks = pygame.time.get_ticks()
    seg_thickness = iterations * 5
    step = 0

    # make tree based on parameters
    screen.fill(WHITE)

    # add background again?
    if (int(sys.argv[3]) == 1):
        screen.blit(backgroundimg,(0,0))

    # store location of trees drawn
    state_location = []

    # create number of trees specified in cmd-line argument 2
    for i in range(int(sys.argv[2])):

        # find random position for tree to grow based on window_length
        posix = random.randint(20, window_length)

        # loop until a grow location reached that doesn't have another tree
        # attempt to get trees to not grow on one another
        # while (posix in state_location):
        #     posix = random.randint(20, window_length)
        #     state_location.append(posix)

        # get list of elements for creating tree
        fullstring = maketree(axiom, iterations)

        # draw the tree based on parameters
        drawtree(screen, fullstring, posix, posiy, seg_thickness, da, iterations)

    # for i in listofbranches:
    #     print("branch num: ",i.id, " start location: ", i.startx,",",i.starty," end location: ",i.endx,",",i.endy)
    #     pygame.draw.circle(screen, RED, (int(i.endx),int(i.endy)), 2)

    # loop until a key is clicked
    while step < 80:
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

    # save final img of tree
    pygame.image.save(screen, ("Tree"+str(current_run)+".jpeg"))
    pygame.quit()

def main():
    current_run = 1

    # for loop so multiple windows can be generated
    for i in range(1):
        # call draw_landscape and increment current_run
        draw_landscape(current_run)
        current_run += 1

    sys.exit(0)

if __name__ == '__main__':
    main()
