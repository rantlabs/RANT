#! /opt/python37/bin/python3

# Uses multiprocessing.dummy threading module
# Multi11-6 is the same as multi11 except
# Different from multi10 Change to arista_eos if cisco_ios fails around line 43
# From multi11 remove modules multiprocessing, os, sys, time


from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
from multiprocessing.dummy import Pool as ThreadPool
import getpass
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

pool = ThreadPool(15)

def rantgather(host):
        print(f'#### COLLECTING DATA FOR {host} ###')
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
        return single_host_total


pool.map(rantgather,hostlist)
pool.close()
pool.join()
