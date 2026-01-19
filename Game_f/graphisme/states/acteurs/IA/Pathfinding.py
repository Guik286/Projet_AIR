

import heapq
from math import sqrt

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Distance from start
        self.h = 0  # Heuristic distance to end
        self.f = 0  # Total cost

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f

    def __hash__(self):
        return hash(self.position)

class Pathfinding:
    def __init__(self, grid, start, end, obstacles):
        self.grid = grid
        self.start = start
        self.end = end
        self.obstacles = obstacles  # List of obstacle positions

    def heuristic(self, a, b):
        # Manhattan distance
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, position):
        neighbors = []
        x, y = position
        # 8 possible directions: up, down, left, right, and diagonals
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            # Check bounds
            if 0 <= nx < len(self.grid) and 0 <= ny < len(self.grid[0]):
                # Check if not obstacle
                if (nx, ny) not in self.obstacles:
                    neighbors.append((nx, ny))

        return neighbors

    def find_path(self):
        start_node = Node(self.start)
        end_node = Node(self.end)

        open_list = []
        closed_list = set()

        heapq.heappush(open_list, start_node)

        while open_list:
            current_node = heapq.heappop(open_list)
            closed_list.add(current_node.position)

            if current_node.position == self.end:
                path = []
                while current_node:
                    path.append(current_node.position)
                    current_node = current_node.parent
                return path[::-1]  # Return reversed path

            neighbors = self.get_neighbors(current_node.position)

            for neighbor_pos in neighbors:
                if neighbor_pos in closed_list:
                    continue

                neighbor_node = Node(neighbor_pos, current_node)
                neighbor_node.g = current_node.g + 1  # Assuming cost 1 for each step
                neighbor_node.h = self.heuristic(neighbor_pos, self.end)
                neighbor_node.f = neighbor_node.g + neighbor_node.h

                # Check if neighbor is already in open list with lower f
                if any(open_node for open_node in open_list if neighbor_node == open_node and neighbor_node.g > open_node.g):
                    continue

                heapq.heappush(open_list, neighbor_node)

        return None  # No path found