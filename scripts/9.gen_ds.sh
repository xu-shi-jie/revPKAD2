python scripts/5.extract_seq.py --res ASP
sh scripts/6.cluster.sh
python scripts/7.nonredundant.py --res ASP

python scripts/5.extract_seq.py --res GLU
sh scripts/6.cluster.sh
python scripts/7.nonredundant.py --res GLU

python scripts/5.extract_seq.py --res HIS
sh scripts/6.cluster.sh
python scripts/7.nonredundant.py --res HIS

python scripts/5.extract_seq.py --res LYS
sh scripts/6.cluster.sh
python scripts/7.nonredundant.py --res LYS

python scripts/5.extract_seq.py --res TYR
sh scripts/6.cluster.sh
python scripts/7.nonredundant.py --res TYR

python scripts/5.extract_seq.py --res CYS
sh scripts/6.cluster.sh
python scripts/7.nonredundant.py --res CYS

python scripts/5.extract_seq.py --res CTR
sh scripts/6.cluster.sh
python scripts/7.nonredundant.py --res CTR

python scripts/5.extract_seq.py --res NTR
sh scripts/6.cluster.sh
python scripts/7.nonredundant.py --res NTR

python scripts/8.cat_ds.py
mkdir -p data/
mv test*.csv data/
mv train*.csv data/
mv val*.csv data/