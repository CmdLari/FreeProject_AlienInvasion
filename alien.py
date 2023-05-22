import pygame
import random
from pygame.sprite import Sprite

class Alien(Sprite):
    '''Represents a single alien in the fleet'''

    def __init__(self, ai_game):
        '''Initialize the alien and set its starting position'''
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        # Load the alien image and set its rect attribute
        rnd_alien = random.choice(['_IMGS/alien.png', '_IMGS/alien2.png', '_IMGS/alien3.png', '_IMGS/alien4.png'])
        self.image = pygame.image.load(rnd_alien)
        self.rect = self.image.get_rect()

        # Start each new alien near the top left of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position
        self.x = float(self.rect.x)

    def check_edges(self):
        '''Return True if alien hit the edge of the screen'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        '''Move the alien ship to the right or left'''
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
