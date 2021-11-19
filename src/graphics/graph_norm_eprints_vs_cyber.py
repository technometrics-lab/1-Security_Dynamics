import numpy as np
import matplotlib.pyplot as plt
from .graphic_base import GraphicBase

class GraphNormEPrintsVsCyber(GraphicBase):
    """Draws the normalized amount of e-prints and cyber ones of a CRTC.

    :param analyse: :class:`src.analysis.Analyse` instance.
    :type analyse: :class:`src.analysis.Analyse`"""
    def __init__(self, analyse):
        GraphicBase.__init__(self,
                               '',
                               '',
                               '',
                               'e-prints (\%)')

        eprints = analyse.get_eprints_count_norm()
        cyber_eprints = analyse.get_cyber_eprints_count_norm()

        self.ax.scatter(eprints.index, eprints.values,
                        label='e-prints (total)')
        self.ax.scatter(cyber_eprints.index, cyber_eprints.values,
                        label='e-prints with security considerations')

        self.ax.set_xlim(left=np.datetime64(analyse.S_DATE),
                         right=np.datetime64(analyse.E_DATE))
        self.ax.set_ylim(0)

        plt.legend(loc='upper left', fontsize=25)
