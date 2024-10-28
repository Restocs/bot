from random import randint

ROCK = 1  # Камень
PAPER = 2  # Бумага
SCISSORS = 3  # Ножницы
MOVES = [ROCK, PAPER, SCISSORS]

class Bot:
  def __init__(self):
    self.total_sets = 0
    self.wins_needed = 0
  def set_parameters(self, set_count: int, wins_per_set: int) -> None:
    self.total_sets = set_count
    self.wins_needed = wins_per_set
    
  def on_game_start(self) -> None:
    pass
        
  def choose(self, previous_opponent_choice) -> int:
    return randint(1,3)
  
  def on_game_end(self) -> None:
    pass