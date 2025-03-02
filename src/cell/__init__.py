import os
from dataclasses import dataclass
import itertools as it
import numpy as np
import writer


class Cell:
    @dataclass
    class Geom:
        volume: float = 0
        area: float = 0
        length: float = 0

        def __iter__(self):
            return (getattr(self, f) for f in self.__dataclass_fields__)

        def __add__(self, other):
            return Cell.Geom(*(x + y for x, y in zip(self, other)))

        def __sub__(self, other):
            return Cell.Geom(*(x - y for x, y in zip(self, other)))

    def clean():
        from neuron import h

        for sec in h.allsec():
            h.delete_section(sec=sec)

    def load(f, gui=False):
        import os
        if gui:
            # remove `-nogui` for gui use
            os.environ["NEURON_MODULE_OPTIONS"] = ""

        from neuron import h
        import neuron_ext  # noqa: F401

        Cell.clean()
        #h.load_file(1, f)  # The first arg of '1' forces re-loading
        import os
        if not os.path.isabs(f):
            f = os.path.abspath(os.path.join(os.getcwd(), f))  # Convert to absolute path
        print(f"🔍 NEURON Loading File: {f}")  # Debugging output
        h.load_file(1, f)  
        return Cell(f, h.allsec())

    def __init__(self, src, allsec):
        self.src = src
        self.root = next(allsec)
        self.classify_soma()
        self.writers = writer.CollectiveWriter()

    @property
    def sections(self):
        return self.root.subtree()

    @property
    def segments(self):
        return it.chain(*((seg for seg in sec.allseg()) for sec in self.sections))

    @property
    def net_geom(self):
        return sum(
            (Cell.Geom(sec.volume(), sec.area(), sec.L) for sec in self.sections),
            Cell.Geom(),
        )

    @property
    def soma_geom(self):
        return sum(
            (Cell.Geom(sec.volume(), sec.area(), sec.L) for sec in [self.soma]),
            Cell.Geom(),
        )

    @property
    def axon_geom(self):
        return sum(
            (Cell.Geom(sec.volume(), sec.area(), sec.L) for sec in self.axon.subtree()),
            Cell.Geom(),
        )

    @property
    def dendrite_geom(self):
        return sum(
            (
                Cell.Geom(sec.volume(), sec.area(), sec.L)
                for sec in self.trunk.subtree()
            ),
            Cell.Geom(),
        )

    def adjust_soma(self):
        if self.soma:
            self.soma.round_shape()
        if self.axon:
            self.axon.adjust_position()
        if self.trunk:
            self.trunk.adjust_position()

    def add_writer(self, writer):
        self.writers.append(writer)

    def test_continuity(self, threshold=0.1):
        for sec in it.chain(self.axon.subtree(), self.trunk.subtree()):
            for i, d in enumerate(sec.diams()):
                if d < threshold:
                    print("%s %d %g" % (sec, i, sec.diam3d(i)))

    def run_litmus(self):
        from neuron import h, gui  # noqa: F401

        ic = h.IClamp(self.soma(0.5))
        ic.delay = 0
        ic.dur = 3000
        ic.amp = 3

        ps = self.soma.display_v()
        h.init()
        for t in range(0, 101, 10):
            h.continuerun(t)
            ps.exec_menu("Redraw Shape")
            self.writers.write_graph(f"litmus/{t:03d}", ps)

        vs = [seg.v for seg in self.segments]
        self.writers.plot_hist("litmus/hist_v", vs)

    def dye_heavy_branches(self, thr):
        ps = self.soma.display()
        self.soma.traverse(
            lambda _, s: thr < s.subtree_volume(), lambda s: ps.color(2, sec=s)
        )
        self.writers.write_graph(f"volume/{thr}", ps)

    def volume_map(self, min, max):
        ps = self.soma.display_v()
        for sec in self.trunk.subtree():
            sec.v = -np.clip(sec.subtree_volume(), min, max)
        ps.scale(-max, -min)
        self.writers.write_graph(f"volume/{min}_{max}", ps)

    def classify_soma(self):
        from neuron import h

        self.soma = self.root
        if "axon" in dir(h) and "sec" in dir(h.axon):
            self.axon = h.axon.sec
        else:
            self.axon = next(x for x in self.soma.children() if "axon" in x.name())
        if "trunk" in dir(h) and "sec" in dir(h.trunk):
            self.trunk = h.trunk.sec
        else:
            self.trunk = next(x for x in self.soma.children() if x != self.axon)
        h.distance(0, self.soma(0.5))

    def classify(self, threshold=1000):
        from neuron import h

        trunk_sections = getattr(h, "trunk_sections", None)
        branch_sections = getattr(h, "branch_sections", None)

        if trunk_sections and branch_sections:
            self.trunk_sections = list(trunk_sections)
            self.branch_sections = list(branch_sections)

            def f(_, x):
                if x in self.trunk_sections:
                    return True
                else:
                    self.branches.append(x)
                    return False
        else:
            self.trunk_sections = []
            self.branch_sections = []

            def f(_, x):
                if threshold < x.subtree_volume():
                    self.trunk_sections.append(x)
                    return True
                else:
                    self.branches.append(x)
                    self.branch_sections.extend(x.subtree())
                    return False

        self.branches = []
        self.trunk.traverse(f, lambda _: 0)
        self.writers.write_names("trunk_sections", [sec for sec in self.trunk_sections])
        self.writers.write_names("branches", [sec for sec in self.branches])

    def colorize(self, colors):
        num_colors = len(colors)

        for i, branch in enumerate(self.branches):
            for sec in branch.subtree():
                sec.v = i % num_colors + 1
        self.soma.v = 0
        for sec in self.axon.subtree():
            sec.v = 0

        ps = self.soma.display_v()
        ps.colormap(num_colors + 1)
        ps.colormap(0, 0, 0, 0)
        for i, color in enumerate(colors):
            ps.colormap(i + 1, *color)
        ps.scale(0, num_colors)

        self.writers.write_graph("branches", ps)

    def mark(self, name, segs, color=4, style="O", size=10):
        from neuron import h, gui  # noqa: F401

        ps = self.soma.display_shape()
        for seg in segs:
            ic = h.IClamp(seg)
            ps.point_mark(ic, color, style, size)
        self.writers.write_graph(name, ps)
