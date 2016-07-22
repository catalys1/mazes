#!/usr/bin/python
import random
import numpy as np
from scipy.misc import imsave
import itertools
import operator
import argparse

def check_f0to1(val):
    fval = float(val)
    if fval < 0.0 or fval > 1.0:
        raise argparse.ArgumentTypeError('%s is not in the range [0, 1.0]' % fval)
    return fval

parser = argparse.ArgumentParser()
parser.add_argument('size',nargs=2,type=int,
        help='The width and height of the maze')
parser.add_argument('-c','--cell-size',type=int,default=10,
        help='Size (in pixels) of a cell')
parser.add_argument('-b','--bias',type=check_f0to1,default=0.5,
        help='Algorithm biasing value (number between 0 and 1)')
args = parser.parse_args()

width = args.size[0]
height = args.size[1]

algo_bias = args.bias

UP      = np.uint8(0x1)
RIGHT   = np.uint8(0x2)
DOWN    = np.uint8(0x4)
LEFT    = np.uint8(0x8)
VISITED = np.uint8(0x10)
DIRECTS = { (-1,0): DOWN, (1,0): UP, (0,1): LEFT, (0,-1): RIGHT }

maze = np.zeros((width,height),dtype=np.uint8)

start = (random.randrange(0,height),random.randrange(0,width))
active = [start]
maze[start] |= VISITED

# When the active list is empty, the maze is done
while(active):
    # Take a cell from the active list
    decider = random.random()
    if decider <= algo_bias:
        curr = active[-1]
    else:
        curr = random.choice(active)
    # Randomly choose one of it's neighbors that hasn't been VISITED
    rows = [(r,curr[1]) for r in (curr[0]-1, curr[0]+1) if r >= 0 and r < height]
    cols = [(curr[0],c) for c in (curr[1]-1, curr[1]+1) if c >= 0 and c < width]
    neighbors = [r for r in rows if not (maze[r] & VISITED)] + \
                [c for c in cols if not (maze[c] & VISITED)]
    # If there are no unvisited neighbors, remove from active list and go to next
    if not neighbors:
        active.remove(curr)
    else:
        adj = random.choice(neighbors)
        # Add the neighbor to the active list and remove the wall between the two
        d = DIRECTS[tuple(map(operator.sub,curr,adj))]
        maze[curr] |= d
        d = DIRECTS[tuple(map(operator.sub,adj,curr))]
        maze[adj] |= d | VISITED
        active.append(adj)

CS = args.cell_size
img = np.zeros((CS*height,CS*width))
img[:,(0,-1)] = 0
img[(0,-1),:] = 0
for row in xrange(height):
    for col in xrange(width):
        r = row*CS
        c = col*CS
        if not maze[(row,col)] & UP: img[r,c:c+CS] = 1
        if not maze[(row,col)] & DOWN: img[r+CS-1,c:c+CS] = 1
        if not maze[(row,col)] & LEFT: img[r:r+CS,c] = 1
        if not maze[(row,col)] & RIGHT: img[r:r+CS,c+CS-1] = 1
imsave('maze.jpg',img)
