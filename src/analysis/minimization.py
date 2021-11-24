import numpy as np
from lmfit import Minimizer, Parameters

from ..function.simple_logistic import simple_logistic, simple_logistic_weight

def minimization(analyse):
    """Finds the best parameters and returns the metrics for the fit of a
    logistical function.

    :param analyse: instance of the :class:`.analyse.Analyse` realated to a crtc.
    :type analyse: :class:`.analyse.Analyse`"""
    df = analyse.get_eprints_count_norm() * 100.
    # We count eprints so the measurement error is its square root
    norm_incert = analyse.get_eprints_count().apply(np.sqrt)
    norm_incert['id'] = norm_incert['id'].apply(lambda x: 1. if x<1. else x)
    norm_incert['id'] = norm_incert['id'] / analyse.arxiv_stats['submissions'] * 100.

    # Convertion of dates into int
    empiric_x = ((df.index - df.index.min()) / np.timedelta64(1,'M')).values
    empiric_y = df['id'].values

    # Parameters to optimize
    params = Parameters()
    params.add('l', value=0.)
    params.add('k', value=0.)
    params.add('t0', value=0.)

    # Settings of the minimization
    minner = Minimizer(simple_logistic_weight,
                       params,
                       fcn_args=(empiric_x, empiric_y, norm_incert['id'].values),
                       calc_covar=False)
    # Minimization
    result = minner.minimize(method='leastsq')

    # Get optimal parameters
    parameters = {}
    for key in result.params.keys():
        parameters[key] = result.params[key].value

    # Regression error
    se_reg = np.sqrt(result.redchi)
    # Fit values
    _, fit_vals = simple_logistic(empiric_x,
                                  *result.params.valuesdict().values())

    # Convertion of int into date (get only the year)
    str_first_time = df.index.strftime('%Y-%m').values[0]
    t0_date = (parameters['t0'] * np.timedelta64(1, 'M')
            + np.datetime64(str_first_time))
    t0_date = str(t0_date)[:4]

    # Save metrics
    results_to_save = {
        'redchi': result.redchi,
        'se_reg': se_reg,
        't0_date': t0_date
    }
    # metrics + optimal parameters
    results_to_save = {**results_to_save, **parameters}

    return {'metrics': results_to_save, 't': df.index, 'y': fit_vals}
