import os
import requests
from bs4 import BeautifulSoup
import re
import shutil
import struct
import ctypes
import random


SPI_SETDESKWALLPAPER = 20

# Shamelessly lifted from the interwebs
def is_64bit_windows():
    """Check if 64 bit Windows OS"""
    return struct.calcsize('P') * 8 == 64

def changeBG(path):
    """Change background depending on bit size"""
    if is_64bit_windows():
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 4, path, 3)
    else:
        ctypes.windll.user32.SystemParametersInfoA(SPI_SETDESKWALLPAPER, 4, path, 3)

url = "https://www.reddit.com/r/earthporn"
output_folder = "C:\\Users\\joncocks\\Pictures\\earthpron"

def get_new_images():
    existing_images = os.listdir(output_folder)
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, features="lxml")
    img_tags = soup.findAll("img", {"alt": "Post image"})
    filenames = []
    for t in img_tags:
        # Extract the the actual jpg filename
        jpgs = re.findall("[a-z0-9A-Z_-]{1,}.jpg", t["src"])
        if len(jpgs) > 1:
            print("found multiple jpgs, skipping")
            continue
        else:
            filenames.append(jpgs[0])

    for f in filenames:
        if f not in existing_images:
            img_url = "https://i.redd.it/" + f
            output_filename = os.path.join(output_folder, f)
            get_image(img_url, output_filename)
    print("Done")


def get_image(url, output_filename):
    r = requests.get(url, stream=True, headers={'User-Agent': 'Mozilla/5.0'})
    r.raw.decode_content = True

    # Open a local file with wb ( write binary ) permission.
    with open(output_filename, 'wb') as f:
        shutil.copyfileobj(r.raw, f)


def update_wallpaper():
    # Randomly update to one of the files in the download folder
    files = os.listdir(output_folder)
    n_files = len(files)
    # TODO: make this actually random
    ix = random.randint(0,n_files-1)
    filepath = os.path.join(output_folder, files[ix])
    changeBG(filepath)


if __name__ == "__main__":
    get_new_images()
    update_wallpaper()