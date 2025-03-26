import os
import sys
import itertools as it
sys.path.append('/Users/tetianasalamovska/Downloads/Akicodes/src') 
from prelude import logger, Store, uniq
from runner import Runner, Spec, Injection, Recording
from try_set import TrySet
from plotter import plot_simple, ScaleSplitter
from exporter import write_file, write_geometry
from fourier import Fourier, CosineSimilarity
import color
import writer
from cell import Cell
#from neuron import h
#print(dir(writer))  # List all attributes of the writer module
os.environ["NEURON_MODULE_OPTIONS"] = "-nogui"

logger.verbose()
# Store.disable()

OUTPUT_DIR = "tmp/output"

PLOT_FINE_TIME = False
PLOT_FINE_VALUE = False
PLOT_PERIPHERAL = False
PLOT_CURRENT = True
PLOT_CURRENT_SUM = True
PLOT_FREQ = False
EXPORT_RESULT = False
EXPORT_GEOM = False #was True


def analyze_morphology(
    morphology,
    adjust_soma=False,
    litmus=False,
    classify_various=False,
    volume_map=False,
    colorize=False,
):
    
    #morphology_file = f"data/{morphology}.hoc"
    #print(f"🔍 Debug: Trying to load morphology from {morphology_file}")
    #cell = Cell.load(morphology_file, gui=True)
       
    cell = Cell.load(f"/Users/tetianasalamovska/Downloads/Akicodes/data/{morphology}.hoc", gui=True)   
    #cell = Cell.load(f"../data/{morphology}.hoc", gui=True)  # Move up a directory
    cell.test_continuity(0.1)

    cell.add_writer(writer.PngWriter(f"{OUTPUT_DIR}/{morphology}/analysis"))
    # cell.add_writer(writer.PdfWriter(f"{OUTPUT_DIR}/{morphology}/analysis"))
    cell.add_writer(writer.TextWriter(f"{OUTPUT_DIR}/{morphology}/analysis"))

    if adjust_soma:
        cell.adjust_soma()

    logger.info(f"Net: {cell.net_geom}")
    logger.info(f"Soma: {cell.soma_geom}")
    logger.info(f"Axon: {cell.axon_geom}")
    logger.info(f"Dendrite: {cell.dendrite_geom}")

    cell.classify()

    if litmus:
        cell.run_litmus()

    if classify_various:
        for thr in range(200, 1201, 200):
            cell.dye_heavy_branches(thr)

    if volume_map:
        min, max = (100, 1000)
        cell.volume_map(min, max)

    if colorize:
        pass
        #cell.colorize(color.round(16))

    if EXPORT_GEOM:
        write_geometry(cell.soma, f"{OUTPUT_DIR}/{morphology}/analysis/geom.hoc")


def capture(spec):
    morphology = spec.morphology
    Runner(spec).run_and_capture(
        writer.PngWriter(
            f"{OUTPUT_DIR}/{morphology}/capture/{spec.to_params('soma', 'axon', 'dend', 'tstop')}"
        ),
        step=spec.dt * 10,
    )

def recording_sites(morphology_or_spec, **params):
    if isinstance(morphology_or_spec, Spec):
        spec = morphology_or_spec
    else:
        spec = Spec(morphology=morphology_or_spec, **params)

    morphology = spec.morphology
    cell = Cell.load(f"../data/{morphology}.hoc", gui=True)

    name = "_".join(uniq(r.location.to_label() for r in spec.recordings))
    cell.add_writer(writer.PngWriter(f"{OUTPUT_DIR}/{morphology}/marks"))
    # cell.add_writer(writer.PdfWriter(f"{OUTPUT_DIR}/{morphology}/analysis"))

    if spec.adjust_soma:
        cell.adjust_soma()

    cell.classify()
    segs = list(dict.fromkeys(r.seg(cell) for r in spec.recordings))
    cell.mark(name, segs)


def xlims(spec):
    if PLOT_FINE_TIME:
        xs = uniq([(0, spec.tstop), (0, 300), (250, 300)])
        return [(x0, x1) for x0, x1 in xs if x1 <= spec.tstop]
    return [(0, spec.tstop)]


def filter_recs(recs):
    return [
        rec
        for rec in recs
        if (PLOT_CURRENT or not rec.is_current)
        and (PLOT_PERIPHERAL or not rec.is_peripheral)
    ]


def export_result(dir, runner, path_maker):
    spec = runner.spec
    recs = filter_recs(spec.recordings)
    for i, rec in enumerate(recs):
        dst = f"{dir}/{path_maker.make(spec, pre=rec.to_label())}.dat"
        _, xs = runner.get_result_at(i)
        write_file(xs, dst)


def plot_result(dir, runner, path_maker):
    spec = runner.spec
    recs = filter_recs(spec.recordings)
    locs = {r.location for r in recs}
    for loc in locs:
        irecs = [(i, r) for (i, r) in enumerate(recs) if loc == r.location]
        ss = ScaleSplitter(irecs, f=lambda irec: runner.get_result_at(irec[0])[1])
        for i, irecs in enumerate(ss):
            logger.info(f"ScaleSplitter: {i + 1}/{ss.count} -----------------------")
            logger.info([r for _, r in irecs])
            for xlim in xlims(spec):
                post = f"t_{xlim[0]}_{xlim[1]}"
                suffix = (1 < ss.count) and f"{i}" or None
                dst = f"{dir}/{path_maker.make(spec, pre=loc.to_label(), post=post, suffix=suffix)}.png"
                plot_simple(
                    [runner.get_result_at(i) for i, _ in irecs],
                    dst,
                    title=", ".join(x.to_label() for x in [loc, *spec.injections]),
                    note=spec.pp("soma", "axon", "dend"),
                    labels=[r.value for _, r in irecs],
                    xlabel="t [ms]",
                    xlim=xlim,
                )
        if PLOT_CURRENT_SUM:
            in_out = Recording.collect_in_out(recs)[loc].items()
            for label, recs_ in in_out:
                for xlim in xlims(spec):
                    plot_recs_sum_variations(
                        dir, label, recs_, runner, xlim, path_maker
                    )


def plot_recs_sum_variations(dir, label, recs, r, xlim, path_maker):
    def sum2(ts, *xss):
        return (ts, sum(xss))

    spec = runner.spec
    all = recs
    post = f"t_{xlim[0]}_{xlim[1]}"
    for j, recs in enumerate(it.combinations(all, max(len(all) - 1, 1))):
        suffix = f"{j}"
        dst = f"{dir}/{path_maker.make(spec, pre=label, post=post, suffix=suffix)}.png"
        all_series = sum2(*r.get_result_at(*[i for i, _ in all]))
        minmax = (min(all_series[1]), max(all_series[1]))
        plot_simple(
            [
                sum2(*r.get_result_at(*[i for i, _ in recs])),
                all_series,
            ],
            dst,
            title=label + ": " + ", ".join(rec.value for _, rec in all),
            note=spec.pp("soma", "axon", "dend"),
            labels=[
                "all - {"
                + ",".join(rec.value for _, rec in (set(all) - set(recs)))
                + "}",
                "all",
            ],
            xlabel="t [ms]",
            xlim=xlim,
            ylim=(max(-0.05, minmax[0]), min(0.05, minmax[1])),
            yzero_visible=True,
        )


class Freq:
    freqs = {}
    peaks = {}

    def get_freq(runner):
        spec = runner.spec
        if spec not in Freq.freqs:
            if spec.tstop < 50:
                Freq.freqs[spec] = ([], [])
            else:
                ts, vs, *_ = runner.result
                xs, ys = Fourier.transform(
                    ts, vs, offset=((spec.tstop < 600) and 50 or 300)
                )
                Freq.freqs[spec] = (xs, ys)
        return Freq.freqs[spec]

    def get_peaks(runner):
        spec = runner.spec
        if spec not in Freq.peaks:
            Freq.peaks[spec] = Fourier.find_peaks(*Freq.get_freq(runner))
        return Freq.peaks[spec]


def plot_spectrum(dir, runner, path_maker):
    dst = f"{dir}/{path_maker.make(runner.spec, pre='freq')}.png"
    peaks = Freq.get_peaks(runner) or [(0.0, 0.0)]
    plot_simple(
        [Freq.get_freq(runner), zip(*peaks)],
        dst,
        title=f"First peak: {peaks[0][0]:0.1f}Hz",
        xlabel="f [Hz]",
        ylabel="FFT Amplitude",
        styles=["-", "x"],
    )
    logger.info(f"First peak: {peaks}")


def plot_recording_variations(dir, runner):
    spec = runner.spec
    recs = filter_recs(spec.recordings)
    vars = {}
    for i, rec in enumerate(recs):
        vars.setdefault(rec.value, [])
        vars[rec.value].append((i, rec))

    vars = {k: rs for k, rs in vars.items() if 1 < len(rs)}
    for val, recs in vars.items():
        for xlim in xlims(spec):
            var = f"recordings--t_{xlim[0]}_{xlim[1]}"
            base = f"{spec.to_params('soma', 'axon', 'dend')}" or "_"
            inj = spec.injections and spec.to_params('inj') or None
            basename = "--".join(s for s in [base, val, inj] if s)
            dst = f"{dir}/{var}/{basename}.png"

            ts, *xss = runner.result
            xss = [xss[i] for i, _ in recs]
            ylims = [None]
            if PLOT_FINE_VALUE and val == "v":
                ylims = [*ylims, (-68, -52), (-60, -55)]

            for ylim in ylims:
                basename_ = basename + (ylim and f"--y_{ylim[0]}_{ylim[1]}" or "")
                dst = f"{dir}/{var}/{basename_}.png"
                plot_simple(
                    [(ts, xs) for xs in xss],
                    dst,
                    title=", ".join([val, *[x.to_label() for x in spec.injections]]),
                    note=spec.pp("soma", "axon", "dend"),
                    labels=[rec.location.to_label() for _, rec in recs],
                    xlabel="t [ms]",
                    xlim=xlim,
                    ylim=ylim,
                )


def plot_injection_variations(dir, runners):
    vars = {}
    for r in runners:
        k = r.spec(injections=None)
        vars.setdefault(k, [])
        vars[k].append(r)

    for spec, rs in vars.items():
        recs = filter_recs(spec.recordings)
        soma_in_out = Recording.collect_in_out(recs)[recs[0].location].items()
        for xlim in xlims(spec):
            var = f"injections--t_{xlim[0]}_{xlim[1]}"
            basename = f"{spec.to_params('soma', 'axon', 'dend')}" or "_"
            for i, rec in enumerate(recs):
                dst = f"{dir}/{var}/{basename}--{rec.to_label()}.png"

                plot_simple(
                    [r.get_result_at(i) for r in rs],
                    dst,
                    title=rec.to_label(),
                    note=spec.pp("soma", "axon", "dend"),
                    labels=[
                        ",".join(
                            inj.to_label()
                            for inj in (r.spec.injections or [Injection()])
                        )
                        for r in rs
                    ],
                    xlabel="t [ms]",
                    xlim=xlim,
                )
            if PLOT_CURRENT_SUM:
                for label, recs_ in soma_in_out:
                    dst = f"{dir}/{var}/{basename}--{label}.png"
                    plot_recs_sum_injection_variations(
                        dst, label, recs_, spec, rs, xlim
                    )


def plot_recs_sum_injection_variations(dst, label, recs, spec, runners, xlim):
    def sum2(ts, *xss):
        return (ts, sum(xss))

    plot_simple(
        [sum2(*r.get_result_at(*[i for i, _ in recs])) for r in runners],
        dst,
        title=label + ": " + ", ".join(rec.value for _, rec in recs),
        note=spec.pp("soma", "axon", "dend"),
        labels=[
            ",".join(inj.to_label() for inj in (r.spec.injections or [Injection()]))
            for r in runners
        ],
        xlabel="t [ms]",
        xlim=xlim,
        ylim=(-0.05, 0.05),
        yzero_visible=True,
    )


def plot_fi_curve(dir, runners, path_maker):
    vars = {}
    for r in runners:
        k = r.spec(injections=None)
        vars.setdefault(k, [])
        vars[k].append(r)

    vars = {k: rs for k, rs in vars.items() if 1 < len(rs)}
    if not vars:
        return

    for spec, rs in vars.items():
        peaks = [
            (
                (r.spec.injections and r.spec.injections[0].amp or 0.0),
                Freq.get_peaks(r) and Freq.get_peaks(r)[0] or (0.0, 0.0),
            )
            for r in rs
        ]
        peaks = [(x, y[0]) for x, y in peaks if y]
        dst = f"{dir}/{path_maker.bio(runner.spec)}/fi.png"
        print(f"FI curve will be saved at: {dst}")  # Debugging line
        plot_simple(
            [zip(*peaks)],
            dst,
            title="FI curve",
            xlabel="Current [nA]",
            ylabel="Frequency [Hz]",
            styles=["^:"],
        )


class PathMaker:
    def guess_scope(specs):
        vars = {}
        for s in specs:
            k = s(injections=None)
            vars.setdefault(k, [])
            vars[k].append(s)

        vars = {k: ss for k, ss in vars.items() if 1 < len(ss)}
        if len(vars) == 1:
            return "inj"
        return "bio"

    def __init__(self, specs):
        self.scope = PathMaker.guess_scope(specs)

    def bio(self, spec):
        return f"{spec.to_params('soma', 'axon', 'dend')}"

    def inj(self, spec, init=False):
        if init and not spec.injections:
            spec = spec(injections=[Injection()])
        return spec.to_params("inj")

    def make(self, spec, pre=None, post=None, suffix=None):
        if self.scope == "bio":
            var = "--".join(
                x
                for x in [pre, *(spec.injections and [self.inj(spec)] or []), post]
                if x
            )
            basename = self.bio(spec)
        elif self.scope == "inj":
            bio = self.bio(spec)
            var = "--".join(x for x in [bio, post] if x)
            basename = "--".join(x for x in [pre, self.inj(spec, init=True)])
        basename = "--".join(x for x in [basename, suffix] if x)
        return f"{var or '_'}/{basename or '_'}"


def stats(tries):
    specs = sum([Runner.expand(*getattr(TrySet, k)()) for k in tries], [])
    time_weight = {
        "human/original": 60 / 300,  # 1hour ~ 300ms
        "zang2021/fig3": 10 / 300,  # 10min ~ 300ms
        "macaque/Axon_withellipse": 10 / 300,  # unknown, but set as the rat anyway
    }
    time_spent = {}

    per_morphology = {}
    for s in specs:
        k = s.morphology
        per_morphology.setdefault(k, [])
        per_morphology[k].append(s)

    for m, ss in per_morphology.items():
        print(f"Morphology: {m}")
        print(f"  Simulations: {len(ss)}")

        per_biophysics = {}
        for s in ss:
            k = s(dt=None, tstop=None, recordings=None, injections=None)
            per_biophysics.setdefault(k, [])
            per_biophysics[k].append(s)

        print(f"  Biophysics variations: {len(per_biophysics)}")

        w = time_weight[m]
        time_spent[m] = sum(s.tstop * w for s in ss)
        print(f"  Time spent: {int(time_spent[m] / 60)} hours")

    print("Total")
    print(f"  Simulations: {len(specs)}")

import matplotlib.pyplot as plt
from collections import defaultdict
import pandas as pd
import os

def plot_ca(runner, variables=None, output_dir="exported_traces"):
    """
    Plot and export traces for each variable across locations.

    Args:
        runner: Runner object with .spec and .get_result_at().
        variables: List of variable names to plot and save (e.g., ['v', 'cai', 'ica']).
        output_dir: Directory to save CSV files to.
    """
    spec = runner.spec
    recordings = spec.recordings

    os.makedirs(output_dir, exist_ok=True)

    # Group recordings by variable (e.g., 'v', 'cai', 'ica', etc.)
    variable_map = defaultdict(list)
    for i, rec in enumerate(recordings):
        variable_map[rec.value].append((i, rec))

    if variables is not None:
        variable_map = {k: v for k, v in variable_map.items() if k in variables}

    for var, entries in variable_map.items():
        plt.figure(figsize=(10, 6))
        df = None  # Initialize DataFrame for this variable

        for i, rec in entries:
            ts, vs = runner.get_result_at(i)
            label = f"{rec.section}({rec.position})"
            plt.plot(ts, vs, label=label)

            # Add to DataFrame for CSV
            if df is None:
                df = pd.DataFrame({"time_ms": ts})
            df[label] = vs

        # Save CSV
        if df is not None:
            csv_path = os.path.join(output_dir, f"{var}_traces.csv")
            df.to_csv(csv_path, index=False)
            print(f"✅ Saved: {csv_path}")

        # Plot display
        plt.title(f"{var} traces across locations")
        plt.xlabel("Time [ms]")
        plt.ylabel(var)
        #plt.yscale("log")  # Add this before plt.legend() to use logarithmic scale
        plt.legend()
        plt.tight_layout()
        plt.show()



if __name__ == "__main__":
    analyze_morphology("human/original", adjust_soma=True, colorize=True)
    #analyze_morphology("macaque/macaque_original", adjust_soma=True, colorize=True)
    #analyze_morphology("zang2021/fig3", colorize=True)
    # analyze_morphology("macaque/Axon_withellipse", colorize=True)
    #capture(TrySet.human_original_base)
    #capture(TrySet.human_original_nice)
    #recording_sites(
        #"human/original",
        #adjust_soma=True,
        #recordings=[
            #("soma", 0.5),
            #("branches[100]", 0.0),
        #],
    #)
    recording_sites(Runner.expand(*TrySet.try_ca_recordings())[0]) # uncomment above for original one 
    #recording_sites(Runner.expand(*TrySet.try_ca_recordings()))
    # recording_sites(Runner.expand(*TrySet.try17())[0])
    # recording_sites(Runner.expand(*TrySet.try57())[0])
    # recording_sites(Runner.expand(*TrySet.try61())[0])
    # recording_sites(Runner.expand(*TrySet.try64())[0])
    # recording_sites(Runner.expand(*TrySet.try99())[0])

    if sys.argv[1:]:
        tries = sys.argv[1:]
    else:
        tries = TrySet.all[-1:]
    tries = ["try_ca_recordings"]
    # stats(TrySet.all)
    cs = None
    # cs = CosineSimilarity(next(TrySet.try04()).result)
    for k in tries:
        logger.info(f"TrySet: {k}")
        specs = getattr(TrySet, k)()
        pm = PathMaker(Runner.expand(*specs))
        runners = []
        for runner in Runner.product(*specs):
            runners.append(runner)
            spec = runner.spec
            #plot_recording_variations(f"{OUTPUT_DIR}/{spec.morphology}/{k}", runner)
            #plot_result(f"{OUTPUT_DIR}/{spec.morphology}/{k}", runner, pm) # uncomment
            plot_ca(runner)
            if EXPORT_RESULT:
                export_result(f"{OUTPUT_DIR}/{spec.morphology}/{k}", runner, pm)
            if PLOT_FREQ:
                plot_spectrum(f"{OUTPUT_DIR}/{spec.morphology}/{k}", runner, pm)
                if cs:
                    ts, vs, *_ = runner.result
                    similarity = cs.calc((ts, vs))
                    logger.info(f"Similarity: {similarity}")
        plot_injection_variations(f"{OUTPUT_DIR}/{spec.morphology}/{k}", runners)
        if PLOT_FREQ:
            plot_fi_curve(f"{OUTPUT_DIR}/{spec.morphology}/{k}", runners, pm)
        
