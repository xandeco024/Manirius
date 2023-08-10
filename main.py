import pygame

pygame.init()

screenX = 1280
screenY = 720

screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("SMAUG-2")

looping = True

while looping:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            looping = False

    