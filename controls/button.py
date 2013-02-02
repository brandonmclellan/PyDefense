'''
Source Name:           button.py
Author:                Brandon McLellan
Last Modified:         August 7th, 2012
Last Modified By:      Brandon McLellan
Description:
    
Revision History:
    Revision 3:
        - Change to allow for dynamic button size and images.
    Revision 2:
        - Added simiplifed collision function.
    Revision 1:
        - Brought code from previous assignment
'''
import pygame
from controls import label

'''
    Button Class
        Allows for a uniform button control throughout my game.
        Does hover effects and splits up the different button images.
'''
class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, text, image="SmallButton.png", fontSize=16):
        pygame.sprite.Sprite.__init__(self)
        
        
        #Load the button-imageset
        buttonSet = pygame.image.load("assets/" + image)
        self.height = buttonSet.get_rect().height / 3
        self.width = buttonSet.get_rect().width
        
        self.rect = pygame.Rect(x, y, self.width, self.height)
        # Setup text label for button.
        self.label = label.Label(self.width / 2, (self.height / 2) - 1, text)
        self.label.fontSize = fontSize
        self.label.bold = True
        self.label.align = label.Label.Center
        self.label.color = (0,0,0)
        self.label.update()       
        
        # Create a surface for each state, blit the proper portion of button and label.
        self.imageUp = pygame.Surface((self.width, self.height))
        self.imageUp.blit(buttonSet, (0, 0), pygame.Rect(0, 0, self.width, self.height))
        self.imageUp.blit(self.label.image, self.label.rect)
        
        self.imageHover = pygame.Surface((self.width, self.height))
        self.imageHover.blit(buttonSet, (0, 0), pygame.Rect(0, self.height, self.width, self.height))
        self.imageHover.blit(self.label.image, self.label.rect)
        
        self.imageDown = pygame.Surface((self.width, self.height))
        self.imageDown.blit(buttonSet, (0, 0), pygame.Rect(0, self.height * 2, self.width, self.height))
        self.imageDown.blit(self.label.image, self.label.rect)

    # Check if the point is within the boundaries of the button
    def collide(self, point):
        return self.rect.collidepoint(point) and self.image == self.imageDown
    
    def update(self):
        #Check if the mouse is hovering or clicking on the mouse
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed() == (1, 0, 0):
                self.image = self.imageDown
            else:
                self.image = self.imageHover
        else:
            self.image = self.imageUp
        
        
        