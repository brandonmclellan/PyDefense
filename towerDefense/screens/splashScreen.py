'''
Source Name:           splashScreen.py
Author:                Brandon McLellan
Last Modified:         August 9th, 2012
Last Modified By:      Brandon McLellan
Description:
    
Revision History:
    Revision 1:
        - Wrote splash screen class
'''
from towerDefense.screens import screen
from controls import label
import pygame

class SplashScreen(screen.Screen):
    def __init__(self):
        screen.Screen.__init__(self, "main")
        
        self.background = pygame.image.load("assets/SplashScreen.png")
        self.blit(self.background, (0,0))
        
        #Initialize buttons for difficulty
        self.loading = label.Label(225, 320, "Loading.")
        self.loading.options(fontName = "assets/MYRIADPRO.otf", fontSize = 30, color = (0,0,0))
        
        self.tick = 0
        self.labelGroup.add(self.loading)
        
    def update(self):
        self.tick += 1
        
        # Slowly add dots to show loading.
        if (self.tick % 60) == 0:
            self.loading.text = "Loading"
        elif (self.tick % 20) == 0:
            self.loading.text = self.loading.text + "."
        
        # After enough frames, switch to main screen.
        if self.tick >= 120:
            self.ChangeScreen("main")
            