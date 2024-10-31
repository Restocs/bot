import random

# Константы
ROCK = 1  # Камень
PAPER = 2  # Бумага
SCISSORS = 3  # Ножницы

# Переменные для анализа
# opponent_history = []
# bot_history = []
# weights = {ROCK: 1.0, PAPER: 1.0, SCISSORS: 1.0}
# move_count = {ROCK: 0, PAPER: 0, SCISSORS: 0}
# last_move = None

class Bot:
	
	def __init__(self):
		self.opponent_history = []
		self.bot_history = []
		self.weights = {ROCK: 1.0, PAPER: 1.0, SCISSORS: 1.0}
		self.move_count = {ROCK: 0, PAPER: 0, SCISSORS: 0}
		self.last_move = None
	
	def set_parameters(self, set_count: int, wins_per_set: int) -> None:
		"""
		Устанавливает параметры игры.
		"""
		#print(f"Играем до {set_count} сетов. Для победы в каждом сете нужно {wins_per_set} побед.")

	def on_game_start(self) -> None:
		"""
		Инициализация бота в начале игры.
		"""
		#global opponent_history, bot_history, weights, move_count, last_move
		self.opponent_history = []
		self.bot_history = []
		self.weights = {ROCK: 1.0, PAPER: 1.0, SCISSORS: 1.0}
		self.move_count = {ROCK: 0, PAPER: 0, SCISSORS: 0}
		self.last_move = None
		#print("Игра началась!")

	def choose(self, previous_opponent_choice: int) -> int:
		"""
		Выбирает ход бота, основываясь на предыдущих ходах.
		"""
		#global last_move
		
		if previous_opponent_choice:
			self.opponent_history.append(previous_opponent_choice)
		
		# Обновляем веса ходов для адаптации
		if self.last_move and previous_opponent_choice:
			self.update_weights(self.last_move, previous_opponent_choice)
		
		# Определяем вероятный ход противника на основе предыдущих
		if self.opponent_history:
			self.likely_opponent_move = self.predict_opponent_move()
		else:
			self.likely_opponent_move = random.choice([ROCK, PAPER, SCISSORS])
		
		# Выбираем ход, который побеждает вероятный ход противника
		if self.likely_opponent_move == ROCK:
			self.bot_move = PAPER
		elif self.likely_opponent_move == PAPER:
			self.bot_move = SCISSORS
		else:
			self.bot_move = ROCK
		
		# Записываем ход бота для анализа
		self.bot_history.append(self.bot_move)
		self.last_move = self.bot_move
		return self.bot_move

	def update_weights(self, bot_move, opponent_move):
		"""
		Обновляет веса на основе результата предыдущего хода.
		"""
		# Если победили, увеличиваем вес текущего хода
		if (bot_move == ROCK and opponent_move == SCISSORS) or \
			(bot_move == PAPER and opponent_move == ROCK) or \
			(bot_move == SCISSORS and opponent_move == PAPER):
			self.weights[bot_move] *= 1.1
		# Если проиграли, уменьшаем вес
		elif (bot_move == ROCK and opponent_move == PAPER) or \
			(bot_move == PAPER and opponent_move == SCISSORS) or \
			(bot_move == SCISSORS and opponent_move == ROCK):
			self.weights[bot_move] *= 0.9

	def predict_opponent_move(self):
		"""
		Предсказывает следующий ход противника на основе его предыдущих.
		"""
		# Определяем самый частый ход противника
		self.total_moves = sum(self.move_count.values())
		if self.total_moves > 0:
			# Нормализуем веса для каждого хода
			self.move_weights = {self.move: self.count / self.total_moves for self.move, self.count in self.move_count.items()}
			self.likely_move = max(self.move_weights, key=self.move_weights.get)
		else:
			# В случае, если нет истории, выбираем случайный ход
			self.likely_move = random.choice([ROCK, PAPER, SCISSORS])
		return self.likely_move

	def on_game_end(self) -> None:
		"""
		Завершение игры и вывод статистики.
		"""
		print("Игра закончена!")
		#print("Ходы противника:", self.opponent_history)
		#print("Ходы бота:", self.bot_history)
		#print("Окончательные веса:", weights)
