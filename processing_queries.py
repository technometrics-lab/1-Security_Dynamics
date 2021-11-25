"""Main file for processing e-prints and getting opinion of them.
To retrieve and update the local copy of arXiv files, use:

    gsutil -m rsync -r gs://arxiv-dataset/arxiv/ dest/
"""
import argparse
import os
from pathlib import PurePath, Path
import pandas as pd

from src.processing.opinion import OpinionProcessing

if __name__ == '__main__' :
    # Get command line args
    parser = argparse.ArgumentParser(description=('Processes opinion on e-prints'
                                     ' database.'))
    parser.add_argument('--arxiv',
                        dest='arxiv_path',
                        action='store',
                        help='path to the arxiv folder',
                        default='/mnt/arxiv')
    parser.add_argument('--eprints',
                        dest='eprints_path',
                        action='store',
                        help='path to the e-prints folder',
                        default='data/query_e-prints_2021_11_11')
    parser.add_argument('--output',
                        dest='output',
                        action='store',
                        help='path to the output folder',
                        default='result')
    args = parser.parse_args()

    # Cleaning path for Windows compatibility
    args.arxiv_path = PurePath(args.arxiv_path)
    args.eprints_path = PurePath(args.eprints_path)
    args.output = PurePath(args.output)

    # mkdir
    Path(args.output).mkdir(parents=True, exist_ok=True)

    # Get list of all files sorted
    queries_files = sorted(os.listdir(args.eprints_path))

    def url_to_arxiv_folder(path: str, arxiv_path: PurePath):
        """Modify URL into path"""
        return arxiv_path.joinpath(path)

    # For each files
    for query in queries_files :
        # Get crtc name
        crtc_name = query[3:3 + 2]
        # Read file and update the arXiv path
        df = pd.read_csv(args.eprints_path.joinpath(query),
                         dtype='str')
        df['arxiv_path'] = df['arxiv_path'].apply(url_to_arxiv_folder,
                                                  args=[args.arxiv_path])
        # Init the opinion analysis
        sentiAnalysis = OpinionProcessing(df['arxiv_path'],
                                          args.output, crtc_name)
        # Processing
        sentiAnalysis.processing(len(os.sched_getaffinity(0)))
