import pygame
import random
import numpy as np
from NPC import (Enemy, Bullet)
from helpers import makeMsg
class Game():
    def __init__(self,win,p1, p2, scWidth, scHeight, totalWaves=10):
        self.win = win
        self.screenWidth= scWidth
        self.screenHeight = scHeight
        self.p1  = p1
        self.p2  = p2
        self.wave = 0
        self.totalWaves = totalWaves
        self.enemys = pygame.sprite.Group()
        self.players = pygame.sprite.Group()
        self.players.add(p1)
        self.players.add(p2)
    def spawnWave(self):
        self.enemys.empty()
        for activeID in self.p1.activeWeaponIDs:
            self.p1.weapons[activeID].bullets.empty()
        for activeID in self.p2.activeWeaponIDs:
            self.p2.weapons[activeID].bullets.empty()

        p_notNormal = self.wave/self.totalWaves
        p_normal = 1 - p_notNormal
        for i in range(5+self.wave*2):
            if np.random.random(1) < p_normal:
                self.enemys.add(Enemy('Normal',self.screenWidth, self.screenHeight))
            else:
                if np.random.random(1) >=0.5:
                    self.enemys.add(Enemy('Big',self.screenWidth, self.screenHeight))    
                else:
                    self.enemys.add(Enemy('Small',self.screenWidth, self.screenHeight))              
        self.wave +=1

    def updatePos(self, x0,y0,x1, y1, speed):
        dx1, dy1 = x0- x1,  y0- y1
        dis = np.sqrt(dx1**2+dy1**2)
        if dis ==0:
            dis = 1
        dx = -dx1/dis*speed
        dy = -dy1/dis*speed
        return dis, dx,dy

    def check_hit_list(self, player):
        hit_list =  []
        for activeID in player.activeWeaponIDs:
            bullets = player.weapons[activeID].bullets
            enmey_hit_list = pygame.sprite.groupcollide(bullets, self.enemys, False, False)
            #find all the enmey that got hit by all the bullets
            usedBullets = []
            for idx, bullet_id in enumerate(enmey_hit_list):
                bullet_hits = enmey_hit_list[bullet_id]
                if len(bullet_hits) > 0:
                    hit_list.extend(bullet_hits)
                    for e in bullet_hits:
                        e.health -=1
                        print(f"{e.typeName} got hit by {player.name}, health {e.health}")
                        if e.health <=0: ## if it dies
                            player.score += e.score ## add this enemey's score to player's score 
                    usedBullets.append(bullets.sprites()[idx])
            bullets.remove(usedBullets) ## kill the bullets that hit a monster
        return hit_list

    def update_enemys(self):
        wave = makeMsg(f"Wave {self.wave}", color = (255,0,0))
        self.win.blit(wave,  (self.screenWidth//2-10, 20))
        hit_list1 = self.check_hit_list(self.p1)
        hit_list2 = self.check_hit_list(self.p2) 
        deadMonsters = []
        for enemy in self.enemys:
            if enemy in hit_list1 or enemy in hit_list2:
                if enemy.health <=0:
                    deadMonsters.append(enemy)
                continue
            dis1, dx1, dy1 = self.updatePos(enemy.x,  enemy.y, self.p1.x, self.p1.y,enemy.speed)
            dis2, dx2, dy2 = self.updatePos(enemy.x,  enemy.y, self.p2.x, self.p2.y,enemy.speed)
            if dis1>=dis2:
                enemy.x += dx2 #+ np.random.random()
                enemy.y += dy2 #+ np.random.random()
            else:
                enemy.x += dx1 #+ np.random.random()
                enemy.y += dy1 #+ np.random.random()
            if enemy.x >self.screenWidth:
                enemy.x = 15
            elif enemy.x < 0:
                enemy.x = self.screenWidth - 50
            if enemy.y >self.screenHeight:
                enemy.y = 15
            elif enemy.y < 0:
                enemy.y = self.screenHeight -50
            enemy.rect.left, enemy.rect.top = enemy.x, enemy.y
        ## kill and remove all of dead monsters
        self.enemys.remove(*deadMonsters)
        for enemy in self.enemys:
            self.win.blit(enemy.image,(enemy.x,enemy.y))

