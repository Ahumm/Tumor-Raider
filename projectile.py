#########################################
# Tumor Raider                          #
# Brett Kaplan, Tate Larsen             #
# Jossued Rivera-Nazario, Peter Skinner #
#########################################

import pygame
from actor import Actor

class Projectile(Actor):
    """The basic projectile."""
    def __init__(self, x, y, image):
        Actor.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.width = 16
        self.rect.height = 16
        self.rect.x = x
        self.rect.y = y
        self.xvel = 12
        self.yvel = 0
        self.health = -1
        self.damage = 10
        
    def update(self):
        """Updates the position of the projectile."""
        self.rect.move_ip(self.xvel, self.yvel)
        
    def take_damage(self, damage=0):
        Actor.take_damage(self, damage)
        
    def draw(self, screen):
        """Draws the projectile."""
        screen.blit(self.image, self.rect)