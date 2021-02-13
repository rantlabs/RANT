#! /opt/python37/bin/python3

import os, sys, getpass
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException

platform = 'cisco_ios'
username = input('Username? ')
passwd = getpass.getpass()

def openfile(file):
        f = open(file,'r')
        x = f.read()
        x = x.strip()
        x = x.split('\n')
        return x

commandfile = input('command file? ')
targetfile = input('target file? ')

show_commands = openfile(commandfile)
hostlist = openfile(targetfile)


outfile = input('output filename? ')

for host in hostlist:
	sys.stdout=open(outfile,"a")
	try:
		device = ConnectHandler(device_type=platform, ip=host, username=username, password=passwd)
	except Exception:
		print (host + " is unavailable")
		continue
	try:
		device.find_prompt()
	except Exception:
		print (host + " is unavailable")
		continue
	for item in show_commands:
		try:
			output = device.send_command(item)
		except:
			continue
		output = output.split('\n')
		for line in output:
			print (host + " " + "|" + item + "|" + " " + line)
	device.disconnect()
	sys.stdout.close()
