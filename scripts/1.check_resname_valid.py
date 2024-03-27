import gzip
import re
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from biotite.structure.io.pdb import PDBFile, get_structure
from tqdm import tqdm

if __name__ == '__main__':
    wt_rev_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Wild Type')
    mt_rev_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Mutant')
    res_names = ['ASP', 'CYS', 'GLU', 'HIS', 'LYS', 'TYR', 'CTR', 'NTR']

    # check if res names are correct
    for i, row in wt_rev_df.iterrows():
        if row['Res Name'] not in res_names:
            print(i, row['PDB ID'], row['Res Name'], row['Res ID'])

    for i, row in mt_rev_df.iterrows():
        if row['Res Name'] not in res_names:
            print(i, row['PDB ID'], row['Res Name'], row['Res ID'])

    print('WT res names:', wt_rev_df['Res Name'].unique())
    print('MT res names:', mt_rev_df['Res Name'].unique())
