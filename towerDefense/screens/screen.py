'''
Source Name:           screen.py
Author:                Brandon McLellan
Last Modified:         August 7th, 2012
Last Modified By:      Brandon McLellan
Description:
    Base screen class, handles drawing buttons and labels.
Revision History:
    Revision 3:
        - Added ability to pass information between screens.
    Revision 2:
        - Added proper screen changing
    Revision 1:
        - Wrote base screen class
'''
import pygame

'''
    Screen Class
        One the core classes of the game, each screen is a surface
        that is blitted to the screen depending on which one is active.
'''
class Screen(pygame.Surface):
    activeScreen = None
    screenList = dict()
    
    def __init__(self, name):
        pygame.Surface.__init__(self, (640, 480))
        
        self.buttonGroup = pygame.sprite.Group()
        self.labelGroup = pygame.sprite.Group()
        
        self.background = pygame.Surface((640, 480))
        self.background.fill((255,255,255))
        
        # Set screen as active if first one initialized
        if Screen.activeScreen == None:
            Screen.activeScreen = self
            
        # Store screen information in dict so we can switch
        Screen.screenList[name] = self
        
    # Function that passes information to other screens.
    # Usually redefined within a inheriting class
    def init(self, info):
        return True
        
    # Function that handles every event from pygame
    # Usually redefined within a inheriting class
    def event(self, event):
        return True
    
    # Function that handles screen updates and ticks.
    # Usually redefined within a inheriting class
    def update(self):
        return True
        
    # Static function used to change screens
    @staticmethod
    def ChangeScreen(screen, info = None):
        if screen in Screen.screenList:
            Screen.activeScreen = Screen.screenList[screen]
            Screen.activeScreen.init(info)
            return True
        return False
    
    # Static function used to pass events to active screen.
    @staticmethod
    def Event(event):
        if Screen.activeScreen == None:
            return True
        return Screen.activeScreen.event(event)
        
    # Static function used to update the active screen.
    @staticmethod
    def Update(surface):
        if Screen.activeScreen == None:
            return True
        
        Screen.activeScreen.blit(Screen.activeScreen.background, (0,0))
        Screen.activeScreen.update()
        
        # Update the buttons for the active screen
        Screen.activeScreen.buttonGroup.clear(Screen.activeScreen, Screen.activeScreen.background)
        Screen.activeScreen.buttonGroup.update()
        Screen.activeScreen.buttonGroup.draw(Screen.activeScreen)
        
        # Update the labels for the active screen
        Screen.activeScreen.labelGroup.clear(Screen.activeScreen, Screen.activeScreen.background)
        Screen.activeScreen.labelGroup.update()
        Screen.activeScreen.labelGroup.draw(Screen.activeScreen)
        
        
        surface.blit(Screen.activeScreen, (0,0))
        
        