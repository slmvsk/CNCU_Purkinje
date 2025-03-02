import os
import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

from prelude import logger

plt.rcParams["font.size"] = 12
plt.rcParams["mathtext.fontset"] = "cm"
plt.rcParams["figure.autolayout"] = True
plt.rcParams["savefig.dpi"] = 300


def output_file_or_show(fig, f=None):
    if f is None:
        plt.show()
    else:
        os.makedirs(os.path.dirname(f) or ".", exist_ok=True)
        plt.savefig(f)
        fig.clf()
        plt.close()
        logger.say(f"create: {f}")


linestyles = [
    ("solid", "solid"),  # Same as (0, ()) or '-'
    ("dotted", "dotted"),  # Same as (0, (1, 1)) or ':'
    ("dashed", "dashed"),  # Same as '--'
    ("dashdot", "dashdot"),  # Same as '-.'
    ("loosely-dotted", (0, (1, 10))),
    ("dotted", (0, (1, 1))),
    ("densely-dotted", (0, (1, 1))),
    ("long-dash-with-offset", (5, (10, 3))),
    ("loosely-dashed", (0, (5, 10))),
    ("dashed", (0, (5, 5))),
    ("densely-dashed", (0, (5, 1))),
    ("loosely-dashdotted", (0, (3, 10, 1, 10))),
    ("dashdotted", (0, (3, 5, 1, 5))),
    ("densely-dashdotted", (0, (3, 1, 1, 1))),
    ("dashdotdotted", (0, (3, 5, 1, 5, 1, 5))),
    ("loosely-dashdotdotted", (0, (3, 10, 1, 10, 1, 10))),
    ("densely-dashdotdotted", (0, (3, 1, 1, 1, 1, 1))),
]


def plot_simple(
    serieses,
    f,
    twins=None,
    labels=None,
    styles=None,
    colors=None,
    title=None,
    note=None,
    xlabel=None,
    ylabel=None,
    xint=False,
    xlog=False,
    ylog=False,
    xlim=None,
    ylim=None,
    yzero_visible=None,
):
    if labels is None:
        labels = [None] * len(serieses)
    if styles is None:
        styles = [None] * len(serieses)
    if colors is None:
        colors = [None] * len(serieses)

    fig, ax = plt.subplots()
    for (xs, series), label, style, color in zip(serieses, labels, styles, colors):
        if xint:
            ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        ax.plot(
            xs,
            np.real(series),
            style or "-",
            label=label,
            color=color,
        )
    if note:
        ax.text(
            0.05,
            0.95,
            note,
            verticalalignment="top",
            transform=ax.transAxes,
            fontsize=8,
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.7),
        )

    if any(labels):
        ax.legend(loc="upper right")
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if xlog:
        ax.set_xscale("log")
    if ylog:
        ax.set_yscale("log")
    if yzero_visible:
        ax.axhline(0, c="gray", lw=0.2)

    if xlim is not None:
        x0, x1 = xlim
        pad = (x1 - x0) * 0.05
        ax.set_xlim([x0 - pad, x1 + pad])
    if ylim is not None:
        y0, y1 = ylim
        pad = (y1 - y0) * 0.05
        ax.set_ylim([y0 - pad, y1 + pad])
    else:
        # Set minimum range to avoid scientific notation get applied, which is confusing
        _, _, y0, y1 = ax.axis()
        if y1 - y0 < 0.001 and not ylog:
            y1 = y0 + 0.001
            pad = (y1 - y0) * 0.05
            ax.set_ylim([y0 - pad, y1 + pad])

    output_file_or_show(fig, f)


class ScaleSplitter:
    def __init__(self, xss, f=None):
        self.xss = xss
        self.f = f or (lambda x: x)
        self.res = list(self.calc())
        self.count = len(self.res)

    def __iter__(self):
        for x in self.res:
            yield x

    def calc(self):
        ranges = [max(*self.f(xs)) - min(*self.f(xs)) for xs in self.xss]
        print(ranges)
        xs = np.array(list(zip(ranges, np.zeros(len(ranges)))))
        bandwidth = estimate_bandwidth(xs, quantile=0.6) or None
        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(xs)

        _, idx = np.unique(ms.labels_, return_index=True)
        labels = ms.labels_[np.sort(idx)]
        for i in labels:
            yield [xs for label, xs in zip(ms.labels_, self.xss) if i == label]
