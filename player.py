#########################################
# Tumor Raider                          #
# Brett Kaplan, Tate Larsen             #
# Jossued Rivera-Nazario, Peter Skinner #
#########################################

import pygame
from actor import Actor
from projectile import Projectile
from WhiteBloodCell import WhiteCellProj

class Player(Actor):
    """The player, a nanobot."""
    def __init__(self, screenSize, playerprojectile):
        #sound
        self.whoosh = pygame.mixer.Sound("sfx/whoosh.wav")
        self.whoosh.play()
        self.buzz = pygame.mixer.Sound("sfx/buzz.wav")
        self.buzzcountmax = 9
        self.buzzcount = 0
        
        Actor.__init__(self)
        self.screenSize = screenSize
        self.image = pygame.image.load("gfx/player.png").convert_alpha()
        self.playerprojectile = playerprojectile
        self.rect = self.image.get_rect()
        self.enter = True
        self.rect.width = 48
        self.rect.height = 48
        self.rect.x = -48
        self.rect.y = self.screenSize[1]/2 - self.rect.height/2
        #shield stuff
        self.shieldimage = pygame.image.load("gfx/shield.png").convert_alpha()
        self.shieldenergy = 300
        self.shield = False
        self.immortal = 60
        #Motion variables.
        self.xvelmin = 1
        self.yvelmin = 1
        self.xvelmax = 6
        self.yvelmax = 6
        self.xvel = self.xvelmin
        self.yvel = self.yvelmin
        #collision variables
        self.nearpower = False #near the white blood cells, determines type of shot
        #Shooting variables.
        self.shootnormalmax = 4 #time (frames) between normal shots
        self.shootnormalwait = self.shootnormalmax
        self.shootpowermax = 8 #time (frames) between power shots
        self.shootpowerwait = self.shootpowermax
        self.damage = 999
        self.fullhealth = 150
        self.health = self.fullhealth

        self.subimage = 0
        self.subimagemax = 3
        self.input = [False, False, False, False, False, False] #left, right, up, down, shoot, shield
            
    def update(self):
        """Updates the position of the player, may create projectiles, take damage, etc."""
        if self.enter:
            self.rect.move_ip(((128-self.rect.x)/4)+2, 0)
            if self.rect.x >= 128:
                self.enter = False
        else:
            #sound
            self.buzzcount -= 1
            if self.buzzcount < 0:
                self.buzzcount = 0
            #The following is for animation
            self.subimage += 1
            if self.subimage > self.subimagemax:
                self.subimage = 0
            #The following deals with left/right motion.
            if self.input[0] and not self.input[1]:
                self.xvel += .5
                if self.xvel > self.xvelmax:
                    self.xvel = self.xvelmax
                self.rect.move_ip(-self.xvel, 0)
            elif self.input[1] and not self.input[0]:
                self.xvel += .5
                if self.xvel > self.xvelmax:
                    self.xvel = self.xvelmax
                self.rect.move_ip(self.xvel, 0)
            else:
                self.xvel -= 1
                if self.xvel < self.xvelmin:
                    self.xvel = self.xvelmin
            #The following deals with up/down motion.
            if self.input[2] and not self.input[3]:
                self.yvel += .5
                if self.yvel > self.yvelmax:
                    self.yvel = self.yvelmax
                self.rect.move_ip(0, -self.yvel)
            elif self.input[3] and not self.input[2]:
                self.yvel += .5
                if self.yvel > self.yvelmax:
                    self.yvel = self.yvelmax
                self.rect.move_ip(0, self.yvel)
            else:
                self.yvel -= 1
                if self.yvel < self.yvelmin:
                    self.yvel = self.yvelmin
            #Keeps it in the screen.
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.bottom > self.screenSize[1]:
                self.rect.bottom = self.screenSize[1]
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.right > self.screenSize[0]:
                self.rect.right = self.screenSize[0]
            
            #The following deals with projectile creation.
            #counters
            self.shootnormalwait -= 1
            if self.shootnormalwait < 0:
                self.shootnormalwait = 0
            self.shootpowerwait -= 1
            if self.shootpowerwait < 0:
                self.shootpowerwait = 0
            #actual shooting
            self.plist = []
            if self.input[4]:
                if self.nearpower:
                    if self.shootpowerwait == 0:
                        self.plist.append(WhiteCellProj(self.rect.x + 52, self.rect.centery - 8))
                        self.shootpowerwait = self.shootpowermax
                else:
                    if self.shootnormalwait == 0:
                        self.plist.append(Projectile(self.rect.x + 40, self.rect.centery - 8, self.playerprojectile))
                        self.shootnormalwait = self.shootnormalmax
            #The following deals with the shield.
            self.shield = False
            if self.input[5]:
                if self.shieldenergy > 0:
                    self.shield = True
                    self.shieldenergy -= 1
                
            if self.immortal > 0:
                self.immortal -= 1
            return self.plist
        
    def take_damage(self, damage):
        if self.immortal > 0:
            pass
        else:
            if self.shield:
                thp = self.health
                self.health = -1
                Actor.take_damage(self, damage)
                if self.health != 0:
                    self.health = thp
            else:
                Actor.take_damage(self, damage)
                #if self.health <= 0:
                #    print "died"
                #elif self.buzzcount == 0:
                if self.health > 0 and self.buzzcount == 0:
                    self.buzzcount = self.buzzcountmax
                    self.buzz.play()
        
    def draw(self, screen):
        """Draws the nanobot."""
        screen.blit(self.image, self.rect, pygame.Rect(0, 48*self.subimage, 48, 48))
        if self.shield or self.immortal > 0:
            screen.blit(self.shieldimage, self.rect)