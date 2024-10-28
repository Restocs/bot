from random import randint, choices

class Bot():
    def calculate_probabilities(self, P_A, P_B_given_A, P_B):
        return (P_B_given_A * P_A) / P_B
    
    def is_win(self, self_choice, opponent_choice):
        winning_moves = {
            0: 2,  # Камень побеждает ножницы
            1: 0,  # Бумага побеждает камень
            2: 1   # Ножницы побеждают бумагу
        }
        return winning_moves[self_choice] == opponent_choice

    def set_parameters(self, set_count: int, wins_per_set: int) -> None:
        pass


    def on_game_start(self) -> None:
        self.req = {
            0: 1,  # Камень
            1: 2,  # Бумага
            2: 3  # Ножницы
        }

        self.probability = [0, 0, 0] # list for op probs 

        self.count_op = [0, 0, 0] # count op moves
        self.count_me = [0, 0, 0] # count my moves

        self.chance_op = [0, 0, 0] # list for op prob 
        self.chance_me = [0, 0, 0] # list for my prob 

        self.wins_op = [0, 0, 0] # list for op wins 
        self.wins_me = [0, 0, 0] # list for my wins 

        self.lap = 0 # count laps and moves litrly

        self.previousSelfChoice = 1


    def choose(self, previous_opponent_choice: int) -> int:
        previous_opponent_choice -= 1

        if not(previous_opponent_choice in [0, 1, 2]):
            # print("prefirst step")
            return self.previousSelfChoice

        if self.is_win(self.previousSelfChoice, previous_opponent_choice):
            self.wins_me[self.previousSelfChoice] += 1
        else:
            self.wins_op[previous_opponent_choice] += 1
    
        self.lap += 1

        # print(f"{self.lap}: {self.req[self.previousSelfChoice]}/{self.req[previous_opponent_choice]} | {self.is_win(self.previousSelfChoice, previous_opponent_choice)}   {self.probability}")

        self.count_op[previous_opponent_choice] += 1
        self.count_me[self.previousSelfChoice] += 1

        for i in range(3):
            self.probability[i] = self.calculate_probabilities(self.count_op[i] / self.lap, self.wins_op[i] / sum(self.wins_op) if sum(self.wins_op) > 0 else 1 / 3, sum(self.count_op) / self.lap if self.lap > 0 else 1.0)

        res = choices([0, 1, 2], weights=self.probability)[0]
        self.previousSelfChoice = res
        return self.req[res]


    def on_game_end(self) -> None:
        print(f"Процент побед: {sum(self.wins_me) / (sum(self.wins_op) + sum(self.wins_me)) * 100:.2f}%")


if __name__ == "__main__":
    raunds = 500
    sets = 10

    bot1 = Bot()
    bot1.on_game_start()

    for i in range (0, sets):
        bot1.choose(52)
        
        for j in range (0, raunds):
            bot1.choose(randint(1, 3))
            
        bot1.on_game_end()
