'''
Source Name:           gameEngine.py
Author:                Brandon McLellan
Last Modified:         August 9th, 2012
Last Modified By:      Brandon McLellan
Description:
    
Revision History:
    Revision 10:
        - Added very hard difficulty.
    Revision 9:
        - Added difficulties.
    Revision 8:
        - Wrote monster waves code.
    Revision 7:
        - Check for monster health and increase score and points on kill.
    Revision 6:
        - Added cannon shooting code
    Revision 5:
        - Seperated game logic from user interface.
    Revision 4:
        - More fixes to pathing.
    Revision 3:
        - Began writing pathing algorthim.
    Revision 2:
        - Added cannon placement and salvage functionality.
    Revision 1:
        - Wrote basic grid code to control cannons.
'''

from towerDefense.cannons.cannon import Cannon
from towerDefense.monsters.monsterTypes import *
import pygame
import math

class GameEngine():
    Width = 20
    Height = 14
    
    # Starting cash for player
    StartingCash = [50, 40, 30, 15]
    
    # Starting lifes for player
    StartingLifes = [20, 10, 5, 3]
    
    # Duration in frames in between spawning monsters
    MonsterSpawn = 10
    
    # Duration in frames in between spawning waves. 
    WaveDuration = [240, 180, 150, 100]
    
    # Multiple of extra monsters per 10 waves.
    WaveMultiplier = [2, 3, 4, 8]
    
    def __init__(self, difficulty):
        self.difficulty = difficulty
        
        # Main game stats
        self.lifes = GameEngine.StartingLifes[self.difficulty]
        self.score = 0
        self.cash = GameEngine.StartingCash[self.difficulty]
        
        self.waveDuration = GameEngine.WaveDuration[self.difficulty]
        self.waveMultiplier = GameEngine.WaveMultiplier[self.difficulty]
        
        self.cannonPlacement = pygame.mixer.Sound("assets/sounds/placecannon.wav")
        self.lifeLossSound = pygame.mixer.Sound("assets/sounds/lifeloss.wav")
        self.shootSound = pygame.mixer.Sound("assets/sounds/shoot.wav")
        self.waveStart = pygame.mixer.Sound("assets/sounds/newwave.wav")
        
        # Hold information about current monster wave, and time until next wave.
        self.wave = 0
        self.waveTick = 0
        self.waveTypes = ["Normal", "Normal", "Normal", "Normal", "Fast", "Immune", "Normal", "Fast", "Immune", "Boss"]
        self.waveCount = [3,4,5,6,4,4,8,6,6,1]
        
        # Hold information about number of monsters to spawn and the last spawn time.
        self.monsterSpawn = []
        self.monsterTick = 0
        self.monstersKilled = 0
        
        # Contains sprite groups
        self.cannons = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.missiles = pygame.sprite.Group()
        
        # Handles generating the map matrix to store cannon placement.
        self.map = []
        for y in range(0, GameEngine.Width):
            self.map.append([0] * GameEngine.Height)
        
        self.path = self.determinePath((0, 7), (19, 7))

        #Stores cannons that are active or on cursor.
        self.active = None
        self.cursor = None
    
    # Handles mouse events for cannon selection.
    def onMouseUp(self, button, x, y):
        if self.active != None:
            self.active.selected = False
            
        # Check if we have clicked on any cannons.
        for cannon in self.cannons:
            if cannon.rect.collidepoint(x, y):
                # Deselect if player clicks on already active cannon.
                if self.active == cannon:
                    self.active = None
                    cannon.selected = False
                else:
                    self.active = cannon
                    cannon.selected = True
                return True

        self.active = None
        return True
        
    '''
        GameEngine.tick(self)
        Handles spawning, waves, missiles and cannon placement.
    '''
    def tick(self):
        
        # Spawn monsters at a steady rate to prevent clumping.
        self.monsterTick += 1
        if len(self.monsterSpawn) > 0 and self.monsterTick > GameEngine.MonsterSpawn:
            self.monsterTick = 0
            self.monsters.add(self.monsterSpawn.pop(0))

        # Check if we have started sending waves of monsters
        self.waveTick += 1
        if self.wave > 0 and self.waveTick >= self.waveDuration:
            self.waveTick = 0
            self.spawn()
                
        
        # Check for cannons that can fire.
        for cannon in self.cannons:
            if not cannon.canFire:
                continue
            # Find a monster within range of this cannon.
            for monster in self.monsters:
                distance = math.fabs(monster.rect.centerx - cannon.rect.centerx) + math.fabs(monster.rect.centery - cannon.rect.centery)
                if distance <= (cannon.range * 20):
                    self.shootSound.play()
                    self.missiles.add(cannon.shoot(monster, distance))
                    break

        # Check for monsters who have died or won.
        for monster in self.monsters:
            if monster.health <= 0:
                self.score += monster.score
                self.cash += monster.cash
                self.monstersKilled += 1
                monster.kill()
            elif monster.fin:
                self.lifes -= 1
                self.lifeLossSound.play()
                monster.kill()
                
        if self.lifes <= 0:
            return False
            
        # Do check for cursor cannon placement
        if self.cursor != None:
            pos = pygame.mouse.get_pos()
            self.cursor.x = -1
            self.cursor.y = -1
            if pos[0] > 128 and pos[1] > 117:
                # Calculate where the cursor is relative to the grid coordinates.
                self.cursor.x = math.floor((pos[0] - 128) / 25)
                self.cursor.y = math.floor((pos[1] - 117) / 25)
                
                #Check if there is already a cannon in that position.
                if self.getPosition(self.cursor.x, self.cursor.y) or (self.cursor.x == 0 and (self.cursor.y == 6 or self.cursor.y == 7)):
                    self.cursor.mode = Cannon.Invalid
                else:
                    self.cursor.mode = Cannon.Placement
        
            # Update and draw cursor cannon
            self.cursor.update()
            #surface.blit(self.cursor.image, self.cursor.rect)
            
        return True
    
    def spawn(self):
        self.wave += 1
        self.waveTick = 0
        
        self.waveStart.play()
        #Determine the type of monster and number of monsters.
        monsterType = (self.wave % 10) - 1
        monsterCount = self.waveCount[monsterType] + (self.waveMultiplier * math.floor(self.wave / 10))
        
        for n in range(0, monsterCount):
            if self.waveTypes[monsterType] == "Normal":
                self.monsterSpawn.append(NormalMonster(self.wave, self.path))
            elif self.waveTypes[monsterType] == "Fast":
                self.monsterSpawn.append(FastMonster(self.wave, self.path))
            elif self.waveTypes[monsterType] == "Immune":
                self.monsterSpawn.append(ImmuneMonster(self.wave, self.path))
            else:
                self.monsterSpawn.append(BossMonster(self.wave, self.path))
                
        return True

    def select(self, cannon):
        # Check if player has enough cash to afford cannon.
        if self.cash < cannon.cost:
            return False
        self.cursor = cannon.getInstance()
    
    def place(self):
        # Check if there is a cannon on the cursor.
        if self.cursor == None:
            return False
        
        # Check if the cannon on the cursor is in placement mode.
        if self.cursor.mode != Cannon.Placement:
            return False
        
        # Check if this cannon will block the path of the monsters.
        self.map[self.cursor.x][self.cursor.y] = 1
        newPath = self.determinePath((0, 7), (19, 7))
        if newPath == None:
            self.map[self.cursor.x][self.cursor.y] = 0
            return False
        self.path = newPath
        
        # Set the cannon as active and deduct cash.
        self.cursor.mode = Cannon.Active
        self.cash -= self.cursor.cost
        
        self.cannonPlacement.play()
        
        # Place cannon on the map.
        self.map[self.cursor.x][self.cursor.y] = 1
        self.cannons.add(self.cursor)
        self.cursor = None
        
        self.updateMonsterPath()
        
        return True
    
    def upgrade(self):
        if self.active == None:
            return False
        
        if self.active.level == 4:
            return False
        
        (dmg, range, speed, costs) = self.active.getUpgradeStats()
        if self.cash < costs:
            return False
        
        self.active.upgrade()
        self.cash -= costs
        
        return True
    
    def salvage(self):
        # Check if there a selected cannon to salvage.
        if self.active == None:
            return False
        
        # Pay the player the salvage price
        self.cash += self.active.salvage
        
        # Remove the cannon from the map.
        self.map[self.active.x][self.active.y] = 0
        self.cannons.remove(self.active)
        
        #Deselect the cannon.
        self.active = None
        
        self.path = self.determinePath((0, 7), (19, 7))
        self.updateMonsterPath()
        
        return True
    
    def updateMonsterPath(self):
        for monster in self.monsters:
            monster.path = self.path
    
    def getPosition(self, x, y):
        for cannon in self.cannons:
            if cannon.x == x and cannon.y == y:
                return cannon
        return None
    
    '''
        Function generates the best path for the monsters to take to reach the end point.
        It is my own implementation of A-Star.
    '''
    def determinePath(self, start, end):
        # Class to hold information about each node.
        class Node():
            def __init__(self, coord, parentNode):
                self.coord = coord
                self.parent = parentNode
                
            # G is the distance from the starting position as your following the path.
            def getG(self, parent = None):
                # If there is no parent node, it has to be starting node.
                if parent == None:
                    if self.parent == None:
                        return 0
                    parent = self.parent
                # Calculates distance using the Manhattan method.
                return parent.getG() + math.fabs(parent.coord[0] - self.coord[0]) + math.fabs(parent.coord[1] - self.coord[1])
            
            # H is the distance from to the end position, disregarding any cannons blocking the path
            # F is the sum of H and G.
            def getF(self, end):
                self.h = math.fabs(end[0] - self.coord[0]) + math.fabs(end[1] - self.coord[1])
                return self.getG() + self.h
            
            # Compares passed node against current node.
            def compare(self, node):
                return self.coord[0] == node.coord[0] and self.coord[1] == node.coord[1]

        # Closed set is list of coordinates that are considered the best path.
        closedSet = []
        # Open set is a list of coordinates that are to be considered and checked.
        openSet = []
        # Start by placing the start position in the open list.
        openSet.append(Node(start, None))
        
        while len(openSet):
            # This will check for the best node by finding the lowest F score in the open list.
            bestNode = None
            for node in openSet:
                if not bestNode or bestNode.getF(end) > node.getF(end):
                    bestNode = node
            
            # Remove the best node from the open list and place on closed list.
            openSet.remove(bestNode)
            closedSet.append(bestNode)
            
            # Check if we have reached destination
            if bestNode.coord[0] == end[0] and bestNode.coord[1] == end[1]:
                # To obtain the correct path, traverse the parents from the last node.
                endPath = [bestNode.coord]
                currentNode = bestNode
                while currentNode.parent:
                    currentNode = currentNode.parent
                    endPath.append(currentNode.coord)
                #Since the list starts with the last coordinate, reverse it.
                endPath.reverse()
                return endPath
            
            #Check every position around best node.
            for x in range(-1, 2, 1):
                for y in range(-1, 2, 1):
                    #This would be the current best node, so skip.
                    if x == 0 and y == 0:
                        continue
                    
                    # These coordinates are adjacent to the best node found above.
                    adjacentX = bestNode.coord[0] + x
                    adjacentY = bestNode.coord[1] + y   
                    
                    # Disregard adjacent node if out of bounds.
                    if adjacentX < 0 or adjacentY < 0 or adjacentX >= GameEngine.Width or adjacentY >= GameEngine.Height:
                        continue
                    
                    # Check to see if node is blocked by cannon
                    if self.map[adjacentX][adjacentY] == 1:
                        continue
                    
                    # Check to make sure we aren't cutting corners
                    if x != 0 and y != 0:
                        # Check corners of the potential node for cannons.
                        if self.map[adjacentX][bestNode.coord[1]] == 1 or self.map[bestNode.coord[0]][adjacentY] == 1:
                            continue

                    # Create a new node to place in open set.
                    new_node = Node((adjacentX, adjacentY), bestNode)
                    # Check to make sure node isn't in closed set.
                    for node in closedSet:
                        if node.compare(new_node):
                            break
                    else:
                        # Check to make sure node isn't in open set.
                        for node in openSet:
                            if node.compare(new_node):
                                # If the node is in open list, check to see if this is a better path.
                                if node.getG(bestNode) < node.getG():
                                    node.parent = bestNode
                                break
                        else:
                            openSet.append(new_node)
        return None
        