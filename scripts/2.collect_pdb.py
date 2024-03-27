import gzip
import itertools
import shutil
from pathlib import Path

import pandas as pd
from loguru import logger
from tqdm import tqdm

if __name__ == '__main__':
    wt_rev_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Wild Type')
    mt_rev_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Mutant')

    # check if residue exists in the PDB file
    deposited_wwpdb = '../database/wwpdb'
    # shutil.rmtree('pdbs', ignore_errors=True)
    Path('pdbs').mkdir(parents=True, exist_ok=True)
    pdbids = itertools.chain(
        wt_rev_df['PDB ID'].unique(), mt_rev_df['PDB ID'].unique(),
    )

    for pdbid in (pbar := tqdm(pdbids)):
        pdbid = str(pdbid).lower()
        output_path = f'pdbs/{pdbid}.pdb'
        if Path(output_path).exists():
            continue
        src = f'{deposited_wwpdb}/{pdbid[1:3]}/pdb{pdbid}.ent.gz'
        if not Path(src).exists():
            logger.error(f'{pdbid} does not exist')
            continue

        file = gzip.open(src, 'rb')
        content = file.read()
        with open(output_path, 'wb') as f:
            f.write(content)
