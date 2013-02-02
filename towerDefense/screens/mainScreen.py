'''
Source Name:           mainScreen.py
Author:                Brandon McLellan
Last Modified:         August 9th, 2012
Last Modified By:      Brandon McLellan
Description:
    
Revision History:
    Revision 3:
        - Added Very Hard difficulty
    Revision 2:
        - Added difficulties
    Revision 1:
        - Wrote orginal screen class
'''
from towerDefense.screens import screen
from controls import button
import pygame

class MainScreen(screen.Screen):
    def __init__(self):
        screen.Screen.__init__(self, "main")
        
        self.background = pygame.image.load("assets/MainScreen.png")
        self.blit(self.background, (0,0))
        
        #Initialize buttons for difficulty
        self.easy = button.Button(36, 145, "Easy", "SmallButton.png", 14)
        self.medium = button.Button(36, 175, "Normal", "SmallButton.png", 14)
        self.hard = button.Button(36, 205, "Hard", "SmallButton.png", 14)
        self.veryHard = button.Button(36, 235, "Very Hard", "SmallButton.png", 14)
        
        self.buttonGroup.add(self.easy, self.medium, self.hard, self.veryHard)
        
    def event(self, event):
        # Check if player pressed any buttons.
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.easy.collide(event.pos):
                self.ChangeScreen("game", 0)
            elif self.medium.collide(event.pos):
                self.ChangeScreen("game", 1)
            elif self.hard.collide(event.pos):
                self.ChangeScreen("game", 2)
            elif self.veryHard.collide(event.pos):
                self.ChangeScreen("game", 3)
        return True