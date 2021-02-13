# RANT - Really Awesome New Tool(s)
SHOW COMMANDS ONLY

GATHER
* Three files are required. A target file, a command file, and an output file (does not need to exist before running script).
* The target file is a list of network devices. One device per line.
* The command file is a list of SHOW commands you want to issue to each one of the the devices in the target file. One command per line.
* The output file is a file that you want to output the text DB to. This is file does not need to exist prior to running the script.


Gather logs in via SSH and issues the commands placed in the command file. Additionally, Gather tags the output flowing to output file with the target name as well as the command issued. I suggest placing every device in your data center in the target file.


# Suggested Command File:
**SEE: [commands.txt](https://github.com/rantlabs/RANT/blob/main/commands.txt)**
* show version
* show running-config
* show running-config section bgp
* show interface status
* show vlan
* show ip int brief
* show running-config section ospf
* show lldp neighbor
* Any other command that is relevant to your specific equipment

* A commands.txt sample file is included in this repo.

# Capabilities

Gather tags every line of the output with the name of device and the name of the command, every line is searchable. Unix text search and 
manipulation tools such as: AWK, SED, GREP (-v, -i), uniq, uniq -c, wc -l (count number of lines), allow you to easily search your entire infrastructure
at once for permanent and semi permanent data. 

**SEE: [SAMPLE_QUERIES.md](https://github.com/rantlabs/RANT/blob/main/SAMPLE_QUERIES.md) file for examples**

# You can do things like:
* Most of these can be done in one simple query
* Gather all the serial numbers of every device and module.
* Find all unused ports on all tors
* Verify the consistent mlag configs on all devices
* Display all VLANS defined on all TORS and Spines.
* Display all unique version of code running and then identify devices that are not running the standard
* Sort and count number of instances and also drill to create more specific searches.
