import os
import json

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


def _load_gun_images(driver: Driver, game_selection):
    item_data = {}

    selection = []
    for game in game_selection:
        selection.append(game_alias_table[game])

    for game in selection:
        print(f"Start Loading of Gun Resources ({game})...")
        url = f"https://www.lootlemon.com/db/{game}/weapons"

        weapons = get_item_list(driver, url)

        cnt = 1
        for item in weapons:
            gun_name = item.get('data-name')
            #gun_rarity = item.get('data-rarity')
            #gun_manufacturer = item.get('data-manufacturer')
            gun_type = item.get('data-type')
            page_link = item.find('a').get('href')  # Extract Weapon page url for high-res image

            # Consolidate or skip certain types of weapons
            _type = gun_type.split('-')[0]
            if _type in ['eridian', 'melee']:  # Skip Melee(WL) or Eridian(BL1) Weapons
                continue

            if _type in ['assault', 'laser']:  # Consolidate 'Assault Rifle' and 'Laser Rifle'(TPS) into 'rifle' type
                _type = 'rifle'

            if _type in ['revolver', 'repeater']:  # Consolidate 'Repeater' and 'Revolver' into 'pistol' type
                _type = 'pistol'

            gun_type = _type

            # Remove non-alphanumerical symbols to create an ID
            gun_id = ''.join(filter(str.isalnum, gun_name)).lower()

            print(f"Gathering asset {cnt}/{len(weapons)}: {gun_name}...")

            asset_loaded = False
            while not asset_loaded:
                # Download image(.avif) from weapon page and convert into a png
                img_url = get_item_image(driver, f"https://www.lootlemon.com{page_link}")  # high-res Get image url from weapon page
                resp = requests.get(img_url)

                # Download image (.avif format) then convert to png
                if resp.status_code == 200:
                    with open(f"img/tmp.avif", 'wb') as f:
                        f.write(resp.content)

                    if not os.path.isdir(f"img/weapons/{gun_type}"):
                        os.makedirs(f"img/weapons/{gun_type}")

                    try:
                        item_img = Image.open(f"img/tmp.avif")
                        filepath = f"img/weapons/{gun_type}/{gun_id}.png"
                        item_img.save(filepath, 'PNG', quality=100)

                        if 'weapons' not in item_data:
                            item_data.update({'weapons': {}})
                        if gun_type not in item_data['weapons']:
                            item_data['weapons'].update({gun_type: []})

                        item_data['weapons'][gun_type].append({'item_id': gun_id, 'item_name': gun_name, 'path_to_img': filepath})
                        asset_loaded = True

                        cnt += 1
                    except Exception as e:
                        pass

    return item_data

def _load_shield_images(driver: Driver, game_selection):
    item_data = {}

    selection = []
    for game in game_selection:
        selection.append(game_alias_table[game])

    for game in selection:
        print(f"Start Loading of Shield Resources ({game})...")
        url = f"https://www.lootlemon.com/db/{game}/shields"

        shields = get_item_list(driver, url)

        cnt = 1
        for item in shields:
            shield_name = item.get('data-name')
            #gun_rarity = item.get('data-rarity')
            #gun_manufacturer = item.get('data-manufacturer')
            shield_type = item.get('data-type')
            page_link = item.find('a').get('href')  # Extract Weapon page url for high-res image

            # Consolidate or skip certain types of weapons
            _type = shield_type.split('-')[0]

            shield_type = _type

            # Remove non-alphanumerical symbols to create an ID
            shield_id = ''.join(filter(str.isalnum, shield_name)).lower()

            print(f"Gathering asset {cnt}/{len(shields)}: {shield_name}...")

            asset_loaded = False

            retries = 0
            while not asset_loaded:
                # Download image(.avif) from weapon page and convert into a png
                img_url = get_item_image(driver, f"https://www.lootlemon.com{page_link}")  # high-res Get image url from weapon page
                resp = requests.get(img_url)

                # Download image (.avif format) then convert to png
                if resp.status_code == 200:
                    with open(f"img/tmp.avif", 'wb') as f:
                        f.write(resp.content)

                    time.sleep(0.1)

                    if not os.path.isdir(f"img/shields"):
                        os.makedirs(f"img/shields")

                    try:
                        item_img = Image.open(f"img/tmp.avif", formats=['avif'])
                        filepath = f"img/shields/{shield_id}.png"
                        item_img.save(filepath, 'PNG', quality=100)

                        if 'shields' not in item_data:
                            item_data.update({'shields': []})

                        item_data['shields'].append({'item_id': shield_id, 'item_name': shield_name, 'path_to_img': filepath})

                        cnt += 1
                        asset_loaded = True
                    except Exception as e:
                        # Try again
                        if retries == 3:
                            asset_loaded = True
                            cnt += 1
                            print(f"Skipping...")
                        else:
                            retries += 1
                            print(f"Trying again...")

    return item_data

def load_resources(game_list, start_clean=False):
    driver = Driver()

    asset_data = {}
    # Load previous data
    if start_clean is False:
        if os.path.isfile('assets.json'):
            with open('assets.json', 'r') as file:
                asset_data = json.load(file)

    # Update Gun Assets
    new_data = _load_gun_images(driver, game_list)
    #new_data = {'weapons': {'pistol': [{'item_id': 'test', 'item_name': 'Test', 'path_to_img': 'img/path/to/file.png'}]}}
    for weapon_type in ['pistol', 'smg', 'rifle', 'shotgun', 'launcher', 'sniper']:
        data_set = asset_data['weapons'][weapon_type]
        for weapon in new_data['weapons'][weapon_type]:
            if weapon not in data_set:
                data_set.append(weapon)
        asset_data['weapons'][weapon_type] = data_set

    # Update Shield Assets
    new_data = _load_shield_images(driver, game_list)
    data_set = asset_data['shields']
    for item in new_data['shields']:
        if item not in data_set:
            data_set.append(item)
    asset_data['shields'] = data_set

    # Save asset info in json file to be used in the generator
    with open('assets.json', 'w') as file:
        json.dump(asset_data, file, indent=4)
