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

for line in open(file):
    vals = line.split()

    if vals[0] == 'numStates':
        S = int(vals[1])
    elif vals[0] == 'numActions':
        A = int(vals[1])
        R = np.zeros((S, A, S))
        T = np.zeros((S, A, S))
    elif vals[0] == 'start':
        start = int(vals[1])
    elif vals[0] == 'end':
        if int(vals[1]) != -1:
            for i in range(1, len(vals)):
                end.append(int(vals[i]))
    elif vals[0] == 'transition':
        s1 = int(vals[1])
        a = int(vals[2])
        s2 = int(vals[3])
        r = float(vals[4])
        p = float(vals[5])

        R[s1, a, s2] = r
        T[s1, a, s2] = p
    elif vals[0] == 'mdptype':
        mdptype = vals[1]
    elif vals[0] == 'discount':
        gamma = float(vals[1])

V = np.zeros(S)
theta = 0.0000001

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

    pi[s] = np.argmax(vals)

    print(str(np.amax(vals)) + " " + str(int(pi[s])))