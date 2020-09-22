#!/usr/bin/env python3

import os
import re
import sys


def pyshell():
	while True:
		if 'PS1' in os.environ:
			os.write(1, os.environ['PS1'].encode())
		else:
			os.write(1, ("$ ").encode())
		try:
			cmd = input()
		except EOFError:
			sys.exit(1)
		cmd = cmd.strip()

		if cmd == "exit":
			break

		#checks if the first three chars are "cd " to initiate change directory 
		elif "cd" in cmd:
			ex = cmd.split()
			pysh_cd(ex[1])
			if len(ex) > 2:
				for i in range(len(ex),2):
					print(ex[i])
					cmd_execute(ex[i])
		elif ">" in cmd:
			redirect_cmd(cmd)
		else:
			cmd = cmd.split(" ", 1)
			cmd_execute(cmd)


#change directory function
def pysh_cd(cmd):
	try:
		os.chdir(cmd)
	except Exception:
		os.write(2, "cd: no such file or directory".encode())

def redirect_cmd(cmd):
	rc = os.fork()

	if rc < 0:		#failed fork
		sys.exit(1)

	elif rc == 0:
		args = [cmd.strip().split()[0]]

		os.close(1)
		sys.stdout = open(cmd.strip().split()[2], "w")  #opens file to write to
		os.set_inheritable(1, True)			#sets inheritability of stdout to true

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
		if cmd != "":
			try:
				os.execve(cmd[0], cmd, os.environ)
			except FileNotFoundError:
				pass
			for dir in re.split(":", os.environ['PATH']):
				program = "%s/%s" % (dir, cmd[0])
				try:
					os.execve(program, cmd, os.environ)
				except FileNotFoundError:
					pass
			print(cmd[0] + ": command not found.")
			sys.exit(1)
	else:
		os.wait()

pyshell()

