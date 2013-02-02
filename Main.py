'''
Source Name:           Main.py
Author:                Brandon McLellan
Last Modified:         August 7th, 2012
Last Modified By:      Brandon McLellan
Description:
    Handles initializing pygame and the main game loop.
Revision History:
    Revision 3:
        - Added end screen
    Revision 2:
        - Merged code from engine.py into Main.py
    Revision 1:
        - Base main function shell
'''
import pygame
from towerDefense.screens import screen, mainScreen, gameScreen, endScreen, splashScreen

def main():
    #Setup pygame
    pygame.init()
    surface = pygame.display.set_mode((640, 480))  
    pygame.display.set_caption("PyDefense")

    pygame.mixer.init()
    
    clock = pygame.time.Clock()

    backgroundMusic = pygame.mixer.Sound("assets/sounds/background.ogg")
    backgroundMusic.play(-1)
    
    #Load the game screens.
    splashScreen.SplashScreen()
    mainScreen.MainScreen()
    gameScreen.GameScreen()
    endScreen.EndScreen()
    
    #Main game loop
    keepGoing = True
    while keepGoing:
        clock.tick(30)
        for event in pygame.event.get():
            if not screen.Screen.Event(event):
                keepGoing = False
            if event.type == pygame.QUIT:
                keepGoing = False
            
        screen.Screen.Update(surface)
        
        pygame.display.flip()
    
if __name__ == '__main__':
    main()
    