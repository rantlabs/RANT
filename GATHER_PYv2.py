#! /usr/bin/python

# OLD PYTHON VERSION 2.7 - NO LONGER MAINTAINED

import os, sys, getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException

platform = 'arista_eos'
username = raw_input('Username? ')
passy = getpass.getpass()

def openfile(file):
        f = open(file,'r')
        x = f.read()
        x = x.strip()
        x = x.split('\n')
        return x

commandfile = raw_input('command file? ')
targetfile = raw_input('target file? ')

show_commands = openfile(commandfile)
hostlist = openfile(targetfile)


outfile = raw_input('output filename? ')

for host in hostlist:
	try:
		device = ConnectHandler(device_type=platform, ip=host, username=username, password=passy)
	except Exception:
		continue
	try:
		device.find_prompt()
	except Exception:
		continue
	sys.stdout=open(outfile,"a")
	for item in show_commands:
		try:
			output = device.send_command(item)
		except:
			continue
		output = output.split('\n')
		for line in output:
			print host + " " + "|" + item + "|" + " " + line
	device.disconnect()
	sys.stdout.close()
