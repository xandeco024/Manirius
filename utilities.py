import pygame
import sys

def cutSpritesheet(spritesheet_path, sprite_width, sprite_height):
    # Carrega a spritesheet
    spritesheet = pygame.image.load(spritesheet_path).convert_alpha()

    # Obtém as dimensões da spritesheet
    sheet_width, sheet_height = spritesheet.get_size()

    # Calcula o número de colunas e linhas de sprites na spritesheet
    columns = sheet_width // sprite_width
    rows = sheet_height // sprite_height

    # Cria uma lista para armazenar os sprites
    sprites = []

    # Percorre cada sprite na spritesheet
    for row in range(rows):
        for column in range(columns):
            # Calcula a posição do sprite na spritesheet
            x = column * sprite_width
            y = row * sprite_height

            # Corta o sprite da spritesheet
            sprite = spritesheet.subsurface(pygame.Rect(x, y, sprite_width, sprite_height))

            # Adiciona o sprite à lista de sprites
            sprites.append(sprite)

    return sprites

def calcMouseTilePos():

    mousePosition = pygame.mouse.get_pos()

    tileX = mousePosition[0] // 64
    tileY = mousePosition[1] // 64

    tileX = tileX * 64
    tileY = tileY * 64

    return (tileX, tileY) 

def inputCheck(inputs):
        
        for key in inputs: #reseta todos os inputs.
            inputs[key] = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #Fecha o jogo
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN: #Apertar tecla
                if event.key == pygame.K_1:
                    inputs['one'] = True
                
                if event.key == pygame.K_SPACE:
                    inputs['space'] = True

                if event.key == pygame.K_TAB:
                    inputs['tab'] = True

            if event.type == pygame.MOUSEBUTTONDOWN: #Botão do mouse
                
                if event.button == 1:
                    inputs['leftClick'] = True

                if event.button == 3:
                    inputs['rightClick'] = True 