import math
import random
import numpy as np
import tkinter as tk
from tkinter import messagebox

class ConnectFourState:
    def __init__(self):
        self.board = np.zeros((6, 7), dtype=int)
        self.current_player = 1  # Player 1: 1, Player 2: -1
        self._is_terminal = False
        self.reward = 0
        
    def is_terminal(self):
        return self._is_terminal

    def get_legal_actions(self):
        if self.is_draw():
            return []
        return [col for col in range(7) if self.board[0][col] == 0]

    def is_draw(self):
        return all(self.board[0][col] != 0 for col in range(7))


    def perform_action(self, action):
        new_state = ConnectFourState()
        new_state.board = np.copy(self.board)
        for row in range(5, -1, -1):
            if new_state.board[row][action] == 0:
                new_state.board[row][action] = self.current_player
                break
        new_state.current_player = -self.current_player
        new_state.check_winner()
        return new_state

    def check_winner(self):
        # Check for a win horizontally, vertically, or diagonally
        for row in range(6):
            for col in range(4):
                if all(self.board[row][col + i] == self.current_player for i in range(4)):
                    self._is_terminal = True
                    self.set_reward()
                    return

        for col in range(7):
            for row in range(3):
                if all(self.board[row + i][col] == self.current_player for i in range(4)):
                    self._is_terminal = True
                    self.set_reward()
                    return

        for row in range(3):
            for col in range(4):
                if all(self.board[row + i][col + i] == self.current_player for i in range(4)):
                    self._is_terminal = True
                    self.set_reward()
                    return

                if all(self.board[row + i][col + 3 - i] == self.current_player for i in range(4)):
                    self._is_terminal = True
                    self.set_reward()
                    return

        # Check for a draw
        if all(self.board[0][col] != 0 for col in range(7)):
            self._is_terminal = True
            self.set_reward()

    def set_reward(self):
        if self._is_terminal:
            if self.reward == 0:
                self.reward = 0.5  # Draw
            else:
                self.reward = 1.0 if self.reward == self.current_player else -1.0

    def get_reward(self):
        return self.reward

    def __str__(self):
        return "\n".join([" ".join(["X" if cell == 1 else "O" if cell == -1 else "_" for cell in row]) for row in self.board])

class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.value = 0

def uct(node):
    if node.visits == 0:
        return float('inf')
    return (node.value / node.visits) + 1.41 * math.sqrt(math.log(node.parent.visits) / node.visits)

def select(node):
    while node.children:
        offense_uct = max(child.value / child.visits + math.sqrt(math.log(node.visits) / child.visits) for child in node.children)
        defense_uct = max(-child.value / child.visits + math.sqrt(math.log(node.visits) / child.visits) for child in node.children)

        current_threats = get_threats(node.state)
        
        offense_weight = 1.0 if current_threats[node.state.current_player] else 0.5
        defense_weight = 1.0 if current_threats[-node.state.current_player] else 0.5

        if current_threats[-node.state.current_player]:
            defense_weight = 2.0  

        node = max(node.children, key=lambda child: offense_weight * offense_uct + defense_weight * defense_uct)

    return node


def get_threats(state):
    threats = {1: False, -1: False} 

    for row in range(6):
        for col in range(4):
            if all(state.board[row][col + i] == state.current_player for i in range(4)):
                threats[state.current_player] = True

            if all(state.board[row][col + i] == -state.current_player for i in range(4)):
                threats[-state.current_player] = True

    return threats

def expand(node):
    action = random.choice(node.state.get_legal_actions())
    new_state = node.state.perform_action(action)
    child_node = Node(new_state, parent=node)
    node.children.append(child_node)
    return child_node

def simulate(node):
    while not node.state.is_terminal():
        action = random.choice(node.state.get_legal_actions())
        node.state = node.state.perform_action(action)
    return node.state.get_reward()

def backpropagate(node, reward):
    while node is not None:
        node.visits += 1
        node.value += reward
        node = node.parent

def monte_carlo_tree_search(root, iterations):
    for _ in range(iterations):
        selected_node = select(root)

        if selected_node.state.is_terminal():
            continue

        expanded_node = expand(selected_node)
        reward = simulate(expanded_node)
        backpropagate(expanded_node, reward)

    return max(root.children, key=lambda x: x.visits).state

def play_connect_four():
    initial_state = ConnectFourState()
    root_node = Node(initial_state)

    while not root_node.state.is_terminal():
        print("Current state:")
        print(root_node.state)

        if root_node.state.current_player == 1:
            player_move = int(input("Enter your move (column): "))
            action = player_move
        else:
            print("Computer's turn:")
            result_state = monte_carlo_tree_search(root_node, iterations=1000)
            action = np.where(result_state.board[0] == 0)[0][0]

        root_node = Node(root_node.state.perform_action(action))

    print("Game over!")
    print("Result:")
    print(root_node.state)

class ConnectFourGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.buttons = []
        self.create_board()
        self.play_connect_four()

    def create_board(self):
        for i in range(6):
            row_buttons = []
            for j in range(7):
                button = tk.Button(self.root, text=" ", width=4, height=2, command=lambda row=i, col=j: self.make_move(row, col))
                button.grid(row=i, column=j)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def update_board(self, state):
        for i in range(6):
            for j in range(7):
                if state.board[i][j] == 1:
                    self.buttons[i][j].config(text="X", state=tk.DISABLED)
                elif state.board[i][j] == -1:
                    self.buttons[i][j].config(text="O", state=tk.DISABLED)

    def make_move(self, row, col):
        if not self.root_node.state.is_terminal() and self.root_node.state.current_player == 1:
            self.root_node = Node(self.root_node.state.perform_action(col))
            self.update_board(self.root_node.state)
            self.computer_move()

    def computer_move(self):
        if not self.root_node.state.is_terminal() and self.root_node.state.current_player == -1:
            result_state = monte_carlo_tree_search(self.root_node, iterations=1000)
            action = np.where(result_state.board[0] == 0)[0][0]
            self.root_node = Node(self.root_node.state.perform_action(action))
            self.update_board(self.root_node.state)

            if self.root_node.state.is_terminal():
                self.show_result()

    def show_result(self):
        result = self.root_node.state.get_reward()
        if result == 0:
            messagebox.showinfo("Game Over", "Computer wins!")
        elif result == 1:
            messagebox.showinfo("Game Over", "You win!")
        else:
            messagebox.showinfo("Game Over", "You Win!")

    def play_connect_four(self):
        initial_state = ConnectFourState()
        self.root_node = Node(initial_state)
        self.root.mainloop()

if __name__ == "__main__":
    ConnectFourGUI()
