import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''manages bullets fired from ship'''

    def __init__(self, ai_game):
        '''Create a bullet at ship's current position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        # self.color = self.settings.bullet_color
        self.image = pygame.image.load('_IMGS/bullet.png')

        # Create a bullet rect at (0, 0) and then set correct position
        self.rect = self.image.get_rect()
        self.rect.midtop = ai_game.ship.rect.midtop

        # Store the bullet's position as a decimal value
        self.y = float(self.rect.y)

    def update(self):
        '''Move the bullet up the screen'''
        # Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

    def draw_bullet(self):
        '''Draw the bullet to the screen'''
        # pygame.draw.rect(self.screen, self.color, self.rect)
        self.screen.blit(self.image, self.rect)