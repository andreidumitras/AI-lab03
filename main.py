import pygame
from utils import WIDTH, HEIGHT
from queue import PriorityQueue
from grid import Grid
from spot import Spot

# setting up how big will be the display window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# set a caption for the window
pygame.display.set_caption("Path Visualizing Algorithm")


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
    pass

def dfs(draw: callable, grid: Grid, start: Spot, end: Spot) -> bool:
    """
    Depth-First Search (DFS) Algorithm.
    Args:
        draw (callable): A function to call to update the Pygame window.
        grid (Grid): The Grid object containing the spots.
        start (Spot): The starting spot.
        end (Spot): The ending spot.
    Returns:
        bool: True if a path is found, False otherwise.
    """
    pass

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
    def h(p1: tuple[int, int], p2: tuple[int, int]) -> float:
        """
        Heuristic function for A* algorithm: uses the Manhattan distance between two points.
        Args:
            p1 (tuple[int, int]): The first point (x1, y1).
            p2 (tuple[int, int]): The second point (x2, y2).
        Returns:
            float: The Manhattan distance between p1 and p2.
        """
        pass
    pass


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
                    # TODO
                    # dfs(lambda: grid.draw(), grid, start, end)
                    # bfs(lambda: grid.draw(), grid, start, end)
                    # astar(lambda: grid.draw(), grid, start, end)

                    started = False
                    # call the algorithm
                    # grid.a_star_algorithm(lambda: grid.draw(), start, end)

                if event.key == pygame.K_c:
                    print("Clearing the grid...")
                    start = None
                    end = None
                    grid.reset()
    pygame.quit()
