'''
Source Name:           cannon.py
Author:                Brandon McLellan
Last Modified:         August 9th, 2012
Last Modified By:      Brandon McLellan
Description:
    Handles core cannon functionality, such as upgrades, shooting, positioning.
    Used for placed cannons, cannon buttons and the cannon the cursor.
Revision History:
    Revision 10:
        - Added freeze bullets
    Revision 9:
        - Added function to upgrade cannons
    Revision 8:
        - Changed variable name to not conflict with reserved name(range).
    Revision 7:
        - Finished missile implementation and remembered basic high school trig.
    Revision 6:
        - Started to implement missiles and cannon aiming.
    Revision 5:
        - Moved radius drawing into Cannon class.
    Revision 4:
        - Added cannon mode for buttons, replaced static images with animated ones.
    Revision 3:
        - Added cannon modes for placement and being on cursor.
    Revision 2:
        - Added actual cannon image, cannons rotate.
    Revision 1:
        - Base sprite class, changes colors on selection.
'''
import pygame
import math

'''
    Missile Class
        Missile sprite class, missiles always take 5 frames
        to reach their target to keep it simple.
'''
class Missile(pygame.sprite.Sprite):
    def __init__(self, damage, x, y, dx, dy, monster):
        pygame.sprite.Sprite.__init__(self)
        
        # Load the image of missile
        self.image = pygame.image.load("assets/missile.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        # Store the damage, delta and destination
        self.damage = damage
        self.dx = dx
        self.dy = dy
        self.tick = 0
        self.monster = monster
        self.freeze = False
        
    def update(self):
        self.tick += 1
        #Missiles always take 5 frames to hit.
        if self.tick > 5:
            #Check if monster is still valid in case they already died.
            if self.monster != None:
                self.monster.shoot(self.damage, self.freeze)
            return self.kill()
            
        self.rect.x += self.dx
        self.rect.y += self.dy
            
        return True
        
'''
    Cannon Class
        Cannon sprite is verastile in the sense that it is used as
        a button, be on the cursor, or on the grid.
'''
class Cannon(pygame.sprite.Sprite):
    #Different modes the cannon can be
    Button = 0
    Invalid = 1
    Active = 2
    Placement = 3

    def __init__(self, x, y, name, image, cost, speed, ranges, damage):
        pygame.sprite.Sprite.__init__(self)
        
        # Determine the mode of the cannon.
        if x == -1 and y == -1:
            self.mode = Cannon.Placement
        else:
            self.mode = Cannon.Button
            
        self.x = x
        self.y = y
        
        # Store upgrade information
        self.costs = cost
        self.speeds = speed
        self.ranges = ranges
        self.damages = damage
        
        # Set the cannons base stats
        self.name = name
        self.level = 1
        self.cost = self.costs[self.level -1]
        self.speed = self.speeds[self.level -1]
        self.range = self.ranges[self.level -1]
        self.damage = self.damages[self.level -1]
        self.salvage = round(self.cost * 0.70)
        self.afford = True
        
        # Bullet information
        self.canFire = True
        self.shotTick = 0
        self.freeze = False
        
        # Load the cannon border
        self.image = pygame.Surface((25, 25))
        self.border = pygame.image.load("assets/Cannon.png")
        self.border.set_colorkey((0,0,0))
        self.selected = False
        
        # Load the cannon specific image
        self.cannon = pygame.image.load("assets/" + image + ".png")
        self.cannon.set_colorkey((255, 255, 255))
        self.rotationAngle = 0
        
        self.rect = self.image.get_rect()

    # Returns information about the next upgrade of the cannon
    def getUpgradeStats(self):
        if self.level == 4:
            return False
        return (self.damages[self.level], self.speeds[self.level], self.ranges[self.level], self.costs[self.level])
        
    # Upgrades the cannon stats and salvage value.
    def upgrade(self):
        if self.level == 4:
            return False
        self.salvage += (self.cost * 0.70)
        self.level += 1
        self.cost = self.costs[self.level -1]
        self.speed = self.speeds[self.level -1]
        self.range = self.ranges[self.level -1]
        self.damage = self.damages[self.level -1]
        
    # Draws the radius circle around an active cannon
    def drawRadius(self, surface):
        pygame.draw.circle(surface, (25, 25, 25), (self.rect.x + 12, self.rect.y + 12), self.range * 20, 1)
        
        
    # Math to determine the angle in different quadrants, this really sucked.
    def calculateAngle(self, x1, y1, x2, y2):
        if x1 == x2 and y1 == y2:
            return 0;
        
        angle = 0
        # Check for vertical and horizontal lines
        if x1 == x2:
            angle = 270 if y2 > y1 else 90
        elif y1 == y2:
            angle = 0 if x2 > x2 else 180
        else:
            # Calculate angle relative to quadrant
            angle = math.atan((y2 - y1) / (x2-x1)) * 180.0 / math.pi

            quadrant = 0
            if y2 < y1:
                quadrant = 1 if x2 > x1 else 2
            else:
                quadrant = 4 if x2 > x1 else 3

            if quadrant == 1:
                return 90 + (angle * -1)
            elif quadrant == 2:
                return 270 - angle
            elif quadrant == 3:
                return 270 + (angle * -1)
            elif quadrant == 4:
                return 90 - angle
            else:
                return 0

        
    # Determines the cannons angle to point at monster, then creates missile to shoot.
    def shoot(self, monster, dist):
        #A missile takes 3 frames to reach it's unit, so calculate where the monster will be in 3 frames.
        (projectedX, projectedY) = (monster.rect.centerx + (monster.pixelDelta[0] * 5), monster.rect.centery + (monster.pixelDelta[1] * 5))

        #Determine the delta to reach monster, divide by three to determine speed.
        dx = (projectedX - self.rect.centerx) / 5
        dy = (projectedY - self.rect.centery) / 5
        
        # Calculate angle to point cannon at monster
        self.rotationAngle = self.calculateAngle(self.rect.centerx, self.rect.centery, projectedX, projectedY)
        if self.rotationAngle == None:
            self.rotationAngle = 0
            
        # Create missile that will be shot at monster.
        missile = Missile(self.damage, self.rect.centerx, self.rect.centery, dx, dy, monster)
        missile.freeze = self.freeze
        
        self.canFire = False
        return missile
    
    def update(self):
        # Cannon cool-down so it shoots relative to it's speed.
        if not self.canFire:
            self.shotTick += 1
            if self.shotTick >= (self.speed * 5):
                self.canFire = True
                self.shotTick = 0
                
        # Determines the position of cannon depending on it's mode.'
        if self.mode == Cannon.Button:
            (self.rect.x, self.rect.y) = (self.x, self.y)
        else:
            #If cursor is not in grid or over a cannon, place cannon on cursor.
            if self.x == -1 and self.y == -1 or self.mode == Cannon.Invalid:
                self.rect.center = pygame.mouse.get_pos()
            else:
                #Place cannon on grid
                (self.rect.x, self.rect.y) = (self.x * 25 + 128, self.y * 25 + 117)
  
        # Sets the border color depending on hover and affordability.
        if self.mode == Cannon.Button:
            if not self.afford:
                self.image.fill((255, 0, 0))
            elif self.rect.collidepoint(pygame.mouse.get_pos()):
                self.image.fill((182, 178, 255))
            else:
                self.image.fill((107, 107, 107))
        # Set border to light-blue if we have on cursor.
        elif self.selected or self.mode == Cannon.Placement:
            self.image.fill((182, 178, 255))
        # Set border to red if it is over another cannon
        elif self.mode == Cannon.Invalid:
            self.image.fill((255, 0, 0))
        # Set the default border color
        else:
            self.image.fill((107, 107, 107))
            
        # Code to rotate the cannon if not firing at monster.
        if self.canFire:
            self.rotationAngle += 3
            if self.rotationAngle >= 360:
                self.rotationAngle = 0

        # Rotating images screws with the rectangle behind it, this corrects it.
        aimedCannon = pygame.transform.rotate(self.cannon, self.rotationAngle)
        newRect = self.cannon.get_rect().copy()
        newRect.center = aimedCannon.get_rect().center
        aimedCannon = aimedCannon.subsurface(newRect).copy()
        
        # Finally draw the cannon
        self.image.blit(self.border, (0,0))
        self.image.blit(aimedCannon, (0,0))