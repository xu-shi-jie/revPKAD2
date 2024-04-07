import argparse
import re

import pandas as pd
from loguru import logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--res', type=str, default='ASP')
    args = parser.parse_args()

    clusters = []
    for line in open(r'tmp/db30.txt.clstr', 'r').read().splitlines():
        if line.startswith('>'):
            cluster_id = line.split()[1]
            clusters.append([])
        else:
            records = re.split('[ \t]+', line)
            if records[3] == '*':
                clusters[-1].append((records[2][1:-3], 100))
            else:
                clusters[-1].append((records[2][1:-3],
                                    float(records[4].split('/')[-1][:-1])))

    nonredundant = []
    for clstr in clusters:
        nonredundant.append(clstr[0][0])

    wt_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Wild Type')
    mt_df = pd.read_excel(
        'process_PKAD2_DOWNLOAD_rev.xlsx', sheet_name='Mutant')
    df = pd.concat([wt_df, mt_df], ignore_index=True)
    # drop if pka is not numeric
    df = df[pd.to_numeric(df['pKa'], errors='coerce').notnull()]
    df = df.drop_duplicates(
        subset=['PDB ID', 'Mutant Pos', 'Mutant Chain', 'Chain', 'Res ID', 'Res Name'])
    df = df[df['Res Name'] == args.res]

    # save nonredundant wild type and mutant data
    df = df[df.apply(
        lambda x: f'{x["PDB ID"]}_{x["Chain"]}_{x["Mutant Pos"]}_{x["Mutant Chain"]}' in nonredundant, axis=1)]
    df.sort_values(by='pKa', inplace=True)

    train_dfs, val_dfs, test_dfs = [], [], []  # 4: 1: 2
    for res in df['Res Name'].unique():
        res_df = df[df['Res Name'] == res]
        train_dfs.append(res_df[0::7])
        train_dfs.append(res_df[3::7])
        train_dfs.append(res_df[6::7])
        test_dfs.append(res_df[1::7])
        test_dfs.append(res_df[5::7])
        val_dfs.append(res_df[4::7])

    test_df = pd.concat(test_dfs)
    train_df = pd.concat(train_dfs + val_dfs)
    val_df = pd.concat(val_dfs)

    train_df.to_csv(f'train_{args.res}.csv', index=False)
    val_df.to_csv(f'val_{args.res}.csv', index=False)
    test_df.to_csv(f'test_{args.res}.csv', index=False)
    logger.info(
        f'Train: {len(train_df)}, Val: {len(val_df)}, Test: {len(test_df)}')
    logger.error("Note: validation set is contained in training set.")
