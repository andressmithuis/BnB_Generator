⚠ WARNING: IN EARLY DEVELOPMENT ⚠

Not all features are complete and expect things to be buggy from time to time.

Features:
- Generation of Gun Cards (Advanced BnB✅)
- Generation of Shield Cards

Extra:
- Generation of Health Potion Cards
- You can influence the properties of generated items by providing the right function arguments (VERY WIP, might not work as expected or even be correct).


# How to Use

Make sure the Python package requirements are installed:

``pip install -r requirements.txt``

Then start the webserver by running:

``python /path/to/directoy/app/routes.py``

The webpage can then be reached locally on http:127.0.0.1:5000 where you can generate the loot you want.
When generating equipment for the first time, it will attempt to download the image files used for weapons, shields, etc. This may take a couple of minutes (Progress is shown in the webserver log). It will only need to do this once.

# Alternate (non-webserver) method

Alternatively, you can run the main.py file directly to generate loot:

``python /path/to/directoy/main.py``

In the <main.py>file, the generator functions are enabled/disabled by setting the corresponding section to True/False. Modify these if-statements to enable only what you want to generate.
In case you want to use the Advanced BnB generation rulesets, set the 'USE_ABNB_SYSTEM' to True.

