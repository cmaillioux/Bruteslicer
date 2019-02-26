# Bruteslicer
A pyrit wrapper which manages bruteforce wordlists generation and disk space.

## Disclaimer
*This site contains materials that can be potentially damaging or dangerous. If you do not fully understand something in this script or its purpose, then do not try to use it. Please refer to the laws in your province/country before accessing, using, or in any other way utilizing these materials. These materials are for educational and research purposes only.*

## Getting Started
### Description
When it comes to practical bruteforcing, two things are limiting the exercice, power and space. Calculating power, thanks to nowadays GPUs, is increasing rapidly. However, a lot of disk space is required to store the huge wordlists generated by tools such as crunch. 
To avoid this problem, the Bruteslicer will manage disk space for you and cut the wordlists into parts. 

It generates wordlists within user specified limits before feeding pyrit with it to crack a ".cap" file and then clean the used wordlist. Then it generated another "slice" of the wordlist which matches size limits, before cleaning it and do it again, and again, until it reaches the end of the charset or finds a matching password.

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
In order to use this script, 

### Using the tool
a

### 

## Authors
The author of the Bruteslicer wrapper tool is Clément MAILLIOUX. 

## License
This script is Licensed under GNU GPL v3. Please refer to LICENSE file for more details.
