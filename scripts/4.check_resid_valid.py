from pathlib import Path

import numpy as np
import pandas as pd
from biotite.structure.io.pdb import PDBFile, get_structure
from loguru import logger
from tqdm import tqdm

codon = {
    'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS', 'Q': 'GLN',
    'E': 'GLU', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE', 'L': 'LEU', 'K': 'LYS',
    'M': 'MET', 'F': 'PHE', 'P': 'PRO', 'S': 'SER', 'T': 'THR', 'W': 'TRP',
    'Y': 'TYR', 'V': 'VAL'
}

if __name__ == '__main__':
    wt_rev_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Wild Type')
    mt_rev_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Mutant')

    logger.info('Checking wild type...')
    for i, row in tqdm(wt_rev_df.iterrows()):
        pdbid, chain, resid, resname = row['PDB ID'], row['Chain'], int(
            row['Res ID']), row['Res Name']
        pdbid = pdbid.lower()
        atoms = get_structure(PDBFile.read(
            f'fixed_pdbs/{pdbid}_nan_nan.pdb'))[0]

        if resname not in ['CTR', 'NTR']:
            res = atoms[(atoms.chain_id == chain) & (atoms.res_id == resid) & (
                atoms.res_name == resname)]
            assert len(set(res.res_name)) == 1, f'{
                i+2} {pdbid} {chain} {resid} {resname}'
        elif resname == 'NTR':
            res = atoms[(atoms.chain_id == chain) & (atoms.hetero == False)]
            min_ri = res.res_id.min()
            res = res[res.res_id == min_ri]
            assert len(set(res.res_name)) == 1, f'{
                i+2} {pdbid} {chain} {resid} {resname}'
        elif resname == 'CTR':
            res = atoms[(atoms.chain_id == chain) & (atoms.hetero == False)]
            max_ri = res.res_id.max()
            res = res[res.res_id == max_ri]
            assert len(set(res.res_name)) == 1, f'{
                i+2} {pdbid} {chain} {resid} {resname}'

    logger.info('Checking mutant...')
    for i, row in tqdm(mt_rev_df.iterrows()):

        pdbid, chain, res_id, res_name, mut_pos, mut_chain = \
            row['PDB ID'], row['Chain'], int(
                row['Res ID']), row['Res Name'], row['Mutant Pos'], row['Mutant Chain']
        pdbid = pdbid.lower()

        atoms = get_structure(PDBFile.read(
            f'fixed_pdbs/{pdbid}_{mut_pos}_{mut_chain}.pdb'))[0]

        res = atoms[(atoms.chain_id == chain) & (atoms.res_id == res_id)]
        assert len(set(res.res_name)) == 1, \
            f'{i+2} {pdbid} {chain} {res_id} {res_name}'
        if res.res_name[0] == res_name:
            continue
        elif res_name == 'CTR':  # NOTE: only CTR, without mutations in the data set
            res = atoms[(atoms.chain_id == chain) & (atoms.hetero == False)]
            max_ri = res.res_id.max()
            res = res[res.res_id == max_ri]
            assert len(set(res.res_name)) == 1, f'{
                i+2} {pdbid} {chain} {res_id} {res_name}'
        else:  # extact mutation position
            raise ValueError(
                f'{i+2} {pdbid} {chain} {res_id} {res_name} {mut_pos}')

    logger.info('Check residues id continuity...')
    df = pd.concat([wt_rev_df, mt_rev_df], ignore_index=True)

    for i, row in tqdm(df.iterrows()):
        pdbid, chain, resid, resname, mut_pos, mut_chain = row['PDB ID'], row['Chain'], int(
            row['Res ID']), row['Res Name'], row['Mutant Pos'], row['Mutant Chain']

        pdbid = pdbid.lower()
        atoms = get_structure(PDBFile.read(
            f'fixed_pdbs/{pdbid}_{mut_pos}_{mut_chain}.pdb'))[0]

        res = atoms[(atoms.chain_id == chain) & (atoms.hetero == False)]
        # change res_id > 9900 to res_id - 10000
        res.res_id = np.where(
            res.res_id > 9900, res.res_id - 10000, res.res_id)

        min_ri, max_ri = res.res_id.min(), res.res_id.max()
        if max_ri - min_ri + \
                1 != len(np.unique(res.res_id)):
            logger.warning(f'May missing residues: {pdbid}_{chain}_{mut_pos}_{mut_chain}: {
                min_ri} {max_ri} {len(np.unique(res.res_id))}')

    logger.info(f'All residues are valid, total {len(df)}')
