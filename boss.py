#########################################
# Tumor Raider                          #
# Brett Kaplan, Tate Larsen             #
# Jossued Rivera-Nazario, Peter Skinner #
#########################################

import pygame
import random
from math import sqrt
from actor import Actor
from player import Player
from enemyprojectile import EnemyProjectile

class Boss(Actor):
    """The boss object."""
    def __init__(self, x, y, screenSize):
        Actor.__init__(self)
        self.screenSize = screenSize
        self.image = []
        self.image.append(pygame.image.load("gfx/Boss1.png").convert_alpha())
        self.image.append(pygame.image.load("gfx/Boss3.png").convert_alpha())
        self.image.append(pygame.image.load("gfx/Boss5.png").convert_alpha())
        self.rect = self.image[0].get_rect()
        self.eyeimage1 = pygame.image.load("gfx/Eye1.png").convert_alpha()
        self.eyeimage2 = pygame.image.load("gfx/Eye2.png").convert_alpha()
        self.eyerect = self.eyeimage1.get_rect()
        self.projimage = pygame.image.load("gfx/enemyprojectile.png").convert_alpha()
        self.rect.width = 200
        self.rect.height = 400
        self.enter = True
        self.xgoal = x
        self.rect.x = self.xgoal+168
        self.rect.y = y + 40
        self.eyerect.x = self.rect.left - 32 + self.rect.x - self.xgoal
        self.eyerect.y = self.rect.centery - 32
        self.maxhealth = 800
        self.health = self.maxhealth
        self.damage = 999
        #Arms
        self.arms = [[],[]]
        self.armvel = 3
        self.armdir = 1
        self.armtime = 30
        #Firerate
        self.s1burstrate = 5
        self.s1firerate = 20
        self.s1burst = self.s1burstrate
        self.s1fire = self.s1firerate
        self.s3firerate = 50
        self.s3fire = self.s3firerate
        #animation stuff
        self.frame = 0
        self.framemax = 4
        self.phase = 0
        self.spawnedarms = False
        
    def update(self, playerx, playery):
        """This has the boss do things."""
        if self.enter:
            self.rect.move_ip(-4, 0)
            self.eyerect.x = self.rect.left - 32
            if self.rect.x <= self.xgoal:
                self.enter = False
        else:
            proj = []
            #animation stuff
            if self.health < 350:
                self.phase = 2
            elif self.health < 400:
                self.phase = 1
            else:
                self.phase = 0

            if self.health > 0:
                self.frame += 1
                if self.frame > self.framemax:
                    self.frame = 0
            if self.phase == 0:
                self.s1fire -= 1
                if self.s1fire == 0:
                    pvel = 6
                    x = 0
                    y = 10
                    while x < 11:
                        hp = sqrt(x**2 + y**2)
                        xvel = (-x/hp)*pvel
                        yvel = (y/hp)*pvel
                        if not x == 10:
                            proj.append(EnemyProjectile(self.eyerect.left - 4, self.eyerect.centery, xvel, -yvel, self.projimage))
                        proj.append(EnemyProjectile(self.eyerect.left - 4, self.eyerect.centery, xvel, yvel, self.projimage))
                        x += 1
                        y -= 1
                    self.s1fire = self.s1firerate
            if self.phase == 1:
                if not self.spawnedarms:
                #Create arms
                    for j, a in enumerate(self.arms):
                        for i in range(0, 4):
                            if i == 0:
                                a.append(Arm(self.rect.left - 32, 120 - 32 + 240*j))
                            else:
                                a.append(Arm(a[i-1].rect.left - 64, a[i-1].rect.top))
                    self.spawnedarms = True
                else:
                #Move arms
                    for a in self.arms:
                        speed = random.randint(2, self.armvel)
                        for j, n in enumerate(a):
                            n.update(0, self.armdir * (((speed**j)) - 1))
                    self.armtime -= 1
                    if self.armtime == 0:
                        self.armdir *= -1
                        self.armtime = 60
                deadarm = False
                for i in self.arms:
                    for j in i:
                        if j.health > 0:
                            deadarm = True
                if not deadarm:
                    self.health -= 50
            elif self.phase == 2:
                pvel = 6
                self.s3fire -= 1
                if self.s3fire == 0:
                    dx = float(playerx - self.eyerect.x)
                    dy = float(playery - self.eyerect.y)
                    hp = float(sqrt(dx**2 + dy**2))                           #Hypothenuse
                    xvel = (dx/hp)*pvel                                       #Cosine * projvel
                    yvel = (dy/hp)*pvel                                       #Sine * projvel
                    #Don't shoot straight up, straight down, or backwards
                    if xvel < 0 and abs(xvel) > abs(yvel):
                        proj.append(EnemyProjectile(self.eyerect.x + 70 - 5, self.eyerect.centery - 165, xvel, yvel, self.projimage))
                        proj.append(EnemyProjectile(self.eyerect.x + 20 - 5, self.eyerect.centery - 85, xvel, yvel, self.projimage))
                        proj.append(EnemyProjectile(self.eyerect.x - 5, self.eyerect.centery, xvel, yvel, self.projimage))
                        proj.append(EnemyProjectile(self.eyerect.x + 20 - 5, self.eyerect.centery + 85, xvel, yvel, self.projimage))
                        proj.append(EnemyProjectile(self.eyerect.x + 70 - 5, self.eyerect.centery + 165, xvel, yvel, self.projimage))
                    self.s3fire = self.s3firerate
            return proj
            #die
        
    def draw(self, screen):
        """Draws the boss."""
        #, pygame.Rect(HEIGHTOFBOSS*(NUMBEROFSTAGES - int(self.health*NUMBEROFSTAGES/self.maxhealth)), WIDTHOFBOSS*self.frame, WIDTHOFBOSS, HEIGHTOFBOSS))#change this to work with animation later
        if self.phase == 0:
            screen.blit(self.eyeimage1, self.eyerect)
        if self.phase == 1:
            screen.blit(self.eyeimage2, self.eyerect)
        screen.blit(self.image[self.phase], self.rect)
        if self.phase == 1:
            for a in self.arms:
                for n in a:
                    n.draw(screen)  
                
    def collide(self, a):
        if isinstance(a, Player):
            if self.phase == 1:
                for i in self.arms:
                    for j in i:
                        radius1 = a.rect.width // 2
                        radius2 = j.rect.width // 2
                        if sqrt(((a.rect.x + radius1)-(j.rect.x + radius2))**2 + ((a.rect.y + radius1)-(j.rect.y + radius2))**2) < (radius1 + radius2):
                            a.take_damage(j.damage)
            radius1 = a.rect.width // 2
            radius2 = self.rect.width // 2
            if sqrt(((a.rect.x + radius1)-(self.rect.x + radius2))**2 + ((a.rect.y + radius1)-(self.rect.y + radius2))**2) < (radius1 + radius2):
                a.take_damage(self.damage)
        else:
            if self.phase == 1:
                for i in self.arms:
                    for j in i:
                        radius1 = a.rect.width // 2
                        radius2 = j.rect.width // 2
                        if sqrt(((a.rect.x + radius1)-(j.rect.x + radius2))**2 + ((a.rect.y + radius1)-(j.rect.y + radius2))**2) < (radius1 + radius2):
                            j.take_damage(a.damage)
                            proj = a.take_damage(-1)
                            if proj:
                                return proj
            if self.phase == 0:
                radius1 = a.rect.width // 2
                radius2 = self.eyerect.width // 2
                if sqrt(((a.rect.x + radius1)-(self.eyerect.x + radius2))**2 + ((a.rect.y + radius1)-(self.eyerect.y + radius2))**2) < (radius1 + radius2):
                    a.take_damage(-1)
                    Actor.take_damage(self, a.damage)
            radius1 = a.rect.width // 2
            radius2 = self.rect.width
            if sqrt(((a.rect.x + radius1)-(self.rect.x + radius2))**2 + ((a.rect.y + radius1)-(self.rect.y + radius2))**2) < (radius1 + radius2):
                a.take_damage(-1)
                if self.phase == 2:
                    Actor.take_damage(self, a.damage)
        
class Arm(Actor):
    """The boss's arm"""
    def __init__(self, x, y):
        Actor.__init__(self)
        self.image = pygame.image.load("gfx/ArmPart1.png").convert_alpha()
        self.image2 = pygame.image.load("gfx/ArmPart3.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.width = 64
        self.rect.height = 64
        self.rect.x = x
        self.rect.y = y
        self.maxhealth = 250
        self.health = self.maxhealth
        self.damage = 2
        
    def update(self, xvel, yvel):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 480:
            self.rect.bottom = 480
        self.rect.move_ip(xvel, yvel)
    
    def draw(self, screen):
        if self.health != 0:
            screen.blit(self.image, self.rect)
        else:
            screen.blit(self.image2, self.rect)