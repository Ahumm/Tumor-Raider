#########################################
# Tumor Raider                          #
# Brett Kaplan, Tate Larsen             #
# Jossued Rivera-Nazario, Peter Skinner #
#########################################

import pygame, sys, math, random
from player import Player
from WhiteBloodCell import WhiteBloodCell, WhiteCellProj
from Enemy import InfectedCell, Virus, SickleCell
from valve import Valve
from boss import Boss

################
# Some Globals #
################
screenSize = (800, 480)
boundaryTolerance = 128
fpsLimit = 30
seed = 0
random.seed(seed)
          
######################
# Collsion Detection #
######################
def collision_detect(a1, a2):
    """Perform collision detection"""
    ## if a1 hits a2, return true, else return false
    radius1 = a1.rect.width // 2
    radius2 = a2.rect.width // 2
    if math.sqrt(((a1.rect.x + radius1)-(a2.rect.x + radius2))**2 + ((a1.rect.y + radius1)-(a2.rect.y + radius2))**2) < (radius1 + radius2):
        return True
    return False
    
def valve_collision_detect(v, a):
    if v.open:
        return False
    else:
        return v.rect.colliderect(a.rect)
    
##############
# Map object #
##############        
class Map(object):
    def __init__(self, start):
        """Initiate the map"""
        self.image = pygame.image.load("gfx/Background1.png").convert()
        self.imagea = self.image
        self.imageb = self.image
        self.rect1 = pygame.Rect(0,0,800,480)
        self.rect2 = pygame.Rect(800,0,800,480)
        self.start = start
        
    def draw(self, screen):
        screen.blit(self.imagea, self.rect1)
        screen.blit(self.imageb, self.rect2)
        self.rect1.x -= 3
        self.rect2.x -= 3
        if self.rect1.x <= -800:
            self.rect1.x = 800
        if self.rect2.x <= -800:
            self.rect2.x = 800
        
################
# Game  Object #
################
class Game(object):
    def __init__(self):
        """Initialize the game"""
        pygame.init()
        self.screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
        pygame.display.set_caption("Tumor Raider")
        self.clock = pygame.time.Clock()
        self.enemies = []
        self.projectiles = []
        self.eprojectiles = []
        self.cells = []
        self.valves = []
        self.player = None
        self.player = None
        self.spawn = 20
        self.state = 0
        self.overlay = pygame.image.load("gfx/UIOverlay.png").convert_alpha()
        self.shipicon = pygame.image.load("gfx/shipicon.png").convert_alpha()
        self.menu = pygame.image.load("gfx/menu.png").convert_alpha()
        self.gameover = pygame.image.load("gfx/gameover.png").convert_alpha()
        self.winrar = pygame.image.load("gfx/WinScreen.png").convert()
        self.wintext = pygame.image.load("gfx/WinScreentext.png").convert_alpha()
        self.numbers = pygame.image.load("gfx/Numbers.png").convert_alpha()
        self.playerprojectile = pygame.image.load("gfx/playerprojectile.png").convert_alpha()
        self.enemyprojectile = pygame.image.load("gfx/enemyprojectile.png").convert_alpha()
        self.valveimage = pygame.image.load("gfx/valve.png").convert_alpha()
        pygame.mixer.music.load("sfx/beat.wav")
        pygame.mixer.music.play(-1)
        self.themeplaying = False
        self.lives = 3
        self.shieldcolor = (61,196,240)
        self.healthcolor = (250,25,20)
        self.bosshealthcolor = (25,250,20)
        self.mitem = 0
        self.map = Map(pygame.time.get_ticks())
        self.start = pygame.time.get_ticks()
        self.v = 0
        self.score = 0
        
    def reset(self):
        self.clock = pygame.time.Clock()
        self.map = Map(pygame.time.get_ticks())
        self.enemies = []
        self.projectiles = []
        self.eprojectiles = []
        self.cells = []
        self.valves = []
        self.player = Player(screenSize, self.playerprojectile)
        self.boss = None
        self.spawn = 20
        self.lives = 3
        self.mitem = 0
        self.start = pygame.time.get_ticks()
        self.v = 0
        if not self.themeplaying:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sfx/themesong.wav")
            pygame.mixer.music.play(-1)
            self.themeplaying = True
        
    def update(self):
        """Update game objects"""
        if self.state == 1:
            #self.player.immortal = 60
            # In Game
            # Spawn Things
            t = (pygame.time.get_ticks() - self.start) / 1000.0
            if self.spawn == 0:
                #Spawn Something
                if t < 30:
                    what = random.randint(0,8)
                elif t < 60:
                    what = random.randint(0,14)
                elif t < 90:
                    what = random.randint(0,15)
                elif t < 120:
                    what = random.randint(0,20)
                elif t < 150:
                    what = [random.randint(0,1),random.randint(9,14)]
                    what = what[random.randint(0,1)]
                elif t < 210:
                    what = random.randint(0,20)
                elif t > 220 and t < 300:
                    what = 100
                else:
                    what = -1
                # White blood cell
                if what == 100:
                    if not self.boss:
                        self.boss = Boss(600,0,screenSize)
                if what in range(0,1):
                    self.cells.append(WhiteBloodCell(801, random.randint(16, 368)))
                # Sickle cell
                if what in range(9,14):
                    for i in range(0,random.randint(1,10)):
                        x,y = random.randint(200,600), random.randint(0,1)
                        yvel = 0
                        xvel = 0
                        if x < 400:
                            xvel = 1
                        else:
                            xvel = -1
                        if y == 0:
                            y = -48
                            yvel = 1
                        else:
                            y = 480
                            yvel = -1
                        self.enemies.append(SickleCell(x, y, xvel * random.randint(0,5), yvel * random.randint(2,5), random.randint(725,9381), self.enemyprojectile))
                # Infected cell
                if what in range(2,8):
                    x,y = random.randint(200,600), random.randint(0,1)
                    yvel = 0
                    xvel = 0
                    if x < 400:
                        xvel = 1
                    else:
                        xvel = -1
                    if y == 0:
                        y = -48
                        yvel = 1
                    else:
                        y = 480
                        yvel = -1
                    self.enemies.append(InfectedCell(x, y, xvel * random.randint(0,3), yvel * random.randint(1,3), random.randint(725,9381), self.enemyprojectile))
                # Valve
                if what == 15 and not self.valves:
                    self.valves.append(Valve(screenSize, self.valveimage))
                # Viruses
                if what in range(16,20):
                    x,y = 800, random.randint(16,416)
                    self.enemies.append(Virus(x, y, -random.randint(2,5), random.randint(725,9381), self.enemyprojectile))
                self.spawn = random.randint(5, 30)
            else:
                self.spawn -= 1
                
            # Spawn Valves at background transitions
            if (int(t) == 60) and self.v == 0:
                self.valves.append(Valve(screenSize, self.valveimage))
                self.v += 1
                self.spawn = random.randint(5, 30)
            if (int(t) == 120) and self.v == 1:
                self.valves.append(Valve(screenSize, self.valveimage))
                self.v += 1
                self.spawn = random.randint(5, 30)
            if (int(t) == 180) and self.v == 2:
                self.valves.append(Valve(screenSize, self.valveimage))
                self.v += 1
                self.spawn = random.randint(5, 30)
            if (int(t) == 200) and self.v == 3:
                self.valves.append(Valve(screenSize, self.valveimage))
                self.v += 1
                self.spawn = random.randint(5, 30)
            
            if self.boss:
                if self.spawn == 0:
                    if self.boss.phase == 0:
                        for i in range(0, random.randint(1, 10)):
                            x,y = random.randint(300,500), random.randint(0,1)
                            yvel = 0
                            if y == 0:
                                y = -48
                                yvel = 1
                            else:
                                y = 480
                                yvel = -1
                            self.enemies.append(SickleCell(x, y, (-1 ** random.randint(0,1)), yvel * random.randint(2,5), random.randint(725,9381), self.enemyprojectile))
                    elif self.boss.phase == 1:
                        if random.randint(0,5):
                            x,y = random.randint(300,500), random.randint(0,1)
                            yvel = 0
                            if y == 0:
                                y = -48
                                yvel = 1
                            else:
                                y = 480
                                yvel = -1
                            self.enemies.append(InfectedCell(x, y, (-1 ** random.randint(0,1)) * random.randint(0,1), yvel * random.randint(1,3), random.randint(725,9381), self.enemyprojectile))
                        else:
                            x, y = random.randint(300,500), random.randint(0,1)
                            xvel = -3
                            yvel = 2 * ((-1)**y)
                            y = (y * 540) - 60
                            ncell = WhiteBloodCell(x, y, xvel, yvel)
                            self.cells.append(ncell)
                    elif self.boss.phase == 2:
                        for i in range(0, random.randint(1, 10)):
                            x,y = random.randint(300,500), random.randint(0,1)
                            yvel = 0
                            if y == 0:
                                y = -48
                                yvel = 1
                            else:
                                y = 480
                                yvel = -1
                            self.enemies.append(SickleCell(x, y, (-1 ** random.randint(0,1)), yvel * random.randint(2,5), random.randint(725,9381), self.enemyprojectile))
                    self.spawn = random.randint(40, 50)
                else:
                    self.spawn -= 1
            
                
            # Do the updates
            p = self.player.update()
            if p:
                self.projectiles = self.projectiles + p
            if self.boss:
                p = self.boss.update(self.player.rect.centerx, self.player.rect.centery)
                if p:
                    self.eprojectiles = self.eprojectiles + p
            for i in self.enemies:
                if isinstance(i, Virus):
                    p = i.update(self.player.rect.x, self.player.rect.y)
                    if p:
                        self.eprojectiles = self.eprojectiles + p
                else:
                    p = i.update()
                    if p:
                        self.eprojectiles = self.eprojectiles + p
            for i in self.projectiles + self.eprojectiles + self.cells + self.valves:
                i.update()
            
            # Check for collisions, deal damage
            #   Check projectiles against enemies and player
            #   Check player/enemies against cells and each other self.enemies + 
            for e1 in self.cells + [self.player]:
                for p in self.projectiles + self.eprojectiles:
                    if collision_detect(p, e1):
                        # Handle WhiteCellProj splitting
                        if isinstance(p, WhiteCellProj):
                            np = p.take_damage(-1)
                            if np:
                                self.projectiles = self.projectiles + np
                        else:
                            p.take_damage(-1)
                        e1.take_damage(p.damage)
                for e2 in self.enemies + self.cells + [self.player]:
                    if e1 != e2:
                        if collision_detect(e1, e2):
                            e1.take_damage(e2.damage)
                            e2.take_damage(e1.damage)
            for e1 in self.enemies:
                for p in self.projectiles:
                    if collision_detect(p, e1):
                        if isinstance(p, WhiteCellProj):
                            np = p.take_damage(-1)
                            if np:
                                self.projectiles = self.projectiles + np
                        else:
                            p.take_damage(-1)
                        e1.take_damage(p.damage)
            for v in self.valves:
                for e in self.enemies + self.cells + self.projectiles + self.eprojectiles + [self.player]:
                    if valve_collision_detect(v, e):
                        e.take_damage(-1)
            
            if self.boss:
                for p in self.projectiles + [self.player]:
                    np = self.boss.collide(p)
                    if np:
                        self.projectiles = self.projectiles + np
            
            np = False
            for c in self.cells:
                w1 = self.player.rect.width // 2
                w2 = c.rect.width // 2
                np = np or (math.sqrt(((self.player.rect.x + w2) - (c.rect.x + w2))**2 + ((self.player.rect.y + w2) - (c.rect.y + w2))**2) < (w1 + w2 + 128))
            self.player.nearpower = np
            
            # If off the screen by 64 pixels, set health to 0 (might need tweaking for spawning)
            for i in self.enemies + self.projectiles + self.eprojectiles + self.cells:
                i.check_off_screen(screenSize[0], screenSize[1], boundaryTolerance)        
            
            # Cull dead items
            for i in self.enemies:
                self.enemies = [e for e in self.enemies if e.health != 0]
            for i in self.projectiles:
                self.projectiles = [p for p in self.projectiles if p.health != 0]
            for i in self.eprojectiles:
                self.eprojectiles = [p for p in self.eprojectiles if p.health != 0]
            for i in self.cells:
                self.cells = [c for c in self.cells if c.health != 0]
            
            t = (pygame.time.get_ticks() - self.start) / 1000.0
            
            if t >= 300:
                self.lives = 0
                
            if self.lives == 0:
                if self.themeplaying:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sfx/beat.wav")
                    pygame.mixer.music.play(-1)
                    self.themeplaying = False
                self.state = 2
            if self.player.health == 0:
                self.player = Player(screenSize, self.playerprojectile)
                self.lives -= 1
            if self.boss and self.boss.health == 0:
                if self.themeplaying:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("sfx/beat.wav")
                    pygame.mixer.music.play(-1)
                    self.themeplaying = False
                self.state = 3
                
            self.score = int(300 - t)

            
    def process_events(self):
        """Process the event queue"""
        ret = True
        if self.state in [0,2,3]:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Exit on Escape
                    if event.key == pygame.K_RETURN:
                        if self.mitem == 1:
                            ret = False
                        else:
                            self.reset()
                            self.state = 1
                    if event.key == pygame.K_ESCAPE:
                        ret = False
                    if event.key == pygame.K_LEFT or event.key == pygame.K_UP:
                        self.mitem = 0
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN:
                        self.mitem = 1
        if self.state == 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    # Exit on Escape
                    if event.key == pygame.K_ESCAPE:
                        self.state = 0
                        if self.themeplaying:
                            pygame.mixer.music.stop()
                            pygame.mixer.music.load("sfx/beat.wav")
                            pygame.mixer.music.play(-1)
                            self.themeplaying = False
                    if event.key == pygame.K_LEFT:
                        self.player.input[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.player.input[1] = True
                    if event.key == pygame.K_UP:
                        self.player.input[2] = True
                    if event.key == pygame.K_DOWN:
                        self.player.input[3] = True
                    if event.key == pygame.K_SPACE:
                        self.player.input[4] = True
                    if event.key == pygame.K_s:
                        self.player.input[5] = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.player.input[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.player.input[1] = False
                    if event.key == pygame.K_UP:
                        self.player.input[2] = False
                    if event.key == pygame.K_DOWN:
                        self.player.input[3] = False
                    if event.key == pygame.K_SPACE:
                        self.player.input[4] = False
                    if event.key == pygame.K_s:
                        self.player.input[5] = False
        return ret
        
    def draw_numbers(self, x, y, number):
        """Draw numbers on the screen."""
        digits = []
        if not number:
            digits = [0]
        while number:
            digits.insert(0, number % 10)
            number /= 10
        for place, digit in enumerate(digits):
            self.screen.blit(self.numbers, pygame.Rect(x + place * 14, y, 14, 18), pygame.Rect(digit * 14, 0, 14, 18))

    def draw(self):
        """Draw game objects"""
        if self.state == 0:
            # Draw menu and box around current selection beased on self.mitem
            self.map.draw(self.screen)
            self.screen.blit(self.menu, pygame.Rect(50,40,700,400), pygame.Rect(700 * self.mitem, 0, 700, 400))
        if self.state == 1:
            self.map.draw(self.screen)
            for i in self.cells + self.valves + self.enemies + [self.player, self.boss] + self.projectiles + self.eprojectiles:
                if i:
                    i.draw(self.screen)
            self.screen.blit(self.overlay, pygame.Rect(0, 0, 800, 25))
            #draws the shield bar for the hud
            self.screen.fill(self.shieldcolor, pygame.Rect(310, 6, self.player.shieldenergy * 5/6, 16))
            #draws the health bar for the hud
            self.screen.fill(self.healthcolor, pygame.Rect(632,6, 1.0 * self.player.health / self.player.fullhealth * 164,16))
            #draws the ship icons, for lives left
            if self.boss:
                self.screen.fill(self.bosshealthcolor, pygame.Rect(200,460, 1.0 * self.boss.health / self.boss.maxhealth * 350,16))
            for i in range(self.lives):
                self.screen.blit(self.shipicon, pygame.Rect(97 + i*52, 1, 26, 25))
            #draws the score
            self.draw_numbers(0, screenSize[1] - 18, self.score)#test values
            
        if self.state == 2:
            # Draw game over menu and box around current selection based on self.mitem
            self.map.draw(self.screen)
            self.screen.blit(self.gameover, pygame.Rect(50,40,700,400), pygame.Rect(700 * self.mitem, 0, 700, 400))
        if self.state == 3:
            self.screen.blit(self.winrar, pygame.Rect(0,0,800,480), pygame.Rect(0, 0, 800, 480))
            self.draw_numbers(480, 85, 300 - self.score)
            self.screen.blit(self.wintext, pygame.Rect(400 * self.mitem,0,400,480), pygame.Rect(400 * self.mitem, 0, 400, 480))
            
def main():
    g = Game()
    gameOver = True
    while gameOver:
        g.clock.tick(fpsLimit)
        gameOver = gameOver and g.process_events()
        g.update()
        g.draw()
        pygame.display.flip()
        
    sys.exit()
    
if __name__ == "__main__":
    main()