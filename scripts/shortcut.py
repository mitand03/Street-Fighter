import pygame


BASE1='graphics/ninja/png/'
BASE2='graphics/knight/png/'

def load_ninja(path):
    surf=pygame.image.load(BASE1 + path)
    surf=pygame.transform.rotozoom(surf,1,0.2)
    return surf

def load_knight(path):
    surf=pygame.image.load(BASE2 + path)
    surf=pygame.transform.rotozoom(surf,1,0.15)
    return surf

