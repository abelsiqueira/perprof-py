#! /usr/bin/env python

import os, random

nvars = []
with open("df.sizes", "w") as out:
    out.write("# Dimensions of files\n")
    out.write("# NAME  NVAR\n")
    for p in range(1,11):
        n = random.randint(2, 10)
        nvars.append(n)
        out.write("prob{:02d}  {:>3d}\n".format(p, n))

with open("df.info", "w") as out:
    out.write("# Information\n" + \
            "solvers: ['DF-alpha', 'DF-beta']\n" + \
            "files: ['df-alpha', 'df-beta']\n")

for solver in ["df-alpha", "df-beta"]:
    if not os.path.isdir(solver):
        os.mkdir(solver)
    for p in range(1,11):
        maxevals = 1000 * nvars[p-1]
        with open("{}/prob{:02d}.out".format(solver, p), "w") as out:
            k = 1
            f = 100.0
            while k < maxevals:
                out.write("{:6d}  {:10.4e}\n".format(k, f))
                k += random.randint(1, 3)
                f *= random.uniform(0.8, 1.1)
