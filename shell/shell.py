#!/usr/bin/env python3

import os
import re
import sys


def pyshell():
	pysh_status = 1
	while pysh_status == 1:
		if 'PS1' in os.environ:
			os.write(1, (os.environ['PS1']).encode())
		else:
			os.write(1, ('$ ').encode())
			try:
				userInput = input()
				inputTokens = pysh_tokenizer(userInput)
				pysh_status = pysh_commands(inputTokens)
			except EOFError:
				sys.exit(1)


#function that tokenizes input so we can parse it for the commands function 
#	seperating the commands from arguments
def pysh_tokenizer(userInput):
	inputTokens = userInput.split(" ")
	return inputTokens

#function is fed tokenized list of commands + arguments to execute shell functions
def pysh_commands(inputTokens):

	#checks if list is empty
	if '' in inputTokens:
		return 1

	for com in range(len(inputTokens)):

		#change directory function
		if(inputTokens[com] == "cd" and len(inputTokens) > 1):
			try:
				os.chdir(inputTokens[com + 1])
				return 1

			except FileNotFoundError:
				print(inputTokens[com + 1] + ": Directory does not exist")
				return 1
		
		#exit function
		elif(inputTokens[com] == "exit"):
			print("Exiting pyshell")
			return 0

		#redirection

		#pipes

	print("Command not recognized")
	return 1

pyshell()

