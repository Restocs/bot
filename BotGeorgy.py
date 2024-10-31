ROCK = 1  # Камень
PAPER = 2  # Бумага
SCISSORS = 3  # Ножницы


class Bot:
    # Глобальные переменные для хранения статистики
    opponent_choices = [0, 0, 0, 0, 0]
    rock_count = 0
    paper_count = 0
    scissors_count = 0
    count = 0
    move = 1  # Начинаем с камня


    def win(count: int) -> int:
        current_move = (count % 3) + 2
        if current_move % 4 == 0:
            current_move = 1

        return current_move


    def lose() -> int:
        global rock_count, paper_count, scissors_count, opponent_choices
        # Подсчет выбора противника за последние 5 игр
        for choice in opponent_choices[-5:]:
            if choice == ROCK:
                rock_count += 1
            elif choice == PAPER:
                paper_count += 1
            elif choice == SCISSORS:
                scissors_count += 1

        # Определение наиболее часто выбираемой фигуры противника
        if rock_count >= paper_count and rock_count >= scissors_count:
            most_common_choice = ROCK
        elif paper_count >= rock_count and paper_count >= scissors_count:
            most_common_choice = PAPER
        else:
            most_common_choice = SCISSORS

    # Сброс статистики для следующего раунда
        rock_count = 0
        paper_count = 0
        scissors_count = 0

    # Выбор фигуры, которая победит наиболее частую фигуру противника
        if most_common_choice == ROCK:
            return PAPER
        elif most_common_choice == PAPER:
            return SCISSORS
        else:  # most_common_choice == SCISSORS
            return ROCK


    def choose(self, previous_opponent_choice: int) -> int:
        global move, count, opponent_choices

        if previous_opponent_choice != 0:
            opponent_choices[count % 5] = previous_opponent_choice
            count += 1

        if previous_opponent_choice == ROCK:
            if move == PAPER:
                move = self.win(count)
            else:
                move = self.lose()
        elif previous_opponent_choice == PAPER:
            if move == SCISSORS:
                move = self.win(count)
            else:
                move = self.lose()
        else:
            if move == ROCK:
                move = self.win(count)
            else:
                move = self.lose()

        return move 
