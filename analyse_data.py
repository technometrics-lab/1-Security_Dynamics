"""Main file for analysing dataset"""
import argparse
from pathlib import PurePath
import os
import pandas as pd

from src.analysis.analyse import Analyse
from src.analysis.stats import stats_into_csv, metrics_into_csv
import src.graphics as graph
from src.analysis.minimization import minimization

if __name__ == '__main__' :
    # Get args
    parser = argparse.ArgumentParser(description=('Analyses the dataset and '
                                     'create all wanted graphics, stats and fits.'))
    parser.add_argument('--dataset_path',
                        action='store',
                        help='path to the e-prints folder',
                        default='data/dataset')
    parser.add_argument('--crtc_info_path',
                        action='store',
                        help='path to the file containing all information ' \
                             'related to category analyses',
                        default='data/crtc_info.csv')
    parser.add_argument('--output_path',
                        action='store',
                        help='path to the output folder',
                        default='result_analysis')
    args = parser.parse_args()

    # Cleaning path for Windows compatibility
    args.dataset_path = PurePath(args.dataset_path)
    args.crtc_info_path = PurePath(args.crtc_info_path)
    args.output_path = PurePath(args.output_path)

    # Open crtc information file
    crtc_info = pd.read_csv(args.crtc_info_path,
                            index_col=0,
                            dtype='str',
                            sep=';')

    # Init list
    analysis_list = {
        'analyse': [],
        'info_fit': [],
        'stats': [],
        'CRTC': [],
    }

    for file in sorted(os.listdir(args.dataset_path)):
        # Cluster code
        CLUSTER_CODE = file[:5]
        # Starting and ending Dates
        S_DATE = str(crtc_info['S_date'].loc[CLUSTER_CODE])
        E_DATE = str(crtc_info['E_date'].loc[CLUSTER_CODE])

        # Debug
        print(CLUSTER_CODE)

        # Process crtc
        analyse = Analyse(S_DATE,
                          E_DATE,
                          'M',
                          args.dataset_path.joinpath(file))

        graph.GraphNormEPrints(analyse).save_graph(
            args.output_path.joinpath('norm_e-prints'),
            CLUSTER_CODE)

        graph.GraphNormEPrintsVsCyber(analyse).save_graph(
            args.output_path.joinpath('e-prints_vs_cyber_e-prints'),
            CLUSTER_CODE)

        graph.GraphShareOfCyber(analyse).save_graph(
            args.output_path.joinpath('cyber_share'),
            CLUSTER_CODE)

        graph.GraphShareOfCyberSmall(analyse, CLUSTER_CODE).save_graph(
            args.output_path.joinpath('small_cyber_share'),
            CLUSTER_CODE)

        graph.GraphOpinionDistrib(analyse,
                                  analyse.get_opinion_quantiles()).save_graph(
            args.output_path.joinpath('opinion_distrib'),
            CLUSTER_CODE)

        graph.GraphOpinionDistribSmall(analyse,
                                       analyse.get_opinion_quantiles(),
                                       CLUSTER_CODE).save_graph(
            args.output_path.joinpath('small_opinion_distrib'),
            CLUSTER_CODE)

        # Cyber opinion
        graph.GraphOpinionDistrib(analyse,
                                  analyse.get_cyber_opinion_quantiles()).save_graph(
            args.output_path.joinpath('cyber_opinion_distrib'),
            CLUSTER_CODE)

        graph.GraphOpinionDistribSmall(analyse,
                                       analyse.get_cyber_opinion_quantiles(),
                                       CLUSTER_CODE).save_graph(
            args.output_path.joinpath('small_cyber_opinion_distrib'),
            CLUSTER_CODE)

        # Calcul sigmoid fit for the normalized number of uploads
        info_fit = minimization(analyse)

        graph.GraphNormEPrintsFit(analyse, info_fit).save_graph(
            args.output_path.joinpath('fit_norm_e-prints'),
            CLUSTER_CODE)

        graph.GraphNormEPrintsFitSmall(analyse,
                                       info_fit, CLUSTER_CODE).save_graph(
            args.output_path.joinpath('small_fit_norm_e-prints'),
            CLUSTER_CODE)

        graph.GraphExpMeanShareCyber(analyse).save_graph(
            args.output_path.joinpath('exp_mean_cyber_share'),
            CLUSTER_CODE)

        graph.GraphExpMeanShareCyberSmall(analyse, CLUSTER_CODE).save_graph(
            args.output_path.joinpath('small_exp_mean_cyber_share'),
            CLUSTER_CODE)

        # Keep values for final aggregation
        analysis_list['analyse'].append(analyse)
        analysis_list['info_fit'].append(info_fit)
        analysis_list['CRTC'].append(CLUSTER_CODE)

    # Final aggregation
    graph.GraphAllNormFit(analysis_list).save_graph(
        args.output_path.joinpath('fit_norm_e-prints'),
        'all')

    stats_into_csv(analysis_list, 3, args.output_path.joinpath('stats'))
    metrics_into_csv(analysis_list, 3, args.output_path.joinpath('stats'))
