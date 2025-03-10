#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 30 17:20:12 2025

@author: tetianasalamovska
"""

from neuron import h
import matplotlib.pyplot as plt
#from neuron import gui

h.load_file("/Users/tetianasalamovska/Downloads/Akicodes/src/tmp/output/human/original/analysis/geom.hoc")

for sec in h.allsec():
    print(sec.name())

from neuron import h
print([m for m in dir(h) if not m.startswith("_")])  # Lists all available mechanisms


for sec in h.allsec():
    try:
        print(sec.name(), sec.cai)
    except AttributeError:
        print(sec.name(), "No cai")


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


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    