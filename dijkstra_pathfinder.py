from matplotlib import pyplot as plt 
import random
import math
import heapq

INFINITY = float('inf')

VISITED_COLOR = 5
UNVISITED_COLOR = 10
WALL_COLOR = 0
START_COLOR = 20
END_COLOR = 25

size = 70

_grid = []
_plt_grid = [] # matrix de visualização

class Node:

    def __init__(self, x, y):

        self.grid_color = UNVISITED_COLOR #para cor no gŕafico
        self.x = x
        self.y = y
        self.d = INFINITY #distância do nodo inicial
       
        self.neighbours = []
        
        self.previous = None #para mantermos um backtrack e construirmos um caminho

        self.wall = False
        if random.random() < 0.45:
            self.wall = True

    def __lt__(self, other): 
        # para a compareção no heap da fila de prioridade 
        return self.d < other.d
    
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


def dijkstra(start, end):
    start = start
    end = end

    pq = [] #fila de prioridade

    start.d = 0

    heapq.heappush(pq, start)

    while pq != []:
        u = heapq.heappop(pq)
        for v in u.neighbours:
            if not v.wall:
                u.grid_color = VISITED_COLOR # marca cor para nodo visitado
                dist = distance(u, v)
                if u.d + dist < v.d:
                    v.d = u.d+dist
                    v.previous = u
                    heapq.heappush(pq, v)
    
    build_graph_path(start, end)

def distance(a, b):
    dist = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
    return dist

def build_graph_path(start, end):
    path = []
    current = end
    path.append(end)
    if current is None:
        print("Nenhum caminho possível")
        return
    else:
        while (current.x != start.x or current.y != start.y):
            path.append(current)
            current = current.previous
        
        for u in path:
            u.grid_color = 30

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

build_grid()

start = set_start(0,0)
end = set_end(size-1, size-1)

dijkstra(start, end)
build_visualization_grid()

plt.figure(figsize =(20, 20))
plt.axis('off')
plt.imshow(_plt_grid)
plt.savefig("pathfinder.png")