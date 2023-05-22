
from ctypes import pointer
import pygame
from pygame.locals import *
from button import Button


class Settings:
    '''All settings for alien invasion are stored here'''

    def __init__(self):
        '''intitialize game settings'''
        # Screen settings
        self.screen_width = 1920
        self.screen_height = 1080
        self.bg_color = (5, 0, 16)
                    
        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        # self.bullet_width = 5
        # self.bullet_height = 15
        # self.bullet_color = (255, 100, 200)
        self.bullets_allowed = 4
    
        # Alien settings
        self.fleet_drop_speed = 10

        # Speedup settings
        self.speedup_scale = 1.5

        # How quickly the points increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()
       
        # Change cursor
        self.cursor_img = pygame.image.load('_IMGS/cursor.png')
        self.cursor_img_rect = self.cursor_img.get_rect()

    def initialize_dynamic_settings(self):
        '''Initialize settings that change throughout the game'''
        self.ship_speed = 10
        self.bullet_speed = 6
        self.alien_speed = 8

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50
    
    def increase_speed(self):
        '''Increase speed settings and alien point values'''
        # self.ship_speed *= self.speedup_scale
        # self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
