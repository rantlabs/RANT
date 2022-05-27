#! /usr/bin/python3

# Uses multiprocessing module for threading and the ordered map function
# Multi11 is the same as multi10 except I try to change to arista_eos if cisco_ios fails around line 43
# Trying some radically different threading techniques. This could be very differnet.
# Adding unavaialable device message into main output
# Added netmiko global_delay_factor of 0.4 it is increments of 100
# import threading
# Change from TQDM to atpbar
# Adding argparse
# Removed for loop in Multithread call


from multiprocessing.pool import ThreadPool as Pool
from time import time
# import os, sys, getpass
import getpass
from netmiko import ConnectHandler
# from netmiko.ssh_exception import NetMikoTimeoutException
# from paramiko.ssh_exception import SSHException
from atpbar import atpbar
import argparse

platform = 'cisco_ios'

def openfile(file):
        f = open(file,'r')
        x = f.read()
        x = x.strip()
        x = x.split('\n')
        return x

def rantgather(host):
        # If rantgather is imported, platform, username, and passwd will need to be set as global variables
        single_host_total = []
        try:
                device = ConnectHandler(device_type=platform, ip=host, username=username, password=passwd, timeout=30, global_delay_factor=0.4)
        except Exception:
                try:
                        device = ConnectHandler(device_type='arista_eos', ip=host, username=username, password=passwd, timeout=30, global_delay_factor=0.4)
                except Exception:
                        with open(outfile, 'a') as file:
                                file.write(host + " is unavailable\n")
                        return None

        try:
                device.find_prompt()
        except Exception:
                with open(outfile, 'a') as file:
                        file.write(host + " is unavailable\n")

        for item in atpbar((show_commands), name=host):
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


def main():
        global platform
        global username
        global passwd
        global commandfile
        global targetfile
        global outfile
        global show_commands

        platform = 'cisco_ios'
        # ARGPARSE CODE
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store', dest='commandfile',help='Enter Command File - One Per Line', default=False)
        parser.add_argument('-o', action='store', dest='outfile',help='Enter Output Log File Name',default=False)
        parser.add_argument('-u', action='store', dest='username',help='Username',default=False)
        parser.add_argument('-t', action='store', dest='targetfile',help='Host File - One Per Line',default=False)
        parser.add_argument('-p', action='store', dest='passwd',help='Enter Password',default=False)
        parser.add_argument('--os', action='store', dest='platform',help='Enter Netmiko Platform',default='False')
        results = parser.parse_args()
        username = results.username
        commandfile = results.commandfile
        targetfile = results.targetfile
        outfile = results.outfile
        passwd = results.passwd
        platform = results.platform 
        # END ARGPARSE CODE

        if not username:
                username = input('Username? ')

        if not passwd:
                passwd = getpass.getpass()
        
        if not commandfile:
                commandfile = input('command file? ')

        if not targetfile:
                targetfile = input('target file? ')

        if not outfile:
                outfile = input('output filename? ')

        if not results.platform:
                platform = 'cisco_ios'          

        show_commands = openfile(commandfile)
        hostlist = openfile(targetfile)

        pool = Pool(30)
        start = time()
        pool.map(rantgather, hostlist)
        end = time()
        print("GatherDB Creation Complete")
        print('Elapsed time:', end - start)

if __name__ == '__main__':
	main()
