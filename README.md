![undervoidtitle](/data/img/undervoidtitle.png)

# Undervoid

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Copyright (c) 2019 Matthew Geary  

>"There are more things in the Undervoid, Horatio, than are dreamt of in your philosophy."

Undervoid is a very-much-under-development dungeon crawler/bullet hell/rpg lite experience being developed with pygame. Choose one of several wacky characters and venture, in search of glory and treasure, into the Undervoid, an interdemensional rift beneath the world where the laws of nature and time lose all meaning and enemies lurk around every corner. 

## Requirements

python 3.7+  
pipenv

## Run

Undervoid is developed to utilize pipenv, which takes care of dependencies for you. To install pipenv, run:  
`pip3 install --user pipenv`. 

Refer to https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv for more information on installing pipenv. 

Once you've cloned the repository and installed pipenv, you can install dependencies with:  
`pipenv install`

Then, you can run Undervoid with:  
`pipenv run python3 main.py`  

## Gameplay

### Introduction

When you begin a new game of Undervoid and choose your character, you will begin the game in the Temple, a starting area which you can return to in between levels if you choose. In future times, you may find more travelers and strange beings beginning to populate the Temple, but for the present time it is a rather lonely place. In the center of the temple is a "Rift". These portals are found throughout the Undervoid, and they can either take you further in, or bring you back to the Temple, depending on your choice.  

The levels in Undervoid are randomly generated from a premade set of dungeon pieces. The goal of each level is to make it to the end and use the level's Rift, collecting as many gold coins as possible along the way. Enemies will try to stop you, so make sure your health doesn't get too low! Enemies will drop gold coins and health potions, which will replenish player health. 

### Controls 

* `W` - move up/north
* `A` - move left/west
* `S` - move down/south
* `D` - move right/east
* `E` - use Rift to venture further into the Undervoid
* `R` - use Rift to return to the Temple
* `Mouse` - aim
* `Mouse1` or `Spacebar` - shoot
* `ESC` - exit

### Points of Interest

![rift](/data/img/rift01.png)  
Rift - use these mystical doors to move around the Undervoid

### Playable Characters

![pilgrim](/data/img/pilgrim_magic.png)  
__Pilgrim__
>"To go back is nothing but death; to go forward is fear of death, and life everlasting beyond it. I will yet go forward."[1](https://www.goodreads.com/work/quotes/1960084-the-pilgrim-s-progress)

![voidwalker](/data/img/voidwalker_magic.png)  
__Voidwalker__
>"The further in you go, the more clearly you'll hear the All-Knowing whispering the truth most beautiful, which can only be conveyed in the ancient tongue..."

![lizardwizard](/data/img/lizardwizard_magic.png)  
__Lizard Wizard__
>" I gave you the chance of aiding me willingly, but you have elected the way of pain!" [2](https://www.imdb.com/title/tt0120737/characters/nm0000489)

### Enemies

![thrall](/data/img/thrall.png)  
__Thrall__
>"*Snarl*"

![sleeper](/data/img/sleeper.png)  
__Sleeper__
>"*Yawn*"

### Items

![healthpotion](/data/img/potion01.png)  
__Health Potion__
>"Water of life"

![goldcoin](/data/img/coin01.png)  
__Gold Coin__
>"A coin in the hand is worth two in the Void"

## Acknowledgements  

### Music

"Leaving Home" - Kevin MacLeod (incompetech.com)  
"voidwalk" - Matthew Geary  
  
The music for Undervoid is licensed under Creative Commons: By Attribution 4.0 License  
Found in `\data\music\MUSIC_LICENSE` or at http://creativecommons.org/licenses/by/4.0/  

### Art and Sound

In-game artwork and sounds by Matthew Geary.  
Title Art generated at https://fontmeme.com/pixel-fonts/

## License  
  
This program is licensed under the "MIT License".  Please
see the file `LICENSE` in the source distribution of this
software for license terms.
