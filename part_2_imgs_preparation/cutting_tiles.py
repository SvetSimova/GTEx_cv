import json
import os
from slideio import open_slide
import matplotlib.image as img
import numpy as np
from glob import glob
from tqdm.auto import tqdm
import cv2

project_path = 'data'

tis_sl_dict = json.load(open('data/all_50.json', 'rb'))
tis_list = list(tis_sl_dict.keys())

img_dir_path = 'data/images_gtex'
tiles_dir_path = os.path.join(project_path, 'tiles_filtered2')
os.makedirs(tiles_dir_path, exist_ok=True)

thr_size_dict = json.load(open('data/thr_size_dict_448.json', 'rb'))


def cut_tiles(tls_dir, f_name, sc, h=448):
    x_bd, y_bd = (sc.rect[2] // h) * h - h, (sc.rect[3] // h) * h - h
    for ix in range(0, x_bd, h):
        for iy in range(0, y_bd, h):
            tl = sc.read_block((ix, iy, 448, 448))
            img.imsave(os.path.join(tls_dir, f_name + "_" + str(ix) + "_" + str(iy) + ".jpg"), tl)


def filter1(image, h=224, h_=224, cr=5):
    im = cv2.imread(image, 0)
    n_cr = 0
    for ix in range(0, 440, h_):
        for iy in range(0, 440, h_):
            b = im[ix:(ix+h), iy:(iy+h)]
            crit = np.array(b).std()
            if crit < cr:
                n_cr += 1
    return n_cr


def filter2(image, thr_crit=0.6):
    im = cv2.imread(image)
    b, g, r = im[:, :, 0], im[:, :, 1], im[:, :, 2]
    bm, gm, rm = np.array(b).mean(), np.array(g).mean(), np.array(r).mean()
    crit = np.array((bm, gm, rm)).std()
    if crit < thr_crit:
        return True


for folder in tqdm(tis_list):
    print(f'Tissue: {folder}')
    tiles_tis_dir = os.path.join(tiles_dir_path, folder)
    os.makedirs(tiles_tis_dir, exist_ok=True)
    svs_files_ = glob(os.path.join(img_dir_path, folder,  "*.svs"))
    svs_files = [f for f in svs_files_ if os.path.splitext(os.path.basename(f))[0] in tis_sl_dict[folder]]

    # Cutting into tiles
    for k, file in enumerate(svs_files):
        with open_slide(file) as slide:
            file_name = os.path.splitext(os.path.basename(file))[0]
            print(f'{k+1}/{len(svs_files)}   {file_name}')
            scene = slide.get_scene(0)
            cut_tiles(tiles_tis_dir, file_name, scene)

    # Filtering good tiles
    tiles = glob(os.path.join(tiles_tis_dir, "*.jpg"))
    n_total, n_fit = len(tiles), 0
    for tile in tiles:
        file_size = os.path.getsize(tile)
        if file_size <= (thr_size_dict[folder] * 1024) or filter1(tile, h=224, h_=224) \
                or filter1(tile, h=112, h_=84) > 6 or filter2(tile):
            os.remove(tile)
        else:
            n_fit += 1

    print(f'Total tiles: {n_total}, good tiles: {n_fit}.')
