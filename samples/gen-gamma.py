#!/usr/bin/python

import random

with open('alpha.table','r') as alphafile:
    with open('beta.table','r') as betafile:
        with open('gamma.table','w') as gammafile:
            for alphaline in alphafile:
                betaline = betafile.readline()

                if alphaline.split()[0] == "#Name":
                    gammafile.write("#Name Gamma\n")
                    continue

                r = random.randint(0,1)

                if r == 0:
                    gammafile.write(alphaline)
                elif r == 1:
                    gammafile.write(betaline)

