import numpy as np
from scipy.interpolate import interp1d
from scipy.signal import find_peaks


CUTOFF = 400  # Maximum frequency for Fourier analysis


def zip_filter(xs, ys, pred):
    xys = [(x, y) for x, y in zip(xs, ys) if pred(x, y)]
    return tuple(np.transpose(xys))


class Fourier:
    def transform(ts, vs, offset):
        dt = (ts[-1] - ts[0]) / (len(ts) - 1)
        ts, vs = zip_filter(ts, vs, lambda t, _: offset <= t)
        n = len(ts)
        xs = np.fft.rfftfreq(n, d=dt) * 1000
        ys = np.abs(np.fft.rfft(vs) / n)
        xs, ys = zip_filter(xs, ys, lambda x, _: 0 < x and x < CUTOFF)
        return xs, ys

    def find_peaks(xs, ys):
        return [(xs[i], ys[i]) for i in find_peaks(ys, height=0.2, distance=10)[0]]


class CosineSimilarity:
    def __init__(self, ref, offset=50, cutoff=400):
        self.ref = ref
        self.offset = offset
        self.cutoff = cutoff

    def calc(self, obj):
        ref_ts, ref_vs = self.ref
        obj_ts, obj_vs = obj

        ref_dt = (ref_ts[-1] - ref_ts[0]) / (len(ref_ts) - 1)
        obj_dt = (obj_ts[-1] - obj_ts[0]) / (len(obj_ts) - 1)
        dt = min(ref_dt, obj_dt)

        ts = np.arange(self.offset, max(ref_ts[-1], obj_ts[-1]), dt)
        fs = np.fft.rfftfreq(len(ts), d=dt) * 1000

        def transform(xs, ys):
            interp = interp1d(xs, ys, bounds_error=False, fill_value=0)
            ys = np.abs(np.fft.rfft(interp(ts)))
            _, ys = zip_filter(fs, ys, lambda f, _: 0 < f and f < self.cutoff)
            return ys / np.linalg.norm(ys)

        ref_fs = transform(ref_ts, ref_vs)
        obj_fs = transform(obj_ts, obj_vs)
        return np.dot(ref_fs, obj_fs)
