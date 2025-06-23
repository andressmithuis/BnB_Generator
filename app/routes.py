from flask import Flask, render_template, request, url_for

from AdvancedBnB import Gun as Abnb_gun
from StandardBnB import Gun as Bnb_gun

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-gun', methods=['GET', 'POST'])
def generate_gun():
    img_file = None
    bnb_ruleset = 'Bunkers&Badasses'

    if request.method == 'POST':
        props = {
            # 'level': 1,
            # 'manufacturer': Manufacturers.ERIDIAN,
            # 'gun_type': Guntypes.PISTOL,
            # 'rarity': Rarity.LEGENDARY,
        }

        if 'bnb_ruleset' in request.form:
            bnb_ruleset = request.form['bnb_ruleset']
            new_gun = Abnb_gun()
        else:
            new_gun = Bnb_gun()


        new_gun.generate(props=props)
        print(new_gun)
        new_gun.generate_card()

        img_file = url_for('static', filename=f"generated/new_gun.bmp")


    return render_template('guns.html', image_file=img_file, bnb_ruleset=bnb_ruleset)

if __name__ == '__main__':
    app.run(debug=True)