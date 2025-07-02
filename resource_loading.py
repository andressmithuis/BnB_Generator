import os
import json
import shutil

from PIL import Image
import pillow_avif  # DO NOT REMOVE! Enables reading of AVIF files when imported even though it looks like it's not being used!

import requests
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from bs4 import BeautifulSoup

game_alias_table = {
    'bl1': 'borderlands-1',
    'bl2': 'borderlands-2',
    'bl3': 'borderlands-3',
    'bl-tps': 'borderlands-tps',
    'bl-wl': 'wonderlands'
}

class Driver:
    def __init__(self):
        opt = Options()
        opt.add_argument('--headless=new')
        self.browser = webdriver.Chrome(options=opt)

    def scrape_page(self, url):
        self.browser.get(url)

        elem = self.browser.find_element(By.TAG_NAME, 'html')
        elem.send_keys(Keys.END)
        #time.sleep(1)
        #elem.send_keys(Keys.HOME)

        return self.browser.page_source


def get_item_list(driver: Driver, url):
    page = driver.scrape_page(url)

    soup = BeautifulSoup(page, 'html.parser')
    item_list = soup.find('div', class_='w-dyn-items')
    items = item_list.find_all('div', class_='db_item w-dyn-item')

    return items

def get_item_image(driver: Driver, url):
    page = driver.scrape_page(url)

    soup = BeautifulSoup(page, 'html.parser')
    img_url = soup.find('img', class_='card_thumbnail zoom').get('src')

    return img_url

def delete_directory(path):
    if os.path.exists(path):
        shutil.rmtree(path)

def load_item_images(driver: Driver, game_filter, item_filter):
    item_data = {}
    if not item_filter in ['weapons', 'shields']:
        return item_data

    selection = []
    for game in game_filter:
        selection.append((game, game_alias_table[game]))

    for game in selection:
        print(f"Start Loading of {game[1]} {item_filter.capitalize()}...")
        url = f"https://www.lootlemon.com/db/{game[1]}/{item_filter}"

        items = get_item_list(driver, url)

        cnt = 1
        for item in items:
            item_name = item.get('data-name')
            #gun_rarity = item.get('data-rarity')
            #gun_manufacturer = item.get('data-manufacturer')
            item_type = item.get('data-type').split('-')[0]
            page_link = item.find('a').get('href')  # Extract Weapon page url for high-res image

            # Consolidate or skip certain types of weapons
            if item_type in ['eridian', 'melee']:  # Skip Melee(WL) or Eridian(BL1) Weapons
                continue

            if item_type in ['assault', 'laser']:  # Consolidate 'Assault Rifle' and 'Laser Rifle'(TPS) into 'rifle' type
                item_type = 'rifle'

            if item_type in ['revolver', 'repeater']:  # Consolidate 'Repeater' and 'Revolver' into 'pistol' type
                item_type = 'pistol'

            # Remove non-alphanumerical symbols to create an ID
            item_id = f"{game[0]}_{''.join(filter(str.isalnum, item_name)).lower()}"

            # Create image output directory
            if item_type in ['pistol', 'smg', 'rifle', 'shotgun', 'sniper', 'launcher']:
                item_img_path = f"img/{item_filter}/{item_type}"
            else:
                item_img_path = f"img/{item_filter}"

            os.makedirs(item_img_path, exist_ok=True)

            print(f"Gathering asset {cnt}/{len(items)}: {item_name}...")

            asset_done = False
            n_retries = 0
            while not asset_done:
                # Download image(.avif) from weapon page and convert into a png
                img_url = get_item_image(driver, f"https://www.lootlemon.com{page_link}")  # high-res Get image url from weapon page
                resp = requests.get(img_url)

                # Download image (.avif format) then convert to png
                if resp.status_code == 200:
                    with open(f"img/tmp.avif", 'wb') as f:
                        f.write(resp.content)

                    try:
                        # Convert avif to png
                        item_img = Image.open(f"img/tmp.avif")
                        filepath = f"{item_img_path}/{item_id}.png"
                        item_img.save(filepath, 'PNG', quality=100)

                        # Add to item data
                        item_data.setdefault(item_filter, [])

                        if item_type in ['pistol', 'smg', 'rifle', 'shotgun', 'sniper', 'launcher']:
                            # Prepare data structure
                            if not isinstance(item_data[item_filter], dict):
                                item_data[item_filter] = {}
                            item_data[item_filter].setdefault(item_type, [])

                            # Add new item to data structure
                            item_data[item_filter][item_type].append({'item_id': item_id, 'item_name': item_name, 'path_to_img': filepath})
                        else:
                            item_data[item_filter].append({'item_id': item_id, 'item_name': item_name, 'path_to_img': filepath})

                        asset_done = True

                        cnt += 1

                    except Exception as e:
                        if n_retries == 3:
                            asset_done = True
                            cnt += 1
                            print(f"Skipping...")
                        else:
                            n_retries += 1
                            print(e)
                            print(f"Trying again...")
                else:
                    print(f"ERROR - resp code: {resp.status_code}")

        # Remove tmp avif image file
        if os.path.isfile(f"img/tmp.avif"):
            os.remove(f"img/tmp.avif")

    return item_data

def load_resources(game_list, item_list, start_clean=False):
    if start_clean:
        # Remove all previously loaded files
        delete_directory('img/weapons')
        delete_directory('img/shields')
        if os.path.isfile('assets.json'):
            os.remove('assets.json')

    driver = Driver()

    asset_data = {}
    for weapon_type in ['pistol', 'smg', 'rifle', 'shotgun', 'launcher', 'sniper']:
        asset_data.setdefault('weapons', {}).setdefault(weapon_type, [])
    asset_data.setdefault('shields', [])

    # Load previous data
    if os.path.isfile('assets.json'):
        with open('assets.json', 'r') as file:
            asset_data = json.load(file)

    # Load Gun Assets
    if any(item in ['all', 'weapons'] for item in item_list):
        new_data = load_item_images(driver, game_list, 'weapons')
        for weapon_type in ['pistol', 'smg', 'rifle', 'shotgun', 'launcher', 'sniper']:
            data_set = asset_data['weapons'][weapon_type]

            if weapon_type in new_data['weapons']:
                for weapon in new_data['weapons'][weapon_type]:
                    if weapon not in data_set:
                        data_set.append(weapon)

                asset_data['weapons'][weapon_type] = data_set

    # Load Shield Assets
    if any(item in ['all', 'shields'] for item in item_list):
        new_data = load_item_images(driver, game_list, 'shields')
        data_set = asset_data['shields']
        for item in new_data['shields']:
            if item not in data_set:
                data_set.append(item)

        asset_data['shields'] = data_set

    # Save asset info in json file to be used in the generator
    with open('assets.json', 'w') as file:
        json.dump(asset_data, file, indent=4)
