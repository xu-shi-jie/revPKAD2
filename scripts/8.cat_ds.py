from pathlib import Path

import pandas as pd

if __name__ == '__main__':
    train_dfs, val_dfs, test_dfs = [], [], []
    for res in ['ASP', 'GLU', 'HIS', 'LYS', 'CYS', 'TYR', 'CTR', 'NTR']:
        train_df = pd.read_csv(f'train_{res}.csv')
        val_df = pd.read_csv(f'val_{res}.csv')
        test_df = pd.read_csv(f'test_{res}.csv')
        train_dfs.append(train_df)
        val_dfs.append(val_df)
        test_dfs.append(test_df)

    train_df = pd.concat(train_dfs)
    val_df = pd.concat(val_dfs)
    test_df = pd.concat(test_dfs)
    train_df.to_csv('train.csv', index=False)
    val_df.to_csv('val.csv', index=False)
    test_df.to_csv('test.csv', index=False)
