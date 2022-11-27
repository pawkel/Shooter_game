import pygame
import random
import numpy as np
from PIL import Image,ImageOps

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, enemyType, screen_width=800, screen_hight=800):
       # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        self.enemyType = {'Normal':[2, 2,'Enemy_normal.png', 30, 1], \
            'Big':[4,1.5,'Enemy_big.png', 55, 2], 'Small':[1,3.5,'Enemy_small.png', 20, 4]}
        eType =  self.enemyType[enemyType]
        self.typeName =enemyType
        self.health = eType[0]
        self.speed = eType[1]
        size = eType[3]
        enemyskin = pygame.image.load(eType[2])
        self.score = eType[4]
        self.image = pygame.transform.scale(enemyskin, (size,size))
        self.screen_width = screen_width
        self.screen_height = screen_hight
        self.possibleXY = [random.randrange(0, self.screen_width),\
            random.randrange(0, self.screen_height)]

        self.x = self.possibleXY[0]
        self.y = self.possibleXY[1]
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top = self.x, self.y

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
        self.rotateCooldown = 1# 3 loops
        self.rotateCounter = 0
        self.win = win
        self.angle = 0
        self.imageFileName = skin
        skin = pygame.image.load(skin)
        self.image= pygame.transform.scale(skin, (20,20))
        self.bulletLook = bullet_look
        self.fire_speed = fire_speed
        self.counter = 0
        self.bullets = pygame.sprite.Group()

    def rotate(self, angle = 0):
        if self.rotateCounter > self.rotateCooldown:
            self.rotateCounter = 0
            im = Image.open(self.imageFileName)
            self.angle += angle
            if self.angle < 0 :
                self.angle +=360
            self.angle = np.mod(self.angle, 360)
            if self.angle > 90 and self.angle <270:
                im = ImageOps.flip(im)
            x0,y0 = im.size[0]//2,im.size[1]//2
            im_rotate = im.rotate(-self.angle, center=(x0,y0),
            expand=False)
            x1, y1 = im.size[0]//2,im.size[1]//2
            im_rotate = im_rotate.crop((x1-x0, y1-y1, x1+x0, y1+y0))
            im_fn = self.imageFileName.split('.png')[0]+"rotated.png"
            im_rotate.save(im_fn)
            skin = pygame.image.load(im_fn)
            self.image = pygame.transform.scale(skin, (20,20))
        else:
            self.rotateCounter +=1

    def shoot(self):
        if self.ammo_amount >0:
            self.counter = 0
            bullet_x = self.x
            bullet_y = self.y
            self.bullets.add(Bullet(self.win,self.bulletLook, bullet_x, bullet_y))
            # self.ammo_amount-=1
    def updateGameloop(self):
        for bullet in self.bullets:       
            bullet.bullet_distance +=1
            dx = int(bullet.bullet_distance*np.cos(self.angle/180*np.pi))
            dy = int(bullet.bullet_distance*np.sin(self.angle/180*np.pi))
            bullet.bullet_x +=dx
            bullet.bullet_y +=dy
            bullet.rect.left, bullet.rect.top= bullet.bullet_x,  bullet.bullet_y
            if bullet.bullet_x > self.win.get_width() or bullet.bullet_y > self.win.get_height() \
                or bullet.bullet_x <0  or bullet.bullet_y <0:
                bullet.kill()
                return 1
            else:
                bullet.draw_bullet()
                return 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, win, bulletLook, bX, bY):
        pygame.sprite.Sprite.__init__(self)
        self.win = win
        self.bullet_x,self.bullet_y = bX, bY
        self.bullet_distance = 0
        bullet_skin = pygame.image.load(bulletLook)
        bullet_skin = pygame.transform.scale(bullet_skin, (10,10))
        self.image = bullet_skin
        self.rect = self.image.get_rect()
        self.rect.left,self.rect.top= self.bullet_x, self.bullet_y

    def draw_bullet(self):
        self.win.blit(self.image,(self.bullet_x,self.bullet_y))
