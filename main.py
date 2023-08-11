import pygame
import sys
import math

screenX = 1280
screenY = 720

attractiveObjects = pygame.sprite.Group()



scoreText = 0
scoreTextColor = (255, 255, 255)

class AttactiveOBJ(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Sprites/object.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, playerSpeed):
        super().__init__()
        self.image = pygame.image.load('Sprites/player.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.playerSpeed = playerSpeed

pygame.init()
screen = pygame.display.set_mode((screenX, screenY))
pygame.display.set_caption("SMAUG-2")

clock = pygame.time.Clock()

font = pygame.font.SysFont('Arial', 20)
player = Player(screenX/2, screenY/2, 5)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not attractiveObjects:
                attractiveOBJ = AttactiveOBJ(mousePos[0], mousePos[1])
                attractiveObjects.add(attractiveOBJ)
                scoreText += 1

                # Atualizando a posição do player
    if attractiveObjects:
        dx = attractiveOBJ.rect.centerx - player.rect.centerx
        dy = attractiveOBJ.rect.centery - player.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 5:
            player.rect.centerx += player.playerSpeed * dx / distance
            player.rect.centery += player.playerSpeed * dy / distance

        else:
            attractiveOBJ.kill()

    playerPos = player.rect.center
    mousePos = pygame.mouse.get_pos()

    scoreTextSurface = font.render(str(scoreText), True, scoreTextColor)
    scoreTextRect = scoreTextSurface.get_rect()
    scoreTextRect.center = (100, 200)

    screen.fill((0, 0, 0))
    
    if attractiveObjects:
        pygame.draw.line(screen, (255, 0, 0), playerPos, attractiveOBJ.rect.center)

    screen.blit(scoreTextSurface, scoreTextRect)
    attractiveObjects.draw(screen)
    screen.blit(player.image, player.rect)
    clock.tick(60)
    pygame.display.update()