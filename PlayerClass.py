from NPC import Gun
import pygame
import random
import numpy as np
from helpers import makeMsg

class Player(pygame.sprite.Sprite):
    def __init__(self,win, screenwidth, screenhight, id,name=''):
        pygame.sprite.Sprite.__init__(self)
        self.screenwidth = screenwidth
        self.screenhight = screenhight
        self.win = win
        sc_w, sc_h = 1920, 1080
        scalingFactor = sc_h / sc_w
        self.x = random.randrange(1, self.screenwidth)
        self.y = random.randrange(1, self.screenhight)
        self.speed = 5
        self.gold = 100
        self.score = 0
        self.id = id
        self.health = 3
        self.name = f'P{id} '
        self.weapons = []
        self.activeWeaponIDs = []
        self.armors = []
        self.controls = {}
        self.players_skins = ['Classic_player.png', 'Dark_guy.png', 'Emoji_guy.png']
        if self.id == 1:
            self.msgLocationX = 10
            self.color  = (50, 250, 0)
        else:
            self.msgLocationX = self.screenwidth - 120
            self.color  = (25, 25, 250)
        if name == '':
            self.name = f'Player{id}'
        else:
            self.name += name
        skin = random.randrange(0,len(self.players_skins))
        player = pygame.image.load(self.players_skins[skin])
        self.image = pygame.transform.scale(player, (20,20))
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top= self.x, self.y
        self.controlOptions()
        self.AddWeapon()

    def showPlayerStatus(self):
        name = makeMsg(self.name, color = self.color)
        score = makeMsg(f"score: {self.score}",color = (0, 0, 0))
        health = makeMsg(f"Health: {self.health}", color = (0, 0, 0))
        self.win.blit(name,  (self.msgLocationX, 20))
        self.win.blit(score,  (self.msgLocationX+20, 35))
        self.win.blit(health, (self.msgLocationX+20, 50))

    def controlOptions(self):
        if self.id == 1:
            self.controls= {'Up': pygame.K_w,'Left':pygame.K_a,\
                'Right':pygame.K_d,'Down':pygame.K_s,'Shoot':pygame.K_SPACE,'RotateRight':pygame.K_e\
                    ,'RotateLeft':pygame.K_q}
        else:
            self.controls = {'Up': pygame.K_KP8,'Left':pygame.K_KP4,\
                'Right':pygame.K_KP6,'Down':pygame.K_KP5,'Shoot':pygame.K_KP_ENTER,'RotateRight':pygame.K_KP9\
                    ,'RotateLeft':pygame.K_KP7}

    def update(self,keys, isShoot):
        if keys[self.controls['Up']]:
            self.move_h(-1)  
        elif keys[self.controls['Down']]:
            self.move_h(1)
        elif keys[self.controls['Left']]:
            self.move_w(-1) 
        elif keys[self.controls['Right']]:
            self.move_w(1)
        elif isShoot:
            self.fight()
        elif keys[self.controls['RotateRight']]:
            for w in self.weapons:
                 w.rotate(5)
        elif keys[self.controls['RotateLeft']]:
            for w in self.weapons:
                 w.rotate(-5)
        self.updatePlayerStatus()
        self.updateWeapons()
        self.updateWeaponStatus()
        self.showPlayerStatus()

    def updateWeaponStatus(self):
        for wid in self.activeWeaponIDs:
            weaponStatus = self.weapons[wid].updateGameloop()
            if weaponStatus:
                self.activeWeaponIDs.remove(wid)

    def updatePlayerStatus(self):
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top= self.x, self.y

    def updateWeapons(self):
        for w in self.weapons:
            # w.x,w.y = self.x+45, self.y
            w.x = self.x + int(45*np.cos(w.angle/180*np.pi))
            w.y= self.y + int(45*np.sin((w.angle-15)/180*np.pi))
            self.win.blit(w.image, (w.x, w.y))

    def move_w(self,sign=1):
        ''' Move right or left'''
        self.x += self.speed*sign
        if self.x >self.screenwidth:
            self.x -= self.speed*sign
        elif self.x < 0:
            self.x = 0

    def move_h(self,sign=1):
        ''' Move up or down'''
        self.y += self.speed*sign
        if self.y >self.screenhight:
            self.y -= self.speed*sign
        elif self.y < 0:
            self.y = 0
            
    def AddWeapon(self):
        pistol = Gun(self.win, 'Pistol', '10mm', 2, 1, 'Pistol.png', 'Pistol_bullet.png')
        pistol.x,pistol.y = self.x+10, self.y
        self.weapons.append(pistol)
    
    def fight(self, weaponID=0):
        if weaponID < len(self.weapons):
            self.activeWeaponIDs.append(weaponID)
            self.weapons[weaponID].shoot()
