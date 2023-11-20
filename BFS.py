import pygame
import sys
import random
from collections import deque

# Constants
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
SNAKE_SIZE = 20
FPS = 10

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class SnakeGame:
    def __init__(self):
        self.width = WIDTH // GRID_SIZE
        self.height = HEIGHT // GRID_SIZE
        self.snake = deque([(self.width // 2, self.height // 2)])
        self.food = self.generate_food()
        self.direction = RIGHT
        self.score = 0
        self.game_over = False

    def generate_food(self):
        while True:
            food = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if food not in self.snake:
                return food

    def move(self):
        current_head = self.snake[0]
        new_head = (current_head[0] + self.direction[0], current_head[1] + self.direction[1])

        if (
            0 <= new_head[0] < self.width
            and 0 <= new_head[1] < self.height
            and new_head not in self.snake
        ):
            self.snake.appendleft(new_head)

            if new_head == self.food:
                self.score += 1
                self.food = self.generate_food()
            else:
                self.snake.pop()

        else:
            self.game_over = True

    def get_neighbors(self, pos):
        directions = [UP, DOWN, LEFT, RIGHT]
        neighbors = []

        for direction in directions:
            neighbor = (pos[0] + direction[0], pos[1] + direction[1])
            if 0 <= neighbor[0] < self.width and 0 <= neighbor[1] < self.height:
                neighbors.append(neighbor)

        return neighbors

    def bfs(self):
        start = self.snake[0]
        goal = self.food

        queue = deque([(start, [])])
        visited = set()

        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path

            if current in visited:
                continue

            visited.add(current)

            neighbors = self.get_neighbors(current)
            for neighbor in neighbors:
                queue.append((neighbor, path + [current]))

        return None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.direction != DOWN:
                    self.direction = UP
                elif event.key == pygame.K_DOWN and self.direction != UP:
                    self.direction = DOWN
                elif event.key == pygame.K_LEFT and self.direction != RIGHT:
                    self.direction = LEFT
                elif event.key == pygame.K_RIGHT and self.direction != LEFT:
                    self.direction = RIGHT

    def draw(self, screen):
        screen.fill(WHITE)

        for segment in self.snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, SNAKE_SIZE, SNAKE_SIZE))

        pygame.draw.rect(screen, RED, (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, SNAKE_SIZE, SNAKE_SIZE))

        pygame.display.flip()

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()

        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake Game")

        while not self.game_over:
            self.handle_events()
            path = self.bfs()

            if path:
                if len(path) > 1:
                    self.direction = (path[1][0] - self.snake[0][0], path[1][1] - self.snake[0][1])

            self.move()
            self.draw(screen)

            clock.tick(FPS)

        print("Game Over. Your score:", self.score)
        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
