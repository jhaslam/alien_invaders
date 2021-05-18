from settings import Settings


class GameStats():
    def __init__(self, ai_settings: Settings) -> None:
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = True
        self.game_paused = False
    
    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit
        