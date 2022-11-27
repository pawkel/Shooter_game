import pygame
pygame.init()
font = pygame.font.SysFont(None, 20)
def makeMsg(text, color = (0,0,0)):
    msg = font.render(text, True, color)
    return msg