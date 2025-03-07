#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:00:56 2025

@author: tetianasalamovska
"""
import os
print("Current Working Directory:", os.getcwd())

from neuron import h

file_path = "/Users/tetianasalamovska/Downloads/Akicodes/data/human/original.hoc"
print(f"Trying to load: {file_path}")

h.load_file(1, file_path)

sections = list(h.allsec())
if sections:
    print("Successfully loaded morphology!")
else:
    print("Failed to load morphology.")
    
print(f"🔍 Debug: Morphology variable = {morphology}")



from neuron import h

file_path = "/Users/tetianasalamovska/Downloads/Akicodes/data/human/original.hoc"
print(f"🔍 Trying to load manually: {file_path}")

h.load_file(1, file_path)  # Force NEURON to load
sections = list(h.allsec())

if sections:
    print("✅ NEURON successfully loaded the morphology!")
else:
    print("❌ NEURON failed to load the morphology!")