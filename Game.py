import pygame
from Game_Classes import (Player,Gun)
pygame.init()
screen_width = 800
screen_hight = 800
font = pygame.font.SysFont(None, 50)
win = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption("Shooter game")
clock = pygame.time.Clock()
run = True
player1 = Player(win, screen_width, screen_hight, 1,name='Pawkel')
player2 = Player(win, screen_width, screen_hight, 2,name='Mlk99')

while run:
    win.fill((0,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    win.blit(player1.player, (player1.x, player1.y))
    win.blit(player2.player, (player2.x, player2.y))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        controls = font.render('P1 Arrow keys, P2 WASD', True, (0,0,0))
        win.blit(controls, (20,20))
    if keys[pygame.K_n]:
        p1name = font.render(str(player1.name), True, (0,0,0))
        p2name = font.render(str(player2.name), True, (0,0,0))
        win.blit(p1name, (player1.x, player1.y-20))
        win.blit(p2name, (player2.x, player2.y-20))
    player1.update(keys)
    player2.update(keys)
    pygame.display.update()
    clock.tick(30)
