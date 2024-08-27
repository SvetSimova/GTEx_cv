import os
import json
import requests

# !!! Change to your working folder path (as in prep_download.ipynb)
project_dir = 'data'
img_tis = json.load(open('data/all_50.json', 'rb')) # download the list of sample names
                            # put the file 'all_50.json' into project_dir if it's not in it yet

# Create a folder for downloading histopathological images
save_dir = 'images_gtex'
os.makedirs(os.path.join(project_dir, save_dir), exist_ok=True)

url_glob = "https://brd.nci.nih.gov/brd/imagedownload/"

# Function to download files
def download_files(img_list, save_dir):
    # Loop through each image_id in the img_list
    for i, image_id in enumerate(img_list):
        url = url_glob + image_id
        print(f'Try {i+1}/{len(img_list)}: {url}')

        # Extract the filename from the URL
        filename = os.path.join(save_dir, os.path.basename(url) + '.svs')

        # Send a GET request to the URL
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Write the content of the response to a file
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {url}: Status code {response.status_code}")

for k, tis in enumerate(list(img_tis.keys())):
    print(f'Tissue {tis} {k+1}/{50}:')
    os.makedirs(os.path.join(project_dir, save_dir, tis), exist_ok=True)
    download_files(img_tis[tis], os.path.join(project_dir, save_dir, tis))
