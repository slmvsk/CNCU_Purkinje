#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 14:44:30 2025

@author: tetianasalamovska
"""
from neuron import h
import matplotlib.pyplot as plt

# Load model
h.load_file("/Users/tetianasalamovska/Downloads/Akicodes/data/human/original.hoc")

# List of locations for calcium recording
sections_to_record = {
    "soma": h.soma(0.5),  # Middle of soma
    "AIS": h.ais(0.5),  # Axon Initial Segment
    "proximal_dend": h.dend[3](0.5),  # Middle of 3rd dendrite
    "distal_dend": h.dend[-1](0.9),  # Near end of last dendrite
    "axon": h.axon[1](0.5),  # Middle of 2nd axon section
}

recordings = [
    Recording("soma[0]", 0.5, "cai"),      # Center of the soma
    Recording("axon[0]", 0.7, "cai"),      # Random point in the axon
    Recording("dend_6[2]", 0.0, "cai"),    # Beginning of the dendritic tree
    Recording("dend_6[1271]", 0.5, "cai"), # One of the major dendritic branches
    Recording("dend_5[2657]", 0.5, "cai"), # Another main dendritic branch
    Recording("dend_6[415]", 1.0, "cai"),  # Distant end of the dendrite
]

# Initialize recording vectors
t = h.Vector()
t.record(h._ref_t)

calcium_traces = {}
for name, seg in sections_to_record.items():
    calcium_traces[name] = h.Vector()
    calcium_traces[name].record(seg._ref_cai)

# Inject current in soma
stim = h.IClamp(h.soma(0.5))
stim.delay = 100  # Start injection at 100 ms
stim.dur = 500  # Duration of stimulus
stim.amp = 0.5  # Current amplitude in nA

# Run simulation
h.tstop = 1000
h.run()

# Plot results
plt.figure(figsize=(10, 5))
for name, vec in calcium_traces.items():
    plt.plot(t, vec, label=name)

plt.xlabel("Time (ms)")
plt.ylabel("Calcium Concentration (mM)")
plt.title("Calcium Traces in Different Locations")
plt.legend()
plt.show()