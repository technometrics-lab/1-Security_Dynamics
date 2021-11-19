import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .graphic_base import GraphicBase

class GraphNormEPrintsFit(GraphicBase):
    def __init__(self, analyse, fit_info):
        """Draws the normalized amount of e-prints of a CRTC.

        :param analyse: :class:`src.analysis.Analyse` instance.
        :type analyse: :class:`src.analysis.Analyse`

        :param fit_info: information on the fit for this CRTC.
        :type fit_info: dict"""
        GraphicBase.__init__(self,
                               '',
                               '',
                               '',
                               'e-prints (\%)')

        eprints = analyse.get_eprints_count_norm() * 100.

        self.plot_empiric = self.ax.scatter(eprints.index,
                                            eprints.values,
                                            color = 'b')

        self.plot_fit, = self.ax.plot(eprints.index,
                                      fit_info['y'],
                                      color = 'r')

        # Center the graph on 0
        self.ax.set_ylim(0)
        self.ax.set_xlim(left=np.datetime64(analyse.S_DATE),
                         right=np.datetime64(analyse.E_DATE))

        # Specify the legend
        self.add_text_legend('Data', self.plot_empiric)
        self.add_text_legend(r'$\sigma(t) = \frac{L}{1 + e^{-k(t -t_0)}}$',
                             self.plot_fit)
        self.add_text_legend('Metrics :')
        self.add_text_legend(r'$\chi_{\nu}^{2}$ : ' + '{:.2f}'.format(fit_info['metrics']['redchi']))
        self.add_text_legend('RSE : {:.2f}'.format(fit_info['metrics']['se_reg']))
        self.add_text_legend('L = {:.2f}'.format(fit_info['metrics']['l']))

        # Convertion for dates
        str_first_time = eprints.index.strftime('%Y-%m').values[0]
        t0_date = (fit_info['metrics']['t0'] * np.timedelta64(1, 'M')
                + np.datetime64(str_first_time))

        self.add_text_legend('$t_0$ : ' + str(t0_date)[:4])
        self.add_text_legend('k : {:.2f}'.format(fit_info['metrics']['k']))

        self.show_legend()

        # Display t0 on the x axis
        if (np.datetime64(t0_date) < np.datetime64(analyse.E_DATE)
            and np.datetime64(t0_date) > np.datetime64(analyse.S_DATE)):

            inf_point = fit_info['y'][int(fit_info['metrics']['t0'])]
            plt.vlines(t0_date, 0, inf_point,
                colors='#058B8C',
                linestyles='dashed',
                linewidths=3)

class GraphNormEPrintsFitSmall(GraphicBase):
    def __init__(self, analyse, fit_info, crtc_code):
        """Draws the small version of the normalized amount of e-prints of a CRTC.

        :param analyse: :class:`src.analysis.Analyse` instance.
        :type analyse: :class:`src.analysis.Analyse`

        :param fit_info: information on the fit for this CRTC.
        :type fit_info: dict

        :param crtc_code: CRTC code.
        :type crtc_code: str"""
        GraphicBase.__init__(self,
                             crtc_code,
                             '',
                             '',
                             'e-prints (\%)',
                             figsize=(6.4, 4.8),
                             fontsize=10)

        eprints = analyse.get_eprints_count_norm() * 100.

        self.plot_empiric = self.ax.scatter(eprints.index,
                                            eprints.values,
                                            color = 'b',
                                            s=[1 for _ in range(len(eprints.index))])

        self.plot_fit, = self.ax.plot(eprints.index,
                                      fit_info['y'],
                                      color = 'r')

        # Center the graph on 0
        self.ax.set_ylim(0, max(eprints[eprints.index < analyse.E_DATE].values))
        self.ax.set_xlim(left = np.datetime64(analyse.S_DATE),
                         right = np.datetime64(analyse.E_DATE))

        str_first_time = eprints.index.strftime('%Y-%m').values[0]
        t0_date = (fit_info['metrics']['t0'] * np.timedelta64(1, 'M')
                + np.datetime64(str_first_time))

        # Display t0 on the X axe
        if (np.datetime64(t0_date) < np.datetime64(analyse.E_DATE)
            and np.datetime64(t0_date) > np.datetime64(analyse.S_DATE)):

            inf_point = fit_info['y'][int(fit_info['metrics']['t0'])]
            plt.vlines(t0_date, 0, inf_point,
                colors = '#058B8C',
                linestyles = 'dashed',
                linewidths = 1)

class GraphAllNormFit(GraphicBase):
    """Draws all normalized amount of e-prints fits of each CRTC.

    :param analyse: :class:`src.analysis.Analyse` instance.
    :type analyse: :class:`src.analysis.Analyse`"""
    def __init__(self, analysis_list):
        GraphicBase.__init__(self,
                               '',
                               '',
                               '',
                               'Normalized fits of e-prints')

        colors = ['dimgray',
                  'lightgray',
                  'lightcoral',
                  'brown',
                  'red',
                  'tomato',
                  'sandybrown',
                  'orange',
                  'bisque',
                  'goldenrod',
                  'gold',
                  'olive',
                  'olivedrab',
                  'palegreen',
                  'lime',
                  'aquamarine',
                  'paleturquoise',
                  'turquoise',
                  'cyan',
                  'deepskyblue',
                  'violet',
                  'fuchsia',
                  'pink']

        t_fits = [info_fit['t'] for info_fit in analysis_list['info_fit']]
        y_fits = [info_fit['y'] for info_fit in analysis_list['info_fit']]

        for t_fit, y_fit, index, crtc in zip(t_fits,
                                             y_fits,
                                             range(len(t_fits)),
                                             analysis_list['CRTC']):
            y_norm = y_fit / y_fit.max()
            lines ,= self.ax.plot(t_fit, y_norm, color=colors[index])
            self.add_text_legend(crtc, lines)

        self.ax.set_ylim(0)
        self.ax.set_xlim(left=np.datetime64('2000'),
                         right=np.datetime64('2021-04'))
        self.show_legend(size=25)
