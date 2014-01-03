# Linux Music To Android

A simple utility to copy your music from your Linux music manager's playlist to your Android device.  
As for now, [Rhythmbox](https://wiki.gnome.org/Apps/Rhythmbox/) is supported and I plan to integrate [Banshee](http://banshee.fm) in the future.

## Configure
Tweak the app settings in `config.json`.

## How to use
Launch from a terminal : `$ python main.py`.

#### Parameters
At the moment, these parameters cannot be passe at the same time.

`-r` : syncs the Rhythmbox playlist as configured in `config.json`  

#### Options 
`-d` or `--debug` : detailed debugging output  
`--rebase` : purges all the content already copied from the selected music player and performs a fresh sync.

`-s` or `--silent` : logs the output in `lmtoa.log` instead of displaying it in the standard output.  
**This may not be a great idea** since the utility expects inputs from you, for now.

## Developper's documentation
A full [Doxygen](http://www.stack.nl/~dimitri/doxygen/)-generated documentation is available [here](http://doc.quentinbarrand.com/LinuxMusicToAndroid). You can also contact me if you have any question.  
Do not hesitate to contribute !

