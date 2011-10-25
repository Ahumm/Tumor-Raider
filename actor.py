#########################################
# Tumor Raider                          #
# Brett Kaplan, Tate Larsen             #
# Jossued Rivera-Nazario, Peter Skinner #
#########################################

import pygame

class Actor(object):
    def __init__(self):
        """Initiate the actor"""
        self.rect = pygame.Rect(0,0,0,0)
        self.health = 0
        self.damage = 0
    
    def take_damage(self, damage=0):
        """
           Reduces the actor's health by a passed value
             Negative value will *kill* an immortal
        """
        # Check if we have health/can take damage
        if self.health > 0:
            if damage > 0:
                self.health -= damage
                # If we aren't invincible, set health to 0 if it falls below 0
                #   (For culling reasons)
                if self.health < 0:
                    self.health = 0
        # Get rid of immortals
        if damage < 0:
            self.health = 0
                
    def check_off_screen(self, screenWidth, screenHeight, tolerance):
        """Check if within the boundary of the screen, mark for delete if off-screen"""
        wt = screenWidth + tolerance
        ht = screenHeight + tolerance
        if self.rect.left > wt:
            self.health = 0
        elif self.rect.right < -tolerance:
            self.health = 0
        elif self.rect.top > ht:
            self.health = 0
        elif self.rect.bottom < -tolerance:
            self.health = 0