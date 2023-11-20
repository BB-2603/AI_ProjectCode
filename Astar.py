import time
import random
import matplotlib.pyplot as plt

class MapNode:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.cost_from_start = 0
        self.heuristic_cost_to_goal = 0
        self.total_cost = 0

    def __eq__(self, other):
        return self.position == other.position

def find_path(maze, start, goal, max_iterations=10000):
    start_time = time.time()

    start_node = MapNode(None, start)
    start_node.cost_from_start = start_node.heuristic_cost_to_goal = start_node.total_cost = 0

    goal_node = MapNode(None, goal)
    goal_node.cost_from_start = goal_node.heuristic_cost_to_goal = goal_node.total_cost = 0

    open_nodes = []
    closed_nodes = []

    open_nodes.append(start_node)

    iterations = 0

    while open_nodes and iterations < max_iterations:
        current_node = open_nodes[0]
        current_index = 0

        for index, node in enumerate(open_nodes):
            if node.total_cost < current_node.total_cost:
                current_node = node
                current_index = index

        open_nodes.pop(current_index)
        closed_nodes.append(current_node)

        if current_node == goal_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent

            end_time = time.time()
            execution_time = end_time - start_time

            return path[::-1], execution_time, len(path) - 1

        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if (
                0 <= node_position[0] < len(maze)
                and 0 <= node_position[1] < len(maze[0])
                and maze[node_position[0]][node_position[1]] == 0
            ):
                new_node = MapNode(current_node, node_position)
                children.append(new_node)

        for child in children:
            if child in closed_nodes:
                continue

            child.cost_from_start = current_node.cost_from_start + 1
            child.heuristic_cost_to_goal = (
                (child.position[0] - goal_node.position[0]) ** 2
                + (child.position[1] - goal_node.position[1]) ** 2
            )
            child.total_cost = child.cost_from_start + child.heuristic_cost_to_goal

            for open_node in open_nodes:
                if child == open_node and child.cost_from_start > open_node.cost_from_start:
                    continue

            open_nodes.append(child)

        iterations += 1

    print("Warning: Maximum iterations reached without finding a path.")
    return None, None, None



def generate_random_maze():
    maze_size = 100
    difficulty_level= [0.3]  

    maze = [[0] * maze_size for _ in range(maze_size)]

    difficulty = random.choice(difficulty_level)
    for i in range(maze_size):
        for j in range(maze_size):
            if random.random() < difficulty:
                maze[i][j] = 1

    start_point = (0,0)
    end_point = (99,99)

    while maze[start_point[0]][start_point[1]] == 1:
        start_point = (random.randint(0, maze_size - 1), random.randint(0, maze_size - 1))

    while maze[end_point[0]][end_point[1]] == 1 or end_point == start_point:
        end_point = (random.randint(0, maze_size - 1), random.randint(0, maze_size - 1))

    return maze, start_point, end_point

def main():
    maze_size = 100
    num_iterations = 100
    path_lengths = []
    execution_times = []

    for i in range(num_iterations):
        my_maze, start_point, end_point = generate_random_maze()

        found_path, execution_time, path_length = find_path(my_maze, start_point, end_point)

        print(i)

        if found_path is not None:
            path_lengths.append(path_length)
            execution_times.append(execution_time)

    plt.figure(figsize=(12, 6))

    plt.subplot(1, 2, 1)
    plt.plot(path_lengths, marker='o', linestyle='-', color='b')
    plt.title('Path Lengths for 600 Random Mazes')
    plt.xlabel('Iteration')
    plt.ylabel('Path Length')

    plt.subplot(1, 2, 2)
    plt.plot(execution_times, marker='o', linestyle='-', color='r')
    plt.title('Execution Times for 600 Random Mazes')
    plt.xlabel('Iteration')
    plt.ylabel('Execution Time (seconds)')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
