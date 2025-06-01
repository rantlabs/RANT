from datetime import datetime
from multiprocessing.pool import ThreadPool as Pool
from time import time
from time import strftime
import getpass
from netmiko import ConnectHandler
from atpbar import atpbar
import argparse
import re
import os
import platform as pltfm

def simpleopen(file):
        f = open(file,'r')
        x = f.read()
        return x

def pinglist(DBfile):
        pattern = '(?=.*[1-9]\\.)(?=.*int)(?=.*ip)(?=.*brief)'
        newlist = [col.split() for col in DBfile.splitlines() if re.search(pattern,col)]
        return newlist

responselist = []
def func_pingcheck(hostinfo):
        pattern_ip = '((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)'
        if pltfm.system() == 'Windows':
                try:
                        response = os.system("ping /n 1 /w 1000 " + re.search(pattern_ip,hostinfo[6]).group())
                except Exception:
                        responselist.append(f'PING ERROR {hostinfo}\n')

        else:
                try:
                        response = os.system("ping -c 1 -t 1 " + re.search(pattern_ip,hostinfo[6]).group())
                except Exception:
                        responselist.append(f'PING ERROR {hostinfo}\n')

        
        try:
                if response == 0:
                        try:
                                print(f'{hostinfo[0]} {hostinfo[5]} {hostinfo[6]} is UP')
                                responselist.append(f'{hostinfo[0]} {hostinfo[5]} {hostinfo[6]} is UP\n')
                        except Exception:
                                responselist.append(f'PING ERROR {hostinfo}\n')
                else:
                        try:
                                print(f'{hostinfo[0]} {hostinfo[5]} {hostinfo[6]} is DOWN')
                                responselist.append(f'{hostinfo[0]} {hostinfo[5]} {hostinfo[6]} is DOWN\n')
                        except Exception:
                                responselist.append(f'PING ERROR {hostinfo}\n')

        except Exception:
                responselist.append(f'PING ERROR {hostinfo}\n')

        # with open(outfile, 'a') as file:
        #         for item in responselist:
        #                 for line in item:
        #                         file.write(line)



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
                device = ConnectHandler(device_type=platform, ip=host, username=username, password=passwd, secret=enablepasswd, timeout=30, global_delay_factor=0.4)
        except Exception:
                try:
                        device = ConnectHandler(device_type='cisco_ios', ip=host, username=username, password=passwd, secret=enablepasswd, timeout=30, global_delay_factor=0.4)
                except Exception:
                        with open(outfile, 'a') as file:
                                file.write(host + " is unavailable\n")
                        return None

        try:
                device.find_prompt()
        except Exception:
                with open(outfile, 'a') as file:
                        file.write(host + " is unavailable\n")

        if enablepasswd != 'gatherdefault':
                try:
                        device.enable()
                except Exception:
                     with open(outfile, 'a') as file:
                             file.write(host + " enable mode is not available\n")



        for item in atpbar((show_commands), name=host):
                try:
                        output = device.send_command(item)
                except:
                        continue
                output = output.split('\n')
                single_cmd_out = []

                if notag:
                        single_host_total.append('#' * len(item) +'\n')
                        single_host_total.append(f'{item}\n')
                        single_host_total.append('#' * len(item) + '\n')
                        for line in output:
                                single_host_total.append(f'{line}\n')

                elif date_time:
                        datetag = strftime("%Y-%m-%d-%H:%M")
                        for line in output:
                                single_cmd_out.append(f'{host} |{item}| {datetag}| {line}\n')
                        single_host_total.append(single_cmd_out)


                else:
                        for line in output:
                                single_cmd_out.append(f'{host} |{item}| {line}\n')
                        single_host_total.append(single_cmd_out)

        if notag:
                with open(host + '.txt', 'a')  as file:
                        for item in single_host_total:
                                for line in item:
                                        file.write(line)

        else:
                if (overwrite):
                        open(outfile, 'w').close()
                with open(outfile, 'a') as file:
                        for item in single_host_total:
                                for line in item:
                                        file.write(line)

        return True #Changed from host



def main():
        global platform
        global username
        global passwd
        global commandfile
        global singlecommand
        global targetfile
        global singletarget
        global outfile
        global show_commands
        global notag
        global enablepasswd
        global date_time
        global overwrite

        #platform = 'cisco_ios'
        # ARGPARSE CODE
        parser = argparse.ArgumentParser()
        parser.add_argument('-c', action='store', dest='commandfile',help='Enter Command File - One Per Line', default=False)
        parser.add_argument('-sc', action='store', dest='singlecommand',help='Enter A Single Command Enclosed in Quotes - Example "show version"', default=False)
        parser.add_argument('-o', action='store', dest='outfile',help='Enter Output Log File Name - If not specified default is GatherDB...',default=False)
        parser.add_argument('-u', action='store', dest='username',help='Username',default=False)
        parser.add_argument('-t', action='store', dest='targetfile',help='Host File - One Per Line',default=False)
        parser.add_argument('-st', action='store', dest='singletarget',help='Enter One Target Host Only',default=False)
        parser.add_argument('-p', action='store', dest='passwd',help='Enter Password',default=False)
        parser.add_argument('-mt', action='store', dest='maxthread', type=int, help='Number of simultateous threads - maximum value is 30',default=30)
        parser.add_argument('-en', action='store', dest='enable',help='Please enter the enable password only if you explicity wish to be in enable mode',default='gatherdefault')
        parser.add_argument('-notag', action='store_true', dest='notag',help='NO TAG places untagged output into seperate files',default=False)
        parser.add_argument('-pc', action='store', dest='pingcheck',help='YOU MUST ENTER THE NAME OF A GatherDB containing the output of the "show ip interface brief" command. This option searches the GatherDB and compiles all Layer 3 Interfaces present in the "show ip interface brief" command. If you use the same filename specified in the -o option, a GatherDB will be generated with the specifiied filename and then the same file will be used for the ping check. You can also use this option alone to ping check an existing GatherDB.',default='pingchecknull')
        parser.add_argument('-datetime', action='store_true', dest='date_time',help='Date Time adds the date and time to the output tags',default=False)
        parser.add_argument('-os', action='store', dest='platform',help='Enter OS Type - Default value is cisco_ios - Other available platform values are. [SSH OPTIONS] a10, accedian, adtran_os, alcatel_aos, alcatel_sros, allied_telesis_awplus, apresia_aeos, arista_eos, aruba_os, aruba_osswitch, aruba_procurve, avaya_ers, avaya_vsp, broadcom_icos, brocade_fastiron, brocade_fos, brocade_netiron, brocade_nos, brocade_vdx, brocade_vyos, calix_b6, cdot_cros, centec_os, checkpoint_gaia, ciena_saos, cisco_asa, cisco_ftd, cisco_ios, cisco_nxos, cisco_s300, cisco_tp, cisco_viptela, cisco_wlc, cisco_xe, cisco_xr, cloudgenix_ion, coriant, dell_dnos9, dell_force10, dell_isilon, dell_os10, dell_os6, dell_os9, dell_powerconnect, dell_sonic, dlink_ds, eltex, eltex_esr, endace, enterasys, ericsson_ipos, extreme, extreme_ers, extreme_exos, extreme_netiron, extreme_nos, extreme_slx, extreme_tierra, extreme_vdx, extreme_vsp, extreme_wing, f5_linux, f5_ltm, f5_tmsh, flexvnf, fortinet, generic, generic_termserver, hp_comware, hp_procurve, huawei, huawei_olt, huawei_smartax, huawei_vrpv8, ipinfusion_ocnos, juniper, juniper_junos, juniper_screenos, keymile, keymile_nos, linux, mellanox, mellanox_mlnxos, mikrotik_routeros, mikrotik_switchos, mrv_lx, mrv_optiswitch, netapp_cdot, netgear_prosafe, netscaler, nokia_sros, oneaccess_oneos, ovs_linux, paloalto_panos, pluribus, quanta_mesh, rad_etx, raisecom_roap, ruckus_fastiron, ruijie_os, sixwind_os, sophos_sfos, supermicro_smis, tplink_jetstream, ubiquiti_edge, ubiquiti_edgerouter, ubiquiti_edgeswitch, ubiquiti_unifiswitch, vyatta_vyos, vyos, watchguard_fireware, yamaha, zte_zxros, zyxel_os, [TELNET OPTIONS] adtran_os_telnet, apresia_aeos_telnet, arista_eos_telnet, aruba_procurve_telnet, brocade_fastiron_telnet, brocade_netiron_telnet, calix_b6_telnet, centec_os_telnet, ciena_saos_telnet, cisco_ios_telnet, cisco_xr_telnet, cisco_s300_telnet, dell_dnos6_telnet, dell_powerconnect_telnet, dlink_ds_telnet, extreme_telnet, extreme_exos_telnet, extreme_netiron_telnet, generic_telnet, generic_termserver_telnet, hp_procurve_telnet, hp_comware_telnet, huawei_telnet, huawei_olt_telnet, ipinfusion_ocnos_telnet, juniper_junos_telnet, nokia_sros_telnet, oneaccess_oneos_telnet, paloalto_panos_telnet, rad_etx_telnet, raisecom_telnet, ruckus_fastiron_telnet, ruijie_os_telnet, supermicro_smis_telnet, tplink_jetstream_telnet, yamaha_telnet, zte_zxros_telnet',default='cisco_ios')
        parser.add_argument('-w', action='store_true', dest='overwrite',help='Overwrite exsiting non-tagged Database outfile. ',default=False)
        
        results = parser.parse_args()
        username = results.username
        commandfile = results.commandfile
        singlecommand = results.singlecommand
        targetfile = results.targetfile
        singletarget = results.singletarget
        outfile = results.outfile
        passwd = results.passwd
        enablepasswd = results.enable
        maxthread = results.maxthread
        notag = results.notag
        platform = results.platform
        pingcheck = results.pingcheck
        date_time = results.date_time
        overwrite = results.overwrite
        

        # END ARGPARSE CODE

        if ((username or passwd or commandfile or singlecommand or targetfile or singletarget) and (pingcheck != 'pingchecknull')):
                if (not username):
                        username = input('Username? ')
                if (not passwd): 
                        passwd = getpass.getpass()
                if ((not commandfile) and (not singlecommand)):
                        commandfile = input('command file? ')
                if ((not targetfile) and (not singletarget)):
                        targetfile = input('target file? ')


        if ((not username) and (pingcheck == 'pingchecknull')):
                username = input('Username? ')

        if ((not passwd) and (pingcheck == 'pingchecknull')): 
                passwd = getpass.getpass()

        if ((not commandfile) and (not singlecommand) and (pingcheck == 'pingchecknull')):
                commandfile = input('command file? ')

        if ((not targetfile) and (not singletarget) and (pingcheck == 'pingchecknull')):
                targetfile = input('target file? ')

        if not outfile:
                outfile = 'GatherDB_' + strftime("%Y%m%d-%H%M%S") + '.txt'

        # if pingcheck == 'pingchecknull':        
        #         if singletarget:
        #                 hostlist = singletarget.split(" ")
        #         else:
        #                 hostlist = openfile(targetfile)

        if singletarget:
                hostlist = singletarget.split(" ")
        elif targetfile:
                hostlist = openfile(targetfile)
        else:
                pass


        # if pingcheck == 'pingchecknull':
        #         if singlecommand:
        #                 show_commands = singlecommand.split('\n')
        #         else:
        #                 show_commands = openfile(commandfile)

        if singlecommand:
                show_commands = singlecommand.split('\n')
        elif commandfile:
                show_commands = openfile(commandfile)
        else:
                pass


        if maxthread:
                if maxthread > 30:
                        maxthread = 30

        #if pingcheck:
        #        if pingcheck == 'pingchecknull':
        #                pingcheck = input('Enter Name of GatherDB containing "show ip interface brief" command: ')
                

        hostvar = True
        pool = Pool(maxthread)
        try:
                hostlist and show_commands
        except Exception:
                hostvar = False
        if hostvar:
                start = time()
                start = time()
                pool.map(rantgather, hostlist)
                end = time()
                print("GatherDB Creation Complete")
                print('Elapsed time:', end - start)
                print(f'Output File {outfile} if -notag flag enabled {outfile} file contains unavailable devices')
        # if pingcheck == 'pingchecknull':
        #         start = time()
        #         pool.map(rantgather, hostlist)
        #         end = time()
        #         print("GatherDB Creation Complete")
        #         print('Elapsed time:', end - start)
        #         print(f'Output File {outfile} if -notag flag enabled {outfile} file contains unavailable devices')
        if pingcheck != "pingchecknull":
                gatherdbOUT = simpleopen(pingcheck)
                to_pinglist = pinglist(gatherdbOUT)
                pool = Pool(20)
                pool.map(func_pingcheck,to_pinglist)
                # for item in to_pinglist:
                #         func_pingcheck(item)
                #         print("Gather PingDB Creation Complete")
                #print('Elapsed time:', end - start)
                with open(outfile, 'a') as file:
                        for item in responselist:
                                for line in item:
                                        file.write(line)

                print(f'Output File {outfile}')


                

if __name__ == '__main__':
        main()
