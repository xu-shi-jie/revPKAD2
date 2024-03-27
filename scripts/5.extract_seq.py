
import os
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from Bio import SeqIO
from biotite.structure.io.pdb import PDBFile, get_structure
from loguru import logger
from tqdm import tqdm

three_to_one = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C',
    'GLN': 'Q', 'GLU': 'E', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I',
    'LEU': 'L', 'LYS': 'K', 'MET': 'M', 'PHE': 'F', 'PRO': 'P',
    'SER': 'S', 'THR': 'T', 'TRP': 'W', 'TYR': 'Y', 'VAL': 'V'
}


def fetch_seq(file, chain):
    atoms = get_structure(PDBFile.read(file))[0]
    ca_atoms = atoms[(atoms.chain_id == chain) & (atoms.atom_name == 'CA')]
    # change res_id > 9900 to res_id - 10000
    ca_atoms.res_id = np.where(
        ca_atoms.res_id > 9900, ca_atoms.res_id-10000,
        ca_atoms.res_id)
    min_ri, max_ri = ca_atoms.res_id.min(), ca_atoms.res_id.max()
    seq = ''
    for i in np.arange(min_ri, max_ri+1):
        if len(ca_atoms[ca_atoms.res_id == i]) == 0:
            seq += 'X'
            logger.warning(f'{file} {chain} {i} does not have CA atom')
        else:
            res_name = ca_atoms[ca_atoms.res_id == i].res_name[0]
            seq += three_to_one[res_name]
    return seq


if __name__ == '__main__':
    shutil.rmtree('seqs', ignore_errors=True)
    Path('seqs').mkdir(parents=True, exist_ok=True)

    wt_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Wild Type')
    mt_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Mutant')
    df = pd.concat([wt_df, mt_df], ignore_index=True)

    # drop if pka is not numeric
    df = df[pd.to_numeric(df['pKa'], errors='coerce').notnull()]
    df = df.drop_duplicates(
        subset=['PDB ID', 'Mutant Pos', 'Mutant Chain', 'Chain', 'Res ID', 'Res Name'])

    for i, row in tqdm(df.iterrows()):
        pdbid, chain, resid, resname, mut_pos, mut_chain = row['PDB ID'], row['Chain'], int(
            row['Res ID']), row['Res Name'], row['Mutant Pos'], row['Mutant Chain']
        file = f'fixed_pdbs/{pdbid.lower()}_{mut_pos}_{mut_chain}.pdb'
        out_file = f'seqs/{pdbid.lower()}_{chain}_{mut_pos}_{mut_chain}.fasta'
        if not Path(file).exists():
            raise FileNotFoundError(f'{file} does not exist')
        if Path(out_file).exists():
            continue
        seq = fetch_seq(file, chain)
        with open(out_file, 'w') as f:
            f.write(f'>{pdbid}_{chain}_{mut_pos}_{mut_chain}\n')
            f.write(f'{seq}\n')

    shutil.rmtree('tmp', ignore_errors=True)
    Path('tmp').mkdir(parents=True, exist_ok=True)
    os.system('cat seqs/*.fasta > tmp/in.txt')
