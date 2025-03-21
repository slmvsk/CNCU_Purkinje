import os
from dataclasses import dataclass, fields, field, make_dataclass, asdict, astuple
from functools import reduce
import numpy as np
import itertools as it
import operator
from multiprocessing import Process
import re
from prelude import logger, with_store, read_store
from neuron import h

#def read_current_mod():
    #arch = os.uname().machine
    #try:
        #path = os.readlink(arch)
        #return os.path.basename(path)
    #except FileNotFoundError as e:
        #logger.warn(f"Not ready: {arch}")
        #raise e

import logging

logger = logging.getLogger(__name__)

def read_current_mod():
    arch = os.uname().machine  # Detect system architecture
    try:
        if os.path.exists(arch):  # Check if the symlink exists
            print(f"arch: {arch}")
            if os.path.islink(arch):
                path = os.readlink(arch)  # Only use readlink if it's a symlink
            else:
                    path = arch  # Directly assign if it's just a string like "arm64", I changed here 
            return os.path.basename(path)
        else:
            logger.warning(f"⚠️ No architecture file found for {arch}. Using default.")
            return None  # Return None instead of raising an error
    except FileNotFoundError:
        logger.warning(f"⚠️ Not ready: {arch}. Architecture file is missing.")
        return None  # Handle missing file more gracefully




DEFAULT_MOD = "6c2f1f7e692fc73cca2f00514622c0b6221da9b5"


@dataclass(frozen=True)
class Pointing:
    section: str = "soma"
    position: float = 0.5

    def to_label(self):
        return f"{self.section}({self.position})"

    @property
    def location(self):
        return Pointing(self.section, self.position)

    @property
    def is_peripheral(self):
        return self.location != Pointing.center

    def loc(self, cell):
        return self.seg(cell).point()[0:3]

    #def seg(self, cell):
        #return self.sec(cell)(self.position)
    def seg(self, cell):
        sec = self.sec(cell)

        # Case 1: It's a Section – return the Segment at the given position
        if hasattr(sec, 'psection') and callable(getattr(sec, '__call__', None)):
            return sec(self.position)

        #  Case 2: It's already a Segment
        if hasattr(sec, 'v') and hasattr(sec, 'x'):
            return sec

        raise TypeError(f"❌ Unexpected section or segment: {self.section} → Got: {type(sec)}, Object: {sec}")

    #def sec(self, cell):
        #m = re.match(r"([\w\d_]+)\[(\d+)\]", self.section)
        #if m:
            #return getattr(cell, m[1])[int(m[2])]
        #return getattr(cell, self.section)
        
    def sec(self, cell):
        m = re.match(r"([\w\d_]+)\[(\d+)\]", self.section)
        if m:
            name, idx = m[1], int(m[2])
            sec_obj = getattr(cell, name, None) or getattr(h, name, None)

            # Try direct indexing if possible
            try:
                return sec_obj[idx]
            except (TypeError, AttributeError):
                raise TypeError(f"Section {name} is not indexable or doesn't exist.")
    
        # Fallback to non-indexed section
        return getattr(cell, self.section, None) or getattr(h, self.section)
    
    


Pointing.center = Pointing()


@dataclass(frozen=True)
class Recording(Pointing):
    value: str = "v"

    def to_label(self):
        return f"{super().to_label()}.{self.value}"

    def to_params(self):
        return self.to_label()

    def ref(self, cell):
        return self.ref_at(self.seg(cell))

    def ref_at(self, seg):
        return getattr(seg, f"_ref_{self.value}")

    @property
    def is_inward(self):
        prefix = self.value.split("_")[0].lower()
        return prefix in ["i", "ina", "ica"]

    @property
    def is_outward(self):
        prefix = self.value.split("_")[0].lower()
        return prefix in ["ik"]

    @property
    def is_current(self):
        return self.is_inward or self.is_outward


    #def wrap(obj):
        #if type(obj) is Recording:
            #return obj
        #if type(obj) is dict:
            #return Recording(**obj)
        #else:
            #return Recording(*obj)
    
    def wrap(obj):
        #print(f"DEBUG: Recording.wrap received -> {obj} (Type: {type(obj)}, Length: {len(obj) if hasattr(obj, '__len__') else 'N/A'})")
        if isinstance(obj, Recording):  #  Already a Recording object, return as-is
            return obj
        elif isinstance(obj, dict):  # Convert dict to Recording
            return Recording(**obj)
        elif isinstance(obj, (tuple, list)):  
            if len(obj) == 3:
                section, position, value = obj  # Explicit unpacking
                return Recording(section=section, position=position, value=value)  # Explicit assignment
            else:
                raise TypeError(f" Unexpected tuple/list format: {obj}, Length: {len(obj)}")
        else:
            raise TypeError(f" Unexpected input type for Recording: {type(obj)}, Value: {obj}")
            

    def collect_in_out(recordings):
        res = {}
        for i, rec in enumerate(recordings):
            pt = rec.location
            res.setdefault(pt, {})
            if rec.is_inward:
                k = f"{pt.to_label()}.inwards"
                res[pt].setdefault(k, [])
                res[pt][k].append((i, rec))
            if rec.is_outward:
                k = f"{pt.to_label()}.outwards"
                res[pt].setdefault(k, [])
                res[pt][k].append((i, rec))
        return res


@dataclass(frozen=True)
class Injection(Pointing):
    amp: float = 0.0
    delay: float = None
    dur: float = None

    def to_label(self):
        if self.location == Pointing().location:
            return f"[{self.amp:.2f}nA]"
        else:
            return f"{super().to_label()}[{self.amp:.2f}nA]"

    def to_params(self):
        if self.location == Pointing().location:
            return f"[{self.amp:.2f}]"
        else:
            return f"{super().to_label()}[{self.amp:.2f}]"

    def wrap(obj):
        if type(obj) is Injection:
            return obj
        if type(obj) is dict:
            return Injection(**obj)
        else:
            return Injection(*obj)


@dataclass(frozen=True)
class Spec:
    morphology: str = ""
    adjust_soma: bool = None
    soma_gbar_naRsg: float = None
    soma_gbar_nap: float = None
    soma_gbar_Kv3: float = None
    soma_gbar_mslo: float = None
    soma_gabkbar_abBK: float = None
    soma_gkbar_SK2: float = None
    soma_pcabar_newCaP: float = None
    soma_vshift_newCaP: float = None
    soma_pcabar_CaT3_1: float = None
    axon_gbar_naRsg: float = None
    axon_gbar_nap: float = None
    axon_gbar_Kv3: float = None
    axon_gbar_mslo: float = None
    axon_gabkbar_abBK: float = None
    axon_gkbar_SK2: float = None
    dend_gbar_naRsg: float = None
    dend_gbar_nap: float = None
    dend_gbar_Kv1: float = None
    dend_gbar_Kv3: float = None
    dend_gbar_Kv4: float = None
    dend_gbar_Kv4s: float = None
    dend_gbar_mslo: float = None
    dend_gkbar_SK2: float = None
    dend_pcabar_newCaP: float = None
    dend_vshift_newCaP: float = None
    dend_pcabar_CaT3_1: float = None

    celsius: float = 34.0
    dt: float = 0.02
    tstop: int = 300

    recordings: list[Recording] = field(default_factory=lambda: [Recording()])
    injections: list[Injection] = field(default_factory=list)

    def __post_init__(self):
        #print(f"DEBUG: __post_init__() received recordings -> {self.recordings}")  # Added this line
        if self.recordings is not None:
            object.__setattr__(
                self, "recordings", [Recording.wrap(r) for r in self.recordings]
            )
        if self.injections is not None:
            object.__setattr__(
                self, "injections", [Injection.wrap(r) for r in self.injections]
            )

    def __iter__(self):
        return self.values

    def __call__(self, **kwargs):
        return self.__class__(**(self.to_dict() | kwargs))

    def __hash__(self):
        def list_to_tuple(x):
            if type(x) is list:
                return tuple(x)
            else:
                return x

        xs = [list_to_tuple(x) for x in astuple(self)]
        return hash(tuple(xs))

    def items(self, *filters):
        kvs = ((f, getattr(self, f)) for f in self.__dataclass_fields__)
        kvs = [(k, v) for k, v in kvs if v is not None]
        if filters:
            kvs = list(
                it.chain(
                    *([(k, v) for k, v in kvs if k.startswith(f)] for f in filters)
                )
            )
        return kvs

    @property
    def values(self):
        return (getattr(self, f) for f in self.__dataclass_fields__)

    def to_dict(self):
        return asdict(self)

    def to_key(self):
        default = Spec()
        fallbacks = {}
        # When having defaults in certain attrs, fallback to None.
        for k in ["recordings", "injections"]:
            if getattr(self, k) == getattr(default, k):
                fallbacks[k] = None
        if fallbacks:
            return [(k, v) for k, v in self(**fallbacks).to_dict().items()]
        else:
            return [(k, v) for k, v in self.to_dict().items()]

    def to_params(self, *filters):
        def to_s(v):
            if type(v) is list:
                return "_".join([to_s(w) for w in v])
            if type(v) is dict:
                return to_s([w for w in v.values() if w is not None])
            if hasattr(v, "to_params"):
                return v.to_params()
            else:
                return str(v)

        items = [(k, to_s(v)) for k, v in self.items(*filters)]
        return "-".join(f"{k}_{v}" for k, v in items).replace("/", "_")

    def pp(self, *filters, sep="\n"):
        items = self.items(*filters)
        return sep.join(f"{k}: {v}" for k, v in items).replace("/", "_")

    def lift(self):
        return SpecSet(*([v] for v in self))


SpecSetBase = make_dataclass(
    "SpecSetBase",
    ((fld.name, list[fld.type], field(default_factory=list)) for fld in fields(Spec)),
    frozen=True,
)


@dataclass(frozen=True)
class SpecSet(SpecSetBase):
    def __iter__(self):
        vss = [([d] if vs == [] else vs) for vs, d in zip(self.values, Spec().values)]
        return (Spec(*vs) for vs in it.product(*vss))

    def __add__(self, other):
        return self.__class__(
            *(stable_uniq(xs + ys) for xs, ys in zip(self.values, other.values))
        )

    def __call__(self, **kwargs):
        return self.__class__(**(self.to_dict() | kwargs))

    def to_dict(self):
        return asdict(self)

    @property
    def values(self):
        return (getattr(self, f) for f in self.__dataclass_fields__)

    def accum(xs):
        return reduce(operator.add, (x.lift() for x in xs))

    def scope(self, *ks):
        for si in self.__class__(**{k: getattr(self, k) for k in ks}):
            yield si, self(**{k: [getattr(si, k)] for k in ks})


def stable_uniq(xs):
    res = []
    for x in xs:
        if x not in res:
            res.append(x)
    return res


class Runner:
    @staticmethod
    def expand(*specss):
        return list(it.chain(*specss))

    @staticmethod
    def product(*specss, **kwargs):
        if kwargs:
            if not specss:
                specss = [SpecSet()]
            specss = [s(**kwargs) for s in specss]
        logger.info(list(specss))
        specs = list(it.chain(*specss))
        count = len(specs)
        for i, s in enumerate(specs):
            logger.info(f"{i+ 1}/{count}")
            p = Process(target=Runner._execute, args=astuple(s))
            p.start()
            p.join()
            yield Runner(s)

    @staticmethod
    def _execute(*spec):
        Runner(Spec(*spec)).execute()

    def __init__(self, spec):
        self.spec = spec
        self._result = None

        self.store_key = self.spec.to_key()
        mod = read_current_mod()
        if mod != DEFAULT_MOD:
            self.store_key = [*self.store_key, ("mod", mod)]

    def setup(self):
        from cell import Cell
        from cell.config import Config

        #self.cell = Cell.load(f"data/{self.spec.morphology}.hoc")
        self.cell = Cell.load(f"../data/{self.spec.morphology}.hoc")
        cell = self.cell
        cell.classify()
        if self.spec.adjust_soma:
            cell.adjust_soma()
        config = Config(
            soma=[cell.soma],
            axon=cell.axon.subtree(),
            trunk=cell.trunk_sections,
            branch=cell.branch_sections,
        )
        config.configure(**self.spec.to_dict())
        config.apply()

    def run(self):
        from neuron import h
        from neuron import gui  # noqa: F401, Required for simulation runner, ie h.init(), h.run()

        self.setup()
        self.recs = [h.Vector()]
        self.recs[0].record(h._ref_t)
        for r in self.spec.recordings:
            self.recs.append(h.Vector())
            self.recs[-1].record(r.ref(self.cell))
        for inj in self.spec.injections:
            ic = h.IClamp(inj.seg(self.cell))
            ic.amp = inj.amp
            ic.delay = inj.delay or 0.0
            ic.dur = inj.dur or self.spec.tstop

        h.celsius = self.spec.celsius
        h.dt = self.spec.dt
        h.tstop = self.spec.tstop
        h.steps_per_ms = 1.0 / h.dt
        v_init = -70
        h.finitialize(v_init)
        h.continuerun(h.tstop)
        return [np.array(rec) for rec in self.recs]

    def execute(self):
        logger.info(self.spec)
        self._result = with_store(
            self.store_key,
            "voltages",
            self.run,
            # force=True,
        )

    @property
    #def result(self):
        #if self._result is None:
            #self._result = read_store(self.store_key, "voltages")
        #return self._result
    def result(self):
        if self._result is None:
            print(f"DEBUG: No cached result found. Trying to read from store_key: {self.store_key}")
        self._result = read_store(self.store_key, "voltages")
        if self._result is None:
            print("ERROR: read_store() returned None. No results found.")
        return self._result

    #def get_result_at(self, *idxs):
        #if self.result is None:
            #raise ValueError(" No simulation result found. Check for errors in NEURON execution.")
            #ts, *xss = self.result
            #return (ts, *[xss[i] for i in idxs])
    
    def get_result_at(self, *idxs):
        if self.result is None:
            raise ValueError("No simulation result found. Check for errors in NEURON execution.")

        print(f" DEBUG: Simulation result found. Fetching indexes {idxs}")

        ts, *xss = self.result  # Unpack results
        return (ts, *[xss[i] for i in idxs])
        

    def run_and_capture(self, writer, step=10):
        # remove `-nogui` for gui use, should be done before importing neuron module
        os.environ["NEURON_MODULE_OPTIONS"] = ""

        from neuron import h, gui  # noqa: F401

        self.setup()
        h.celsius = self.spec.celsius
        h.dt = self.spec.dt
        h.tstop = self.spec.tstop
        h.steps_per_ms = 1.0 / h.dt
        v_init = -70
        h.finitialize(v_init)

        ps = self.cell.soma.display_v(width=800, height=800)
        for tk in range(0, int(self.spec.tstop * 1000) + 1, int(step * 1000)):
            t = tk / 1000
            if h.t < t:
                logger.info(f"{t:07.3f}")
                h.continuerun(t)
            ps.exec_menu("Redraw Shape")
            if step < 1:
                writer.write_graph(f"voltages/{t:07.3f}", ps)
            else:
                writer.write_graph(f"voltages/{t:03d}", ps)
