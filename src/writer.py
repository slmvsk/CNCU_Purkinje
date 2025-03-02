import os
import subprocess
import contextlib as ctx
import tempfile
#from wand.image import Image
import matplotlib.pyplot as plt


def export(file, ps):
    os.makedirs(os.path.dirname(file), exist_ok=True)
    with ctx.suppress(FileNotFoundError):
        os.remove(file)
    ext = os.path.splitext(file)[-1]
    if ext == ".ps":
        ps.printfile(file)
    else:
        pass
        

def plot_hist(file, xs):
    with ctx.suppress(FileNotFoundError):
        os.remove(file)
    fig, ax = plt.subplots()
    ax.hist(xs, bins=100)
    plt.savefig(file, dpi=300)


def convert_ps(src, dst):
    subprocess.call(["ps2pdf", "-dEPSCrop", "-dEPSFitPage", src, dst])


class CollectiveWriter(list):
    def __init__(self, key=""):
        self.key = key

    def write_graph(self, key, ps):
        key = os.path.join(self.key, key)
        for writer in self:
            writer.write_graph(key, ps)

    def plot_hist(self, key, xs):
        key = os.path.join(self.key, key)
        for writer in self:
            writer.plot_hist(key, xs)

    def write_names(self, key, names):
        key = os.path.join(self.key, key)
        for writer in self:
            writer.write_names(key, names)


class FileWriter:
    def __init__(self, dir):
        self.dir = dir

    def path_for(self, key, ext="", ensure_dir=True):
        dst = os.path.join(self.dir, f"{key}{ext}")
        if ensure_dir:
            self.ensure_dir(dst)
        return dst

    def ensure_dir(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)

    def write_graph(self, key, ps):
        pass

    def plot_hist(self, key, xs):
        pass

    def write_names(self, key, names):
        pass


class PngWriter(FileWriter):
    def write_graph(self, key, ps):
        dst = self.path_for(key, ".png")
        export(dst, ps)

    def plot_hist(self, key, xs):
        dst = self.path_for(key, ".png")
        plot_hist(dst, list(xs))


class PdfWriter(FileWriter):
    def write_graph(self, key, ps):
        with tempfile.TemporaryDirectory() as dir:
            tmp = os.path.join(dir, "tmp.ps")
            dst = self.path_for(key, ".pdf")
            export(tmp, ps)
            convert_ps(tmp, dst)

    def plot_hist(self, key, xs):
        dst = self.path_for(key, ".pdf")
        plot_hist(dst, list(xs))


class TextWriter(FileWriter):
    def write_names(self, key, names):
        dst = self.path_for(key, ".txt")
        with open(dst, mode="w") as f:
            for name in names:
                f.write(f"{name}\n")
