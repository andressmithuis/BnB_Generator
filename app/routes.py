from flask import Flask, render_template, request, url_for

from AdvancedBnB import Gun as Abnb_gun
from StandardBnB import Gun as Sbnb_gun, Shield as Sbnb_shield

from StandardBnB import HealthPotion

from util import Rarity

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-gun', methods=['GET', 'POST'])
def generate_gun():
    img_file = None
    bnb_ruleset = request.form.get('bnb_ruleset', 'standard')

    if request.method == 'POST':
        props = {
            # 'level': 1,
            # 'manufacturer': Manufacturers.ERIDIAN,
            # 'gun_type': StandardBnB.Guntypes.PISTOL,
            # 'rarity': Rarity.LEGENDARY,
        }

        if bnb_ruleset == 'standard':
            new_gun = Sbnb_gun()
        elif bnb_ruleset == 'advanced':
            new_gun = Abnb_gun()
        else:
            raise f"Returned Ruleset does not exist: {bnb_ruleset}"

        new_gun.generate(props=props)
        print(new_gun)
        new_gun.generate_card()

        img_file = url_for('static', filename=f"generated/new_gun.bmp")

    return render_template('guns.html', image_file=img_file, bnb_ruleset=bnb_ruleset)

@app.route('/generate-shield', methods=['GET', 'POST'])
def generate_shield():
    img_file = None
    bnb_ruleset = request.form.get('bnb_ruleset', 'standard')

    if request.method == 'POST':
        props = {
            # 'level': 1,
            # 'manufacturer': Manufacturers.ERIDIAN,
            # 'gun_type': StandardBnB.Guntypes.PISTOL,
            # 'rarity': Rarity.LEGENDARY,
        }

        if bnb_ruleset == 'standard':
            new_shield = Sbnb_shield()
        elif bnb_ruleset == 'advanced':
            new_shield = Sbnb_shield()
        else:
            raise f"Returned Ruleset does not exist: {bnb_ruleset}"

        new_shield.generate()
        print(new_shield)
        new_shield.generate_card()

        img_file = url_for('static', filename=f"generated/new_shield.bmp")

    return render_template('shields.html', image_file=img_file, bnb_ruleset=bnb_ruleset)

@app.route('/health-potions', methods=['GET', 'POST'])
def health_potions():
    img_file = None
    item_rarity = 'common'

    if request.method == 'POST':
        item_rarity = request.form.get('item_rarity', 'common')

        conv_table = {
            'common': Rarity.COMMON,
            'uncommon': Rarity.UNCOMMON,
            'rare': Rarity.RARE,
            'epic': Rarity.EPIC,
            'legendary': Rarity.LEGENDARY
        }

        new_potion = HealthPotion(conv_table[item_rarity])
        new_potion.generate_card()

        img_file = url_for('static', filename=f"generated/new_potion.bmp")

    return render_template('health_potions.html', image_file=img_file, item_rarity=item_rarity)

if __name__ == '__main__':
    app.run(debug=False)
