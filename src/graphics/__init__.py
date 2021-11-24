"""All graphs are implemented in this module"""

__all__ = ['GraphicBase',
           'GraphNormEPrints',
           'GraphNormEPrintsVsCyber',
           'GraphShareOfCyber',
           'GraphShareOfCyberSmall',
           'GraphOpinionDistrib',
           'GraphOpinionDistribSmall',
           'GraphNormEPrintsFit',
           'GraphNormEPrintsFitForecast',
           'GraphNormEPrintsFitSmall',
           'GraphExpMeanShareCyber',
           'GraphAllNormFit']

# Import of graphs without GraphiqueBase
from .graph_norm_eprints import GraphNormEPrints
from .graph_norm_eprints_vs_cyber import GraphNormEPrintsVsCyber
from .graph_share_of_cyber import GraphShareOfCyber, GraphShareOfCyberSmall
from .graph_opinion_distrib import GraphOpinionDistrib, GraphOpinionDistribSmall
from .graph_norm_eprints_fit import GraphNormEPrintsFit, \
                                    GraphNormEPrintsFitSmall, \
                                    GraphAllNormFit
from .graph_norm_eprints_fit_forecast import GraphNormEPrintsFitForecast

from .graph_exp_mean_share_cyber import GraphExpMeanShareCyber, \
                                        GraphExpMeanShareCyberSmall
