# TEXTpY_Dungeon
#### Video Demo: https://www.youtube.com/watch?v=vR5vCuTJCFc
## Description
TEXTpY_Dungeon is a text-based rogue-like game that offers endless hours of pain and death. As part of my final project for CS50's Introduction to Programming with Python, I have meticulously designed this game to provide an immersive and deadly experience for players.


## Folder Contents
- **project.py**: This file contains the ```main``` function, along with several other helper functions necessary to implement the game.
- **game_classes.py**: This file contains all the game classes necessary to implement TEXTpY_Dungeon.
- **test_project.py**: This contains test functions written using the ```pytest``` library for the project.py file.
- **requirements.txt**: All ```pip```-installable libraries that I used for this project are listed here.

## How to Play
- Execute the program using the command `python project.py`.
- Input your desired username when prompted.
- Whenever you encounter an event, follow the prompts accordingly.
- After several attempts, you will understand the logic behind the game and face more satisfying challenges. Have fun playing or should I say dying!

## Game Mechanics

In every game, your character’s stats, starter weapon, and mysterious elements will be randomly generated, offering a unique gameplay experience each time.

#### map info
TEXTpY_Dungeon is a text-based rogue-like game that provides you with a map filled with various characters. The game mechanics and features of the map are as follows:

- **Player** - represented by **x** on the map.
- **Random event** - represented by **?** on the map. A place where you can either gain a reward or suffer a penalty.
- **Campfire** - represented by **+** on the map. The final stop before you face the **Boss**.
- **Normal enemies** - represented by **!** on the map.
- **Elite enemies** - represented by **\*** on the map.
- **Boss** - represented by **#** on the map.

#### character's stats info
Your character has several stats - **real stats** and **complex stats**:

- **Real stats**: These include vitality, aura density, dexterity, constitution, and prediction:
  - **Vitality** plays an important role in determining how much health and aura_regeneration points you have.
  - **Aura Density** serves as a damage multiplier for mysteries. It is limited by your weapon's aura_affinity value.
  - **Dexterity** plays a vital role in determining your initiative.
  - **Constitution** plays an important role in how much health and primordial_aura points you have.
  - **Prediction** plays a role in determining your initiative and how many of your enemies' stats you can see.

- **Complex stats**: These include health, initiative, primordial_aura, and aura_regeneration:
  - **Health** determines how many hits you can take before dying.
  - **Initiative** determines the order of battle queue and whether or not you can avoid traps.
  - **Primordial_aura** is a stamina-like stat that determines how many mystery abilities you can use.
  - **Aura_regeneration** determines how much primordial_aura you can regain each turn during a battle.

#### mysteries' info;
- Each mystery takes those stats: target, target_stat_and_strength, aura_cost, is_active, turn_count, permanence
  - **target**: Determines whether the mystery affects the user or the enemy.
  - **target_stat_and_strength**: Determines which stat(s) are affected by the mystery and how strong the impact is.
  - **aura_cost**: Specifies the amount of primordial aura required to use the mystery once.
  - **is_active**: Indicates whether the mystery is an active skill that can be used during battles or a passive one that's always active.
  - **turn_count**: Specifies how many turns the mystery can be used before it is exhausted.
  - **permanence**: If it's a turn-based mystery, this determines whether its effects become permanent after the duration is over.

#### Weapons' info:
- Each weapon in the game has an **aura affinity**, which acts as a limiter for the player’s aura density stat. This means that using a weapon with a different aura affinity than your own may lower the effectiveness of your attacks. In addition to their unique aura affinity, each weapon has its own set of mysteries that can only be utilized when the weapon is equipped. These mysteries add an extra layer of strategy and depth to battles, and encourage players to experiment with different weapon choices to find the ones that best suit their gameplay styles.



## Contribution
If you find any issues or want to contribute to this project, feel free to create a pull request or submit an issue.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
