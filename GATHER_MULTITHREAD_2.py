#! /opt/python37/bin/python3

# Uses multiprocessing module for threading and the unordered imap function
# Multi11 is the same as multi10 except I try to change to arista_eos if cisco_ios fails around line 43
# Trying some radically different threading techniques. This could be very differnet.

from multiprocessing.pool import ThreadPool as Pool
import threading

from tqdm import tqdm
from time import time
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


def rantgather(host):
        print(f'#### COLLECTING DATA FOR {host} ###')
#        file = open(outfile,"a")
        single_host_total = []
        try:
                device = ConnectHandler(device_type=platform, ip=host, username=username, password=passwd)
        except Exception:
                try:
                        device = ConnectHandler(device_type='arista_eos', ip=host, username=username, password=passwd)
                except Exception:
                        print(host + " is unavailable")

        try:
                device.find_prompt()
        except Exception:
                print(host + " is unavailable")

        for item in tqdm(show_commands):
                try:
                        output = device.send_command(item)
                except:
                        continue
                output = output.split('\n')
                single_cmd_out = []
                for line in output:
                        single_cmd_out.append(f'{host} |{item}| {line}\n')
                single_host_total.append(single_cmd_out)
        with open(outfile, 'a') as file:
                for item in single_host_total:
                        for line in item:
                                file.write(line)
        return host


if __name__ == '__main__':
	pool = Pool(15)
	start = time()
	for i in pool.imap_unordered(rantgather, hostlist):
		print(f'{i} is complete')
	end = time()
	print('Elapsed time:', end - start)
