### Part 1. Collecting the data and preprocessing

-To merge all samples which are in both images and genes data (`prep_to_download.ipynb`) -
img_sample_list.json + gen_sample_list.json = both_img_gen_list.json 
where 13797 images - too much! 
-Visualization with Data Dashboard for tissues `GTEx_both_tis.pbix` (based on `gtex_both_tis.csv`).

So we create the sampling: 50 samples for each of 40 tissues
(as for 5 types of tissues there are less than 50 samples we take them all)
 - in total 1803 slides.

Results: 
 - all_50.json - file with the sample's names for image downloading;
 - genexpr_all_50.csv - file with their genes data (already preprocessed). 
for further usage.

### Part 2. Image Preparation

-Download all slides from gtexportal (`slides_download.py`).
-Cutting into tiles & filtering them (`cutting_tiles.py` + ``thr_size_dict_448.json`)  
-Creation of train, test folders (with equal number of tiles for every sample) 
	for further usage in DataLoaders.

Results: 
 - train -> 40 folders (each for every tissue) with 40*50*80 = 160 000 tiles
 - test -> 40 folders (each for every tissue) with 40*50*20 = 40 000 tiles
