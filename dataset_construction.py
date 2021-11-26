"""Script to merge dataset into a single one."""
import argparse
import os
from pathlib import PurePath, Path
import pandas as pd

if __name__ == '__main__' :
    # Get args
    parser = argparse.ArgumentParser(description='Merge all dataset into a single one.')
    parser.add_argument('--eprints',
                        dest='e_prints_path',
                        action='store',
                        default=PurePath('data').joinpath('query_e-prints_2021_11_11'))
    parser.add_argument('--ceprints',
                        dest='cyber_eprints_path',
                        action='store',
                        default=PurePath('data').joinpath('cyber_e_prints_2021_11_11'))
    parser.add_argument('--opinion',
                        dest='opinion_path',
                        action='store',
                        default=PurePath('data').joinpath('opinion_2021_11_11'))
    parser.add_argument('--output',
                        dest='output_path',
                        action='store',
                        default=PurePath('data').joinpath('dataset'))
    args = parser.parse_args()

    # Cleaning path for Windows compatibility
    args.e_prints_path = PurePath(args.e_prints_path)
    args.cyber_eprints_path = PurePath(args.cyber_eprints_path)
    args.opinion_path = PurePath(args.opinion_path)
    args.output_path = PurePath(args.output_path)

    # Get path
    e_prints_files = sorted(os.listdir(args.e_prints_path))
    cyber_e_prints_files = sorted(os.listdir(args.cyber_eprints_path))
    opinion_files = sorted(os.listdir(args.opinion_path))

    # mkdir
    Path(args.output_path).mkdir(parents=True, exist_ok=True)

    files_path = []
    for q_file, c_q_file, s_file, in zip(e_prints_files,
                                         cyber_e_prints_files,
                                         opinion_files):
        # Open all files
        df_eprints = pd.read_csv(args.e_prints_path.joinpath(q_file),
                                 index_col=0,
                                 dtype='str')
        df_ceprints = pd.read_csv(args.cyber_eprints_path.joinpath(c_q_file),
                                  index_col=0,
                                  dtype='str')
        df_opinion = pd.read_csv(args.opinion_path.joinpath(s_file),
                                 index_col=0,
                                 dtype='str').sort_index()

        df_ceprints['cyber'] = [True for _ in range(len(df_ceprints))]

        # Create the final dataset
        merged_df = df_eprints.merge(df_ceprints[['id', 'cyber']],
                                     how='left',
                                     on='id').fillna('False').join(df_opinion)
        # Write it into a new file
        merged_df.to_csv(args.output_path.joinpath(q_file), mode='w')
