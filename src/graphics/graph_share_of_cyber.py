import numpy as np
from .graphic_base import GraphicBase

class GraphShareOfCyber(GraphicBase):
    """Draws the security share of a CRTC.

    :param analyse: :class:`src.analysis.Analyse` instance.
    :type analyse: :class:`src.analysis.Analyse`"""
    def __init__(self, analyse):
        GraphicBase.__init__(self,
                             '',
                             '',
                             '',
                             'Percent (\%)')

        cyber_eprints = (analyse.get_cyber_eprints_count()
                        / analyse.get_eprints_count())

        self.ax.plot(cyber_eprints.index,
                     cyber_eprints.values * 100,
                     'o',
                     color = 'tab:orange')

        self.ax.set_xlim(left = np.datetime64(analyse.S_DATE),
                         right = np.datetime64(analyse.E_DATE))
        self.ax.set_ylim(0, 100)

class GraphShareOfCyberSmall(GraphicBase):
    """Draws the small version of the security share of a CRTC.

    :param analyse: :class:`src.analysis.Analyse` instance.
    :type analyse: :class:`src.analysis.Analyse`

    :param crtc_code: CRTC code.
    :type crtc_code: str"""
    def __init__(self, analyse, crtc_code):
        GraphicBase.__init__(self,
                               crtc_code,
                               '',
                               '',
                               'Percent (\%)',
                               figsize=(6.4, 4.8),
                               fontsize=10)

        cyber_eprints = (analyse.get_cyber_eprints_count()
                        / analyse.get_eprints_count())

        self.ax.plot(cyber_eprints.index,
                     cyber_eprints.values * 100,
                     'o',
                     color = 'tab:orange',
                     markersize=2)

        self.ax.set_xlim(left = np.datetime64(analyse.S_DATE),
                         right = np.datetime64(analyse.E_DATE))
        self.ax.set_ylim(0)
