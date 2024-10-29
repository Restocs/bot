import random

# Константы
ROCK = 1    # Камень
PAPER = 2   # Бумага
SCISSORS = 3  # Ножницы

class Bot:
	def __init__(self):
		self.opponent_history = []  # История ходов противника
		self.move_count = {ROCK: 0, PAPER: 0, SCISSORS: 0}  # Подсчет ходов противника
		self.last_move = None  # Последний ход бота

	def set_parameters(self, set_count: int, wins_per_set: int) -> None:
		pass

	def on_game_start(self) -> None:
		# Инициализация перед началом игры
		self.opponent_history = []
		self.move_count = {ROCK: 0, PAPER: 0, SCISSORS: 0}  # Сброс счетчиков ходов
		self.last_move = None

	def choose(self, previous_opponent_choice: int) -> int:
		# Добавляем предыдущий ход противника в историю
		if previous_opponent_choice:
			self.opponent_history.append(previous_opponent_choice)
			self.move_count[previous_opponent_choice] += 1  # Увеличиваем счетчик для данного хода противника
		        
		# Предсказать следующий ход противника
		likely_opponent_move = self.predict_opponent_move()
		        
		# Выбор хода, который побеждает предсказанный ход противника
		bot_move = self.get_best_move(likely_opponent_move)
		
		# Запоминаем последний ход бота
		self.last_move = bot_move
		return bot_move

	def predict_opponent_move(self):
		# Определяем самый частый ход противника
		total_moves = sum(self.move_count.values())
		if total_moves == 0:
			return random.choice([ROCK, PAPER, SCISSORS])  # Если нет истории, выбираем случайно
		        
		# Определяем наиболее вероятный ход противника
		predicted_move = max(self.move_count, key=self.move_count.get)
		return predicted_move

	def get_best_move(self, opponent_move):
		# Выбор лучшего ответа на ход противника
		if opponent_move == ROCK:
			return PAPER  # Бумага бьет камень
		elif opponent_move == PAPER:
			return SCISSORS  # Ножницы бьют бумагу
		elif opponent_move == SCISSORS:
			return ROCK  # Камень бьет ножницы
		else:
			return random.choice([ROCK, PAPER, SCISSORS])  # На всякий случай

	def on_game_end(self) -> None:
		# Завершение игры
		print("Игра закончена!")
		#print("Ходы противника:", self.opponent_history)