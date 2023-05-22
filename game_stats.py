import json

class GameStats:
    '''Track stats for Return to the stars'''

    def __init__(self, ai_game):
        '''Initialize game stats'''
        self.settings = ai_game.settings
        self.reset_stats()

        # Start game in inactive state
        self.game_active = False

        # # Start Alien Invasion in active state
        # self.game_active = True

        # Highscore should never be reset

        with open('highscore.json') as openhighsc:
            json_hs = int(json.load(openhighsc))
            self.high_score = json_hs

        # self.high_score = 0
        
    def reset_stats(self):
        '''Initialize stats that can change during the game'''
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1