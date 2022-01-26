import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .graphic_base import GraphicBase

class GraphOpinionDistrib(GraphicBase):
    """Draws the opinion distribution of a CRTC.

    :param analyse: :class:`src.analysis.Analyse` instance.
    :type analyse: :class:`src.analysis.Analyse`

    :param quantiles: contain the first, second and third quantiles.
    :type quantiles: :class:`pandas.DataFrame`"""
    def __init__(self, analyse, quantiles):
        GraphicBase.__init__(self,
                               '',
                               '',
                               '',
                               'Opinion')

        plot_q_1 ,= self.ax.plot(quantiles.index,
                                 quantiles['quantile_1'],
                                 color = '#2C75FF')
        plot_q_2 ,= self.ax.plot(quantiles.index,
                                 quantiles['quantile_2'],
                                 'o',
                                 color = '#0F056B')
        plot_q_3 ,= self.ax.plot(quantiles.index,
                                 quantiles['quantile_3'],
                                 color = '#2C75FF')

        self.ax.fill_between(quantiles.index,
                             quantiles['quantile_2'],
                             quantiles['quantile_1'],
                             facecolor='#2C75FF',
                             alpha = 0.2)

        self.ax.fill_between(quantiles.index,
                             quantiles['quantile_2'],
                             quantiles['quantile_3'],
                             facecolor='#2C75FF',
                             alpha = 0.2)

        plt.axhline(0, color= 'black')

        self.add_text_legend('Quantile 1', plot_q_1)
        self.add_text_legend('Median', plot_q_2)
        self.add_text_legend('Quantile 3', plot_q_3)

        self.show_legend()

        # self.ax.set_ylim(0.005, 0.015)
        #
        self.ax.set_xlim(left = np.datetime64(analyse.S_DATE),
                         right = np.datetime64(analyse.E_DATE))

class GraphOpinionDistribSmall(GraphicBase):
    """Draws the small version of the opinion distribution of a CRTC.

    :param analyse: :class:`src.analysis.Analyse` instance.
    :type analyse: :class:`src.analysis.Analyse`

    :param quantiles: contain the first, second and third quantiles.
    :type quantiles: :class:`pandas.DataFrame`

    :param crtc_code: CRTC code.
    :type crtc_code: str"""
    def __init__(self, analyse, quantiles, crtc_code):
        GraphicBase.__init__(self,
                               crtc_code,
                               '',
                               '',
                               'Opinion',
                               figsize=(6.4, 4.8),
                               fontsize=14)

        self.ax.plot(quantiles.index,
                     quantiles['quantile_1'],
                     color = '#2C75FF',
                     linewidth=0.2,
                     markersize=2)
        self.ax.plot(quantiles.index,
                     quantiles['quantile_2'],
                     'o',
                     color = '#0F056B',
                     linewidth=0.2,
                     markersize=2)
        self.ax.plot(quantiles.index,
                     quantiles['quantile_3'],
                     color = '#2C75FF',
                     linewidth=0.2,
                     markersize=2)

        self.ax.fill_between(quantiles.index,
                             quantiles['quantile_2'],
                             quantiles['quantile_1'],
                             facecolor='#2C75FF',
                             alpha = 0.2)

        self.ax.fill_between(quantiles.index,
                             quantiles['quantile_2'],
                             quantiles['quantile_3'],
                             facecolor='#2C75FF',
                             alpha = 0.2)

        plt.axhline(0, color= 'black')

        # self.ax.set_ylim(0.005, 0.015)
        #
        self.ax.set_xlim(left = np.datetime64(analyse.S_DATE),
                         right = np.datetime64(analyse.E_DATE))
