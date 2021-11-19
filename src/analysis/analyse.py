import os
import urllib.request
import pandas as pd
from pandas.tseries.offsets import MonthEnd

class Analyse:
    """The Analyse class process .csv files inclued into dataset_path and
    process it.

    :param start_date: The starting date of the analyse, all data before this
        date is ignored. The format must be : 'YYYY-MM' or only 'YYYY'.
    :type start_date: str
    :param end_date: The ending date of the analyse, all data after this date
        is ignored. The format must be : 'YYYY-MM' or only 'YYYY'.
    :type end_date: str
    :param freq: The frequency of result output. Authorized value : 'M' for a
        monthly frequency or 'Y' for an annual frequency.
    :type freq: str
    :param dataset_path: The input folder path containing all .csv files.
    :type dataset_path: str
    """
    def __init__(self, start_date, end_date, freq, dataset_path):
        # Parameters of the analysis
        # Period to analyse
        #: Starting date.
        self.S_DATE = pd.to_datetime(start_date, utc=True)
        #: Ending date.
        self.E_DATE = pd.to_datetime(end_date, utc=True)

        # Grouper use to group by frequency on the published column
        if freq not in ['M', 'Y']:
            raise TypeError('freq must be M or Y')
        self.__gp = pd.Grouper(key='published', freq=freq)
        self.__freq = freq

        ##################################
        # Inputs
        ##################################
        #: Raw ``pandas.DataFrame`` dataset.
        self.dataset_raw = pd.read_csv(dataset_path,
                                       index_col=0,
                                       dtype={
                                           'id': 'str',
                                           'version': 'str',
                                           'primary_category': 'str',
                                           'arxiv_path': 'str',
                                           'http_link': 'str',
                                           'cyber': 'bool',
                                           'opinion': 'float'
                                       },
                                       parse_dates=[
                                           'published',
                                           'updated',
                                       ])
        self.dataset_raw.drop(['arxiv_path', 'http_link'], axis=1, inplace=True)

        # Cleaning Input for the analyse period
        #: Clean ``pandas.DataFrame`` dataset (in the current period).
        self.dataset_clean = self.cleaning_period(self.dataset_raw, 'published')

        # Init the normalization
        self.__init_normalization()

    def cleaning_period(self, df: pd.DataFrame, col_name) -> pd.DataFrame:
        """Remove data which is not in the interval"""
        # Mask construction
        mask = df[col_name] < self.S_DATE
        mask = mask | (df[col_name] >= self.E_DATE)
        # Check if there is something to do, to avoid an error
        if True in mask :
            # Cleaning DataFrame
            df = df.drop(df[mask].index)
            return df
        return df

    def get_eprints_count(self) -> pd.DataFrame:
        """"""
        df = self.dataset_clean.groupby(self.__gp).count()
        return df.drop(['updated',
                        'version',
                        'primary_category',
                        'all_categories',
                        'cyber',
                        'opinion'],
                       axis=1)

    def get_cyber_eprints_count(self) -> pd.DataFrame:
        """"""
        df = self.dataset_clean[self.dataset_clean['cyber'] == True]
        df = df.groupby(self.__gp).count()
        return df.drop(['updated',
                        'version',
                        'primary_category',
                        'all_categories',
                        'cyber',
                        'opinion'],
                       axis=1)

    def get_eprints_count_norm(self) -> pd.DataFrame:
        """"""
        df = self.get_eprints_count()
        df['id'] = df['id'] / self.arxiv_stats['submissions']
        return df

    def get_cyber_eprints_count_norm(self) -> pd.DataFrame:
        """"""
        df = self.get_cyber_eprints_count()
        df['id'] = df['id'] / self.arxiv_stats['submissions']
        return df

    def get_opinion_quantiles(self) -> pd.DataFrame:
        df = self.dataset_clean.drop(['updated',
                    'version',
                    'primary_category',
                    'all_categories',
                    'cyber'],
                    axis=1).groupby(self.__gp)
        quantiles = {
            'quantile_1': df['opinion'].quantile(0.25),
            'quantile_2': df['opinion'].quantile(0.5),
            'quantile_3': df['opinion'].quantile(0.75),
        }
        return pd.DataFrame(quantiles)

    def get_cyber_opinion_quantiles(self) -> pd.DataFrame:
        df = self.dataset_clean[self.dataset_clean['cyber'] == True]
        df = df.drop(['updated',
                      'version',
                      'primary_category',
                      'all_categories',
                      'cyber'],
                      axis=1).groupby(self.__gp)
        quantiles = {
            'quantile_1': df['opinion'].quantile(0.25),
            'quantile_2': df['opinion'].quantile(0.5),
            'quantile_3': df['opinion'].quantile(0.75),
        }
        return pd.DataFrame(quantiles)

    def __init_normalization(self) :
        """Init a serie which contain arXiv stats"""
        # Retrieve arXiv stats if the file doesn't exist
        if os.path.exists('data/arxiv_monthly_stats.csv') :
            pass
        else :
            urllib.request.urlretrieve(
                'https://arxiv.org/stats/get_monthly_submissions',
                'data/arxiv_monthly_stats.csv')

        # Open the file
        arxiv_stats = pd.read_csv('data/arxiv_monthly_stats.csv',
                                  parse_dates=['month'],
                                  index_col='month',
                                  date_parser=lambda x: pd.to_datetime(x, utc=True) + MonthEnd(1))

        # Remove excedent
        arxiv_stats.drop(['historical_delta'], axis=1, inplace=True)

        # Stock into the object
        self.arxiv_stats = arxiv_stats
