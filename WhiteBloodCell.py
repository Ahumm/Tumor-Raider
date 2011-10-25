#########################################
# Tumor Raider                          #
# Brett Kaplan, Tate Larsen             #
# Jossued Rivera-Nazario, Peter Skinner #
#########################################

import pygame
from actor import Actor

class WhiteBloodCell(Actor):
    """White Blood Cell that gives the player different ability if close"""
    def __init__(self, x, y, xvel = -5, yvel = 0):
        Actor.__init__(self)
        self.image = pygame.image.load("gfx/whitebloodcell.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.auraimage = pygame.image.load("gfx/WhiteAura.png").convert_alpha()
        self.aurarect = self.auraimage.get_rect()
        # self.aurarect.width = 400
        # self.aurarect.width = 400
        self.aurarect.center = self.rect.center
        #self.aurarect.centery = self.rect.centery
        # self.aurarect.x = x - 128
        # self.aurarect.y = y - 128
        self.xvel = xvel
        self.yvel = yvel
        self.angle = 0                      #Indicates rotation of the image
        self.frame = 0                      #Used on the aura
        self.health = -1
        self.damage = 999
        
    def draw(self, screen):
        rot_image = pygame.transform.rotate(self.image, self.angle*5)
        rot_rect = rot_image.get_rect()
        rot_rect.center = self.rect.center                          #Makes the image rotate on its center
        rot_auraimage = pygame.transform.rotate(self.auraimage, -self.angle*10)
        rot_aurarect = rot_auraimage.get_rect()
        rot_aurarect.center = self.aurarect.center
        screen.blit(rot_auraimage, rot_aurarect)#, pygame.Rect(self.frame/6*357, 0, 357, 400))
        screen.blit(rot_image, rot_rect)
        
    def update(self):
        self.rect.move_ip(self.xvel, self.yvel)
        self.aurarect.move_ip(self.xvel, self.yvel)
        self.angle += 1
        if self.angle > 71:
            self.angle = 0
        self.frame += 1
        if self.frame > 35:
            self.frame = 0
            
class WhiteCellProj(Actor):
    """Projectile fired by player when close to a White Blood Cell"""
    def __init__(self, x, y, xvel=8, yvel=0, split=0):
        if split == 0:
            self.image = pygame.image.load("gfx/WhiteProjectile.png").convert_alpha()
        elif split == 1:
            self.image = pygame.image.load("gfx/WhiteProjectile2.png").convert_alpha()
        else:
            self.image = pygame.image.load("gfx/WhiteProjectile1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = -1
        self.xvel = xvel
        self.yvel = yvel
        self.damage = 20
        self.split = split
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def update(self):
        """Returns True if WhiteBloodCell is still on the screen, False if it's off the screen"""
        self.rect.move_ip(self.xvel, self.yvel)
            # if collision_detect(self, self.target):
                # self.target.take_damage(5)
            #Possible problem when projectile passes target
            #Move and check for collision?
    
    def take_damage(self, damage):
        newProj = []
        if damage < 0:
            #spawn new things
            if self.split == 0:
                newProj.append(WhiteCellProj(self.rect.x + 52, self.rect.y, self.xvel, self.yvel, 1))
                newProj.append(WhiteCellProj(self.rect.x + 52, self.rect.y + 16, self.xvel/2, self.xvel/2, 2))
                newProj.append(WhiteCellProj(self.rect.x + 52, self.rect.y - 16, self.xvel/2, -self.xvel/2, 2))
            elif self.split == 1:
                newProj.append(WhiteCellProj(self.rect.x + 52, self.rect.y + 16, self.xvel/2, self.xvel/2, 2))
                newProj.append(WhiteCellProj(self.rect.x + 52, self.rect.y  - 16, self.xvel/2, -self.xvel/2, 2))
                
            Actor.take_damage(self, damage)
        return newProj