#########################################
# Tumor Raider                          #
# Brett Kaplan, Tate Larsen             #
# Jossued Rivera-Nazario, Peter Skinner #
#########################################

import pygame, random
from actor import Actor
from enemyprojectile import EnemyProjectile
from math import sqrt

class Enemy(Actor):
    def __init__(self, xvel, yvel, seed, projimage):
        Actor.__init__(self)
        #self.image = pygame.image.load("").convert_alpha()
        #self.rect.x = x#
        #self.rect.y = y#
        self.projimage = projimage
        self.xvel = xvel
        self.yvel = yvel
        self.frame = 0
        self.health = 1
        random.seed(seed)
        
class Virus(Enemy):
    def __init__(self, x, y, xvel, seed, projimage):
        Enemy.__init__(self, xvel, 0, seed, projimage)
        self.image = pygame.image.load("gfx/Virus.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.width = 40
        self.rect.height = 48
        self.rect.x = x
        self.rect.y = y
        self.maxyvel = 5
        self.updown = True
        self.health = 90
        self.damage = 10
        self.framemax = 23
        self.frame = random.randint(0, self.framemax)
        self.firerate = 50
        self.fire = self.firerate
        self.projvel = 6
        
    def draw(self, screen):
        screen.blit(self.image, self.rect, pygame.Rect(0, (self.frame/6)*48, 48, 48))
        
    def update(self, playerx, playery):
        """Moves the virus according to its x velocity and a small random y velocity"""
        if self.updown:
            randyvel = random.randint(1, self.maxyvel)
            self.updown = False
        else:
            randyvel = -(random.randint(1, self.maxyvel))
            self.updown = True 
        self.rect.move_ip(self.xvel, randyvel)
        self.frame += 1
        if self.frame > self.framemax:
            self.frame = 0
        proj = []
        self.fire -= 1
        if self.fire == 0:
            dx = float(playerx - self.rect.x)
            dy = float(playery - self.rect.y)
            hp = float(sqrt(dx**2 + dy**2))                           #Hypothenuse
            xvel = (dx/hp)*self.projvel                                  #Cosine * projvel
            yvel = (dy/hp)*self.projvel                                  #Sine * projvel
            #Don't shoot straight up, straight down, or backwards
            if xvel < 0 and abs(xvel) > abs(yvel):
                proj.append(EnemyProjectile(self.rect.x - 10, self.rect.centery, xvel, yvel, self.projimage))
            self.fire = self.firerate
        return proj

        
class InfectedCell(Enemy):
    def __init__(self, x, y, xvel, yvel, seed, projimage):
        Enemy.__init__(self, xvel, yvel, seed, projimage)
        if random.randint(0, 9) / 5 == 1:
            self.image = pygame.image.load("gfx/InfectedCell2.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.XorY = False
        else:
            self.image = pygame.image.load("gfx/InfectedCell3.png").convert_alpha()
            self.rect = self.image.get_rect()
            self.XorY = True
        self.rect.width = 48
        self.rect.height = 48
        self.rect.x = x
        self.rect.y = y
        self.health = 30
        self.damage = 10
        self.firerate = 50
        self.fire = self.firerate
        self.framemax = 23
        self.frame = random.randint(0, self.framemax)
        
    def draw(self, screen):
        if self.XorY:
            screen.blit(self.image, self.rect, pygame.Rect(0, (self.frame/6)*48, 48, 48))
        else:
            screen.blit(self.image, self.rect, pygame.Rect((self.frame/6)*48, 0, 48, 48))
            
    def update(self):
        self.rect.move_ip(self.xvel, self.yvel)
        self.frame += 1
        if self.frame > 23:
            self.frame = 0
        
        proj = []
        self.fire -= 1
        if self.fire == 0:
            proj.append(EnemyProjectile(self.rect.x - 10, self.rect.centery, -5, 0, self.projimage))
            self.fire = self.firerate
        return proj

class SickleCell(Enemy):
    def __init__(self, x, y, xvel, yvel, seed, projimage):
        Enemy.__init__(self, xvel, yvel, seed, projimage)
        self.image = pygame.image.load("gfx/SickleCell.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.width = 24
        self.rect.height = 24
        self.rect.x = x
        self.rect.y = y
        self.health = 10
        self.damage = 10
        self.anglemax = 35
        self.angle = random.randint(0, self.anglemax)
        
    def draw(self, screen):
        rot_image = pygame.transform.rotate(self.image, self.angle*10)
        screen.blit(rot_image, self.rect)
        
    def update(self):
        self.rect.move_ip(self.xvel, self.yvel)
        self.angle += 1
        if self.angle > self.anglemax:
            self.angle = 0