import pygame
import sys
import math

#region Inicio do codigo

pygame.init()
screen = pygame.display.set_mode((640, 640),0,32)
pygame.display.set_caption("SMAUG-2")
clock = pygame.time.Clock()

#endregion

attractiveObjects = pygame.sprite.Group()

#Sprites
playerSprite = "Sprites/player.png"

#Tileset
tileWidth = 64
tileHeight = 64
tilesetSprite = "Sprites/tileset.png"
tileset = pygame.image.load(tilesetSprite).convert_alpha()

map = [
    [1,0,1,0,1],
    [1,0,0,0,1],
    [1,0,0,0,0],
    [1,1,1,1,0],
    [1,1,1,1,0]
]

#não é uma matriz, é um vetor de 3 vetores. por isso o tamanho da linha 0, pra idicar a largura, e o tamanho do array principal pra definir a altura.
#HUD
scoreText = 0
scoreTextColor = (255, 255, 255)

class AttactiveOBJ(pygame.sprite.Sprite): #Classe do objeto atraente
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('Sprites/object.png').convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

class Player(pygame.sprite.Sprite): #Classe do player
    def __init__(self, x, y, playerSpeed):
        super().__init__()
        self.image = pygame.image.load(playerSprite).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.playerSpeed = playerSpeed

playerStartPos = (0, 0)

font = pygame.font.SysFont('Arial', 20)
player = Player(playerStartPos[0], playerStartPos[1], 2)

angle = 0

tilemap = pygame.Surface((640, 640))

while True: #Game Loop
    
    screen.fill((100, 100, 100))

    #Atualizações 
    clock.tick(60)
    playerPos = player.rect.center
    mousePos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #Fecha o jogo
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Cria objeto no lugar do clique
            if not attractiveObjects:
                attractiveOBJ = AttactiveOBJ(mousePos[0], mousePos[1])
                attractiveObjects.add(attractiveOBJ)
                scoreText += 1

    if attractiveObjects: #move o player em direção ao objeto
        dx = attractiveOBJ.rect.centerx - player.rect.centerx
        dy = attractiveOBJ.rect.centery - player.rect.centery
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 5:
            player.rect.centerx += player.playerSpeed * dx / distance
            player.rect.centery += player.playerSpeed * dy / distance

        else: #destroi o objeto quando o player chega nele
            attractiveOBJ.kill()

    #region cut tiles
    tiles = []

    tile = pygame.Surface((tileWidth,tileHeight)).convert_alpha()
    tile.blit(tileset, (0,0), (0 * 64, 0, tileWidth, tileHeight))


    #endregion


    #desenha o mapa
    
    '''
    tileRects = []
    y = 0
    for row in map:
        x = 0
        for tile in row:
            if tile == 1:
                tilemap.blit(tilemap, (x * tileWidth, y * tileHeight), (0,0, tileWidth, tileHeight))

            if tile != 0:
                tileRects.append(pygame.Rect(x * tileWidth, y * tileHeight, tileWidth, tileHeight))
            x += 1
        y += 1

    scaledTilemap = pygame.transform.scale(tilemap, (640,640))
    screen.blit(scaledTilemap, (0,0))
    '''


    #region Score
    scoreTextSurface = font.render(str(scoreText), True, scoreTextColor)
    scoreTextRect = scoreTextSurface.get_rect()
    scoreTextRect.center = (100, 200)
    #endregion

    if attractiveObjects:
        pygame.draw.line(screen, (255, 0, 0), playerPos, attractiveOBJ.rect.center)

    screen.blit(scoreTextSurface, scoreTextRect)
    attractiveObjects.draw(screen)

    playerRotatedImg = pygame.transform.rotate(player.image, angle)
    playerRotatedImgRect = playerRotatedImg.get_rect(center = player.rect.center)
    screen.blit(playerRotatedImg, playerRotatedImgRect)

    pygame.display.update() #Atualiza a tela