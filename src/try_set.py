import re
import numpy as np
from runner import SpecSet, Spec
from cell.config import Config


class TrySet:
    def try01():
        base = SpecSet(
            morphology=["human/original"],
            tstop=[10],
        )
        return [
            base(soma_gbar_naRsg=[0.8, 1.2]),
            base(soma_gbar_nap=[0.8, 1.2]),
            base(soma_gbar_Kv3=[0.8, 1.2]),
            base(soma_gbar_mslo=[0.8, 1.2]),
            base(soma_gabkbar_abBK=[0.8, 1.2]),
            base(soma_gkbar_SK2=[0.8, 1.2]),
            base(axon_gbar_naRsg=[0.8, 1.2]),
            base(axon_gbar_nap=[0.8, 1.2]),
            base(axon_gbar_Kv3=[0.8, 1.2]),
            base(axon_gbar_mslo=[0.8, 1.2]),
            base(axon_gabkbar_abBK=[0.8, 1.2]),
            base(axon_gkbar_SK2=[0.8, 1.2]),
            base(axon_gkbar_SK2=[0.8, 1.2]),
        ]

    def try02():
        base = SpecSet(
            morphology=["human/original"],
            tstop=[300],
        )
        return [
            base(axon_gbar_naRsg=[0.8, 1.2]),
            base(axon_gbar_nap=[0.8, 1.2]),
            base(axon_gbar_Kv3=[0.8, 1.2]),
            base(axon_gbar_mslo=[0.8, 1.2]),
            base(axon_gabkbar_abBK=[0.8, 1.2]),
            base(axon_gkbar_SK2=[0.8, 1.2]),
            base(axon_gkbar_SK2=[0.8, 1.2]),
        ]

    def try03():
        return [
            SpecSet(
                morphology=["human/original"],
                tstop=[300],
                axon_gkbar_SK2=[0.5, 0.6, 0.8, 1.2],
            )
        ]

    # Rat cell, reproducing Zang2021
    def try04():
        return [
            SpecSet(
                morphology=["zang2021/fig3"],
                dt=[0.02],
                tstop=[500],
            )
        ]

    def try05():
        base = SpecSet(
            morphology=["human/original"],
            dt=[0.01],
            tstop=[300],
        )
        return [
            base,
            base(axon_gkbar_SK2=[0.5, 0.6, 0.8, 1.2]),
        ]

    def try06():
        base = SpecSet(
            morphology=["human/original"],
            dt=[0.01],
            tstop=[300],
        )
        return [
            base(soma_gbar_naRsg=[0.8, 1.2]),
            base(soma_gbar_nap=[0.8, 1.2]),
            base(soma_gbar_Kv3=[0.8, 1.2]),
            base(soma_gbar_mslo=[0.8, 1.2]),
            base(soma_gabkbar_abBK=[0.8, 1.2]),
            base(soma_gkbar_SK2=[0.8, 1.2]),
            base(axon_gbar_naRsg=[0.8, 1.2]),
            base(axon_gbar_nap=[0.8, 1.2]),
            base(axon_gbar_Kv3=[0.8, 1.2]),
            base(axon_gbar_mslo=[0.8, 1.2]),
            base(axon_gabkbar_abBK=[0.8, 1.2]),
            base(axon_gkbar_SK2=[0.8, 1.2]),
        ]

    def try07():
        base = SpecSet(
            morphology=["human/original"],
            dt=[0.01],
            tstop=[300],
        )
        return [
            base(soma_gbar_naRsg=[1.2, 1.4, 1.6, 1.8, 2.0, 3.0, 5.0, 10.0]),
        ]

    def try08():
        base = SpecSet(
            morphology=["human/original"],
            dt=[0.01],
            tstop=[300],
            soma_gbar_naRsg=[2.0],
        )
        return [
            base(soma_gbar_nap=[2.0, 3.0]),
            base(soma_gbar_Kv3=[2.0, 3.0]),
            base(soma_gbar_mslo=[2.0, 3.0]),
            base(soma_gabkbar_abBK=[2.0, 3.0]),
            base(soma_gkbar_SK2=[2.0, 3.0]),
            base(axon_gbar_naRsg=[2.0, 3.0]),
            base(axon_gbar_nap=[2.0, 3.0]),
            base(axon_gbar_Kv3=[2.0, 3.0]),
            base(axon_gbar_mslo=[2.0, 3.0]),
            base(axon_gabkbar_abBK=[2.0, 3.0]),
            base(axon_gkbar_SK2=[2.0, 3.0]),
        ]

    # Macaque config
    def try09():
        base = SpecSet(
            morphology=["macaque/Axon_withellipse"],
            dt=[0.02],
            tstop=[300],
        )
        return [
            base(
                soma_gbar_naRsg=[4.7],
                soma_gbar_nap=[0.21],
                soma_gbar_Kv3=[4.4],
                soma_gbar_mslo=[2.3],
                soma_gabkbar_abBK=[2.3],
                soma_gkbar_SK2=[13.3],
            )
        ]

    # Macaque config to the human cell
    def try10():
        base = SpecSet(
            morphology=["human/original"],
            dt=[0.01],
            tstop=[300],
        )
        return [
            base(
                soma_gbar_naRsg=[4.7],
                soma_gbar_nap=[0.21],
                soma_gbar_Kv3=[4.4],
                soma_gbar_mslo=[2.3],
                soma_gabkbar_abBK=[2.3],
                soma_gkbar_SK2=[13.3],
            )
        ]

    # Potassium channels of dendrites
    def try11():
        base = SpecSet(
            morphology=["human/original"],
            adjust_soma=[True],
            dt=[0.01],
            tstop=[300],
        )
        return [
            base(dend_gbar_Kv3=[2, 4, 8]),
            base(dend_gbar_mslo=[2, 4, 8]),
            base(dend_gkbar_SK2=[2, 4, 8, 16]),
        ]

    # Potassium channels mslo of dendrites
    def try12():
        base = SpecSet(
            morphology=["human/original"],
            adjust_soma=[True],
            dt=[0.01],
            tstop=[1000],
        )
        return [
            base(dend_gbar_mslo=[4, 8, 16]),
        ]

    # Potassium channels of dendrites x Sodium channels of soma
    def try13():
        base = SpecSet(
            morphology=["human/original"],
            adjust_soma=[True],
            dt=[0.01],
            tstop=[300],
        )
        return [
            base(
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
            ),
        ]

    # Same to try13 but longer
    def try14():
        base = SpecSet(
            morphology=["human/original"],
            adjust_soma=[True],
            dt=[0.01],
            tstop=[1000],
        )
        return [
            base(
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
            ),
        ]

    # Macaque with try13 setup
    def try15():
        base = SpecSet(
            morphology=["macaque/Axon_withellipse"],
            dt=[0.02],
            tstop=[1000],
        )
        return [
            base(
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
            ),
        ]

    # Same to try13, try14 but even longer
    def try16():
        base = SpecSet(
            morphology=["human/original"],
            adjust_soma=[True],
            dt=[0.01],
            tstop=[1300],
        )
        return [
            base(
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
            ),
        ]

    _try17_recordings = [
        ("soma", 0.5, "v"),
        ("branches[0]", 0.0, "ica_newCaP"),
        ("branches[0]", 0.0, "iCa_CaT3_1"),
        ("branches[0]", 0.0, "ik_mslo"),
        ("branches[0]", 0.0, "ik_SK2"),
        ("branches[0]", 0.0, "ik_Kv1"),
        ("branches[0]", 0.0, "ik_Kv3"),
        ("branches[0]", 0.0, "ik_Kv4"),
        ("branches[0]", 0.0, "ik_Kv4s"),
        ("branches[100]", 0.0, "ica_newCaP"),
        ("branches[100]", 0.0, "iCa_CaT3_1"),
        ("branches[100]", 0.0, "ik_mslo"),
        ("branches[100]", 0.0, "ik_SK2"),
        ("branches[100]", 0.0, "ik_Kv1"),
        ("branches[100]", 0.0, "ik_Kv3"),
        ("branches[100]", 0.0, "ik_Kv4"),
        ("branches[100]", 0.0, "ik_Kv4s"),
    ]

    # Same to try13 and record ion channel currents
    def try17():
        base = SpecSet(
            morphology=["human/original"],
            adjust_soma=[True],
            dt=[0.01],
            tstop=[300],
            recordings=[TrySet._try17_recordings],
        )
        return [
            base(
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
            ),
        ]

    # Configure Ca channels at dendrites
    def try18():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[1000],
                recordings=[TrySet._try17_recordings],
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                dend_pcabar_newCaP=[2.0, 3.0, 4.0],
                dend_pcabar_CaT3_1=[2.0, 3.0, 4.0],
            )
        ]

    # Configure CaP channels at dendrites
    def try19():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[1000],
                recordings=[TrySet._try17_recordings],
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                dend_pcabar_newCaP=[0.5, 0.8, 1.2, 1.5],
            )
        ]

    # Configure CaT channels at dendrites
    def try20():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[1000],
                recordings=[TrySet._try17_recordings],
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                dend_pcabar_CaT3_1=[0.5, 0.8, 1.2, 1.5],
            )
        ]

    # Configure CaP channels vshift at dendrites
    def try21():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[1000],
                recordings=[TrySet._try17_recordings],
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                dend_vshift_newCaP=[0.0, 0.5, 0.8],
            )
        ]

    # Configure CaP channels vshift at dendrites finer
    def try22():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[350],
                recordings=[TrySet._try17_recordings],
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                dend_vshift_newCaP=[0.0, 0.2, 0.4, 0.5, 0.6, 0.8],
            )
        ]

    # Variation in CaP while CaP vshift set zero
    def try23():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[350],
                recordings=[TrySet._try17_recordings],
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                dend_vshift_newCaP=[0.0],
                dend_pcabar_newCaP=[0.5, 0.8, None, 1.2, 1.5],
            )
        ]

    # Variation in CaT while CaP vshift set zero
    def try24():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[350],
                recordings=[TrySet._try17_recordings],
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                dend_vshift_newCaP=[0.0],
                dend_pcabar_CaT3_1=[0.5, 0.8, None, 1.2, 1.5],
            )
        ]

    # Variation in CaT while CaP vshift more
    def try25():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[350],
                recordings=[TrySet._try17_recordings],
                dend_gbar_mslo=[4],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                dend_vshift_newCaP=[1.2, 1.5, 2.0],
                dend_pcabar_newCaP=[0.5, 0.8, None, 1.2, 1.5],
            )
        ]

    # vshift zero, with no soma configuration
    def try26():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[300],
                recordings=[TrySet._try17_recordings],
                dend_gbar_mslo=[1, 2, 3, 4],
                dend_vshift_newCaP=[0],
            )
        ]

    # vshift 0.8, explore soma naRsg
    def try27():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[300],
                recordings=[TrySet._try17_recordings],
                soma_gbar_naRsg=[1.0, 2.0, 3.0, 4.0, 8.0],
                soma_gabkbar_abBK=[3.0],
                dend_gbar_mslo=[4.0],
                dend_vshift_newCaP=[0.8],
            )
        ]

    # vshift 0.8, explore soma abBK
    def try28():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[300],
                recordings=[TrySet._try17_recordings],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[1.0, 2.0, 3.0, 4.0, 8.0],
                dend_gbar_mslo=[4.0],
                dend_vshift_newCaP=[0.8],
            )
        ]

    # Explore soma mslo
    def try29():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[300],
                recordings=[TrySet._try17_recordings],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                soma_gbar_mslo=[None, 2.0, 3.0, 4.0, 8.0],
                dend_gbar_mslo=[4.0],
            )
        ]

    # vshift 0.8, explore soma mslo
    def try30():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[300],
                recordings=[TrySet._try17_recordings],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[3.0],
                soma_gbar_mslo=[None, 2.0, 3.0, 4.0, 8.0],
                dend_gbar_mslo=[4.0],
                dend_vshift_newCaP=[0.8],
            )
        ]

    # soma mslo 4, explore soma naRsg
    def try31():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[300],
                recordings=[TrySet._try17_recordings],
                soma_gbar_naRsg=[2.0, 3.0, 4.0, 8.0],
                soma_gabkbar_abBK=[3.0],
                soma_gbar_mslo=[4.0],
                dend_gbar_mslo=[4.0],
            )
        ]

    # soma mslo 4, explore soma abBK
    def try32():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[300],
                recordings=[TrySet._try17_recordings],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[2.0, 3.0, 4.0, 8.0],
                soma_gbar_mslo=[4.0],
                dend_gbar_mslo=[4.0],
            )
        ]

    # soma mslo 4, explore soma abBK finer
    def try33():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[300],
                recordings=[TrySet._try17_recordings],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[0.5, 0.8, 1.0, 1.2, 1.5],
                soma_gbar_mslo=[4.0],
                dend_gbar_mslo=[4.0],
            )
        ]

    # soma mslo 4, explore soma abBK reducing
    def try34():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[1000],
                recordings=[TrySet._try17_recordings],
                soma_gbar_naRsg=[2.0],
                soma_gabkbar_abBK=[0.5, 0.8, 1.0, 1.2, 1.5],
                soma_gbar_mslo=[4.0],
                dend_gbar_mslo=[4.0],
            )
        ]

    # Unset abBK
    def try35():
        return [
            SpecSet(
                morphology=["human/original"],
                adjust_soma=[True],
                dt=[0.01],
                tstop=[1000],
                recordings=[TrySet._try17_recordings],
                soma_gbar_naRsg=[2.0],
                soma_gbar_mslo=[4.0],
                dend_gbar_mslo=[4.0],
            )
        ]

    def _injection_soma(amp):
        if amp == 0.0:
            return []
        else:
            return [("soma", 0.5, amp)]

    # Inject current
    def try36():
        return [
            TrySet.human_original_nice.lift()(
                injections=[
                    TrySet._injection_soma(amp) for amp in np.arange(-0.5, 1.51, 0.2)
                ],
            )
        ]

    def try36_1():
        return [
            TrySet.human_original_nice.lift()(
                injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5, 0.0]],
            )
        ]

    # Inject current with abBK variations
    def try37():
        return [
            TrySet.human_original_nice.lift()(
                injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
                soma_gabkbar_abBK=[0.5, 0.8, None, 1.2, 1.5, 2.0, 4.0],
            )
        ]

    # Inject current with mslo incresing
    def try38():
        return [
            TrySet.human_original_nice.lift()(
                injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
                soma_gbar_mslo=[4.0, 5.0, 6.0],
            )
        ]

    # Inject current with mslo incresing
    def try39():
        return [
            TrySet.human_original_nice.lift()(
                injections=[TrySet._injection_soma(amp) for amp in [1.5]],
                soma_gbar_mslo=[4.0, 5.0, 6.0, 8.0, 10.0, 12.0, 16.0],
            )
        ]

    # Inject current with mslo 16 and various abBK
    def try40():
        return [
            TrySet.human_original_nice.lift()(
                injections=[TrySet._injection_soma(amp) for amp in [1.5]],
                soma_gabkbar_abBK=[2.0, 4.0, 8.0, 16.0],
                soma_gbar_mslo=[16.0],
            )
        ]

    # Inject current with mslo 16 and various naRsg
    def try41():
        return [
            TrySet.human_original_nice.lift()(
                injections=[TrySet._injection_soma(amp) for amp in [1.5]],
                soma_gbar_naRsg=[2.0, 4.0, 8.0, 16.0],
                soma_gbar_mslo=[16.0],
            )
        ]

    # Inject current with mslo incresing, longer
    def try42():
        return [
            TrySet.human_original_nice.lift()(
                tstop=[1000],
                injections=[TrySet._injection_soma(amp) for amp in [1.5]],
                soma_gbar_mslo=[6.0, 8.0, 10.0, 12.0],
            )
        ]

    # Inject current with mslo 8 and abBK variations
    def try43():
        return [
            TrySet.human_original_nice.lift()(
                injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
                soma_gabkbar_abBK=[2.0, 4.0, 8.0, 10.0, 16.0],
                soma_gbar_mslo=[8.0],
            )
        ]

    # Inject current with mslo 8, abBK 8 and naRsg variations
    def try44():
        return [
            TrySet.human_original_nice.lift()(
                injections=[TrySet._injection_soma(amp) for amp in [1.5]],
                soma_gbar_naRsg=[2.0, 4.0, 8.0],
                soma_gabkbar_abBK=[8.0],
                soma_gbar_mslo=[8.0],
            )
        ]

    # With mslo 8, abBK 8 and current variations
    def try45():
        return [
            TrySet.human_original_nice.lift()(
                injections=[
                    TrySet._injection_soma(amp) for amp in [-0.5, 0.0, 0.5, 1.0, 1.5]
                ],
                soma_gabkbar_abBK=[8.0],
                soma_gbar_mslo=[8.0],
            )
        ]

    def try45_1():
        return [
            TrySet.human_original_nice.lift()(
                injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
                soma_gabkbar_abBK=[8.0],
                soma_gbar_mslo=[8.0],
            )
        ]

    # Variations of the same value pair of mslo abBK
    def try46():
        base = TrySet.human_original_nice.lift()(
            injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
        )
        return [
            base(
                soma_gabkbar_abBK=[x],
                soma_gbar_mslo=[x],
            )
            for x in [4.0, 5.0, 6.0, 8.0]
        ]

    # Variations of the dend vshift CaP with various current
    def try47():
        base = TrySet.human_original_nice.lift()(
            injections=[TrySet._injection_soma(amp) for amp in [-0.5, 0.0, 1.5]],
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
        )
        return [
            base(
                dend_vshift_newCaP=[0.0, 0.5, 0.8, 1.2, 1.5, 2.0],
            )
        ]

    # Variations of the dend CaP with various current
    def try48():
        base = TrySet.human_original_nice.lift()(
            injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
            dend_vshift_newCaP=[2.0],
        )
        return [
            base(
                dend_pcabar_newCaP=[2.0, 3.0, 4.0],
            )
        ]

    # Variations of the dend mslo with vshift CaP 0
    def try49():
        base = TrySet.human_original_nice.lift()(
            injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
            dend_vshift_newCaP=[0.0],
        )
        return [
            base(
                dend_gbar_mslo=[4.0, 5.0, 8.0, 16.0],
            )
        ]

    # Variations of the soma mslo with vshift CaP 0
    def try50():
        base = TrySet.human_original_nice.lift()(
            injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
            dend_vshift_newCaP=[0.0],
        )
        return [
            base(
                soma_gbar_naRsg=[2.0, 3.0, 4.0, 8.0, 16.0],
            )
        ]

    # Variations of the dend CaT with various current
    def try51():
        base = TrySet.human_original_nice.lift()(
            injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
        )
        return [
            base(
                dend_pcabar_CaT3_1=[2.0, 3.0, 4.0, 8.0],
            )
        ]

    # Variations of the dend CaT and CaP with various current
    def try52():
        base = TrySet.human_original_nice.lift()(
            injections=[TrySet._injection_soma(amp) for amp in [-0.5, 1.5]],
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
        )
        return [
            base(
                dend_pcabar_CaT3_1=[2.0],
                dend_pcabar_newCaP=[2.0, 3.0, 4.0, 8.0],
            )
        ]

    # With mslo 8, abBK 8 and current variations more than try45
    def try53():
        base = TrySet.human_original_nice.lift()(
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
        )
        return [
            base(injections=[TrySet._injection_soma(i / 10) for i in range(-2, 37, 2)])
        ]

    def try53_1():
        base = TrySet.human_original_nice.lift()(
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
        )
        return [
            base(injections=[TrySet._injection_soma(amp) for amp in [-0.5, 0.0, 0.5]])
        ]

    # From try48 with more variations of current
    def try54():
        base = TrySet.human_original_nice.lift()(
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
            dend_vshift_newCaP=[2.0],
            dend_pcabar_newCaP=[2.0],
        )
        return [
            base(
                injections=[TrySet._injection_soma(amp) for amp in [0.0, 0.5, 1.0]],
            )
        ]

    #  Less K at soma than try54
    def try55():
        base = TrySet.human_original_nice.lift()(
            soma_gabkbar_abBK=[6.0],
            soma_gbar_mslo=[6.0],
            dend_vshift_newCaP=[2.0],
            dend_pcabar_newCaP=[2.0],
        )
        return [
            base(
                injections=[TrySet._injection_soma(amp) for amp in [0.0, 0.5, 1.0]],
            )
        ]

    # As try 53 but longer
    def try56():
        base = TrySet.human_original_nice.lift()(
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
            tstop=[1300],
        )
        return [
            base(injections=[TrySet._injection_soma(i / 10) for i in range(-2, 37, 2)])
        ]

    def try56_1():
        base = TrySet.human_original_nice.lift()(
            soma_gabkbar_abBK=[8.0],
            soma_gbar_mslo=[8.0],
            tstop=[1300],
        )
        return [
            base(injections=[TrySet._injection_soma(i / 10) for i in range(4, 16, 2)])
        ]

    _try57_recordings = [
        ("soma", 0.5, "v"),
        ("soma", 0.5, "ina_nap"),
        ("soma", 0.5, "ik_mslo"),
        ("trunk_sections[1]", 0.0, "i_hpkj"),
        ("trunk_sections[1]", 0.0, "ica_newCaP"),
        ("trunk_sections[1]", 0.0, "iCa_CaT3_1"),
        ("trunk_sections[1]", 0.0, "ik_mslo"),
        ("trunk_sections[1]", 0.0, "ik_SK2"),
        ("trunk_sections[1]", 0.0, "ik_Kv1"),
        ("trunk_sections[1]", 0.0, "ik_Kv3"),
        ("trunk_sections[1]", 0.0, "ik_Kv4"),
        ("trunk_sections[1]", 0.0, "ik_Kv4s"),
    ]

    # Record ion channel currents
    def try57():
        base = TrySet.human_original_nice_inj.lift()(
            recordings=[TrySet._try57_recordings],
        )
        return [
            base(
                injections=[
                    TrySet._injection_soma(amp) for amp in [-0.2, 0.0, 0.2, 0.4]
                ]
            )
        ]

    # Record ion channel currents
    def try58():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try57_recordings],
        )
        return [
            base(
                injections=[
                    TrySet._injection_soma(amp) for amp in [-0.2, 0.0, 0.2, 0.4]
                ]
            )
        ]

    ## Here, I found a misconfiguration on smooth dendrites.
    ## Thus, the results up to this point may be correct or wrong depending on re-calculation done or not.
    ## The items below is specifically, correct.

    # The nice without injection
    def try59():
        return [
            TrySet.human_original_nice.lift()(
                injections=[
                    TrySet._injection_soma(amp) for amp in [-0.2, 0.0, 0.2, 0.4]
                ],
            )
        ]

    # The nice with injection
    def try60():
        return [
            TrySet.human_original_nice_inj.lift()(
                injections=[
                    TrySet._injection_soma(amp) for amp in [-0.2, 0.0, 0.2, 0.4]
                ],
            )
        ]

    _try61_recordings = [
        ("soma", 0.5, "v"),
        ("soma", 0.5, "ina_nap"),
        ("soma", 0.5, "ik_mslo"),
        ("trunk_sections[1]", 0.0, "i_hpkj"),
        ("trunk_sections[1]", 0.0, "ica_newCaP"),
        ("trunk_sections[1]", 0.0, "iCa_CaT3_1"),
        ("trunk_sections[1]", 0.0, "ik_mslo"),
        ("trunk_sections[1]", 0.0, "ik_SK2"),
        ("trunk_sections[1]", 0.0, "ik_Kv1"),
        ("trunk_sections[1]", 0.0, "ik_Kv3"),
        ("trunk_sections[1]", 0.0, "ik_Kv4"),
        ("trunk_sections[1]", 0.0, "ik_Kv4s"),
        ("branches[100]", 0.0, "i_hpkj"),
        ("branches[100]", 0.0, "ica_newCaP"),
        ("branches[100]", 0.0, "iCa_CaT3_1"),
        ("branches[100]", 0.0, "ik_mslo"),
        ("branches[100]", 0.0, "ik_SK2"),
        ("branches[100]", 0.0, "ik_Kv1"),
        ("branches[100]", 0.0, "ik_Kv3"),
        ("branches[100]", 0.0, "ik_Kv4"),
        ("branches[100]", 0.0, "ik_Kv4s"),
    ]

    # Retry try58
    def try61():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try61_recordings],
        )
        return [
            base(
                injections=[
                    TrySet._injection_soma(amp) for amp in [-0.2, 0.0, 0.2, 0.4]
                ]
            )
        ]

    def try61_1():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try61_recordings],
        )
        return [base(injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]])]

    # Retry try57
    def try62():
        base = TrySet.human_original_nice_inj.lift()(
            recordings=[TrySet._try61_recordings],
        )
        return [
            base(
                injections=[
                    TrySet._injection_soma(amp) for amp in [-0.2, 0.0, 0.2, 0.4]
                ]
            )
        ]

    def try62_1():
        base = TrySet.human_original_nice_inj.lift()(
            recordings=[TrySet._try61_recordings],
        )
        return [base(injections=[TrySet._injection_soma(amp) for amp in [0.0, 0.2]])]

    # Longer try61
    def try63():
        base = TrySet.human_original_nice.lift()(
            tstop=[1300],
            recordings=[TrySet._try61_recordings],
        )
        return [
            base(
                injections=[
                    TrySet._injection_soma(amp) for amp in [-0.2, 0.0, 0.2, 0.4]
                ]
            )
        ]

    def try63_1():
        base = TrySet.human_original_nice.lift()(
            tstop=[1300],
            recordings=[TrySet._try61_recordings],
        )
        return [base(injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]])]

    _try64_recordings = [
        ("soma", 0.5, "v"),
        ("soma", 0.5, "i_hpkj"),
        ("soma", 0.5, "ina_nap"),
        ("soma", 0.5, "ina_naRsg"),
        ("soma", 0.5, "ik_mslo"),
        ("soma", 0.5, "ik_Kv3"),
        ("soma", 0.5, "ica_newCaP"),
        ("soma", 0.5, "ik_SK2"),
        ("axon", 0.5, "v"),
        ("axon", 0.5, "i_hpkj"),
        ("axon", 0.5, "ina_naRsg"),
        ("axon", 0.5, "ik_Kv3"),
        ("trunk_sections[1]", 0.0, "i_hpkj"),
        ("trunk_sections[1]", 0.0, "ica_newCaP"),
        ("trunk_sections[1]", 0.0, "iCa_CaT3_1"),
        ("trunk_sections[1]", 0.0, "ik_mslo"),
        ("trunk_sections[1]", 0.0, "ik_SK2"),
        ("trunk_sections[1]", 0.0, "ik_Kv1"),
        ("trunk_sections[1]", 0.0, "ik_Kv3"),
        ("trunk_sections[1]", 0.0, "ik_Kv4"),
        ("trunk_sections[1]", 0.0, "ik_Kv4s"),
    ]

    # Record soma and axon
    def try64():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base]

    def try64_1():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2]],
        )
        return [base]

    # More Na, K channels at soma
    def try65():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[3.0],
                soma_gbar_Kv3=[3.0],
            )
        ]

    # More Na, K channels at soma
    def try66():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[4.0],
                soma_gbar_Kv3=[4.0],
            )
        ]

    # More Na, K channels at axon
    def try67():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                axon_gbar_naRsg=[2.0],
                axon_gbar_Kv3=[2.0],
            )
        ]

    # More Na, K channels at axon
    def try68():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                axon_gbar_naRsg=[3.0],
                axon_gbar_Kv3=[3.0],
            )
        ]

    # More Na, K channels at axon
    def try69():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                axon_gbar_naRsg=[4.0],
                axon_gbar_Kv3=[4.0],
            )
        ]

    # More Na, K channels at soma
    def try70():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[2.0],
                soma_gbar_Kv3=[2.0],
            )
        ]

    # More Na, K channels at soma
    def try71():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[2.0],
                soma_gbar_nap=[2.0],
                soma_gbar_Kv3=[2.0],
            )
        ]

    # Reduce mslo to 2
    def try72():
        base = TrySet.human_original_base.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[2.0],
                soma_gbar_nap=[2.0],
                soma_gbar_Kv3=[2.0],
                soma_gbar_mslo=[2.0],
                dend_gbar_mslo=[2.0],
            )
        ]

    # Reduce mslo to 3
    def try73():
        base = TrySet.human_original_base.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[2.0],
                soma_gbar_nap=[2.0],
                soma_gbar_Kv3=[2.0],
                soma_gbar_mslo=[3.0],
                dend_gbar_mslo=[3.0],
            )
        ]

    # naRsg 1.5, nap 1.5, Kv3 2 at soma
    def try74():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[1.5],
                soma_gbar_nap=[1.5],
                soma_gbar_Kv3=[2.0],
            )
        ]

    # naRsg 2, nap 2, Kv3 3 at soma
    def try75():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[2.0],
                soma_gbar_nap=[2.0],
                soma_gbar_Kv3=[3.0],
            )
        ]

    # Summary for the recent results
    def try76():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base,
            base(
                soma_gbar_naRsg=[3.0],
                soma_gbar_Kv3=[3.0],
            ),
            base(
                soma_gbar_naRsg=[4.0],
                soma_gbar_Kv3=[4.0],
            ),
            base(
                soma_gbar_naRsg=[1.5],
                soma_gbar_nap=[1.5],
                soma_gbar_Kv3=[2.0],
            ),
            base(
                soma_gbar_naRsg=[2.0],
                soma_gbar_nap=[2.0],
                soma_gbar_Kv3=[2.0],
            ),
            base(
                soma_gbar_naRsg=[2.0],
                soma_gbar_nap=[2.0],
                soma_gbar_Kv3=[3.0],
            ),
        ]

    # CaP 2 at soma
    def try77():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_pcabar_newCaP=[2.0],
            )
        ]

    # CaP 3 at soma
    def try78():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_pcabar_newCaP=[3.0],
            )
        ]

    # Variations similar to try76
    def try79():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[None],
                soma_gbar_nap=[2.0],
            ),
            base(
                soma_gbar_naRsg=[None],
                soma_gbar_nap=[2.0],
                soma_gbar_Kv3=[2.0],
            ),
        ]

    # CaP 0.8 at soma
    def try80():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base(soma_pcabar_newCaP=[0.8])]

    # CaP 0.5 at soma
    def try81():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base(soma_pcabar_newCaP=[0.5])]

    # CaP 0.2 at soma
    def try82():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base(soma_pcabar_newCaP=[0.2])]

    # naRsg 1.5, CaP 0.8 at soma
    def try83():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[1.5],
                soma_pcabar_newCaP=[0.8],
            )
        ]

    # naRsg 1.5, CaP 0.5 at soma
    def try84():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[1.5],
                soma_pcabar_newCaP=[0.5],
            )
        ]

    # naRsg 1.5, nap 1.5, Kv3 1.5 at soma, like try74
    def try85():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[1.5],
                soma_gbar_nap=[1.5],
                soma_gbar_Kv3=[1.5],
            )
        ]

    # naRsg 1.5, nap 1.2, Kv3 1.5 at soma, like try74
    def try86():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[1.5],
                soma_gbar_nap=[1.2],
                soma_gbar_Kv3=[1.5],
            )
        ]

    # From here, set nap 0 and see the frequency
    # nap 0
    def try87():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_nap=[0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base]

    # nap 0, naRsg 3.0
    def try88():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_nap=[0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[3.0],
            )
        ]

    # nap 0, naRsg 3.0, Kv3 1.5
    def try89():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_nap=[0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[3.0],
                soma_gbar_Kv3=[1.5],
            )
        ]

    # nap 0, naRsg 2.0, Kv3 2.0
    def try90():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_nap=[0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[2.0],
                soma_gbar_Kv3=[2.0],
            )
        ]

    # nap 0, naRsg 3.0, Kv3 2.0
    def try91():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_nap=[0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[3.0],
                soma_gbar_Kv3=[2.0],
            )
        ]

    # Collect the results for nap 0
    def try92():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_nap=[0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base,
            base(
                soma_gbar_naRsg=[2.0],
                soma_gbar_Kv3=[2.0],
            ),
            base(
                soma_gbar_naRsg=[3.0],
            ),
            base(
                soma_gbar_naRsg=[3.0],
                soma_gbar_Kv3=[1.5],
            ),
            base(
                soma_gbar_naRsg=[3.0],
                soma_gbar_Kv3=[2.0],
            ),
            base(
                soma_gbar_naRsg=[3.0],
                soma_gbar_Kv3=[3.0],
            ),
        ]

    # nap 0, naRsg 3.0, Kv3 *
    def try93():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_naRsg=[3.0],
            soma_gbar_nap=[0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_Kv3=[None, 1.5, 2.0, 3.0],
            )
        ]

    # nap 0, naRsg 4.0, Kv3 *
    def try94():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_naRsg=[4.0],
            soma_gbar_nap=[0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_Kv3=[None, 1.5, 2.0, 3.0, 4.0],
            )
        ]

    # naRsg 4.0, Kv3 2.0, nap *
    def try95():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_naRsg=[4.0],
            soma_gbar_Kv3=[2.0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_nap=[0.5, None, 1.5, 2.0],
            )
        ]

    # naRsg 2.0, Kv3 2.0, nap *
    def try96():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_naRsg=[2.0],
            soma_gbar_Kv3=[2.0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_nap=[0.2, 0.5, 0.8, None],
            )
        ]

    # Try33 shows that more abBK decreses freq
    # naRsg 2.0, nap 0.5, Kv3 2.0, abBK *
    def try97():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_naRsg=[2.0],
            soma_gbar_nap=[0.5],
            soma_gbar_Kv3=[2.0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gabkbar_abBK=[1.2, 1.5, 1.8, 2.0],
            )
        ]

    # naRsg 2.0, nap 0.8, Kv3 2.0, abBK *
    def try98():
        base = TrySet.human_original_nice.lift()(
            soma_gbar_naRsg=[2.0],
            soma_gbar_nap=[0.8],
            soma_gbar_Kv3=[2.0],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gabkbar_abBK=[1.2, 1.5, 1.8, 2.0],
            )
        ]

    # With Zang's model, record ion currents with injection
    def try99():
        return [
            SpecSet(
                morphology=["zang2021/fig3"],
                dt=[0.02],
                tstop=[300],
                recordings=[TrySet._try64_recordings],
                injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
            )
        ]

    def try99_1():
        return [
            SpecSet(
                morphology=["zang2021/fig3"],
                dt=[0.02],
                tstop=[300],
                recordings=[TrySet._try64_recordings],
                injections=[TrySet._injection_soma(amp) for amp in [-0.2]],
            )
        ]

    def try99_2():
        return [
            SpecSet(
                morphology=["zang2021/fig3"],
                dt=[0.02],
                tstop=[300],
                recordings=[TrySet._try64_recordings],
                injections=[TrySet._injection_soma(amp) for amp in [0.0]],
            )
        ]

    # abBK *
    def try100():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gabkbar_abBK=[1.2, 1.5, 1.8, 2.0],
            )
        ]

    # CaP 0.8, abBK *
    def try101():
        base = TrySet.human_original_nice.lift()(
            soma_pcabar_newCaP=[0.8],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gabkbar_abBK=[1.2, 1.5, 1.8, 2.0],
            )
        ]

    # CaP 0.5, abBK *
    def try102():
        base = TrySet.human_original_nice.lift()(
            soma_pcabar_newCaP=[0.5],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gabkbar_abBK=[1.2, 1.5, 1.8, 2.0],
            )
        ]

    # CaP 1.5, abBK *
    def try103():
        base = TrySet.human_original_nice.lift()(
            soma_pcabar_newCaP=[1.5],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gabkbar_abBK=[1.2, 1.5, 1.8, 2.0],
            )
        ]

    # From here, focus on the first spikes, i.e. short tstop
    # naRsg: *
    def try104():
        base = TrySet.human_original_base.lift()(
            tstop=[100],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2]],
        )
        return [base(soma_gbar_naRsg=[x / 10 for x in range(20, 41)])]

    # naRsg: *, soma/dend mslo: 4.0
    def try105():
        base = TrySet.human_original_base.lift()(
            soma_gbar_mslo=[4.0],
            dend_gbar_mslo=[4.0],
            tstop=[100],
            recordings=[TrySet._try64_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2]],
        )
        return [base(soma_gbar_naRsg=[x / 10 for x in range(20, 41)])]

    # Record gating variables of naRsg
    _try106_recordings = [
        ("soma", 0.5, "v"),
        ("soma", 0.5, "ina_naRsg"),
        *[("soma", 0.5, var) for var in Config.naRsg_gating_vars],
    ]

    def try106():
        base = TrySet.human_original_base.lift()(
            tstop=[100],
            recordings=[TrySet._try106_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base]

    def try107():
        base = TrySet.human_original_nice.lift()(
            tstop=[100],
            recordings=[TrySet._try106_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base]

    def try108():
        return [
            SpecSet(
                morphology=["zang2021/fig3"],
                dt=[0.02],
                tstop=[100],
                recordings=[TrySet._try106_recordings],
            )
        ]

    # Record gating variables of naRsg
    _try109_recordings = [
        ("soma", 0.5, "v"),
        ("soma", 0.5, "ina_naRsg"),
        *[("soma", 0.5, var) for var in Config.naRsg_gating_states],
    ]

    def try109():
        base = TrySet.human_original_base.lift()(
            tstop=[100],
            recordings=[TrySet._try109_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base]

    def try110():
        base = TrySet.human_original_nice.lift()(
            tstop=[100],
            recordings=[TrySet._try109_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base]

    def try111():
        return [
            SpecSet(
                morphology=["zang2021/fig3"],
                dt=[0.02],
                tstop=[100],
                recordings=[TrySet._try109_recordings],
            )
        ]

    # Do the same to 109-111 but with updated narsg.mod, fixing a-factor
    # Use modeldb/zang2021 fix-afac branch
    def try112():
        base = TrySet.human_original_base.lift()(
            tstop=[100],
            recordings=[TrySet._try109_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base]

    def try113():
        base = TrySet.human_original_nice.lift()(
            tstop=[100],
            recordings=[TrySet._try109_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base]

    def try114():
        return [
            SpecSet(
                morphology=["zang2021/fig3"],
                dt=[0.02],
                tstop=[100],
                recordings=[TrySet._try109_recordings],
            )
        ]

    # Find the constants alfac, btfac, afac
    # To run try115, use modeldb/zang2021 fix-afac branch
    _try115_recordings = [
        *[("soma", 0.5, var) for var in Config.naRsg_gating_consts],
    ]

    def try115():
        return [
            SpecSet(
                morphology=["zang2021/fig3"],
                dt=[0.02],
                tstop=[1],
                recordings=[TrySet._try115_recordings],
            )
        ]

    _try116_recordings = [
        ("soma", 0.5, "v"),
        ("axon", 0.5, "v"),
        ("trunk_sections[1]", 0.0, "v"),
    ]

    # Record soma and axon
    def try116():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try116_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [base]

    # _try64_recordings but with v at trunk
    _try117_recordings = [
        ("soma", 0.5, "v"),
        ("soma", 0.5, "i_hpkj"),
        ("soma", 0.5, "ina_nap"),
        ("soma", 0.5, "ina_naRsg"),
        ("soma", 0.5, "ik_mslo"),
        ("soma", 0.5, "ik_Kv3"),
        ("soma", 0.5, "ica_newCaP"),
        ("soma", 0.5, "ik_SK2"),
        ("axon", 0.5, "v"),
        ("axon", 0.5, "i_hpkj"),
        ("axon", 0.5, "ina_naRsg"),
        ("axon", 0.5, "ik_Kv3"),
        ("trunk_sections[1]", 0.0, "v"),
        ("trunk_sections[1]", 0.0, "i_hpkj"),
        ("trunk_sections[1]", 0.0, "ica_newCaP"),
        ("trunk_sections[1]", 0.0, "iCa_CaT3_1"),
        ("trunk_sections[1]", 0.0, "ik_mslo"),
        ("trunk_sections[1]", 0.0, "ik_SK2"),
        ("trunk_sections[1]", 0.0, "ik_Kv1"),
        ("trunk_sections[1]", 0.0, "ik_Kv3"),
        ("trunk_sections[1]", 0.0, "ik_Kv4"),
        ("trunk_sections[1]", 0.0, "ik_Kv4s"),
    ]

    def try117():
        base = TrySet.human_original_base.lift()(
            recordings=[TrySet._try117_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                soma_gbar_naRsg=[0.0, 0.2, 0.5, 0.8],
            )
        ]

    # Variation of SK2
    def try118():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try117_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(soma_gkbar_SK2=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]),
        ]

    # SK2 0.2, CaP *
    def try119():
        base = TrySet.human_original_nice.lift()(
            soma_gkbar_SK2=[0.2],
            recordings=[TrySet._try117_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(soma_pcabar_newCaP=[0.2, 0.5, 0.8]),
        ]

    # SK2 0.5, CaP *
    def try120():
        base = TrySet.human_original_nice.lift()(
            soma_gkbar_SK2=[0.5],
            recordings=[TrySet._try117_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(soma_pcabar_newCaP=[0.2, 0.5, 0.8]),
        ]

    # Reduce dend K
    def try121():
        base = TrySet.human_original_base.lift()(
            soma_gbar_mslo=[4.0],
            dend_gbar_mslo=[4.0],
            recordings=[TrySet._try117_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(
                dend_gbar_Kv1=[x],
                dend_gbar_Kv3=[x],
                dend_gbar_Kv4=[x],
                dend_gbar_Kv4s=[x],
            )
            for x in [0.2, 0.5, 0.8]
        ]

    # SK2 0.5, CaP 0.8, BK *
    def try122():
        base = TrySet.human_original_nice.lift()(
            soma_gkbar_SK2=[0.5],
            soma_pcabar_newCaP=[0.8],
            recordings=[TrySet._try117_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(soma_gabkbar_abBK=[0.5, 0.8, None, 1.2, 1.5, 2.0, 2.5, 3.0]),
        ]

    # Variation of SK2, increasing
    def try123():
        base = TrySet.human_original_nice.lift()(
            recordings=[TrySet._try117_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(soma_gkbar_SK2=[1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0]),
        ]

    # SK2 0.5, BK 2.0, CaP *
    def try124():
        base = TrySet.human_original_nice.lift()(
            soma_gkbar_SK2=[0.5],
            soma_gabkbar_abBK=[2.0],
            recordings=[TrySet._try117_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(soma_pcabar_newCaP=[0.5, 0.6, 0.7, 0.8, 0.9, None]),
        ]

    # SK2 *, BK 2.0, CaP 0.8
    def try125():
        base = TrySet.human_original_nice.lift()(
            soma_gabkbar_abBK=[2.0],
            soma_pcabar_newCaP=[0.8],
            recordings=[TrySet._try117_recordings],
            injections=[TrySet._injection_soma(amp) for amp in [-0.2, 0.0]],
        )
        return [
            base(soma_gkbar_SK2=[0.5, 0.6, 0.7, 0.8, 0.9, None]),
        ]

    # With Zang's model, record ion currents with injection for large tstop
    def try126():
        return [
            SpecSet(
                morphology=["zang2021/fig3"],
                dt=[0.02],
                tstop=[1300],
                recordings=[TrySet._try64_recordings],
                injections=[TrySet._injection_soma(i / 10) for i in range(-5, 15, 1)],
            )
        ]


def to_key(s):
    def f(x):
        return int(x) if x.isdigit() else x

    return [f(x) for x in re.split("([0-9]+)", s)]


TrySet.all = sorted([t for t in dir(TrySet) if t.startswith("try")], key=to_key)
TrySet.last = TrySet.all[-1]

TrySet.human_original_base = Spec(
    morphology="human/original",
    adjust_soma=True,
    dt=0.01,
    tstop=300,
)

TrySet.human_original_nice = TrySet.human_original_base(
    soma_gbar_naRsg=2.0,
    soma_gbar_mslo=4.0,
    dend_gbar_mslo=4.0,
)

TrySet.human_original_nice_inj = TrySet.human_original_base(
    soma_gbar_naRsg=2.0,
    soma_gabkbar_abBK=8.0,
    soma_gbar_mslo=8.0,
    dend_gbar_mslo=4.0,
)
