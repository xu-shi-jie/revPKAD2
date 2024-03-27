cd datasets/PKAD-2/raw/fixed_pdbs
# iterate over all PDB files in the directory
for file in *.pdb; 
do
    stem=$(basename $file .pdb)
    # if [ -f ../sasa/$stem.asa ]; then
    #     echo "Skipping $stem.asa..."
    #     continue
    # fi

    echo "Generating $stem.asa..."
    ../../../../naccess/naccess $file -w -h -y # -w -h -y also contain other atoms except amino acids
done
rm *.log *.rsa
# mkdir -p ../sasa
# mv *.asa *.rsa ../sasa