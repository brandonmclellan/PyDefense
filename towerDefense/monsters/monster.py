'''
Source Name:           monster.py
Author:                Brandon McLellan
Last Modified:         August 9th, 2012
Last Modified By:      Brandon McLellan
Description:
    Monster sprite class, mostly handles following path.
Revision History:
    Revision 6:
        - Added slowing effect when shot by frost cannon.
    Revision 5:
        - Changed static bullet damage to reflect cannon's actual damage.
    Revision 4:
        - Changed the speed of monsters, as they were too fast.
    Revision 3:
        - Added score and cash for killing monster.
    Revision 2:
        - Fixed monster rotation, properly follows given path.
    Revision 1:
        - Rewrote monster class from first attempt.
'''
import pygame
import math

'''
    Monster Class
        Monster sprite class, does a lot of math to properly follow
        path generated.
'''
class Monster(pygame.sprite.Sprite):
    def __init__(self, name, speed, path):
        pygame.sprite.Sprite.__init__(self)
        
        #Store monster's stats
        self.name = name
        self.path = path
        
        # Load the monster's image and create blank surface.
        self.monster = pygame.image.load("assets/" + name + ".png")
        self.monster.set_colorkey((255, 255, 255))
        self.image = pygame.surface.Surface((15, 15))
        self.image.set_colorkey((255, 255, 255))
        
        # Monster position and movement
        self.rect = self.monster.get_rect()
        self.rect.center = (140, 303)
        
        self.health = 0
        self.speed = speed
        self.score = 0
        self.cash = 0
        self.immune = False
        self.freezeTick = 0
        
        # Current grid position and node destination
        self.coord = (0, 7)
        
        # The destination node the monster is moving to in pixel and grid.
        self.gridDest = (0, 0)
        self.pixelDest = (0, 0)
        
        # Current pixel delta and pixel node destination
        self.gridDelta = (0, 0)
        self.pixelDelta = (0, 0)
        
        # Which node in the path the monster is
        self.node = 0
        self.rotation = 0
        self.tick = 0
        self.frames = 1 / (self.speed / 40)
        self.calculateDelta()
        
        self.shotTick = 0
        self.shot = False
        self.fin = False
        
    # Calculates the destination's pixel location, and pixel and grid delta.
    def calculateDelta(self):
        if self.node != 0:
            self.coord = self.gridDest
        # Increment the path node, check if we have reached destination.
        self.node += 1
        if self.node >= len(self.path):
            self.pixelDelta = ((self.speed / 40) * 25, 0)
            self.rotation = 270
            self.fin = True
            return False
        
        # Store the grid and pixel coordinates of the destination node.
        self.gridDest = self.path[self.node]
        self.pixelDest = (self.path[self.node][0] * 25 + 140, self.path[self.node][1] * 25 + 129)
        
        # Determine the delta to reach destination node
        self.pixelDelta = (self.pixelDest[0] - self.rect.centerx, self.pixelDest[1] - self.rect.centery)
        self.gridDelta = (self.gridDest[0] - self.coord[0], self.gridDest[1] - self.coord[1])
        
        # Calculate pixel delta factoring in monster speed.
        self.pixelDelta = ((self.speed / 40) * self.pixelDelta[0], (self.speed / 40) * self.pixelDelta[1])
        
        # Determine the monsters image angle depend on the which way they are moving.
        rotations = ((0, -1, 0), (0, 1, 180), (-1, -1, 45), (-1, 0, 90), (-1, 1, 135), (1, -1, 315), (1, 0, 270), (1, 1, 225))
        for angle in rotations:
            if angle[0] == self.gridDelta[0] and angle[1] == self.gridDelta[1]:
                self.rotation = angle[2]
                break
    
    # Called by missile on contact
    def shoot(self, damage, freeze):
        self.health -= damage
        if freeze and not self.immune:
            self.freezeTick = 30
        
    def update(self):
        self.image.fill((255, 255, 255))
        
        self.tick += 1
        
        # If we have reached the current node, determine delta to next node.
        if self.tick >= self.frames:
            self.calculateDelta()
            self.tick = 0
            
        # Slows the monster movement if hit by freeze cannon
        if self.freezeTick > 0:
            self.freezeTick -= 1
            self.rect.centerx += (self.pixelDelta[0]) / 2
            self.rect.centery += (self.pixelDelta[1]) / 2
        else:
            self.rect.centerx += self.pixelDelta[0]
            self.rect.centery += self.pixelDelta[1]
            
        # Handles proper rotation of monsters
        rotatedMonster = pygame.transform.rotate(self.monster, self.rotation)
        newRect = self.rect.copy()
        newRect.center = rotatedMonster.get_rect().center
        rotatedMonster = rotatedMonster.subsurface(newRect).copy()
        self.image.blit(rotatedMonster, (0,0))