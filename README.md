![undervoidtitle](/data/img/undervoidtitle.png)

# Undervoid

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Copyright (c) 2019 Matthew Geary  

>"There are more things in the Undervoid, Horatio, than are dreamt of in your philosophy."

Undervoid is a very-much-under-development dungeon crawler/bullet hell/rpg lite experience being developed with pygame. Choose one of several wacky characters and venture, in search of glory and treasure, into the Undervoid, an interdemensional rift beneath the world where the laws of nature and time lose all meaning and enemies lurk around every corner. 

# Table of Contents
1. [Requirements](#requirements)
2. [Run](#run)
3. [Gameplay](#gameplay)  
i. [Introduction](#intro)  
ii. [Controls](#controls)  
iii. [Points of Interest](#points)  
iv. [Playable Characters](#chars)  
v. [Enemies](#mobs)  
vi. [Items](#items)  
4. [Acknowledgements](#ack)
4. [License](#license)

## Requirements <a name="requirements"></a>

python 3.7+  
pipenv

## Run <a name="run"></a>

Undervoid is developed to utilize pipenv, which takes care of dependencies for you. To install pipenv, run:  
`pip3 install --user pipenv`. 

Refer to https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv for more information on installing pipenv. 

Once you've cloned the repository and installed pipenv, you can install dependencies with:  
`pipenv install`

Then, you can run Undervoid with:  
`pipenv run python3 main.py`  

## Gameplay <a name="gameplay"></a>

### Introduction <a name="intro"></a>

When you begin a new game of Undervoid and choose your character, you will begin the game in the Temple, a starting area which you can return to in between levels if you choose. In future times, you may find more travelers and strange beings beginning to populate the Temple, but for the present time it is a rather lonely place. In the center of the temple is a "Rift". These portals are found throughout the Undervoid, and they can either take you further in, or bring you back to the Temple, depending on your choice.  

The levels in Undervoid are randomly generated from a premade set of dungeon pieces. The goal of each level is to make it to the end and use the level's Rift, collecting as many gold coins as possible along the way. Enemies will try to stop you, so make sure your health doesn't get too low! Enemies will drop gold coins and health potions, which will replenish player health. 

### Controls <a name="controls"></a>

* `W` - move up/north
* `A` - move left/west
* `S` - move down/south
* `D` - move right/east
* `E` - use Rift to venture further into the Undervoid
* `R` - use Rift to return to the Temple
* `Mouse` - aim
* `Mouse1` or `Spacebar` - shoot
* `ESC` - exit

### Points of Interest <a name="points"></a>

![rift](/data/img/rift01.png)  
__Rift__
> use these mystical doors to move around the Undervoid

### Playable Characters <a name="chars"></a>

![pilgrim](/data/img/pilgrim_magic.png)  
__Pilgrim__
>"To go back is nothing but death; to go forward is fear of death, and life everlasting beyond it. I will yet go forward." [1](https://www.goodreads.com/work/quotes/1960084-the-pilgrim-s-progress)

![voidwalker](/data/img/voidwalker_magic.png)  
__Voidwalker__
>"The further in you go, the more clearly you'll hear the All-Knowing whispering the truth most beautiful, which can only be conveyed in the ancient tongue..."

![lizardwizard](/data/img/lizardwizard_magic.png)  
__Lizard Wizard__
>" I gave you the chance of aiding me willingly, but you have elected the way of pain!" [2](https://www.imdb.com/title/tt0120737/characters/nm0000489)

### Enemies <a name="mobs"></a>

![thrall](/data/img/thrall.png)  
__Thrall__
>"*Snarl*"

![sleeper](/data/img/sleeper.png)  
__Sleeper__
>"*Yawn*"

### Items <a name="items"></a>

![healthpotion](/data/img/potion01.png)  
__Health Potion__
>"Water of life"

![goldcoin](/data/img/coin01.png)  
__Gold Coin__
>"A coin in the hand is worth two in the Void"

## Validation

Undervoid was tested by hand the old-fashioned way: by playing it over and over throughout development. I feel fairly confident in saying that the game is quite stable, at least on the system I've been running it on: Ubuntu 18.04. I have also run it on Windows 10. 

That being said, my formal testing for this project was sorely lacking, especially since I recently descovered pygame has its own testing framework <https://www.pygame.org/docs/ref/tests.html> I was and am planning on implementing a full suite of tests, but at present it seems to have fallen by the wayside. 

### Known Issues

* general screentearing: some monitors exhibit screen tearing when moving around. Research suggests this is largely a pygame issue. Considering a switch to the godot engine, which would solve this issue. 
* somewhat rare: the player spawns into a level a few tiles away from where they are supposed to and gets stuck in a wall, requiring a game restart. 

## Acknowledgements  <a name="ack"></a>

Big thanks to Chris Bradfield's excellent pygame tutorial, which helped me enormously in getting started.
I have sought to cite this and other sources throughout my code where most appropriate.  
Youtube: <https://www.youtube.com/playlist?list=PLsk-HSGFjnaGQq7ybM8Lgkh5EMxUWPm2i>  
Github: <https://github.com/kidscancode/pygame_tutorials/tree/master/tilemap/part%2023>

### Music

"Leaving Home" - Kevin MacLeod (incompetech.com)  
"voidwalk" - Matthew Geary  
  
The music for Undervoid is licensed under Creative Commons: By Attribution 4.0 License  
Found in `\data\music\MUSIC_LICENSE` or at http://creativecommons.org/licenses/by/4.0/  

### Art and Sound

In-game artwork and sounds by Matthew Geary.  
Title Art generated at https://fontmeme.com/pixel-fonts/

## License  <a name="license"></a>
  
This program is licensed under the "MIT License".  Please
see the file `LICENSE` in the source distribution of this
software for license terms.
