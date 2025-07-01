# (Advanced) Bunkers & Badasses Loot Generator
> **⚠** ***IN DEVELOPMENT*** **⚠**

This application is intended to automatically generate equipment cards for the 
TTRPG "[*Bunkers & Badasses*](https://tinytinagames.com/)" by Nerdvana Games and 
for the "*Advanced Bunkers & Badasses*" version of the game created by *Akkator006*
(for more info, check the Discord!).


### Features

| Card Generation | Standard Bunkers&Badasses | Advanced Bunkers&Badasses |
|-----------------|---------------------------|---------------------------|
| Guns            | ✅                         | ✅                         |
| Shields         | ✅                         | ✅                         |
| Grenades        | ❌                         | ❌                         |
| Relics          | ❌                         | ❌                         |
| Class Mods      | (NA)                      | ❌                         |
| Generic Potions | ❌                         | (NA)                      |
| Health Potions  | ✅                         | (NA)                      |
| Shield Potions  | ✅                         | (NA)                      |

### CLI Quick Reference

Overview of CLI commands:

| Command      | Arguments        | Options                                                | Description                                                   |
|--------------|------------------|--------------------------------------------------------|---------------------------------------------------------------|
| ``load``     | \<game(s)>       | ``bl1`` ``bl2`` ``bl3`` ``bl-tps`` ``bl-wl``           | Load item images from selected games.                         |
|              | (``--reset``)    | -                                                      | Clears previsouly loaded resources.                           |
| ``generate`` | \<item>          | ``gun`` ``shield`` ``health_potion`` ``shield_potion`` | Generate an equipment card (based on selection).              |
|              | (``--use-abnb``) | -                                                      | Use the *Advanced Bunkers&Badasses* loot generation rulesets. |


## Set-Up

Make sure the Python package requirements are installed:

``pip install -r requirements.txt``

The application does not automatically come with equipment images and needs to download 
them from the different Borderlands Games (courtesy of *www.lootlemon.com*).
This can be done with the ``load`` argument:

``python /path/to/directoy/main.py load``

*(The download might take a couple of minutes)*

You can also specify which game(s) will be used for the images. If no option is given, 
it defaults to ``bl3`` (Borderlands 3).

| Options    | Game                        |
|------------|-----------------------------|
| ``bl1``    | Borderlands 1               |
| ``bl2``    | Borderlands 2               |
| ``bl3``    | Borderlands 3               |
| ``bl-tps`` | Borderlands: The Pre-Sequal |
| ``bl-wl``  | Tiny Tina's Wonderlands     |


> **EXAMPLE**
> 
> To load equipment from Borderlands 1 & 2:
> 
> ``python /path/to/directoy/main.py load bl1 bl2``

Whenever this command is run again, it will **ADD** the new equipment to the previously loaded
equipment. You can start with a clean slate using the `--reset` argument.

> **EXAMPLE**
> 
> To remove previously loaded items and only load equipment from Borderlands 2:
>
> ``python /path/to/directoy/main.py load bl2 --reset``

## Loot Generation

>Not all items are implemented yet, so refer to the *CLI Quick Reference* table at the top of
this document to see what options are available.

After the image resources have been loaded, you can generate loot using the ``generate`` command.
You need to specify what item you want to generate a card for.

> **EXAMPLES**
> 
> Generate a Gun Card:
> 
> ``python /path/to/directoy/main.py generate gun``
> 
> Generate a Health Potion Card:
> 
> ``python /path/to/directoy/main.py generate health_potion``

You can generate cards using the *Advanced Bunkers & Badasses* rulesets using 
the ``--use-abnb`` argument

> **EXAMPLE**
> 
> Generate a Shield Card for *Advanced Bunkers & Badasses*:
> 
> ``python /path/to/directoy/main.py generate shield --use-abnb``


