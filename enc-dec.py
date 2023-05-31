import numpy as np
import sys

file = sys.argv[1]

S = int
A = int
start = int
end = []
R = np.ndarray
T = np.ndarray
mdptype = str
gamma = float

actions = {"E": 0, "W": 1, "N": 2, "S": 3}

grid = []

for line in open(file):
    row = line.split()
    row = [int(x) for x in row]
    grid.append(row)

grid = np.array(grid)

rows = np.shape(grid)[0]
cols = np.shape(grid)[1]
S = rows*cols
A = 4

R = np.zeros((S,A,S))
T = np.zeros((S,A,S))

for i in range(rows):
    for j in range(cols):

        s = i*cols + j

        if grid[i,j] == 2:
            start = s 
        
        if grid[i,j] == 3:
            end.append(s)
            
            for a in range(4):
                R[s,a,s] = 0
                T[s,a,s] = 1
            
            continue

        if grid[i,j] == 1:
            for a in range(4):
                R[s,a,s] = 0
                T[s,a,s] = 1
            continue


        for a in range(4):
            ip = int
            jp = int
            if a == actions["E"]:
                jp = j+1
                ip = i
            elif a == actions["W"]:
                jp = j-1
                ip = i
            elif a == actions["N"]:
                ip = i-1
                jp = j
            elif a == actions["S"]:
                ip = i+1
                jp = j

            if ip<0 or ip>=rows or jp<0 or jp>=cols:
                R[s,a,s] = -1
                T[s,a,s] = 1
                continue;
            
            sp = ip*cols + jp

            if grid[ip, jp] == 1:
                R[s,a,s] = -1
                T[s,a,s] = 1
                continue;

            if grid[ip, jp] == 3:
                R[s,a,sp] = 1
                T[s,a,sp] = 1
                continue;

            if grid[ip, jp] == 0 or grid[ip, jp] == 2:
                R[s,a,sp] = -1
                T[s,a,sp] = 1
                continue;

gamma = 1
V = np.zeros(S)
theta = 0.001

# print(grid)
# print(T[0,0,:])

while True:
    delta = 0

    for s in range(S):
        v = V[s]
        vals = np.zeros(A)

        for a in range(A):
            vals[a] = np.matmul(np.transpose(T[s, a, :]),
                                R[s, a, :] + np.multiply(V, gamma))

        V[s] = np.amax(vals)

        delta = max(delta, abs(v - V[s]))

    if delta < theta:
        break

pi = np.zeros(S)

for s in range(S):
    v = V[s]
    vals = np.zeros(A)

    for a in range(A):
        vals[a] = np.matmul(np.transpose(T[s, a, :]), R[s, a, :] + np.multiply(V, gamma))

    pi[s] = int(np.argmax(vals))

curr_state = start
while True:
    if curr_state in end:
        break

    i = curr_state//rows
    j = curr_state%cols

    if pi[curr_state] == actions["E"]:
        print("E", end=' ')
        j = j+1

    if pi[curr_state] == actions["W"]:
        print("W", end=' ')
        j = j-1

    if pi[curr_state] == actions["N"]:
        print("N", end=' ')
        i = i-1

    if pi[curr_state] == actions["S"]:
        print("S", end=' ')
        i = i+1

    curr_state = i*cols + j

    
    


