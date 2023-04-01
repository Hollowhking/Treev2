import pygame
import random

pygame.init()

# set colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()

def main():

    print ('Press q to quit')
    random.seed(0)

    pygame.init()

# Set up the drawing window
screen = pygame.display.set_mode([500, 500])
line_color = (255, 0, 0)

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    #X → F − [ [ X ] + X ] + F [ + F X ] − X
    # Draw a solid blue circle in the center
    pygame.draw.line(screen, line_color, (100, 200), (150, 250), 10)
    pygame.draw.circle(screen, (0, 0, 255), (250, 250), 75)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
