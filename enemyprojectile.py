#########################################
# Tumor Raider                          #
# Brett Kaplan, Tate Larsen             #
# Jossued Rivera-Nazario, Peter Skinner #
#########################################

import pygame
from projectile import Projectile

class EnemyProjectile(Projectile):
    """The basic enemy projectile."""
    def __init__(self, x, y, xvel, yvel, image):
        Projectile.__init__(self, x, y, image)
        self.rect = self.image.get_rect()
        self.rect.width = 3
        self.rect.height = 3
        self.xvel = xvel
        self.yvel = yvel
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.rect.move_ip(self.xvel, self.yvel)
        
    def take_damage(self, damage=0):
        Projectile.take_damage(self, damage)
        
    def draw(self, screen):
        """Draws the projectile."""
        screen.blit(self.image, self.rect)