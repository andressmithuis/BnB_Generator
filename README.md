⚠ WARNING: IN EARLY DEVELOPMENT ⚠

Not all features are complete and expect things to be buggy from time to time.

Features:
- Generation of Gun Cards (Advanced BnB✅)
- Generation of Shield Cards

Extra:
- Generation of Health Potion Cards
- You can influence the properties of generated items by providing the right function arguments (VERY WIP, might not work as expected or even be correct).


How to Use:

Make sure the Python package requirements are installed:

``pip install -r requirements.txt``

Then run the main.py file to generate loot:

``python /path/to/directoy/main.py``

When run for the first time, it will attempt to download the image files used for weapons, shields, etc. This may take a couple of minutes.

In the <main.py>file, the generator functions are enabled/disabled by setting the corresponding section to True/False. Modify these if-statements to enable only what you want to generate.
In case you want to use the Advanced BnB generation rulesets, set the 'USE_ABNB_SYSTEM' to True.

