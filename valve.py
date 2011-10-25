#########################################
# Tumor Raider                          #
# Brett Kaplan, Tate Larsen             #
# Jossued Rivera-Nazario, Peter Skinner #
#########################################

import pygame
from actor import Actor

class Valve(Actor):
    """A moving valve."""
    def __init__(self, screenSize, image):
        Actor.__init__(self)
        self.health = -1
        self.damage = 999
        self.screenSize = screenSize
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.width = 96
        self.rect.height = self.screenSize[1]
        self.rect.x = self.screenSize[0]
        self.rect.y = 0
        self.xvel = 3
        self.subimage = 0 #0 = fully closed
        self.open = False # 0 if closed, 1 if open
        self.subimagemax = 5#NUMBEROFSUBIMAGES-1
        self.toggle = -1 #direction of subimage change
        self.counter = 0
        self.countermax = 40
        
    def update(self):
        """Updates the position of the valve, takes care of opening/closing."""
        self.rect.move_ip(-self.xvel, 0)
        if self.counter <= 0:
            self.counter = self.countermax
            self.toggle *= -1
            self.open = not self.open
        else:
            self.counter -= 1
        self.subimage += self.toggle
        if self.subimage < 0:
            self.subimage = 0
        if self.subimage > self.subimagemax:
            self.subimage = self.subimagemax
        # Set open toggle (For outside checking)
#        if self.subimage < ((self.subimagemax + 1) / 2):
#            self.open = 0
#        else:
#            self.open = 1
            
    def draw(self, screen):
        """Draws the valve."""
        screen.blit(self.image, self.rect, pygame.Rect(96*self.subimage, 0, 96, self.screenSize[1]))