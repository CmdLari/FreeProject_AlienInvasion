import imp
import sys
import time
from time import sleep
import json

import pygame
from pygame.locals import *

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from scoreboard import Scoreboard
from background import Background

class AlienInvasion:
    '''Manages game assets and behaviours'''

    def __init__(self):
        '''Initialize game, create resources'''
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height                  
        pygame.display.set_caption("Back to the Stars")
        
        # Create an instance to store game stats
        # -- Create a score board
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.background = Background(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the play button
        self.play_button = Button(self, "PLAY")

    def run_game(self):
        '''Main loop for the game'''


        if not self.stats.game_active:
            self.menusound = pygame.mixer.Sound('_MUS/Patek_Dripchord.wav')
            pygame.mixer.Sound.play(self.menusound, loops=-1)

        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def _check_events (self):
        '''Respond to keypresses and mouse events'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        '''Start a new game when the player clicks Play'''
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            
            pygame.mixer.Sound.stop(self.menusound)

            self.gamesound = pygame.mixer.Sound('_MUS/Spinning_Dripchord.wav')
            pygame.mixer.Sound.play(self.gamesound, loops=-1)

            self.startsound = pygame.mixer.Sound('_MUS/start.wav')
            pygame.mixer.Sound.play(self.startsound)

            # Reset game settings
            self.settings.initialize_dynamic_settings()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)

            # Reset the game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            # Create a new fleet and center ship
            self._create_fleet()
            self.ship.center_ship()
        

    def _check_keydown_events(self, event):
        '''Respond to keypresses'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:

            # Dump high score in json file
            with open("highscore.json", "w") as outfile:
                outfile.write(str(self.stats.high_score))

            # Credits
            self.screen.fill((5, 0, 16))

            self.thankyou_image = pygame.image.load("_IMGS/thankyou.png")
            self.thankyou_rect = self.thankyou_image.get_rect()
            self.thankyou_rect.center = self.screen.get_rect().center

            self.screen.blit(self.thankyou_image, self.thankyou_rect)

            pygame.display.flip()
            sleep(5)

            # Exit
            sys.exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_r:
            self.stats.game_active = False
            pygame.mixer.Sound.stop(self.gamesound)
            self.menusound = pygame.mixer.Sound('_MUS/Patek_Dripchord.wav')
            pygame.mixer.Sound.play(self.menusound, loops=-1)


    def _check_keyup_events(self, event):
        '''Respond to key releases'''
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
      
    def _fire_bullet(self):
        '''Create a new bullet and add it to the bullets group'''
        if len(self.bullets) < self.settings.bullets_allowed:
            if self.stats.game_active:
                self.shiphitsound = pygame.mixer.Sound('_MUS/shot.wav')
                pygame.mixer.Sound.play(self.shiphitsound)
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        '''Update the position of bullets and get rid of old bullets'''
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        '''Respond to bullet-alien collisions'''
        # Remove any bullets and aliens that have colided
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        
        if collisions:
            self.shiphitsound = pygame.mixer.Sound('_MUS/alienhit.wav')
            pygame.mixer.Sound.play(self.shiphitsound)
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)    
            self.sb.prep_score()
            self.sb.check_high_score()


        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self):
        '''Create the fleet of aliens'''
        # Make an alien and find number of aliens in a row
        # Spacing between one alien is the width of one alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_alien_x = available_space_x // (1 * alien_width)

        # Determine the number of rows of aliens that fit on the screen
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (2 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the fleet of aliens
        for row_number in range(number_rows):
            for alien_number in range(number_alien_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        '''Create an alien and place it in the row'''
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 1 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = float(alien.rect.height) + 1 * float(alien.rect.height) * row_number
        self.aliens.add(alien)

    def _check_fleet_edges(self):
        '''Respond appropriatly if any aliens hit the edge'''
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        '''Drop the entire fleet and change its direction'''
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        '''Check if the fleet is at an edge, then update the positions of all aliens in the fleet'''
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting rock bottom
        self._check_aliens_bottom()

    def _ship_hit(self):
        '''Respond to ship being hit by an alien'''
        self.shiphitsound = pygame.mixer.Sound('_MUS/shiphit.wav')
        pygame.mixer.Sound.play(self.shiphitsound)


        if self.stats.ships_left > 0:
            # Decrement ships left, and update scoreboard
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()
            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()
            # Pause
            sleep(0.5)
            if self.stats.ships_left == 0:
                self.shiphitsound = pygame.mixer.Sound('_MUS/fail.wav')
                pygame.mixer.Sound.play(self.shiphitsound)
                pygame.mixer.Sound.stop(self.gamesound)
                self.stats.game_active = False
                pygame.mouse.set_visible(True)
                pygame.mixer.Sound.play(self.menusound, loops=-1)
                
        else:
            self.stats.game_active = False

    def _check_aliens_bottom(self):
        '''Check if aliens have reached the bottom of the screen'''
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # Same reaction as if the alien hits the ship
                self._ship_hit()
                break

    def _update_screen(self):
        '''Update images on screen and flip to new screen'''

        if not self.stats.game_active:
            self.background.simpler_bg()

        if self.stats.game_active:
            self.background.ingame_bg()

        # Draw ship to screen            
        self.ship.blitme()        
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # Draw score to screen
        self.sb.show_score()

        # Make the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

            # Get a Fake Start Button
            self.button_img = pygame.image.load('_IMGS/button.png')
            self.button_rec_posx = self.screen.get_rect().width //2 -60
            self.button_rec_posy = self.screen.get_rect().height //2 -30
            self.button_rec = self.button_rec_posx, self.button_rec_posy
            self.screen.blit(self.button_img, self.button_rec)

        # Restart info
        self.restart_info = pygame.image.load('_IMGS/button_restart.png')
        self.restart_info_rec = 38, 38
        self.screen.blit (self.restart_info, self.restart_info_rec)

        # Quit Info
        self.quit_info = pygame.image.load('_IMGS/button_quit.png')
        self.quit_info_rec = self.screen.get_rect().width -318, 38
        self.screen.blit (self.quit_info, self.quit_info_rec)

        # Change Mouse
        pygame.mouse.set_visible(False)
        if self.stats.game_active == False:
            self.settings.cursor_img_rect.center = pygame.mouse.get_pos()
            self.screen.blit (self.settings.cursor_img, self.settings.cursor_img_rect)

        pygame.display.flip()

               
if __name__ == '__main__':
    # Make a game instance and run the game
    ai = AlienInvasion()
    ai.run_game()