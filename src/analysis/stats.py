from pathlib import Path
import pandas as pd

def get_basic_stats(serie):
    """Compute basic stats: mean, median, std, skewness, kurtosis.

    :param serie: input serie to compute.
    :type serie: :class:`pandas.Serie`"""
    mean = serie.mean()
    median = serie.median()
    std = serie.std()
    skewness = serie.skew()
    kurtosis = serie.kurtosis()
    # return [mean, median, std, skewness, kurtosis]
    return {
    'mean': mean,
    'median': median,
    'std': std,
    'skewness': skewness,
    'kurtosis': kurtosis
    }

def append_into_dict(crtc, dict_src, new_dict):
    for key, value in new_dict.items():
        dict_src[key].append(value)
    dict_src['CRTC'].append(crtc)

def stats_into_csv(analysis_list, float_nb, output_path):
    """Compute basic stats all crtc.

    :param analysis_list: list of :class:`.analyse.Analyse` instance.
    :type analysis_list: [:class:`.analyse.Analyse`]

    :param float_nb: number of decimal points.
    :type float_nb: int

    :param output_path: output path to the result folder.
    :type output_path: :class:`pathlib.PurePath`"""
    eprints = {
        'CRTC': [],
        'mean': [],
        'median': [],
        'std': [],
        'skewness': [],
        'kurtosis': []
    }
    cyber_eprints = {
        'CRTC': [],
        'mean': [],
        'median': [],
        'std': [],
        'skewness': [],
        'kurtosis': []
    }
    opinion = {
        'CRTC': [],
        'mean': [],
        'median': [],
        'std': [],
        'skewness': [],
        'kurtosis': []
    }
    cyber_opinion = {
        'CRTC': [],
        'mean': [],
        'median': [],
        'std': [],
        'skewness': [],
        'kurtosis': []
    }

    summary_stats = {
        'CRTC': [],
        'eprints': [],
        'cyber_eprints': [],
        'share_percent': []
    }

    for analyse, crtc in zip(analysis_list['analyse'], analysis_list['CRTC']):
        eprints_sum = analyse.get_eprints_count()['id'].sum()
        cyber_eprints_sum = analyse.get_cyber_eprints_count()['id'].sum()

        append_into_dict(crtc,
                         summary_stats,
                         {
                             'eprints': eprints_sum,
                             'cyber_eprints': cyber_eprints_sum,
                             'share_percent' : (cyber_eprints_sum
                                                / eprints_sum * 100.)
                         })

        append_into_dict(crtc,
                         eprints,
                         get_basic_stats(analyse.get_eprints_count_norm()['id']))
        append_into_dict(crtc,
                         cyber_eprints,
                         get_basic_stats(analyse.get_cyber_eprints_count_norm()['id']))
        append_into_dict(crtc,
                         opinion,
                         get_basic_stats(analyse.dataset_clean['opinion']))
        append_into_dict(crtc,
                         cyber_opinion,
                         get_basic_stats(analyse.dataset_clean[
                             analyse.dataset_clean['cyber']==True]['opinion']))

    # Save
    pd.DataFrame(eprints).to_csv(output_path.joinpath('eprints.csv'),
                                 float_format=''.join(['%.', str(float_nb), 'f']))
    pd.DataFrame(cyber_eprints).to_csv(output_path.joinpath('cyber_eprints.csv'),
                                       float_format=''.join(['%.', str(float_nb), 'f']))
    pd.DataFrame(opinion).to_csv(output_path.joinpath('opinion.csv'),
                                 float_format=''.join(['%.', str(float_nb), 'f']))
    pd.DataFrame(cyber_opinion).to_csv(output_path.joinpath('cyber_opinion.csv'),
                                       float_format=''.join(['%.', str(float_nb), 'f']))
    pd.DataFrame(summary_stats).to_csv(output_path.joinpath('summary.csv'),
                                       float_format=''.join(['%.', str(float_nb), 'f']))

def metrics_into_csv(analysis_list, float_nb, output_path):
    """Save metrics of all crtc into a csv file.

    :param analysis_list: list of :class:`.analyse.Analyse` instance.
    :type analysis_list: [:class:`.analyse.Analyse`]

    :param float_nb: number of decimal points.
    :type float_nb: int

    :param output_path: output path to the result folder.
    :type output_path: :class:`pathlib.PurePath`"""
    all_metrics = {'CRTC': [],
                   'redchi': [],
                   'se_reg': [],
                   'l': [],
                   'k': [],
                   't0': [],
                   't0_date': []}
    info_fits = [info_fit['metrics'] for info_fit in analysis_list['info_fit']]
    for metrics, crtc in zip(info_fits, analysis_list['CRTC']):
        append_into_dict(crtc, all_metrics, metrics)
    pd.DataFrame(all_metrics).to_csv(output_path.joinpath('fit_metrics.csv'),
                                     float_format=''.join(['%.', str(float_nb), 'f']))
