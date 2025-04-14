from prelude import logger


class ModNaRsg:
    gating_consts = [
        "alfac",
        "btfac",
        "afac",
    ]
    gating_vars = [
        "alfac",
        "btfac",
        "afac",
        "f01",
        "f02",
        "f03",
        "f04",
        "f0O",
        "fip",
        "f11",
        "f12",
        "f13",
        "f14",
        "f1n",
        "fi1",
        "fi2",
        "fi3",
        "fi4",
        "fi5",
        "fin",
        "b01",
        "b02",
        "b03",
        "b04",
        "b0O",
        "bip",
        "b11",
        "b12",
        "b13",
        "b14",
        "b1n",
        "bi1",
        "bi2",
        "bi3",
        "bi4",
        "bi5",
        "bin",
    ]

    gating_states = [
        "C1",
        "C2",
        "C3",
        "C4",
        "C5",
        "I1",
        "I2",
        "I3",
        "I4",
        "I5",
        "O",
        "B",
        "I6",
        "Ca",
        "Ia",
    ]


class Config:
    def __init__(
        self,
        soma=[],
        axon=[],
        trunk=[],
        branch=[],
        default_eleak=-65,
        membranecap=0.64,  ## specific membrane capacitance in uF cm^-2
        membraneresist=120236,  ## specific membrane resistance in ohm cm^2
        axialresist=120,  ## axial resistivity in ohm cm
    ):
        self.soma = soma
        self.axon = axon
        self.trunk = trunk
        self.branch = branch

        self.default_eleak = default_eleak
        self.membranecap = membranecap
        self.membraneresist = membraneresist
        self.axialresist = axialresist

        self.config = {"soma_": {}, "axon_": {}, "dend_": {}}

    def configure(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                for pre in self.config.keys():
                    if k.startswith(pre):
                        self.config[pre][k.lstrip(pre)] = v

    def apply(self):
        for scope, xs in self.config.items():
            for k, v in xs.items():
                logger.info(f"Config: {scope}{k}: {v}")
        for sec in self.soma:
            self.setup_general(sec)
            self.setup_soma(sec)
            for k, v in self.config["soma_"].items():
                setattr(sec, k, getattr(sec, k) * v)
        for sec in self.axon:
            self.setup_general(sec)
            self.setup_axon(sec)
            for k, v in self.config["axon_"].items():
                setattr(sec, k, getattr(sec, k) * v)
        for sec in self.trunk:
            self.setup_general(sec)
            self.setup_dend(sec)
            self.setup_trunk(sec)
            for k, v in self.config["dend_"].items():
                setattr(sec, k, getattr(sec, k) * v)
        for sec in self.branch:
            self.setup_general(sec)
            self.setup_dend(sec)
            self.setup_branch(sec)
            for k, v in self.config["dend_"].items():
                setattr(sec, k, getattr(sec, k) * v)

    def setup_general(self, sec):
        sec.insert("pas")
        sec.insert("hpkj") 
        sec.insert("ds")
        sec.insert("pk")
        sec.e_pas = self.default_eleak

    def setup_soma(self, sec):
        sec.g_pas = 1 / self.membraneresist
        sec.Ra = self.axialresist
        sec.cm = self.membranecap

        sec.insert("naRsg")
        sec.gbar_naRsg = 0.03168
        sec.vshifta_naRsg = 0
        sec.vshiftk_naRsg = 0
        sec.vshifti_naRsg = -5

        sec.insert("nap")
        sec.gbar_nap = 0.00014
        sec.insert("pk")
        sec.ena = 63
        sec.ghbar_hpkj = 0.000108

        sec.insert("cdp20N_FD2")
        cdp = sec(0.5).cdp20N_FD2
        cdp.CBnull = 0.08

        sec.insert("Kv3")
        sec.gbar_Kv3 = 1.8
        sec.vshift_Kv3 = 4
        sec.insert("newCaP")
        sec.pcabar_newCaP = 0.00019
        sec.kt_newCaP = 1
        sec.vshift_newCaP = -5
        sec.insert("mslo")
        sec.gbar_mslo = 0.8736
        sec.insert("abBK")
        sec.gabkbar_abBK = 0.3
        sec.insert("SK2")
        sec.gkbar_SK2 = 0.0075

    def setup_axon(self, sec):
        sec.g_pas = 1 / self.membraneresist
        sec.Ra = self.axialresist
        sec.cm = self.membranecap

        sec.insert("naRsg")
        sec.gbar_naRsg = 0.56
        sec.vshifta_naRsg = 15
        sec.vshiftk_naRsg = 5
        sec.vshifti_naRsg = -5
        sec.insert("nap")
        sec.gbar_nap = 0.0023
        sec.insert("CaT3_1")
        sec.pcabar_CaT3_1 = 0.000128
        sec.ena = 63
        sec.ghbar_hpkj = 0.000108
        sec.insert("cdpAIS")

        sec.insert("Kv3")
        sec.gbar_Kv3 = 115.2
        sec.vshift_Kv3 = 4
        sec.insert("newCaP")
        sec.pcabar_newCaP = 0.00228
        sec.kt_newCaP = 1
        sec.vshift_newCaP = -5
        sec.insert("mslo")
        sec.gbar_mslo = 6
        sec.insert("abBK")
        sec.gabkbar_abBK = 1.05
        sec.insert("SK2")
        sec.gkbar_SK2 = 0.027777778

    def setup_dend(self, sec):
        sec.insert("Kv3")
        sec.gbar_Kv3 = 0.1512
        sec.vshift_Kv3 = 4
        sec.insert("newCaP")
        sec.pcabar_newCaP = 0.00019
        sec.vshift_newCaP = -5
        sec.insert("CaT3_1")
        sec.pcabar_CaT3_1 = 2.7e-05
        sec.insert("mslo")
        sec.gbar_mslo = 0.21504
        sec.insert("SK2")
        sec.gkbar_SK2 = 2.4000e-04 * 1.5
        sec.scal_SK2 = 1.0
        sec.ghbar_hpkj = 0.00036
        sec.insert("Kv1")
        sec.gbar_Kv1 = 0.002
        sec.insert("Kv4")
        sec.gbar_Kv4 = 0.0252
        sec.insert("Kv4s")
        sec.gbar_Kv4s = 0.015

    def setup_trunk(self, sec):
        sec.g_pas = 1.2 / self.membraneresist
        sec.Ra = self.axialresist
        sec.cm = 1.2 * self.membranecap
        sec.insert("cdp4N")

    def setup_branch(self, sec):
        sec.g_pas = 5.3 / self.membraneresist
        sec.Ra = self.axialresist
        sec.cm = 5.3 * self.membranecap

        sec.insert("cdp4Nsp")
        sec.gkbar_SK2 = 0.00036
        sec.scal_SK2 = 1.0
        sec.gbar_Kv4 = 0.0264
        sec.gbar_Kv4s = 0.015
        sec.ghbar_hpkj = 0.000324
        sec.vshift_Kv4 = 0
        sec.gbar_Kv1 = 0.001
        sec.gbar_Kv3 = 0.1512
        sec.vshift_Kv3 = 0
        sec.pcabar_CaT3_1 = 0.000108
        sec.pcabar_newCaP = 0.00076
        sec.vshift_newCaP = -5
        sec.scale_cdp4Nsp = 3.5
        sec.gbar_mslo = 0.0896
        sec.insert("abBK")
        sec.gabkbar_abBK = 0.15

    naRsg_gating_consts = [f"{var}_naRsg" for var in ModNaRsg.gating_consts]
    naRsg_gating_vars = [f"{var}_naRsg" for var in ModNaRsg.gating_vars]
    naRsg_gating_states = [f"{var}_naRsg" for var in ModNaRsg.gating_states]
