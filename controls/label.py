'''
Source Name:           label.py
Author:                Brandon McLellan
Last Modified:         August 7th, 2012
Last Modified By:      Brandon McLellan
Description:
    
Revision History:
    Revision 3:
        - Added easy way of mass-updating options.
    Revision 2:
        - Overhauled label options
    Revision 1:
        - Brought label class in from previous assignment.
'''
import pygame


'''
    Label Class
        Provides a easy, uniform way to place text in my game.
'''
class Label(pygame.sprite.Sprite):
    Left = 0
    Center = 1
    Right = 2
    
    def __init__(self, x, y, text):
        pygame.sprite.Sprite.__init__(self)
        
        # Basic label options
        self.x = x
        self.y = y
        self.color = (255,255,255)
        self.text = text

        # Font options
        self.fontSize = 12
        self.fontName = "Tahoma"
        self.bold = False
        self.underlined = False
        self.italic = False
        
        self.align = Label.Left
        
    #Allows for easy mass-option changes.
    def options(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
        
    def update(self):
        #Setup font with proper values for rendering
        font = pygame.font.SysFont(self.fontName, self.fontSize)
        font.set_underline(self.underlined)
        font.set_bold(self.bold)
        font.set_italic(self.italic)
        
        #Render text
        self.image = font.render(str(self.text), True, self.color)
        self.rect = self.image.get_rect()       
    
        # Determine label position based on alignment
        if self.align == Label.Left:
            self.rect.x = self.x
            self.rect.y = self.y
        elif self.align == Label.Center:
            self.rect.centerx = self.x
            self.rect.centery = self.y
        elif self.align == Label.Right:
            self.rect.right = self.x
            self.rect.y = self.y
        
            