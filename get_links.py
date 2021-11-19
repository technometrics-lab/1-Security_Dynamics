"""Main file to retrieve arXiv categories from arXiv API."""
import argparse
from pathlib import PurePath, Path
from datetime import datetime
import pandas as pd

from src.query_making.query_arxiv_cat import QueryArXivCat

if __name__ == '__main__' :
    # Get command line args
    parser = argparse.ArgumentParser(description=('Makes queries and does them '
                                     'on the arXiv API in order to create a database.'))
    parser.add_argument('--output',
                        dest='output',
                        action='store',
                        help='path to the output folder',
                        default='data/')
    parser.add_argument('--categories',
                        dest='categories_path',
                        action='store',
                        help='path to the file containing the list of categories',
                        default='data/crtc_info.csv')
    args = parser.parse_args()

    # Creation of folders
    cur_time = datetime.now().strftime('%Y_%m_%d')

    # Cleaning path for Windows compatibility
    e_prints_path = PurePath(args.output).joinpath('query_e-prints_' + cur_time)
    cyber_e_prints_path = PurePath(args.output).joinpath('cyber_e_prints_' + cur_time)
    args.categories_path = PurePath(args.categories_path)

    # mkdir
    Path(e_prints_path).mkdir(parents=True, exist_ok=True)
    Path(cyber_e_prints_path).mkdir(parents=True, exist_ok=True)

    # Format queries
    query_formater = lambda key: 'ti:' + key + ' OR abs:' + key
    cyber_keywords = '%28' + query_formater('secur*') + ' OR ' \
                           + query_formater('safe*') + ' OR ' \
                           + query_formater('reliability') + ' OR ' \
                           + query_formater('dependability') + ' OR ' \
                           + query_formater('confidentiality') + ' OR ' \
                           + query_formater('integrity') + ' OR ' \
                           + query_formater('availability') + ' OR ' \
                           + query_formater('defen*') + ' OR ' \
                           + query_formater('priva*') + '%29'

    # Open the list of categories
    categories = pd.read_csv(args.categories_path,
                             sep=';',
                             dtype='string')['CRTC']

    for category in categories.values:
        # All e-prints in a category
        query = QueryArXivCat(e_prints_path, category)
        query.processing()

        # Only e-prints with security considerations in a category
        query = QueryArXivCat(cyber_e_prints_path, category, cyber_keywords)
        query.processing()
