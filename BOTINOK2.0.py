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
        self.pattern_counter = Counter()
        self.trend_counter = Counter()
        self.total_sets = 0
        self.wins_needed = 0

    def set_parameters(self, set_count: int, wins_per_set: int) -> None:
        self.total_sets = set_count
        self.wins_needed = wins_per_set

    def on_game_start(self) -> None:
        self.opponent_history.clear()
        self.move_counter.clear()
        self.transition_counter.clear()
        self.pattern_counter.clear()
        self.trend_counter.clear()

    def choose(self, previous_opponent_choice: int) -> int:
        # Обновление истории и частоты переходов
        if previous_opponent_choice != 0:
            self.opponent_history.append(previous_opponent_choice)
            self.move_counter.update([previous_opponent_choice])

            if len(self.opponent_history) > 1:
                prev_move = self.opponent_history[-2]
                self.transition_counter[prev_move][previous_opponent_choice] += 1

            # Обновление паттернов
            if len(self.opponent_history) > 2:
                pattern = tuple(self.opponent_history[-3:])  # Последние три хода
                self.pattern_counter[pattern] += 1

            # Обновление трендов
            if len(self.opponent_history) > 3:
                trend = tuple(self.opponent_history[-4:])  # Последние четыре хода
                self.trend_counter[trend] += 1

        # Применение предсказания, если данных уже достаточно
        if len(self.opponent_history) < 2:
            return ROCK  # Начинаем с камня

        predicted_move = self.predict_opponent_move()
        return self.counter_move(predicted_move)

    def predict_opponent_move(self) -> int:
        last_move = self.opponent_history[-1]
        
        # 1. Предсказание на основе переходов
        if last_move in self.transition_counter:
            transition_weights = self.transition_counter[last_move]
            if transition_weights:
                next_move = max(transition_weights, key=lambda x: transition_weights[x])
                return next_move

        # 2. Анализ паттернов
        if len(self.opponent_history) > 3:
            recent_pattern = tuple(self.opponent_history[-3:])
            if recent_pattern in self.pattern_counter:
                most_common_pattern = self.pattern_counter.most_common(1)[0][0]
                next_move = self.counter_move(most_common_pattern[-1])
                return next_move

        # 3. Анализ трендов
        if len(self.opponent_history) > 4:
            recent_trend = tuple(self.opponent_history[-4:])
            if recent_trend in self.trend_counter:
                most_common_trend = self.trend_counter.most_common(1)[0][0]
                next_move = self.counter_move(most_common_trend[-1])
                return next_move

        # 4. Используем общий частотный анализ
        weighted_moves = Counter()
        weight = 1.0
        decay = 0.8
        for move in reversed(self.opponent_history[-10:]):  # Последние 10 ходов
            weighted_moves[move] += weight
            weight *= decay

        # 5. Выбор наиболее вероятного хода
        return max(weighted_moves, key=weighted_moves.get)

    def counter_move(self, move: int) -> int:
        # Определяем контр-ход
        return {ROCK: PAPER, PAPER: SCISSORS, SCISSORS: ROCK}[move]

    def on_game_end(self) -> None:
        self.opponent_history.clear()
        self.move_counter.clear()
        self.transition_counter.clear()
        self.pattern_counter.clear()
        self.trend_counter.clear()
