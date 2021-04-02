from matplotlib import pyplot as plt 
import random
import math
import heapq

size = 70

class Node:

    def __init__(self, x, y):
        self.set = 10
        self.x = x
        self.y = y
        self.d = float('inf') ##distância do nodo inicial
       
        self.neighbours = []
        
        self.wall = False
        self.previous = None #para mantermos um backtrack e construirmos um caminho

        if random.random() < 0.40:
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


def dijkstra(grid):
    start = grid[0][0]
    end = grid[size-1][size-1]

    start.set = 20
    end.set = 25

    pq = [] #fila de prioridade

    start.d = 0

    heapq.heappush(pq, start)

    while pq != []:
        u = heapq.heappop(pq)

        for v in u.neighbours:
            if not v.wall:
                dist = distance(u, v)
                if u.d + dist < v.d:
                    v.d = u.d+dist
                    v.previous = u
                    heapq.heappush(pq, v)
    
    path = []
    current = end
    path.append(end)
    while (current.x != 0 or current.y != 0):
        path.append(current)
        current = current.previous
        print(current.x, current.y)
    
    for u in path:
        u.set = 30

_grid = []

def distance(a, b):
    dist = math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)
    return dist

def populate_grid(grid):
    for i in range(size):
        row = [Node(0,0) for i in range(size)]
        _grid.append(row)

    for i in range(size):
        for j in range(size):
            _grid[i][j] = Node(i, j)

def add_neighbours():
    for i in range(size):
        for j in range(size):
            _grid[i][j].set_neighbours(_grid)


populate_grid(_grid)
add_neighbours()

dijkstra(_grid)

start = _grid[0][0]
end = _grid[size - 1][size - 1]

if end == None:
    end = Node(size-1, size-1)

_grid[0][0].wall = False
_grid[size - 1][size - 1].wall = False

vis_grid = [] #matriz de visualização
for i in range(size):
    row = [0 for i in range(size)]
    vis_grid.append(row)

for i in range(size):
    for j in range(size):
        if _grid[i][j].wall:
            vis_grid[i][j] = _grid[i][j].set - 10
        else:
            vis_grid[i][j] = _grid[i][j].set

plt.figure(figsize =(20, 20))
plt.imshow(vis_grid)
plt.axis('off')
plt.savefig("pathfinder.png")