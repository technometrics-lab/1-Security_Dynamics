import numpy as np
from .graphic_base import GraphicBase

class GraphNormEPrints(GraphicBase):
    """Draws the normalized amount of e-prints of a CRTC.

    :param analyse: :class:`src.analysis.Analyse` instance.
    :type analyse: :class:`src.analysis.Analyse`"""
    def __init__(self, analyse):
        GraphicBase.__init__(self,
                             '',
                             '',
                             '',
                             'Uploads (\%)')

        eprints = analyse.get_eprints_count_norm()

        self.ax.plot(eprints.index,
                     eprints.values * 100,
                     'o',
                     color='b')

        self.ax.set_xlim(left = np.datetime64(analyse.S_DATE),
                         right = np.datetime64(analyse.E_DATE))
        self.ax.set_ylim(0)
