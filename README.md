# Discord Dice Generator
###  Discord bot to roll dice for rpg like D&amp;D or Savage World and manage utilities for OtakusHouse/Ideaverse servers

:dragon: Author: Samuele Ferri (@ferrixio, ferri#9207)

:star: Version 3.2

## Requirements

Python 3.10 and Discord.py 2.3.1 (this version of discord.py doesn't work with python 3.11)

## Story

This bot was created in 2021, a year after the beginning of the covid, and after my firts steps in the world of role-play games. Me and my friends were using [Dice Maiden bot](https://alternative.me/discord/bots/dice-maiden) during our sessions, but sometimes we needed some features that this bot doesn't have.
So I decide to write my own Dice Maiden using python and that how Dice Generator (or Dama Fortuna for us) was born!

Most of bot's answers are in italian, because me and friends' of mine are italian, but the code is written written in english.

I'm thankful to Daniel (@Scarlet06) and Flavio, two friends of mine, for their help.

## Features

This bot can do many things:

    > simple rolls
    > advantage & disavantage rolls
    > toss coins
    > stats generator for D&ampD 5e
    > explosive rolls

Dice Generator is currently run on a server, and if you want to add to your server (and also customize it) just write to me.

Main feature of the bot is roll dice in the following way:

`!tira 1d20+3 2d10-1` -> `Tiro di ferrixio:  [1], [3, 3],  totale: [4, 5]`

The bot is also responsible to send a welcome message and count members in [OtakusHouse server](https://discord.gg/9e4HPeWhbf).

## Changelog

### Version 3.2
+ Create this repository and write this file;
+ Fixed a bug involving username display in answers. Now the bot uses the `global_name` attribute;
+ Changed some values and names in the code, not in the answers;
+ Renamed `!lc` command in `!explode`;
+ Discovered that not writing a return statements in a function, automatically it returns None (after 3 years of coding);
+ Fixed a bug in `!member` that brakes the function when the command is invoked in a private chat with the bot;
+ Now `!member` sends to the author the number of members of the server and works with everybody;
+ Added `!reset` to reset the random number generator seed;
+ Reworked some parts of the code to optimize them;
+ Removed `!SFmembri` because it was useless;
+ Edited `!help` to avoid bugs if there are other bots/clients that uses the same syntax to call this command.

### Version 3.1
+ Edited the function `!forall`. Now accepts dice as modifiers (they will be rolled, too).
+ Added standard deviation in output of function `!stats`.
+ Corrected a bug in `on_message()` method, which could cause a loop of the bot (strange that I've never notice it)
+ Added `!login` for my owner to get where I am. Improved tiraDadi.

### Version 3.0
+ Brand new programming implementations!
+ Created a new function "conversione" that converts input list in a compact version of it. Ex: `!tira 5d6+1d4 +1 1- 2d10 --> [5d6+1d4+1, 1-2d10]`
+ Adjusted the processing after `f_roll` and handled some error, like "no dice in input".
+ Now the bot will ignore isolated numbers in input (that have not +/-).
+ Adjusted ALL the functions of the bot.
+ Now, ALL the functions that roll dice can make multiple rolls at the same time, separately

### Version 2.6.1
Corrected a type error and an output's bug in !stats

Added `!lc` to roll explosive dice rolls for savage world and similar games.

### Version 2.6
Rewritten functions `!adv` and `!dis`. Removed `!pandoru`.

Added `!elvenchad` for elven accuracy feature

### Version 2.5.3
Compressed some if-statements. Fixed some bugs. Move some part of code among classes.

Added `!ping` to get bot latency

### Version 2.5.2
Added the `!changelog` command; it sends as DM this file.

Improved some details

Add `!SFmembri` to get guild's member number that works only for me

### Version 2.5.1
Created a stand-alone class for auxiliary functions, like `!help`

### Version 2.5
Created a custom `!help` command with dictionaries

### Version 2.4
Corrected `!loli` command (because Omar annoyed me...). Edited `!help` command.

Added `!membri` for admins (@commands.has_permissions(administrator=True)) and `!pandoru` for X-mas

### Version 2.4.2
Corrected a type error in the output of function `!forall`. Added the private function `!membri`.
Avoided some bugs.

### Version 2.4.1
Corrected an error in the output of function `!cento`.

### Version 2.4
Implemented a new function, `!forall`, which rolls some dice and add modifiers to each result.
By an unkown reason, it doesn't work if there is a blank space between multiple dice, but it works if there is a '+'.

Added a new function, `!cento`, which rolls 1d100.

### Version 2.3
Changed output font of dice' results.

Added new pictures to `!loli`.

Added a phrase exclusively for Visco in `!stats` (because he doesn't remember, even after 99999 times, that this function returns automatically the sum of the three highest dice over four).

Added a new welcome phrase in 'Otakus'

### Version 2.2
Added new class, called 'Otakus', used in Otaku's server for welcome message.

Compacted the output message in `!stats` and added some emojis.

Corrected some typos in messages.

Added the 'soap' answer (thanks to 'soap-opera dungeon master' Visco).

### Version 2.1
Added the commands:
+ `!adv` for advantage rolls
+ `!dis` for disadvantage rolls
+ `!stats` to generate automatically n stats, n among 1 and 6
+ `!loli` to send ""cute"" loli's pictures
+ `!tpc` to roll `!tira 1d20+mod` (useful for attack rolls and saving throws)
+ `!coin` to toss a 1d2 (it has a 1/256 chance that the coin returns a draw)

### Version 2.0
Built a 'real' programm.
Implemented in `!tira`:

	- single throws
	- multiple separated throws
	- multiple summed throws
	- correction of some type errors in input string:
		*) operators + or - at the beginning/end of the string
		*) blank spaces between characters in the input string
		*) type error in dice' numbers and amplitude

### Version 1.1
Bug fixed

### Version 1.0
Built a basic programm, which was able to roll dice but with some issue in the main function `!tira`.
Implemented the base answer to "master" for me and friends' of mine.
Learned how to use 'dotenv' methods for storing information.