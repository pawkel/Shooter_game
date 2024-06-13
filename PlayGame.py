import pygame
from Game_Classes import Game
from PlayerClass import Player
from helpers import makeMsg
pygame.init()
screen_width = 800
screen_hight = 800
font = pygame.font.SysFont(None, 20)
win = pygame.display.set_mode((screen_width, screen_hight))
pygame.display.set_caption("Shooter game")
clock = pygame.time.Clock()
run = True
player1 = Player(win, screen_width, screen_hight, 1,name='Pawkel')
player2 = Player(win, screen_width, screen_hight, 2,name='Mlk99')
game = Game(win, player1, player2, screen_width, screen_hight)
game.spawnWave()

while run:
    p1_shoot = 0
    p2_shoot = 0
    win.fill((100,175,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key==player1.controls['Shoot']:
                p1_shoot = 1          
            if event.key==player2.controls['Shoot']:
                p2_shoot = 1
    
    win.blit(player1.image, (player1.x, player1.y))
    win.blit(player2.image, (player2.x, player2.y))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        controls = font.render('P1 8456 Enter to shoot, P2 WASD Space to shoot', True, (0,0,0))
        win.blit(controls, (20,20))
    if keys[pygame.K_n]:
        p1name = font.render(str(player1.name)+str(player1.rect), True, (0,0,0))
        p2name = font.render(str(player2.name)+str(player2.rect), True, (0,0,0))
        win.blit(p1name, (player1.x, player1.y-20))
        win.blit(p2name, (player2.x, player2.y-20))
        for e in game.enemys:
            text = font.render(str(e.rect.top)+'_'+str(e.rect.left)+'_'+str(e.health), True, (0,0,0))
            win.blit(text, (e.x+10, e.y-10))
    player1.update(keys, p1_shoot)
    player2.update(keys, p2_shoot)
    game.update_enemys()
    if len(game.enemys) == 0:
        print(f"game wave: {game.wave}")
        game.spawnWave()
    pygame.display.update()
    clock.tick(40)

pygame.quit()