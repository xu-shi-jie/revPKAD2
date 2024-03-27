import random
import re

import pandas as pd
from loguru import logger

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

# save nonredundant wild type and mutant data
df = df[df.apply(
    lambda x: f'{x["PDB ID"]}_{x["Chain"]}_{x["Mutant Pos"]}_{x["Mutant Chain"]}' in nonredundant, axis=1)]
df.sort_values(by='pKa', inplace=True)
df.to_csv('nonredundant.csv', index=False)

test_dfs = []
for res in df['Res Name'].unique():
    res_df = df[df['Res Name'] == res]
    test_dfs.append(res_df[::3])

test_df = pd.concat(test_dfs)
train_df = df.drop(test_df.index)
train_df.to_csv('train.csv', index=False)
test_df.to_csv('test.csv', index=False)
logger.info(f'Train: {len(train_df)}, Test: {len(test_df)}')
