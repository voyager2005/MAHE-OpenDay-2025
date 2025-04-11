import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up canvas size
WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Draw Your Track (Press P to Save)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fill background with white
screen.fill(WHITE)

# Brush settings
brush_radius = 10
drawing = False

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Start drawing on mouse click
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                drawing = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pygame.image.save(screen, "track.png")
                print("Track saved as track.png ✅")

    if drawing:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.circle(screen, BLACK, mouse_pos, brush_radius)

    pygame.display.flip()
    clock.tick(60)
