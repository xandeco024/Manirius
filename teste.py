import pygame
import sys
import math

#Tileset
tilesetSprite = "Sprites/tileset.png"

tileWidth = 16
tileHeight = 16

map = [
    [0,1,2],
    [3,4,5],
    [6,7,8],
    [9,10,11],
    [12,13,14],
    [15,16,17],
    [18,19,20],
]

#não é uma matriz, é um vetor de 3 vetores. por isso o tamanho da linha 0, pra idicar a largura, e o tamanho do array principal pra definir a altura.
mapWidth = len(map[0] * tileWidth)
mapHeight = len(map * tileHeight)

pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("teste")

tileset = pygame.image.load(tilesetSprite).convert_alpha()

for row_index, row in enumerate(map):
    for col_index, col in enumerate(row):
        x = col_index * tileWidth * 4
        y = row_index * tileHeight * 4
        rect = pygame.Rect(col * tileWidth, 0, tileWidth, tileHeight)
        screen.blit(tileset, (x, y), rect)

pygame.display.flip()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()