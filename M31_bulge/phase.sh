#!/bin/bash

# Written by Ryan Hofmann

python << phase
from phase import PhaseDiagram
PhaseDiagram('M31_000.txt', ptype=3, p_axis='y', v_axis='x')
phase
