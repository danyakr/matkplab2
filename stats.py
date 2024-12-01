class GameStats:
    """Отслеживание статистики для игры 'Инопланетное Вторжение'."""

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats() 
        self.game_active = False

    def reset_stats(self):
        self.ships_left = self.ai_settings.ship_limit  # Количество оставшихся жизней (кораблей)
        self.score = 0  # Текущий счет
        self.level = 1  # Текущий уровень игры




