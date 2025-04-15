#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 17:20:12 2025

@author: tetianasalamovska
"""


from neuron import h
import matplotlib.pyplot as plt
#from neuron import gui
from cell import Cell

cell = Cell.load("/Users/tetianasalamovska/Downloads/Akicodes/data/zang2021/fig3.hoc", gui=False)   

print(h.soma.psection()['density_mechs'].keys())


#dendA1_01

from neuron import h
import pandas as pd
from cell import Cell

# Load and classify the cell
cell = Cell.load("/Users/tetianasalamovska/Downloads/Akicodes/data/zang2021/fig3.hoc")
cell.classify()

# Gather all dendritic sections
all_dends = []
for group in "dendA1":
    sec_list = getattr(h, group, None)
    if sec_list:
        for i in range(len(sec_list)):
            sec = sec_list[i]
            all_dends.append({
                "group": group,
                "index": i,
                "name": sec.name(),
                "sec": sec
            })

# Helper to find match
def find_match(sec):
    for d in all_dends:
        if d["name"] == sec.name():
            return d
    return None

# Create tables
trunk_table = []
for i, sec in enumerate(cell.trunk_sections):
    m = find_match(sec)
    if m:
        trunk_table.append({
            "type": "trunk",
            "index": i,
            "group": m["group"],
            "dend_index": m["index"],
            "sec_name": m["name"]
        })

branch_table = []
for i, sec in enumerate(cell.branch_sections):
    m = find_match(sec)
    if m:
        branch_table.append({
            "type": "branch",
            "index": i,
            "group": m["group"],
            "dend_index": m["index"],
            "sec_name": m["name"]
        })

# Combine and view
df = pd.DataFrame(trunk_table + branch_table)
print(df.to_string(index=False))  # or save as CSV: df.to_csv("sections_mapping.csv", index=False)










print("=== Trunk Sections ===")
for sec in cell.trunk_sections:
    print(sec.name())

print("\n=== Branch Sections ===")
for sec in cell.branch_sections:
    print(sec.name())


for sec in h.allsec():
    print(sec.name())

from neuron import h
print([m for m in dir(h) if not m.startswith("_")])  # Lists all available mechanisms


for sec in h.dend:
    print(sec)


for sec in h.dend:
    print(sec.name()) 



for sec in h.allsec():
    try:
        print(sec.name(), sec.cai)
    except AttributeError:
        print(sec.name(), "No cai")


print("Recordings content:", TrySet._try_ca_recordings)
for rec in TrySet._try_ca_recordings:
    print(f"Length: {len(rec)} -> {rec}")


if hasattr(h, "dend"):
    dend = getattr(h, "dend", None)
    print(isinstance(dend, type(h.Section())))  # Should return True if dend is a section


# Access the first dendrite (if it is a list-like HocObject)
if hasattr(h, "dend"):
    print(dend[0])  # Check if it behaves like an indexed list


print(h.soma)

for i in range(int(h.soma.n3d())):
    print(f"Point {i}: x={h.soma.x3d(i)}, y={h.soma.y3d(i)}, z={h.soma.z3d(i)}, diam={h.soma.diam3d(i)}")
    


h.Shape().plot(plt)

ps = h.PlotShape(False)  # Create a PlotShape object
ps.show(1)  # Display the neuron

print(h.soma)
stim = h.IClamp(h.soma(0.5))  # Place at middle of soma
stim.delay = 10  
stim.dur = 1   
stim.amp = -0.5  
v_soma = h.Vector()
t = h.Vector()
v_soma.record(h.soma(0.5)._ref_v)  
t.record(h._ref_t)  
h.tstop = 200  
h.run()


plt.plot(t.as_numpy(), v_soma.as_numpy(), label="Soma Voltage")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Voltage (mV)")
plt.title("Soma Stimulation")
plt.legend()
plt.show()

for sec in h.allsec():
    print(sec.name())  # Print section names
    
selected_dendrites = [sec for sec in h.allsec() if "dend[0]" in sec.name()]
print(f"Selected {len(selected_dendrites)} dendrites")  # Debugging: See how many are selected

ps = h.PlotShape()
for dend in selected_dendrites:
    ps.section(dend, seccolor=2)  # Red color
ps.show(1)


for sec in h.allsec():
    print(f"{sec.name()} is connected to {sec.parentseg()}")
    
for sec in h.allsec():
    parent = sec.parentseg()
    if parent and parent.sec.name() == "soma":
        print(f"{sec.name()} is connected to soma at {parent.x}")    
    
def get_single_dendrite_branch(start_sec):
    """Find a single continuous dendrite branch starting from `start_sec`."""
    branch = []

    def traverse(sec):
        branch.append(sec)
        # Find the first child dendrite (choosing one path only)
        children = [child for child in h.allsec() if child.parentseg() and child.parentseg().sec == sec]
        if children:
            traverse(children[0])  # Follow only the first child (choosing one branch)

    traverse(start_sec)
    return branch  # Returns a list of sections in one branch

dendrite_branch = get_single_dendrite_branch(h.dend[0])
print(f"Selected {len(dendrite_branch)} sections in one branch:")
for sec in dendrite_branch:
    print(sec.name())






stim = h.IClamp(h.soma(0.5))  # Place current clamp at the center of the soma
stim.delay = 20  # Start at 5 ms
stim.dur = 50  # Duration: 100 ms
stim.amp = 0.5  # Inject 0.5 nA

v_soma = h.Vector()
v_dend = h.Vector()
t = h.Vector()

v_soma.record(h.soma(0.5)._ref_v)  # Record voltage at soma
v_dend.record(dendrite_branch[-1](0.5)._ref_v)  # Record at the last section of the branch
t.record(h._ref_t)  # Record time

h.tstop = 300  # Simulate for 300 ms
h.run()


plt.figure(figsize=(6, 4))
plt.plot(t, v_soma, label="Soma")
plt.plot(t, v_dend, label=f"{dendrite_branch[-1].name()} (Dendrite)")
plt.xlabel("Time (ms)")
plt.ylabel("Membrane Voltage (mV)")
plt.title("Response to Stimulation")
plt.legend()
plt.show()

print(f"Max voltage in soma: {max(v_soma)} mV")
print(f"Max voltage in dendrite: {max(v_dend)} mV")

for mech in h.soma.psection()["mechs"]:
    print(mech)  # Print ion channel mechanisms in the soma

#print(h.soma.psection().keys())  # See available keys
#dict_keys(['point_processes', 'density_mechs', 'ions', 
#'morphology', 'nseg', 'Ra', 'cm', 'regions', 'species', 'name', 'hoc_internal_name', 'cell'])
    
print(h.soma.psection()["density_mechs"])
for sec in dendrite_branch:
    print(f"{sec.name()}:", sec.psection()["density_mechs"])    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    