# VivoSwap
This is a dig site fossil swapper. You can specify two Vivosaurs, and this program will patch your game so that all fossils of Vivosaur 1 will be found at the dig sites and locations where Vivosaur 2 was originally found, and vice versa.
You can specify as many swaps in the program as you want. I have tested up to 10 swapping pairs at once, all were successfully swapped.

This code is branched from code created by opiter09 to randomize various aspects of the game, found here: https://github.com/opiter09/Fossil-Fighters-Randomizer

It is well worth checking out. Major props to opiter09 for all of the work to patch the actual game, I only modified his randomizer to make it so you can specify the swaps yourself instead.
I also removed a lot of other features from his program because I did not need them, such as changing your Starter Vivosaur and increasing the difficulty of Battles. Please check it out if that sounds interesting.

I created this program out of simple annoyance that some Vivosaurs like T-Rex are only able to be revived in Post-Game where it is basically pointless and you can never use them. At least Pokemon allows you to catch the game's mascot before you beat it.

As this is based on opiter09's work, it shares some of the same quirks and features.

Quirks:
- You MUST put the ROM in the same folder as swapper.exe, or it won't work.
- Using swapper.exe will modify the game to skip the Trial Dig Site (awesome), but as a result of this, if you try to leave the dig site selection menu when talking to Beth during Chapter 1, the game will freeze, so dont do that.
- You can only swap the main 100 Vivosaurs, the other special Vivosaurs will remain as they were.
- I have only tested this program on a USA version of the game, and I suspect it will only work on USA or English versions of the game
- Be EXTRA careful if you ever plan on swapping V-Raptor, as you can lock yourself out of the rest of the game in Chapter 3 if you swap it with a Vivosaur that is only found in dig sites after Rivet Ravine. This is because you must use a V-Raptor when battling Holt at the Junk Depot.

Features:
- The Trial Dig Site tutorial is skipped (see above)
- You can swap as many Vivosaurs as you want
- Only the first swap of a Vivosaur will take place. If you try to specify another swap involving a previously swapped Vivosaur, that swap will be skipped
- If at least one of a swaps entries is left blank, that swap will be skipped
- Specifying a swap involving a Donation Point Vivosaur will also swap them at the Donation Booth (see newDPVivos.txt)
- A list of all the Dig sites with the original spawns and rates is available in originalDigsiteSpawns.txt. After running the program, you can see the new Vivosaur locations in newDigsiteSpawns.txt

How to use:
- Obtain a ROM of Fossil Fighters
- Download: press the green "Code" button and choose "Download ZIP." Extract the files and place your ROM into the extracted file folder
- Windows ONLY: drag and drop your ROM onto swapper.exe to start the program
- Other OS: If you are tech-savvy enough, you can install Python and run the script swapper.py with the ROM name as the only argument, otherwise, I am not sure I can help you

# Source Codes
- Base Code: https://github.com/opiter09/Fossil-Fighters-Randomizer
- FFTool: https://github.com/jianmingyong/Fossil-Fighters-Tool
- NDSTool: https://github.com/devkitPro/ndstool (this is a later version; the one used here came without a license as part of DSLazy)
- xdelta: https://github.com/jmacd/xdelta-gpl

