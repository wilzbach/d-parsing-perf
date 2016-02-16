#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

if len(sys.argv) <= 1:
    sys.exit("No input file")

inFilePath = sys.argv[1]
with open(inFilePath, "r") as inFile:
    inFile.readline()
    n = 0
    for line in inFile:
        n += sum(list(map(int, line.split())))
    print(n)
