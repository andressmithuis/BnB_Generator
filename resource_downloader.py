import os
import json
from threading import Lock

from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests

from PIL import Image
import pillow_avif  # DO NOT REMOVE! Enables reading of AVIF files when imported even though it looks like it's not being used!

from dataclasses import dataclass

from file_handling import *

game_alias = {
    'bl1': 'borderlands-1',
    'bl2': 'borderlands-2',
    'bl3': 'borderlands-3',
    'bl4': 'borderlands-4',
    'bl-tps': 'borderlands-tps',
    'tt-wl': 'wonderlands'
}

@dataclass
class DownloadProgress:
    currently_at: int
    complete_at: int
    last_img: str

class Downloader:
    def __init__(self):
        self.lock = Lock()
        self.is_done = False
        self.progress = 0
        self.last_image = None

        self.page = None

    def init_browser(self):
        if getattr(sys, 'frozen', False):
            # Add Playwright browser to path for packaged application
            browser_path = Path(sys._MEIPASS) / 'ms-playwright'
            os.environ['PLAYWRIGHT_BROWSERS_PATH'] = f"{browser_path}"

        playwright = sync_playwright().start()
        self.browser = playwright.chromium.launch(
            headless = True
        )

        self.page = self.browser.new_page()

    def get_list_url(self, game, item_type):
        url_item_type = item_type

        # Item url exceptions
        if game == 'tt-wl':
            if item_type == 'grenade-mods':
                url_item_type = 'spells'
            elif item_type == 'class-mods':
                url_item_type = 'armor'

        if item_type == 'relics':
            if game == 'bl1':
                print(f"Game {game} does not have Relic type Equipment! Skipping...")
                return None

            relic_alias = {
                'bl2': 'relics',
                'bl3': 'artifacts',
                'bl-tps': 'oz-kits',
                'tt-wl': 'rings-amulets'
            }

            url_item_type = relic_alias[game]

        return f"https://www.lootlemon.com/db/{game}/{url_item_type}"

    def get_page_source(self, url):
        if self.page is None:
            self.init_browser()

        self.page.goto(url)
        # Scroll to bottom of page
        self.page.keyboard.press("End")

        return self.page.content()




    def get_item_list(self, page_url):
        # Get page source from url
        page_source = self.get_page_source(page_url)

        # Extract list from webpage
        html_source = BeautifulSoup(page_source, 'html.parser')
        page_content = html_source.find('div', class_='w-dyn-items')
        item_list = page_content.find_all('div', class_='db_item w-dyn-item')

        # Rework data
        items = []
        for item in item_list:
            # Extract item name
            item_name = item.get('data-name')
            if item_name is None:  # Grenades exception
                item_name = item.get('data-named')

            # extract item type
            data_type = item.get('data-type').split('-')
            item_type = data_type[0]
            game_src = '-'.join(data_type[1:])

            # Consolidate or skip certain types of weapons
            if item_type in ['eridian', 'melee']:  # Skip Melee(WL) or Eridian(BL1) Weapons
                continue

            if item_type in ['assault', 'laser']:  # Consolidate 'Assault Rifle(BL1/BL4)' and 'Laser Rifle'(TPS) into 'rifle' type
                item_type = 'rifle'

            if item_type in ['revolver', 'repeater']:  # Consolidate 'Repeater(BL1)' and 'Revolver(BL1)' into 'pistol' type
                item_type = 'pistol'

            # Create item ID
            item_id = f"{game_src}_{''.join(filter(str.isalnum, item_name)).lower()}"

            # Extract item page url
            item_link = item.find('a').get('href')  # Extract Weapon page url for high-res image
            item_url = f"https://www.lootlemon.com{item_link}"

            # Add item to list
            res_item = {
                'name': item_name,
                'id': item_id,
                'type': item_type,
                'url': item_url
            }
            items.append(res_item)

        return items

    def get_img_url(self, item_url):
        page = self.get_page_source(item_url)

        html_source = BeautifulSoup(page, 'html.parser')
        img_url = html_source.find('img', class_='card_thumbnail zoom').get('src')

        return img_url

    def download_img(self, img_url, output_path):
        n_attempts = 0

        while n_attempts < 3:
            resp = requests.get(img_url)

            if resp.status_code == 200:
                try:
                    # Download into temporary AVIF file
                    with open(appdata_path(f"img/tmp.avif"), 'wb') as f:
                        f.write(resp.content)

                    item_img = Image.open(appdata_path(f"img/tmp.avif"))
                    item_img.save(appdata_path(output_path), 'PNG', quality=100)

                    # Remove tmp AVIF image file
                    if os.path.isfile(appdata_path(f"img/tmp.avif")):
                        os.remove(appdata_path(f"img/tmp.avif"))

                    return True

                except Exception as e:
                    print(f"Error converting image: {e}")

            else:
                print(f"Response error {resp.status_code}!")

            n_attempts += 1

        return False

    def download(self, game, item_type):
        with self.lock:
            self.progress = 0
            self.last_image = None
            self.is_done = False

        # Sanity checks
        if not item_type in ['weapons', 'shields', 'grenades', 'relics', 'class mods']:
            return

        if not game in game_alias:
            return

        # Get list of items
        game_url = game_alias[game]
        list_url = self.get_list_url(game_url, item_type)
        item_list = self.get_item_list(list_url)

        # Download all item images
        items_done = 0
        for item in item_list:
            img_url = self.get_img_url(item['url'])
            img_path = f"img/{item['type']}/{item['id']}.png"
            if item_type == 'weapons':
                img_path = f"img/weapons/{item['type']}/{item['id']}.png"

            Path(appdata_path(img_path)).parent.mkdir(parents=True, exist_ok=True)

            ret = self.download_img(img_url, img_path)
            if ret is True:
                # Download was a success! Add img path to signal a successfull download
                item['img_path'] = img_path
                # yield progress / image path
                #yield DownloadProgress(items_done + 1, len(item_list), img_path)

                with self.lock:
                    self.progress = (items_done+1) / len(item_list) * 100
                    self.last_image = img_path

            items_done += 1

        # Update items in assets.json
        # Load previous data (if exists)
        asset_data = {}
        if os.path.isfile(appdata_path('assets.json')):
            with open(appdata_path('assets.json'), 'r') as file:
                asset_data = json.load(file)
        else:
            # Initialize asset_data for new file
            for weapon_type in ['pistol', 'smg', 'rifle', 'shotgun', 'launcher', 'sniper']:
                asset_data.setdefault('weapons', {}).setdefault(weapon_type, [])
            asset_data.setdefault('shields', [])
            asset_data.setdefault('grenades', [])
            asset_data.setdefault('relics', [])
            asset_data.setdefault('class mods', [])

        # Update asset data
        for item in item_list:
            if 'img_path' in item:
                asset_list = asset_data[item_type]
                if item_type == 'weapons':  # 'Weapons' is plit into the item types
                    asset_list = asset_list[item['type']]

                new_entry = {'item_id': item['id'], 'item_name': item['name'], 'path_to_img': item['img_path']}
                if new_entry not in asset_list:
                    asset_list.append(new_entry)

        # Save asset info in json file to be used in the generator
        with open(appdata_path('assets.json'), 'w') as file:
            json.dump(asset_data, file, indent=4)

        self.is_done = True
        self.browser.close()



if __name__ == "__main__":
    downloader = Downloader()
    downloader.download('bl-tps', 'weapons')