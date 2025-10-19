from utils import *
import math
from queue import PriorityQueue
from grid import Grid
from spot import Spot

# setting up how big will be the display window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# set a caption for the window
pygame.display.set_caption("Path Visualizing Algorithm")


def h(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    """
    Heuristic function for A* algorithm: uses the Manhattan distance between two points.
    Args:
        p1 (tuple[int, int]): The first point (x1, y1).
        p2 (tuple[int, int]): The second point (x2, y2).
    Returns:
        float: The Manhattan distance between p1 and p2.
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

from collections import deque

def bfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Breadth-First Search (BFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    queue = deque([start])  # FIFO queue
    visited = {start}  # set of Spot objects already visited
    came_from = {}  # map for path reconstruction

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = queue.popleft()  # get the first spot in the queue

        if current == end:
            # reconstruct path
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            return True  # path found

        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
                neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False  # no path found

def astar(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    A* Pathfinding Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        None
    """
    count = 0  # counter to break ties in the priority queue
    open_set = PriorityQueue()  # priority queue for open set
    open_set.put((0, count, start))  # add the start spot to the open set with f_score 0
    came_from = {}  # dictionary to keep track of the path

    g_score = {spot: float("inf") for row in grid.grid for spot in row}
    g_score[start] = 0  # g_score of start is 0

    f_score = {spot: float("inf") for row in grid.grid for spot in row}
    f_score[start] = h(start.get_position(), end.get_position())  # f_score of start is heuristic to end

    open_set_lookup = {start}  # to keep track of items in the priority queue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]    # get the spot with the lowest f_score
        open_set_lookup.remove(current)  # remove it from the hash set

        if current == end:
            # reconstruct path
            while current in came_from:
                current = came_from[current]
                current.make_path()
                draw()
            end.make_end()
            start.make_start()
            # path found
            return True
        for neighbor in current.neighbors:
            next_g_score = g_score[current] + 1  # assume each step has a cost of 1

            if next_g_score < g_score[neighbor]:
                # This path to neighbor is better than any previous one. Record it!
                came_from[neighbor] = current
                g_score[neighbor] = next_g_score
                f_score[neighbor] = next_g_score + h(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_lookup:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_lookup.add(neighbor)
                    neighbor.make_open()
        draw()
        if current != start:
            current.make_closed()
    return False  # no path found


if __name__ == "__main__":
    ROWS = 50  # number of rows
    COLS = 50  # number of columns
    grid = Grid(WIN, ROWS, COLS, WIDTH, HEIGHT)

    start = None
    end = None

    # flags for running the main loop
    run = True
    started = False

    while run:
        grid.draw()  # draw the grid and its spots
        for event in pygame.event.get():
            # verify what events happened
            if event.type == pygame.QUIT:
                run = False

            if started:
                # do not allow any other interaction if the algorithm has started
                continue  # ignore other events if algorithm started

            if pygame.mouse.get_pressed()[0]:  # LEFT CLICK
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)
                if row >= ROWS or row < 0 or col >= COLS or col < 0:
                    continue  # ignore clicks outside the grid
                print(f"Clicked position: {pos}, Grid position: ({row}, {col})")
                spot = grid.grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            elif pygame.mouse.get_pressed()[2]:  # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                row, col = grid.get_clicked_pos(pos)
                spot = grid.grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    # run the algorithm
                    for row in grid.grid:
                        for spot in row:
                            spot.update_neighbors(grid.grid)
                    astar(lambda: grid.draw(), grid, start, end)
                    # bfs(lambda: grid.draw(), grid, start, end)

                    started = False
                    # call the algorithm
                    # grid.a_star_algorithm(lambda: grid.draw(), start, end)

                if event.key == pygame.K_c:
                    print("Clearing the grid...")
                    start = None
                    end = None
                    grid.reset()
    pygame.quit()
