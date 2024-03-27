import multiprocessing as mp
# check if windows
import os
import random
import re
import shutil
from pathlib import Path

import pandas as pd
from loguru import logger
from tqdm import tqdm

if os.name == 'nt':
    os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
import biotite.structure.io.pdb as bio_pdb
from openmm import *
from openmm.app import *
from openmm.unit import *
from pdbfixer import PDBFixer

codon = {
    'A': 'ALA', 'R': 'ARG', 'N': 'ASN', 'D': 'ASP', 'C': 'CYS',
    'Q': 'GLN', 'E': 'GLU', 'G': 'GLY', 'H': 'HIS', 'I': 'ILE',
    'L': 'LEU', 'K': 'LYS', 'M': 'MET', 'F': 'PHE', 'P': 'PRO',
    'S': 'SER', 'T': 'THR', 'W': 'TRP', 'Y': 'TYR', 'V': 'VAL',
}


def fix_pdb(params):
    try:
        infile, outfile, mut_pos, mut_chain = params

        # check if outfile exists
        if os.path.exists(outfile):
            return

        if not os.path.exists(infile):
            logger.warning(f'{infile} does not exist')
            return

        forcefield = ForceField('amber14-all.xml', 'amber14/tip3pfb.xml')
        fixer = PDBFixer(filename=infile)
        # check if mutation, not nan
        if mut_chain == mut_chain and mut_pos == mut_pos:
            fixer.applyMutations([
                f'{codon[mut[0]]}-{mut[1:-1]}-{codon[mut[-1]]}'
                for mut in mut_pos.split(',')
            ], chain_id=mut_chain)

        fixer.findMissingResidues()
        fixer.findNonstandardResidues()
        fixer.replaceNonstandardResidues()
        fixer.removeHeterogens(keepWater=False)  # do not keep water
        fixer.findMissingAtoms()
        fixer.addMissingAtoms(seed=0)
        # for reproducibility: https://github.com/openmm/openmm/issues/1836
        random.seed(0)
        modeller = Modeller(fixer.topology, fixer.positions)
        modeller.delete(modeller.topology.bonds())
        modeller.topology.createStandardBonds()  # create bonds
        modeller.delete([r for r in modeller.topology.residues() if r.name in [
                        'DG', 'DC', 'DA', 'DT']])  # delete DNA/RNA
        modeller.addHydrogens(forcefield, pH=7.0)
        PDBFile.writeFile(
            modeller.topology, modeller.positions, open(outfile, 'w'), keepIds=True)
    except Exception as e:
        print(infile)
        # copy the file to the fixed_pdbs folder
        logger.warning(f'Error in {infile}: {e}, copying the file')
        shutil.copy(infile, outfile)


if __name__ == '__main__':
    wt_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Wild Type')
    mt_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Mutant')
    df = pd.concat([wt_df, mt_df], ignore_index=True)
    # remove redundant
    df = df.drop_duplicates(subset=['PDB ID', 'Mutant Pos', 'Mutant Chain'])

    shutil.rmtree('fixed_pdbs', ignore_errors=True)
    Path('fixed_pdbs').mkdir(parents=True, exist_ok=True)

    with mp.Pool(mp.cpu_count()) as pool:
        list(tqdm(pool.imap(fix_pdb, [(
            'pdbs/{}.pdb'.format(row['PDB ID'].lower()),
            'fixed_pdbs/{}_{}_{}.pdb'.format(
                row['PDB ID'].lower(), row['Mutant Pos'], row['Mutant Chain']),
            row['Mutant Pos'],
            row['Mutant Chain'],
        ) for i, row in df.iterrows()]),
            desc='Fixing PDBs',
            total=len(df),
            leave=False))
