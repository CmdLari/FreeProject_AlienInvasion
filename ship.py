import pygame
import random
from pygame.sprite import Sprite

class Ship(Sprite):
    '''manages the ship'''

    def __init__(self, ai_game):
        '''starts ship and it's position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # Load ship image and get its rect
        self.image = pygame.image.load('_IMGS/playership.png')
        self.rect = self.image.get_rect()

        # each new ship start at bottom centre
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # Movement 
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Update the ship's position according to the movement flag'''
        # Update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        '''Draw ship at current position'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        '''Center the ship on the bottom screen'''
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)