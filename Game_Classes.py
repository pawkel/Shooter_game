import pygame
import random
import numpy as np
# class Gane():
#     def __init__(self) -> None:
#         pass
#     def update(self):

class Player(object):
    def __init__(self,win, screenwidth, screenhight, id,name=''):
        self.screenwidth = screenwidth
        self.screenhight = screenhight
        self.win = win
        sc_w, sc_h = 1920, 1080
        scalingFactor = sc_h / sc_w
        self.x = random.randrange(1, self.screenwidth)
        self.y = random.randrange(1, self.screenhight)
        self.speed = 5
        self.gold = 100
        self.id = id
        self.name = f'P{id} '
        self.weapons = []
        self.activeWeaponIDs = []
        self.armors = []
        self.controls = {}
        self.players_skins = ['Classic_player.png', 'Dark_guy.png', 'Emoji_guy.png']
        if name == '':
            self.name = f'Player{id}'
        else:
            self.name += name
        skin = random.randrange(1,len(self.players_skins))
        player = pygame.image.load(self.players_skins[skin])
        self.player = pygame.transform.scale(player, (200, int(200*scalingFactor)))
        self.controlOptions()
        self.AddWeapon()
        
    def controlOptions(self):
        if self.id == 1:
            self.controls= {'Up': pygame.K_w,'Left':pygame.K_a,\
                'Right':pygame.K_d,'Down':pygame.K_s,'Shoot':pygame.K_e}
        else:
            self.controls = {'Up': pygame.K_UP,'Left':pygame.K_LEFT,\
                'Right':pygame.K_RIGHT,'Down':pygame.K_DOWN,'Shoot':pygame.K_KP0}

    def update(self,keys):
        if keys[self.controls['Up']]:
            self.move_h(-1)  
        elif keys[self.controls['Down']]:
            self.move_h(1)
        elif keys[self.controls['Left']]:
            self.move_w(-1) 
        elif keys[self.controls['Right']]:
            self.move_w(1)
        elif keys[self.controls['Shoot']]:
            self.fight()
        self.updateWeapons()
        self.updateWeaponStatus()

    def updateWeaponStatus(self):
        for wid in self.activeWeaponIDs:
            weaponStatus = self.weapons[wid].updateGameloop()
            if weaponStatus:
                self.activeWeaponIDs.remove(wid)
    def updateWeapons(self):
        for w in self.weapons:
            w.x,w.y = self.x+40, self.y
            self.win.blit(w.gun_skin, (w.x, w.y))
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
        pistol = Gun(self.win, 'Pistol', '10mm', 2,' ', 'Pistol.png', 'Pistol_bullet.png')
        pistol.x,pistol.y = self.x+40, self.y
        self.weapons.append(pistol)
    
    def fight(self, weaponID=0):
        if weaponID < len(self.weapons):
            self.activeWeaponIDs.append(weaponID)
            self.weapons[weaponID].shoot()


class Gun(object):
    def __init__(self, win, gun_type, ammo_type, dam, fire_speed, skin, bullet_look):
        '''
            win: pygame window
            gun_type: Pistol ex.
            ammo type: Pistol bullet
            dam: damage, 10 hp
            fire_speed: 1 per second
            skin: how it looks
            bullet_look; how the bullet looks
        '''
        self.gun_type = gun_type
        self.ammo_amount = 10
        self.ammo_type = ammo_type
        self.damage = dam
        self.x = -10
        self.y = -10
        self.bullet_x,self.bullet_y = 0, 0
        self.win = win
        sc_w, sc_h = 1920, 1080
        scalingFactor = sc_h / sc_w
        gun_skin = pygame.image.load(skin)
        self.gun_skin = pygame.transform.scale(gun_skin, (200, int(200*scalingFactor)))
        bullet = pygame.image.load(bullet_look)
        self.bullet = pygame.transform.scale(bullet, (200, int(200*scalingFactor)))
        self.fire_speed = fire_speed

    def shoot(self):
        if self.ammo_amount >0:
            self.bullet_x,self.bullet_y = self.x, self.y
            self.draw_bullet()
            self.ammo_amount-=1

    def draw_bullet(self):
        self.win.blit(self.bullet,(self.bullet_x,self.bullet_y))

    def updateGameloop(self):
        self.bullet_x +=1
        self.bullet_y +=1
        if self.bullet_x > self.win.get_width() or self.bullet_y > self.win.get_height() \
            or self.bullet_x <0  or self.bullet_y <0:
            return 1
        else:
            self.draw_bullet()
            return 0
