#!/bin/bash

# Wrtten by Ryan Hofmann

python <<Plot
import plot
plot.PlotBulge(plane='yz', contours=1, ellipse=1)
Plot
