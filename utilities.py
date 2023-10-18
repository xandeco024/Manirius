import pygame

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