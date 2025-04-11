import pygame
from car import Car

# === Config ===
WIDTH, HEIGHT = 800, 600
FPS = 60
TRACK_IMAGE = "track.png"  # Black = walls, White = road
START_POS = (100, 300)

# === Init ===
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self-Driving Virtual Car")
clock = pygame.time.Clock()

# === Load Track ===
track = pygame.image.load(TRACK_IMAGE).convert()
track = pygame.transform.scale(track, (WIDTH, HEIGHT))
track_mask = pygame.mask.from_surface(track)

# === Create Car ===
car = Car(*START_POS)

# === Main Loop ===
running = True
while running:
    screen.blit(track, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    car.update(screen, track_mask)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
