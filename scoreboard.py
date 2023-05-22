from turtle import Screen
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    '''A class to report scoring information'''

    def __init__ (self, ai_game):
        '''Initialize score keeping attributes'''
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = 0, self. screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Font settings for scoring information
        self.text_color = (208, 254, 180)
        self.font = pygame.font.SysFont(None, 45)

        # Prepare initial score boards
        self.prep_level()
        self.prep_score()
        self.prep_high_score()
        self.prep_ships()

    def prep_level(self):
        '''Turn lvl into rendered image'''
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        self.restart_info = pygame.image.load('_IMGS/button_restart.png')
        self.restart_info_rec = self.screen.get_rect().width -318, 38

        # Position level right of the restart info
        self.level_rect = self.level_image.get_rect()
        self.level_x1 = 70
        self.level_x2 = self.restart_info.get_rect().width + 38
        self.level_rect.left = self.level_x1 + self.level_x2
        self.level_rect.top = 45

    def prep_score(self):
        '''Turn the score into a rendered image'''
        rounded_score = round(self.stats.score, -1)
        score_str = "{:}".format(rounded_score)

        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score to the right of the level
        
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.level_rect.right + 38
        self.score_rect.top = 45

    def show_score(self):
        '''Draw scores. ships and lvl to screen'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def prep_high_score(self):
        '''Turn the highscore into a rendered image'''
        high_score = round(self.stats.high_score, -1)
        high_score_str = "{:}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        # Display the high score to the left of the quit info

        self.quit_info = pygame.image.load('_IMGS/button_quit.png')
        self.quit_info_rec = self.screen.get_rect().width -318, 38

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect_x1 = self.screen.get_rect().width -318
        self.high_score_rect_x2 = 38
        self.high_score_rect.right = self.high_score_rect_x1 - self.high_score_rect_x2
        self.high_score_rect.top = 45

    def check_high_score(self):
        '''Check to see if there is a new high score'''
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def prep_ships(self):
        '''Show how many ships are left'''
        self.ships = Group()
        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship_rect_x1 = self.screen.get_rect().width // 2 
            ship_rect_x2 = ship_number * ship.rect.width 
            ship.rect.x = ship_rect_x1 - ship_rect_x2
            ship.rect.y = 10
            self.ships.add(ship)

            