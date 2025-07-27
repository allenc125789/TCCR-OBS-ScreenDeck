
## Description

A school project i'm sharing on github.

I'm in my school's Combat Robotics Club, and have been tasked with making the live-stream look nice and professional, thanks to having previous experience with OBS and live-stream production. I also utilized my programming knowledge to make this script to help control everything!

This script has 2 main benefits:

+ A custom UI with the ability to control multiple sources, scenes, and effects more consistently and efficiently than the standard OBS scene/source layout.
+ Very easy to control for someone new to OBS or doesn't know my specific scene setup.

## Dependancies:
Software:

[OBS-Studio](https://obsproject.com/download), [GoPro Webcam](https://community.gopro.com/s/article/GoPro-Webcam?language=en_US#gettingstartedwithwindows)

Libraries:

[obsws](https://pypi.org/project/obsws-python/)

## Setup:
Refer to the README.md, located in the file TCCR_OBS_Resources.zip, found in the TCCR Club's socialmedia gmail/gdrive...

## ToDo:

+ ~~Add a match/round counter, one that has 2 buttons, for making the round go up or down, then a third button to hide/show it.~~

+ Add a name vs name section, with a red and blue bar background, for the bots battling. make a little red and blue pixel bot to put on the either side of it.

+ add loop to wait for obs to launch. (if its delayed by a popup, itll poop out an error)

+ ~~add transition between cams~~

+ Add a webserver function to control starting the round, and activating a sfx for a bell.
