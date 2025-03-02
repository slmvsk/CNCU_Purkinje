import os
import numpy as np

from prelude import logger


def write_file(data, f):
    os.makedirs(os.path.dirname(f) or ".", exist_ok=True)
    with open(f, mode="w") as io:
        for x in data:
            io.write(f"{x}\n")
    logger.say(f"create: {f}")


def seg_point(seg):
    sec = seg.sec
    return [
        np.interp(seg.x, np.linspace(0, 1, sec.n3d()), [pt[i] for pt in sec.points()])
        for i in range(0, 3)
    ]


def str_pt(pt):
    return f"({','.join(str(x) for x in pt)})"


def to_geom(sec):
    lcpt = None
    if sec.pt3dstyle():
        lcpt = seg_point(sec.parentseg())
    return "\n".join(
        [
            f"{sec.name()}" + " {pt3dclear()",
            *(lcpt and [f"  pt3dstyle{str_pt([1, *lcpt])}"] or []),
            *(f"  pt3dadd{str_pt(pt)}" for pt in sec.points()),
            "}",
        ]
    )


def write_geometry(sec, f):
    os.makedirs(os.path.dirname(f) or ".", exist_ok=True)
    with open(f, mode="w") as io:
        for s in sec.subtree():
            io.write(f"{to_geom(s)}\n")
    logger.say(f"create: {f}")
