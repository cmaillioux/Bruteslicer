# Bruteslicer
A wrapper which manages bruteforce wordlists generation and disk space before feeding Pyrit to crack handshakes.

## Disclaimer
*This site contains materials that can be potentially damaging or dangerous. If you do not fully understand something in this script or its purpose, then do not try to use it. Please refer to the laws in your province/country before accessing, using, or in any other way utilizing these materials. These materials are for educational and research purposes only.*

## Getting Started
### Description
When it comes to practical bruteforcing, two things are limiting the exercice: calculation power and disk space. Calculating power, thanks to nowadays GPUs, is increasing rapidly. However, a lot of disk space is required to store the huge wordlists generated by tools such as crunch. 
To avoid this problem, the Bruteslicer will manage disk space for you and cut the wordlists into parts. 

It generates wordlists within user specified limits before feeding pyrit with it to crack a ".cap" file and then clean the used wordlist. Then it generated another "slice" of the wordlist which matches size limits, before cleaning it and do it again, and again, until it reaches the end of the charset or finds a matching password.

If you exit the program before it ends, you will be able to resume from where it lefts or to re-configure another cracking session from the beginning.

### Prerequisite
* As this tool is a wrapper for pyrit, you must have pyrit installed on your system before using the Bruteslicer tool.
* Your Graphic Card, OpenCL or CUDA, must be installed and configured so that Pyrit can use it. Bruteforcing WPA without GPU is no use.
* Bruteslicer is a python script designed to run with python 2.7.
* Python modules : itertools, datetime, os, subprocess, sys, re

### Installing
* Installing the Bruteslicer is easy with git, just type : `git clone https://github.com/cmaillioux/Bruteslicer.git`
* go to the cloned folder : `cd ./Bruteslicer`
* run the script with : `python ./bruteslicer.py`

Please check the manual for detailed usage instructions.

## Manual
### Before starting
This script uses Pyrit to crack WPA handshakes. In order for the bruteforce to succeed, you must have a captured handshake in a ".cap" file. Such a file may be generated with the [aircrack-ng suite](https://www.aircrack-ng.org/).
Then, put this file ___in the same folder___ than the "bruteslicer.py" script.

### What should I configure?
Once the script is executed, you will have to answer to several questions in order to configure the tool. Here is a summary : 
__Resuming previously stopped bruteslicing :__ This is possible by answering "y" to the first question of the tool : `[?] Resume from a previously stopped Bruteslicing ? (y/n) : y`.

__Creating parameters for a new bruslicing :__ If you choose to answer not to resume from a previous session, you will have to specify 
- the name of the access point, for instance `[?] ESSID of the victim Access Point : KlemSSID`
- the length of the password you try to bruteslice, 8 chars long is a minimum for WPA passphrases : `[?] Requested length of passphrase to Bruteslice : 8`. Please note that the tool currently not increase the password length alone. If no password is found for an 8 chars long passphrase, then a brand new bruteslicing must be started with 9 in this parameter.
- the .cap file name that must be analyzed : `[?] .cap Filename to use (Should be in the same folder than "bruteslicer.py)". Type "xxxxxx.cap" : KlemSSID-02.cap` It must be in the same folder than the script.
- the max size allowed for all the bruteslicing operations. This include the wordlist, the pyrit database, its conversion with batches, etc. This tool will manage all `[?] Max space allowed on disk for bruteforcing operations (in Mb) : 400`
- The name of the wordlists which are created before beeing processed as a pyrit database `[?] Name of the generated wordlist : wrdlst`

__Modifying the charset__ The tool currently runs with ASCII chars. This is the only "configuration" which doesn't rely on questions starting the tool. If you want to modify the charset, you will have to edit the line 97 of the script (the "charset" variable) and modify the characters. Each character is separated by a space. 
In order to prevent any disk space overflow, if any non-ASCII character is detected, the max wordlist length is adapted using worst case scenario (chars coded on 3 bytes and on all lines). This will only increase the number of slicing iterations.

## Authors
The author of the Bruteslicer wrapper tool is Clément Maillioux. 

## License
This script is Licensed under GNU GPL v3. Please refer to LICENSE file for more details.
