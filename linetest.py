import pygame
import math

pygame.init()
screen_size = 600
surface = pygame.display.set_mode((screen_size,screen_size))

step = 0
angle_per_step = .05
angle = 0
swap = False
# animation loop
while (step<300):

    # erase background each time
    surface.fill((0, 0, 0))  # erase surface memory before we draw new things

    #update draw rules
    # seg_length = 2
    # angle = 20
    connection_pointx = 0
    connection_pointy = 0
    # end_pointx = seg_length/2.0*math.sin(angle)
    # end_pointy = seg_length/2.0*math.cos(angle)
    #

    #pygame.draw.line(surface, (255,255,0), (connection_pointx,connection_pointy),(end_pointx,end_pointy), 4)

    line_len = 50
    cx = cy = screen_size // 2 # center of rotation
    x = line_len/4.0*math.sin(math.radians(angle))
    y = line_len/4.0*math.cos(math.radians(angle))

    pygame.draw.line(surface, (255,255,0), (connection_pointx,connection_pointy),((cx-x),(cy-y)), 4)

    x2 = (line_len*2)/2.0*math.sin(math.radians(angle))
    y2 = (line_len*2)/2.0*math.cos(math.radians(angle))
    pygame.draw.line(surface, (255,0,255), ((cx-x),(cy-y)),((cx-x2),(cy-y2)),4)
    # update to display, await clock check for quit advance animation state
    pygame.display.update()
    pygame.time.Clock().tick(60)

    print("step: ",step," angle: ",angle)
    if pygame.event.peek(pygame.QUIT):  # detect user quit
        break
    if (angle == 95):
        swap = False
    if (angle == 20):
        swap = True
    if (angle == -5):
        swap = False

    if (swap):
        angle = angle-1
    else:
        angle = angle+1

    step += 1  # advance state of animation


pygame.quit()  # close window
