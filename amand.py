import pygame
import math

def animate_rotating_line(point, radius, angle):
    pygame.init()

    # Set up the display window
    width, height = 640, 480
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Rotating Line")

    # Set up the clock
    clock = pygame.time.Clock()

    # Set up the line
    line_length = 100
    line_color = (255, 255, 255)

    # Run the animation loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        # Calculate the endpoint of the line
        x = point[0] + radius * math.cos(angle)
        y = point[1] + radius * math.sin(angle)
        endpoint = (x, y)

        # Draw the line
        screen.fill((0, 0, 0))
        pygame.draw.line(screen, line_color, point, endpoint, 2)

        # Update the angle for the next frame
        angle += 0.01

        # Update the display
        pygame.display.flip()

        # Wait for the next frame
        clock.tick(60)

# Example usage
point = (320, 240)
radius = 100
angle = 0
animate_rotating_line(point, radius, angle)
