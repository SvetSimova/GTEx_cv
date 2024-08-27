import os
import json
import shutil
import random
from glob import glob

project_path = 'data'

tis_sl_dict = json.load(open('data/all_50.json', 'rb'))
tis_list = list(tis_sl_dict.keys())

# Create folder for tiles and two folders in it: train and test
tls_dest_path = os.path.join(project_path, 'randsamp_5000_per_tis')
tls_source_path = os.path.join(project_path, 'tiles_filtered')
train_test = ['train', 'test']

os.makedirs(tls_dest_path, exist_ok=True)
os.makedirs(os.path.join(tls_dest_path, 'train'), exist_ok=True)
os.makedirs(os.path.join(tls_dest_path, 'test'), exist_ok=True)

random.seed(42)
for tis in tis_list:
    n_sl_tiles, n_slides, k = 100, 50, 0.8

    print(f'Tissue: {tis}')
    files = glob(os.path.join(tls_source_path, tis, '*.jpg'))
    tiles = [os.path.basename(f) for f in files]
    sl_names = tis_sl_dict[tis]
    tis_tiles_dict = {sl: [] for sl in sl_names}

    # Correction for tissues which have several slides only (< 50)
    n_sls = len(sl_names)       # actual number of tissue slides
    if n_sls < n_slides:
        n_sl_tiles = int(n_sl_tiles * n_slides / n_sls)

    # Collect all the tiles which belong to each slide (create the dictionary)
    for tl in tiles:
        [tis_tiles_dict[sl].append(tl) for sl in sl_names if tl.startswith(sl)]

    # Create a sampling for each slide of this tissue
    for tis_sl in tis_tiles_dict:
        n_total = len(tis_tiles_dict[tis_sl])
        if n_total >= n_sl_tiles:
            tiles_to_sample = random.sample(tis_tiles_dict[tis_sl], n_sl_tiles)
        else:
            p, tiles_to_sample = 2, []
            while p * n_total < n_sl_tiles:
                p += 1
            l1 = tis_tiles_dict[tis_sl]
            for _ in range(p - 1):
                tiles_to_sample += l1
            add_tiles = random.sample(tis_tiles_dict[tis_sl], (n_sl_tiles - len(tiles_to_sample)))
            tiles_to_sample.extend(add_tiles)

        n_sl_tls = round(k*len(tiles_to_sample))

        for folder in train_test:
            os.makedirs(os.path.join(tls_dest_path, folder, tis), exist_ok=True)
            files_to_copy = tiles_to_sample[:n_sl_tls] if folder == 'train' else tiles_to_sample[n_sl_tls:]
            for file in files_to_copy:
                shutil.copyfile(os.path.join(tls_source_path, tis, file),
                            os.path.join(tls_dest_path, folder, tis, file))
