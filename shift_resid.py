import argparse

from biotite.structure.io.pdb import PDBFile, get_structure

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--pdb', help='PDB file')
    parser.add_argument('--shift', help='Shift residue ID', type=int)
    parser.add_argument('--out', help='Output file')
    args = parser.parse_args()

    atoms = get_structure(PDBFile.read(args.pdb))[0]
    atoms.res_id = atoms.res_id+args.shift
    file = PDBFile()
    file.set_structure(atoms)
    file.write(args.out)
