#!/usr/bin/env python

from random import random, seed

seed(0)
speed = [0.1, 5, 2]
rob   = [0.60, 0.95, 0.70]
with open('perf.example', 'w') as file_:
    file_.write("---\nsolver_names: ['Solver 1', 'Solver 2', 'Solver 3']\n---\n")
    for i in range(0, 100):
        file_.write("P{:03}".format(i+1))
        for j in range(0, 3):
            if random() > rob[j]:
                file_.write(" {:>7}".format("inf"))
            else:
                r = max(min(600, speed[j] * random() / (random())), 0.001)
                file_.write(" {:07.4f}".format(r))
        file_.write("\n")
