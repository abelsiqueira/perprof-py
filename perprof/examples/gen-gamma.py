#!/usr/bin/python

### WARNING
# This will not work alone. You have to edit the YAML manually

import random

open_yaml = False
with open('alpha.table','r') as alphafile:
    with open('beta.table','r') as betafile:
        with open('gamma.table','w') as gammafile:
            for alphaline in alphafile:
                betaline = betafile.readline()

                r = random.randint(0,1)

                if r == 0:
                    line = alphaline
                elif r == 1:
                    line = betaline
                line = line.split()

                if line[0] == "#Name":
                    gammafile.write("#Name Gamma\n")
                elif line[0] == "---":
                    if open_yaml:
                        gammafile.write("col_name: 5\n")
                        gammafile.write("col_exit: 3\n")
                        gammafile.write("col_time: 2\n")
                        gammafile.write("col_fval: 6\n")
                        gammafile.write("col_primal: 1\n")
                        gammafile.write("col_dual: 4\n")
                    gammafile.write("---\n")
                    open_yaml = not open_yaml
                elif line[0] == "algname:":
                    gammafile.write("algname: Gamma\n")
                elif line[0] == "success:":
                    gammafile.write("success: converged,success\n")
                elif line[0] == "free_format:":
                    gammafile.write("free_format: True\n")
                else:
                    line[4], line[2], line[1], line[5], line[0], line[3] = line
                    gammafile.write(' '.join(line) + '\n')
