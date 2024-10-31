from collections import Counter, defaultdict

ROCK = 1  # Камень
PAPER = 2  # Бумага
SCISSORS = 3  # Ножницы
MOVES = [ROCK, PAPER, SCISSORS]

class Bot:
    def __init__(self):
        self.opponent_history = []
        self.move_counter = Counter()
        self.transition_counter = defaultdict(Counter)
        self.total_sets = 0
        self.wins_needed = 0

    def set_parameters(self, set_count: int, wins_per_set: int) -> None:
        self.total_sets = set_count
        self.wins_needed = wins_per_set

    def on_game_start(self) -> None:
        self.opponent_history.clear()
        self.move_counter.clear()
        self.transition_counter.clear()

    def choose(self, previous_opponent_choice: int) -> int:
        # Обновление истории и частоты переходов
        if previous_opponent_choice != 0:
            self.opponent_history.append(previous_opponent_choice)
            self.move_counter.update([previous_opponent_choice])

            if len(self.opponent_history) > 1:
                prev_move = self.opponent_history[-2]
                self.transition_counter[prev_move][previous_opponent_choice] += 1

        # Применение предсказания, если данных уже достаточно
        if len(self.opponent_history) < 2:
            return ROCK 

        predicted_move = self.predict_opponent_move()
        return self.counter_move(predicted_move)

    def predict_opponent_move(self) -> int:
        last_move = self.opponent_history[-1]
        
        # 1. Предсказание на основе переходов с экспоненциальным сглаживанием
        if last_move in self.transition_counter:
            transition_weights = self.transition_counter[last_move]
            if transition_weights:
                next_move = max(transition_weights, key=lambda x: transition_weights[x])
                return next_move

        # 2. Используем общий частотный анализ с учетом веса последних 5 ходов
        weighted_moves = Counter()
        weight = 1.0
        decay = 0.8
        for move in reversed(self.opponent_history[-5:]):  # Последние 5 ходов с весом
            weighted_moves[move] += weight
            weight *= decay

        most_probable_move = max(weighted_moves, key=weighted_moves.get)
        return next_move

    def counter_move(self, move: int) -> int:
        # Вероятностный выбор контр-хода
        if move == ROCK:
            return PAPER
        elif move == PAPER:
            return SCISSORS
        else:
            return ROCK

    def on_game_end(self) -> None:
        self.opponent_history.clear()
        self.move_counter.clear()
        self.transition_counter.clear()