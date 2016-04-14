#!/bin/bash

# Written by Ryan Hofmann

python << kin
import kinematics
kinematics.VStats('M31_000.txt', axis='z')
kin
