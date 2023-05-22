import pygame
from pygame.locals import *
from settings import Settings

class Background:
    '''Manages the scrolling background and the menu background'''

    def __init__(self, ai_game):

        self.screensurf = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        self.width = self.screensurf.get_rect().width
        self.height = self.screensurf.get_rect().height

        self.bg_img = pygame.image.load('_IMGS/bg.png')
        self.bg_img = pygame.transform.scale(self.bg_img,(self.width,self.height))
        
        self.i = 0

        self.bg_img_y1 = 0
        self.bg_img_x1 = 0

    def simpler_bg(self):
        self.screensurf.blit(self.bg_img, (self.bg_img_x1, self.bg_img_y1))


    def ingame_bg(self):
         
        self.screensurf.fill((0,0,0))
        self.screensurf.blit(self.bg_img,(0,self.i))
        self.screensurf.blit(self.bg_img,(0, self.i-self.height))
        if (self.i==+self.height):
            self.screensurf.blit(self.bg_img,(0, self.i-self.height))
            self.i=0
        self.i+=1.5





    