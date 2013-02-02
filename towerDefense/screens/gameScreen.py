'''
Source Name:           gameScreen.py
Author:                Brandon McLellan
Last Modified:         August 7th, 2012
Last Modified By:      Brandon McLellan
Description:
    Main game screen, handles all screen creation, updating and events.
Revision History:
    Revision 8:
        - Added button to get to main screen.
        - Added code to switch to end screen when you die.
    Revision 7:
        - Added waves information to top-right.
        - Added upgrade button event code.
    Revision 6:
        - Added missile drawing.
    Revision 5:
        - Replaced static cannon buttons with animated version.
        - Added upgrade information to cannon stats.
        - Cleaned up event code
    Revision 4:
        - Seperated game logic from user interface.
        - Added current lives to screen.
    Revision 3:
        - Basic monster testing, re-align some labels.
    Revision 2:
        - Added cannon stats, basic pathing testing.
    Revision 1:
        - Base game screen, draws background, and basic stats.
'''
from towerDefense.screens import screen
from .. import gameEngine
from towerDefense.cannons import cannon, cannonTypes
from controls import button, label

import pygame


class GameScreen(screen.Screen):
    def __init__(self):
        screen.Screen.__init__(self, "game")

        # Create game grid where cannons can be placed
        self.gameGrid = pygame.rect.Rect((128, 117, 500, 350))
        
        # Load the game background
        self.background = pygame.image.load("assets\GameScreen.png")
        self.blit(self.background, (0,0))
        
        # Initialize the cannon buttons.
        self.cannonButtons = pygame.sprite.Group()
        self.basicCannon = cannonTypes.BasicCannon(6, 180)
        self.sniperCannon = cannonTypes.SniperCannon(33, 180)
        self.splashCannon = cannonTypes.SplashCannon(60, 180)
        self.freezeCannon = cannonTypes.FreezeCannon(87, 180)
        self.cannonButtons.add(self.basicCannon, self.splashCannon, self.sniperCannon, self.freezeCannon)
        
        self.mainScreen = button.Button(10, 10, "Main Screen", "SmallButton.png", 14)
        self.buttonGroup.add(self.mainScreen)
        
        # Create labels for life, score and cash values.
        self.lifeLabel = label.Label(60, 67, "")
        self.lifeLabel.options(fontName = "assets/MYRIADPRO.otf", fontSize = 28, color = (0,0,0),
                                align = label.Label.Center)
        self.scoreLabel = label.Label(60, 149, "")
        self.scoreLabel.options(fontName = "assets/MYRIADPRO.otf", fontSize = 28, color = (0,0,0),
                                align = label.Label.Center)        
        self.cashLabel = label.Label(60, 110, "")
        self.cashLabel.options(fontName = "assets/MYRIADPRO.otf", fontSize = 28, color = (0,0,0),
                               align = label.Label.Center)
        self.labelGroup.add(self.lifeLabel, self.scoreLabel, self.cashLabel)
        
        # Create labels for cannon information.
        self.cannonInfo = pygame.sprite.Group()
        
        
        self.nameLabel = label.Label(60, 247, "")
        self.nameLabel.options(fontName = "assets/MYRIADPRO.otf", fontSize = 22, color = (0,0,0), align = label.Label.Center)    
        self.costLabel = label.Label(57, 260, "Cost: 0")
        self.costLabel.options(fontName = "assets/MYRIADPRO.otf", fontSize = 18, color = (0,0,0), align = label.Label.Center)   
        self.attackLabel = label.Label(11, 270, "Attack: 0")
        self.attackLabel.options(fontName = "assets/MYRIADPRO.otf", fontSize = 18, color = (0,0,0))
        self.speedLabel = label.Label(11, 285, "Speed: 0")
        self.speedLabel.options(fontName = "assets/MYRIADPRO.otf", fontSize = 18, color = (0,0,0))
        self.rangeLabel = label.Label(11, 300, "Range: 0")
        self.rangeLabel.options(fontName = "assets/MYRIADPRO.otf", fontSize = 18, color = (0,0,0))
        
        
        self.cannonInfo.add(self.nameLabel, self.attackLabel, self.speedLabel, self.rangeLabel, self.costLabel)
        
        # Button for salvaging the selected cannon.
        self.salvageButton = button.Button(11, 315, "Salvage", "SmallButton.png", 14)
        
        self.upgradeInfo = pygame.sprite.Group()
        
        self.upgradeLabel = label.Label(60, 360, "Lvl 2 Upgrade")
        self.upgradeLabel.options(fontName = "Myriad Pro", fontSize = 18, color = (0,0,0), align = label.Label.Center)
        self.attackUpLabel = label.Label(11, 375, "+2 Attack")
        self.attackUpLabel.options(fontName = "Myriad Pro", fontSize = 18, color = (0,0,0))
        self.speedUpLabel = label.Label(11, 390, "+1 Speed")
        self.speedUpLabel.options(fontName = "Myriad Pro", fontSize = 18, color = (0,0,0))
        self.rangeUpLabel = label.Label(11, 405, "+1 Range")
        self.rangeUpLabel.options(fontName = "Myriad Pro", fontSize = 18, color = (0,0,0))
        self.upgradeCostLabel = label.Label(11, 420, "Cost: 20")
        self.upgradeCostLabel.options(fontName = "Myriad Pro", fontSize = 18, color = (0,0,0))
        self.upgradeButton = button.Button(11, 435, "Upgrade", "SmallButton.png", 14)
        
        self.upgradeInfo.add(self.upgradeLabel, self.attackUpLabel, self.speedUpLabel, self.rangeUpLabel, self.upgradeCostLabel, self.upgradeButton)
        
        self.waveInfo = label.Label(560, 35, "")
        self.waveInfo.options(fontName = "Myriad Pro", fontSize = 18, color = (0,0,0), align = label.Label.Center)
        self.waveNext = label.Label(560, 50, "Upcoming Wave")
        self.waveNext.options(fontName = "Myriad Pro", fontSize = 18, bold = True, color = (0,0,0), align = label.Label.Center)
        self.waveTimer = label.Label(560, 65, "Press to start")
        self.waveTimer.options(fontName = "Myriad Pro", fontSize = 18, color = (0,0,0), align = label.Label.Center)
        self.sendWave = button.Button(510, 80, "Send Wave", "SmallButton.png", 14)
        self.labelGroup.add(self.waveInfo, self.waveNext, self.waveTimer, self.sendWave)
        
    def init(self, info):
        self.difficulty = info
        self.engine = gameEngine.GameEngine(self.difficulty)
        
    def event(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                # Check for button presses and pass to game engine.
                for cannon in self.cannonButtons:
                    if cannon.rect.collidepoint(*event.pos):
                        self.engine.select(cannon)
                        break
                    
                if self.mainScreen.collide(event.pos):
                    self.ChangeScreen("main")    
                if self.salvageButton.collide(event.pos):
                    self.engine.salvage()  
                if self.upgradeButton.collide(event.pos):
                    if self.engine.upgrade():
                        return True
                if self.gameGrid.collidepoint(event.pos):
                    self.engine.place()
                if self.sendWave.collide(event.pos):
                    self.engine.spawn()
                    
                return self.engine.onMouseUp(event.button, event.pos[0], event.pos[1])
            elif event.button == 3:
                self.engine.cursor = None
                
        return True
    
    def update(self):
        
        # Run engine tick, check if we have lost.
        if self.engine.tick() == False:
            self.ChangeScreen("end", (self.engine.wave - 1, self.engine.score, self.engine.monstersKilled, self.engine.difficulty))
            return
        
        #Update and draw the sprites to screen.
        self.engine.cannons.update()
        self.engine.cannons.draw(self)
        
        self.engine.monsters.update()
        self.engine.monsters.draw(self)
        
        self.engine.missiles.update()
        self.engine.missiles.draw(self)
        
        # Draw the attack-radius circle if cannon active.
        if self.engine.active != None:
            self.engine.active.drawRadius(self)
            
        # Draw the cursor cannon if selected.
        if self.engine.cursor != None:
            self.blit(self.engine.cursor.image, self.engine.cursor.rect)
       
        #Update labels for key information.
        self.lifeLabel.text = str(self.engine.lifes)
        self.scoreLabel.text = str(self.engine.score)
        self.cashLabel.text = str(self.engine.cash)
        
        if self.engine.wave > 0:
            currentWave = (self.engine.wave % 10) - 1
            self.waveInfo.text = "Wave " + str(self.engine.wave) + " - " + self.engine.waveTypes[currentWave]
            nextWave = ((self.engine.wave + 1) % 10) - 1
            waveTime = round((self.engine.waveDuration - self.engine.waveTick) / 30, 1)
            self.waveTimer.text = self.engine.waveTypes[nextWave] + " - " + str(waveTime) + " second" + ("s" if waveTime > 1 else "")
                
        # Determine if we need to draw cannon information.
        stats = self.engine.active
        mouse = pygame.mouse.get_pos()
        for button in self.cannonButtons:
            if self.engine.cash < button.cost:
                button.afford = False
            else:
                button.afford = True
                
            if button.rect.collidepoint(mouse):
                stats = button
        
        self.cannonButtons.clear(self, self.background)       
        self.cannonButtons.update()
        self.cannonButtons.draw(self)
        
        #Check if player has cannon selected.
        if stats != None:
            self.nameLabel.text = stats.name
            self.attackLabel.text = "Attack: " + str(stats.damage)
            self.speedLabel.text = "Speed: " + str(stats.speed)
            self.rangeLabel.text = "Range: " + str(stats.range)
            
            if stats.mode == cannon.Cannon.Active:
                self.salvageButton.update()
                self.blit(self.salvageButton.image, self.salvageButton.rect)
                self.costLabel.color = (0, 0, 0)
                self.costLabel.text = "Resell: " + str(stats.salvage)
                
                if stats.level < 4:
                    (atk, speed, rnge, cost) = stats.getUpgradeStats()
                    self.upgradeLabel.text = "Level " + str(stats.level + 1) + " Upgrade"
                    self.attackUpLabel.text = "+" + str(atk - stats.damage) + " Attack"
                    self.speedUpLabel.text = "+" + str(speed - stats.speed) + " Speed"
                    self.rangeUpLabel.text = "+" + str(rnge - stats.range) + " Range"
                    self.upgradeCostLabel.text = "Cost: " + str(cost)
                
                    self.upgradeInfo.update()
                    self.upgradeInfo.draw(self)
                
            elif stats.mode == cannon.Cannon.Button:
                if self.engine.cash < stats.cost:
                    self.costLabel.color = (255, 0, 0)
                else:
                    self.costLabel.color = (0, 0, 0)
                self.costLabel.text = "Cost: " + str(stats.cost)
                
            self.cannonInfo.update()
            self.cannonInfo.draw(self)
                
            
        
        return True