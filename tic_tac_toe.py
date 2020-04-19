import numpy as np
import matplotlib.pyplot as plt

LENGTH = 3


class Agent:
    def __init__(self, eps=0.1, alpha=0.5):
        self.eps = eps
        self.alpha = alpha
        self.verbose = False
        self.state_history = []

    def setV(self, V):
        self.V = V

    def set_symbol(self, sym):
        self.sym = sym

    def set_verbose(self,v):
        self.verbose = v

    def reset_history(self):
        self.state_history = []

    def take_action(self,env):
        r = np.random.rand()
        best_state = None
        if r < self.eps:
            if self.verbose:
                print("Taking a random action")
            possible_moves = []
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i, j):
                        possible_moves.append((i, j))
            idx = np.random.choice(len(possible_moves))
            next_move = possible_moves[idx]
        else:
            pos2value = {}
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i, j):
                        env.board[i, j] = self.sym
                        state = env.get_state()
                        env.board[i, j] = 0
                        pos2value[(i, j)] = self.V[state]
                        if self.V[state] > best_value:
                            best_value = self.V[state]
                            best_state = state
                            next_move = (i, j)
            if self.verbose:
                print("Taking a greedy action")
                for i in range(LENGTH):
                    print("------------------")
                    for j in range(LENGTH):
                        if env.is_empty(i, j):
                            # print the value
                            print(" %.2f|" % pos2value[(i, j)], end="")
                        else:
                            print("  ", end="")
                            if env.board[i, j] == env.x:
                                print("x  |", end="")
                            elif env.board[i, j] == env.o:
                                print("o  |", end="")
                            else:
                                print("   |", end="")
                    print("")
                print("------------------")

                # make the move
            env.board[next_move[0], next_move[1]] = self.sym

    def update_state_history(self, s):
        self.state_history.append(s)

    def update(self, env):
        reward = env.reward(self.sym)
        target = reward
        for prev in reversed(self.state_history):
            value = self.V[prev] + self.alpha * (target - self.V[prev])
            self.V[prev] = value
            target = value
        self.reset_history()


class Environment:
    def __init__(self):
        self.board = np.zeros((LENGTH,LENGTH))
        self.x = -1
        self.o = 1
        self.winner = None
        self.ended = False
        self.num_states = 3**(LENGTH*LENGTH)

    def is_empty(self, i, j):
        return self.board[i,j] == 0

    def reward(self, sym):
        if not self.game_over():
            return 0
        return 1 if self.winner == sym else 0

    def get_state(self):
        k = 0
        h = 0
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.board[i, j] == 0:
                    v = 0
                elif self.board[i, j] == self.x:
                    v = 1
                elif self.board[i, j] == self.o:
                    v = 2
                h += (3 ** k) * v
                k += 1
        return h

    def game_over(self, force_recalculate=False):
        if not force_recalculate and self.ended:
            return self.ended

        for i in range(LENGTH):
            for player in (self.x, self.o):
                if self.board[i].sum() == player * LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

            # check columns
            for j in range(LENGTH):
                for player in (self.x, self.o):
                    if self.board[:, j].sum() == player * LENGTH:
                        self.winner = player
                        self.ended = True
                        return True

            # check diagonals
            for player in (self.x, self.o):
                # top-left -> bottom-right diagonal
                if self.board.trace() == player * LENGTH:
                    self.winner = player
                    self.ended = True
                    return True
                # top-right -> bottom-left diagonal
                if np.fliplr(self.board).trace() == player * LENGTH:
                    self.winner = player
                    self.ended = True
                    return True

            # check if draw
            if np.all((self.board == 0) == False):
                # winner stays None
                self.winner = None
                self.ended = True
                return True

            # game is not over
            self.winner = None
            return False

    def is_draw(self):
        return self.ended and self.winner is None

    def draw_board(self):
        for i in range(LENGTH):
            print("-------------")
            for j in range(LENGTH):
                print("  ", end="")
                if self.board[i, j] == self.x:
                    print("x ", end="")
                elif self.board[i, j] == self.o:
                    print("o ", end="")
                else:
                    print("  ", end="")
            print("")
        print("-------------")


class Human:
    def __init__(self):
        pass

    def set_symbol(self, sym):
        self.sym = sym

    def take_action(self,env):
        while True:
            # break if we make a legal move
            move = input("Enter coordinates i,j for your next move (i,j=0..2): ")
            i, j = move.split(',')
            i = int(i)
            j = int(j)
            if env.is_empty(i, j):
                env.board[i, j] = self.sym
                break

    def update(self, env):
        pass

    def update_state_history(self, s):
        pass


