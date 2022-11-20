import pygame
import random
import numpy as np
from PIL import Image,ImageOps
# class Gane():
#     def __init__(self) -> None:
#         pass
#     def update(self):
def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()


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
        self.health = 3
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
        skin = random.randrange(0,len(self.players_skins))
        player = pygame.image.load(self.players_skins[skin])
        self.player = pygame.transform.scale(player, (200, int(200*scalingFactor)))
        self.controlOptions()
        self.AddWeapon()
        
    def controlOptions(self):
        if self.id == 1:
            self.controls= {'Up': pygame.K_w,'Left':pygame.K_a,\
                'Right':pygame.K_d,'Down':pygame.K_s,'Shoot':pygame.K_SPACE,'RotateRight':pygame.K_e\
                    ,'RotateLeft':pygame.K_q}
        else:
            self.controls = {'Up': pygame.K_KP8,'Left':pygame.K_KP4,\
                'Right':pygame.K_KP6,'Down':pygame.K_KP5,'Shoot':pygame.K_KP_ENTER,'RotateRight':pygame.K_KP9\
                    ,'RotateLeft':pygame.K_KP7}

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
        elif keys[self.controls['RotateRight']]:
            for w in self.weapons:
                 w.rotate(5)
        elif keys[self.controls['RotateLeft']]:
            for w in self.weapons:
                 w.rotate(-5)
        self.updateWeapons()
        self.updateWeaponStatus()

    def updateWeaponStatus(self):
        for wid in self.activeWeaponIDs:
            weaponStatus = self.weapons[wid].updateGameloop()
            if weaponStatus:
                self.activeWeaponIDs.remove(wid)

    def updateWeapons(self):
        for w in self.weapons:
            # w.x,w.y = self.x+45, self.y
            w.x = self.x + int(45*np.cos(w.angle/180*np.pi))
            w.y= self.y + int(45*np.sin(w.angle/180*np.pi))
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
        pistol.x,pistol.y = self.x+45, self.y
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
        self.bullet_distance = 0
        self.win = win
        sc_w, sc_h = 1920, 1080
        scalingFactor = sc_h / sc_w
        self.scalingFactor = scalingFactor
        self.angle = 0
        self.imageFileName = skin
        skin = pygame.image.load(skin)
        self.gun_skin = pygame.transform.scale(skin, (200, int(200*scalingFactor)))
        bullet_skin = pygame.image.load(bullet_look)
        self.bullet = pygame.transform.scale(bullet_skin, (200, int(200*scalingFactor)))
        self.fire_speed = fire_speed

    def rotate(self, angle = 0):
        im = Image.open(self.imageFileName)
        self.angle += angle
        if self.angle < 0 :
            self.angle +=360
        self.angle = np.mod(self.angle, 360)
        x0,y0 = im.size[0]//2,im.size[1]//2
        im_rotate = im.rotate(-self.angle, center=(x0,y0),
         expand=False)
        x1, y1 = im.size[0]//2,im.size[1]//2
        im_rotate = im_rotate.crop((x1-x0, y1-y1, x1+x0, y1+y0))
        # if abs(self.angle) < 270:
        #     im_rotate = ImageOps.flip(im_rotate)
        #     print('flip', self.angle)
        im_fn = self.imageFileName.split('.png')[0]+"rotated.png"
        im_rotate.save(im_fn)
        skin = pygame.image.load(im_fn)
        self.gun_skin = pygame.transform.scale(skin, (200,int(200*self.scalingFactor)))


    def shoot(self):
        if self.ammo_amount >0:
            self.bullet_x,self.bullet_y = self.x, self.y
            self.bullet_distance = 0
            self.draw_bullet()
            # self.ammo_amount-=1


    def draw_bullet(self):
        self.win.blit(self.bullet,(self.bullet_x,self.bullet_y))

    def updateGameloop(self):
        self.bullet_distance +=1
        dx = int(self.bullet_distance*np.cos(self.angle/180*np.pi))
        dy= int(self.bullet_distance*np.sin(self.angle/180*np.pi))
        self.bullet_x +=dx
        self.bullet_y +=dy
        if self.bullet_x > self.win.get_width() or self.bullet_y > self.win.get_height() \
            or self.bullet_x <0  or self.bullet_y <0:
            return 1
        else:
            self.draw_bullet()
            return 0
