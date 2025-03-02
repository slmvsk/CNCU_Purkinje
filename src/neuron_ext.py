from scipy.interpolate import interp1d
import numpy as np
from neuron import h, nrn


class Box:
    def __init__(self):
        self.min = None
        self.max = None

    def __repr__(self):
        return {"min": self.min, "max": self.max}.__repr__()

    def include(self, pt):
        if self.min is None or self.max is None:
            self.min = pt
            self.max = pt
        else:
            self.min = [min(x, y) for x, y in zip(self.min, pt)]
            self.max = [max(x, y) for x, y in zip(self.max, pt)]

    @property
    def size(self):
        if self.min and self.max:
            return [max - min for min, max in zip(self.min, self.max)]

    @property
    def center(self):
        if self.min and self.max:
            return [(max + min) / 2 for min, max in zip(self.min, self.max)]


class Section:
    _volumes = {}

    def diams(self):
        return (self.diam3d(i) for i in range(self.n3d()))

    def points(self):
        return (
            (self.x3d(i), self.y3d(i), self.z3d(i), self.diam3d(i))
            for i in range(self.n3d())
        )

    def bounding_box(self):
        box = Box()
        for sec in self.subtree():
            for pt in sec.points():
                box.include(pt)
        return box

    def area(self):
        return sum(seg.area() for seg in self.allseg())

    def volume(self):
        return sum(seg.volume() for seg in self.allseg())

    # Returns the net volume of the subtree, not the volume of a single section.
    def subtree_volume(self):
        if self.name not in Section._volumes:
            Section._volumes[self.name] = self.volume() + sum(
                s.subtree_volume() for s in self.children()
            )
        return Section._volumes[self.name]

    def translate(self, v):
        for i, pt in enumerate(self.points()):
            self.pt3dchange(i, *(np.array(pt) + np.array([*v, 0])))

    def round_shape(self):
        x, y, z, _ = np.mean(list(self.points()), axis=0)
        d = np.max(list(self.diams()))
        r = d / 2
        self.pt3dclear()

        n = 32
        for theta in np.linspace(np.pi, 0, n + 1):
            dx = r * np.cos(theta)
            d_ = r * np.sin(theta) * 2
            self.pt3dadd(x + dx, y, z, d_)

    def adjust_position(self):
        x, y, z, d = np.mean(list(self.parentseg().sec.points()), axis=0)
        pt0 = np.array([x, y, z])
        r = d / 2
        pt1 = next(self.points())[0:3]
        diff = pt1 - pt0
        dist = np.sqrt(sum(diff**2))
        self.translate(-(1 - r / dist) * diff)

    def traverse(self, pred, f):
        res = [f(self)]
        for s in self.children():
            if pred(self, s):
                res.extend(s.traverse(pred, f))
        return res

    def display(self, width=1200, height=1200):
        box = self.bounding_box()
        size = box.size
        view = (box.min[0], box.min[1], size[0], size[1], 0, 0, width, height)
        ps = h.PlotShape(False)
        ps.view(*view)
        ps.show(0)
        return ps

    def display_v(self, **kwargs):
        ps = self.display(**kwargs)
        ps.exec_menu("Shape Plot")
        return ps

    def display_shape(self, width=1200, height=1200):
        box = self.bounding_box()
        size = box.size
        view = (box.min[0], box.min[1], size[0], size[1], 0, 0, width, height)
        ps = h.Shape(False)
        ps.view(*view)
        ps.show(0)
        return ps


nrn.Section.diams = Section.diams
nrn.Section.points = Section.points
nrn.Section.bounding_box = Section.bounding_box
nrn.Section.area = Section.area
nrn.Section.volume = Section.volume
nrn.Section.subtree_volume = Section.subtree_volume
nrn.Section.translate = Section.translate
nrn.Section.round_shape = Section.round_shape
nrn.Section.adjust_position = Section.adjust_position
nrn.Section.traverse = Section.traverse
nrn.Section.display = Section.display
nrn.Section.display_v = Section.display_v
nrn.Section.display_shape = Section.display_shape


class Segment:
    def point(self):
        pts = np.array(list(self.sec.points()))
        interp = interp1d(np.linspace(0, 1, len(pts)), pts, axis=0)
        return interp(self.x)


nrn.Segment.point = Segment.point
