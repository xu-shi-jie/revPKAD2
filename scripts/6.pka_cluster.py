import subprocess

import pandas as pd
from loguru import logger
from tqdm import tqdm


def compute_sim_by_blastp(seq1_file, seq2_file):
    params = [
        'blastp', '-query', seq1_file, '-subject',
        seq2_file, '-outfmt', '6', '-out', 'tmp/blastp.out']
    subprocess.run(params, check=True)
    total_match, total_length = 0, 0
    for l in open('tmp/blastp.out'):
        match, length = l.split('\t')[2], l.split('\t')[3]
        total_match += float(match) * int(length)
        total_length += int(length)
    sim = total_match / total_length if total_length else 0
    return sim


if __name__ == '__main__':
    wt_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Wild Type')
    mt_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Mutant')
    df = pd.concat([wt_df, mt_df], ignore_index=True)
    df = df[pd.to_numeric(df['pKa'], errors='coerce').notnull()]
    df = df.drop_duplicates(
        subset=['PDB ID', 'Mutant Pos', 'Mutant Chain', 'Chain', 'Res ID', 'Res Name'])

    df['id'] = df.apply(
        lambda x: f'{x["PDB ID"].lower()}_{x["Chain"]}_{x["Mutant Pos"]}_{x["Mutant Chain"]}', axis=1)
    ids = df.groupby('id').size()
    # sort ids from the most frequent to the least
    ids = ids.sort_values(ascending=False).index.tolist()
    clusters = []

    # similar to psi-cd-hit
    while len(ids):
        print(f"Constructing cluster {len(clusters)}...")
        id1 = ids.pop(0)
        seq1_file = f'seqs/{id1}.fasta'
        cluster = [id1]
        for id2 in ids:
            seq2_file = f'seqs/{id2}.fasta'
            sim = compute_sim_by_blastp(seq1_file, seq2_file)
            if sim >= 30:
                cluster.append(id2)
                ids.remove(id2)
        clusters.append(cluster)

    nonredundant = [c[0] for c in clusters]
    df = df[df['id'].isin(nonredundant)]
    df.sort_values(by='pKa', inplace=True)
    df.to_csv('nonredundant.csv', index=False)
