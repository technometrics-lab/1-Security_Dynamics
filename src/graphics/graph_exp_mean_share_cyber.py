import numpy as np
from .graphic_base import GraphicBase

class GraphExpMeanShareCyber(GraphicBase):
    """Draws the expanding mean of the security share of a CRTC.

    :param analyse: :class:`..analysis.Analyse` instance.
    :type analyse: :class:`..analysis.Analyse`"""
    def __init__(self, analyse):
        GraphicBase.__init__(self,
                               '',
                               '',
                               '',
                               'Mean (\%)')

        exp_mean_cyber_eprints = (analyse.get_cyber_eprints_count() /
                                  analyse.get_eprints_count()).rolling(12).mean()

        self.ax.plot(exp_mean_cyber_eprints.index,
                     exp_mean_cyber_eprints.values,
                     color = 'tab:orange')

        self.ax.set_xlim(left = np.datetime64(analyse.S_DATE),
                         right = np.datetime64(analyse.E_DATE))
        self.ax.set_ylim(0)

class GraphExpMeanShareCyberSmall(GraphicBase):
    """Draws the small version of the expanding mean of the security share of
    a CRTC.

    :param analyse: :class:`src.analysis.Analyse` instance.
    :type analyse: :class:`src.analysis.Analyse`

    :param crtc_code: CRTC code.
    :type crtc_code: str"""
    def __init__(self, analyse, crtc_code):
        GraphicBase.__init__(self,
                               crtc_code,
                               '',
                               '',
                               'Mean (\%)',
                               figsize=(6.4, 4.8),
                               fontsize=10)

        exp_mean_cyber_eprints = (analyse.get_cyber_eprints_count() /
                                  analyse.get_eprints_count()).expanding(1).mean()

        self.ax.plot(exp_mean_cyber_eprints.index,
                     exp_mean_cyber_eprints.values,
                     color = 'tab:orange')

        self.ax.set_xlim(left = np.datetime64(analyse.S_DATE),
                         right = np.datetime64(analyse.E_DATE))
        self.ax.set_ylim(0)
