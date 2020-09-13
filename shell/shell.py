#!/usr/bin/env python3

import os
import re
import sys


def pyshell():
	while True:
		cmd = input("$ ")
		if cmd == "exit":
			break

		#checks if the first three chars are "cd " to initiate change directory 
		elif cmd[:3] == "cd ":
			pysh_cd(cmd[3:])
		elif (cmd.find(">") != -1):
			redirect_cmd(cmd)
		else:
			cmd_execute(cmd)


#change directory function
def pysh_cd(path):
	try:
		os.chdir(os.path.abspath(path))
	except Exception:
		os.write(2, "cd: no such file or directory".encode())

def redirect_cmd(cmd):
	rc = os.fork()

	if rc < 0:		
		sys.exit(1)

	elif rc == 0:
		args = [cmd.strip().split()[0]]

		os.close(1)
		sys.stdout = open(cmd.strip().split()[2], "w")
		os.set_inheritable(1, True)

		for dir in re.split(":", os.environ['PATH']):
			program = "%s/%s" % (dir, args[0])
			try:
				os.execve(program, args, os.environ)
			except FileNotFoundError:
				pass

		os.write(2, ("%s: command not found\n" % args[0]).encode())
		os.wait()
		sys.exit(1)
	else:
		childPidCode = os.wait()

def cmd_execute(cmd):
	rc = os.fork()
	
	#failed fork
	if rc < 0:
		sys.exit(1)

	elif rc == 0:
		if "|" in cmd:
			stdin, stdout = (0,0)
			stdin = os.dup(0)
			stdout = os.dup(1)
			
			fileIn= os.dup(stdout)
			
			for command in cmd.split("|"):
				os.dup2(fileIn, 0)
				os.close(fileIn)
				
				if command == cmd.split("|")[-1]:
					fileOut = os.dup(stdout)
				else:
					fileIn, fileOut = os.pipe()

				os.dup2(fileOut, 1)
				os.close(fileOut)

				try:
					print("piped")
				except Exception:
					pass
		else:
			args = [cmd.strip().split()[0]]
			for dir in re.split(":", os.environ['PATH']):
				program = "%s/%s" % (dir, args[0])
				try:
					os.execve(program, args, os.environ)
				except FileNotFoundError:
					pass
			os.write(2, ("%s: command not found\n" %args[0]).encode())
			sys.exit(1)
	else:
		os.wait()

pyshell()

