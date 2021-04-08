from matplotlib import pyplot as plt 
import random
import math
import heapq
from init_logger import init_logger

INFINITY = float('inf')

VISITED_COLOR = 5
UNVISITED_COLOR = 10
WALL_COLOR = 0
START_COLOR = 20
END_COLOR = 25

size = 70

_grid = []
_plt_grid = [] # matrix de visualização

logger = init_logger(__name__, testing_mode=False)

class Node:

    def __init__(self, x, y):

        self.grid_color = UNVISITED_COLOR #para cor no gŕafico
        self.x = x
        self.y = y
        self.d = INFINITY #distância do nodo inicial
        self.f = INFINITY
       
        self.neighbours = []
        self.previous = None #para mantermos um backtrack e construirmos um caminho

        self.wall = False
        if random.random() < 0.3:
            self.wall = True

    def __lt__(self, other): 
        # para a compareção no heap da fila de prioridade 
        return self.f < other.f
    
    def set_neighbours(self, grid):
        x = self.x
        y = self.y

        if y < size-1:
            self.neighbours.append(grid[x][y+1])
        if x > 0:
            self.neighbours.append(grid[x-1][y])
        if y > 0:
            self.neighbours.append(grid[x][y-1])
        if x < size-1:
            self.neighbours.append(grid[x+1][y])
        if x < size-1 and y < size-1:
            self.neighbours.append(grid[x+1][y+1])
        if x > 0 and y < size-1:
            self.neighbours.append(grid[x-1][y+1])
        if x < size-1 and y > 0:
            self.neighbours.append(grid[x+1][y-1])
        if x > 0 and y > 0:
            self.neighbours.append(grid[x-1][y-1])

def a_star(start, end):
    start = start
    end = end

    pq = []

    start.d = 0
    start.f = heuristic(start, end)

    heapq.heappush(pq, start)
    last_visited_node = start #vou usar isso para manter posição do último nodo a ser visitado
    while pq != []:
        u = heapq.heappop(pq)

        if(u == end):
            break

        for v in u.neighbours:
            if not v.wall and v not in pq:
                u.grid_color = VISITED_COLOR # marca cor para nodo visitado
                dist = distance(u, v)
                alt = u.d + dist 
                if alt < v.d:
                    v.previous = u
                    v.d = alt
                    v.f = distance(v, end) + v.d
                    heapq.heappush(pq, v)
                    last_visited_node = v

    
    build_graph_path(last_visited_node, end)
    
def distance(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def heuristic(a, b):
    # procurar uma função de heurística melhor
    # http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html#heuristics-for-grid-maps
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

def build_graph_path(last_visited_node, end):

    path = []
    current = last_visited_node
    path.append(current)

    while (current.previous):
        path.append(current)
        current = current.previous

    for u in path:
        u.grid_color = 30

    if (last_visited_node.x == end.x or last_visited_node.y == end.y):
        logger.info("Matriz gerada com sucesso.")
    else:
        logger.warning("Matriz gerada. Nenhum caminho encontrado")


def build_grid():
    populate_grid()
    add_neighbours_to_nodes()

def populate_grid():
    # cria as colunas
    for i in range(size):
        row = [Node(0,0) for i in range(size)]
        _grid.append(row)

    for i in range(size):
        for j in range(size):
            _grid[i][j] = Node(i, j)

def add_neighbours_to_nodes():
    for i in range(size):
        for j in range(size):
            _grid[i][j].set_neighbours(_grid)

def build_visualization_grid():
    for i in range(size):
        row = [0 for i in range(size)]
        _plt_grid.append(row)


    for i in range(size):
        for j in range(size):
            if _grid[i][j].wall:
                _plt_grid[i][j] = WALL_COLOR
            else:
                _plt_grid[i][j] = _grid[i][j].grid_color

def set_start(x, y):
    start = _grid[x][y]
    _grid[x][y].wall = False
    start.grid_color = START_COLOR

    return start

def set_end(x, y):
    end = _grid[x][y]
    _grid[x][y].wall = False
    end.grid_color = END_COLOR

    return end


if __name__ == "__main__":
    build_grid()

    start = set_start(0,0)
    end = set_end(size-1, size-1)

    a_star(start, end)
    build_visualization_grid()

    plt.figure(figsize =(10, 10))
    plt.axis('off')
    plt.imshow(_plt_grid)
    plt.savefig("images/a_star_pathfinder_5.png")
    