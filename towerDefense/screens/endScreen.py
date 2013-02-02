'''
Source Name:           endScreen.py
Author:                Brandon McLellan
Last Modified:         August 7th, 2012
Last Modified By:      Brandon McLellan
Description:
    Generates end score screen.
Revision History:
    Revision 3:
        - Passed difficulty for play again.
    Revision 2:
        - Added post-game stats
    Revision 1:
        - Wrote base screen class
'''
from towerDefense.screens import screen
from controls import button, label
import pygame

class EndScreen(screen.Screen):
    def __init__(self):
        screen.Screen.__init__(self, "end")
        
        self.background = pygame.image.load("assets/EndScreen.png")
        self.blit(self.background, (0,0))
        
        #Initialize labels to show post-game stats
        self.wavesSurvived = label.Label(336, 182, "")
        self.wavesSurvived.options(fontName = "assets/MYRIADPRO.otf", fontSize = 30, color = (0,0,0))
        
        self.score = label.Label(336, 224, "")
        self.score.options(fontName = "assets/MYRIADPRO.otf", fontSize = 30, color = (0,0,0))
        
        self.monstersKilled = label.Label(336, 265, "")
        self.monstersKilled.options(fontName = "assets/MYRIADPRO.otf", fontSize = 30, color = (0,0,0))
        
        self.labelGroup.add(self.wavesSurvived, self.score, self.monstersKilled)
       
        #Initialize buttons to replay game.
        self.playAgain = button.Button(228, 330, "Play Again")
        self.mainScreen = button.Button(228, 380, "Main Menu")
        self.buttonGroup.add(self.playAgain, self.mainScreen)
        
        self.difficulty = 0
        
    # Gets information passed by other screen.
    def init(self, info):
        (waves, score, monsters, difficulty) = info
        self.wavesSurvived.text = str(waves)
        self.score.text = str(score)
        self.monstersKilled.text = str(monsters)
        self.difficulty = difficulty
        
    def event(self, event):
        # Check if player pressed either button.
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.playAgain.collide(event.pos):
                self.ChangeScreen("game")
            if self.mainScreen.collide(event.pos):
                self.ChangeScreen("main")
        return True