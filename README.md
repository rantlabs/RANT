# RANT - Really Awesome New Tools

GatherDB - The Ultimate Source of Truth. Gather everything you ever wanted to know about your IT infrastructure in one simple searchable file.
Gather is a tool that creates a comprehensive Source of Truth (SOT) for your IT infrastructure. The GatherDB contains an unlimited amount of configuration
management data as well as configuration state data. 

One of the prime features of Gather is its speed. Gather allows you to get a deep understanding of the configuration and state of an infrastructure in 
a few minutes. In addition, Gather allows you to run ad hoc commands such as "show running-config" on a large campus environment in a few seconds.

Another 

GATHER
* Three files are required. A target file, a command file, and an output file (does not need to exist before running script).
* The target file is a list of network devices. One device per line.
* The command file is a list of SHOW commands you want to issue to each one of the the devices in the target file. One command per line.
* The output file is a file that you want to output the text DB to. This is file does not need to exist prior to running the script.


Gather logs in via SSH and issues the commands placed in the command file. Additionally, Gather tags the output flowing to output file with the target name as well as the command issued. I suggest placing every device in your data center in the target file.

### [HOWTO and DEMONSTRATION VIDEOS](https://github.com/rantlabs/RANT/blob/main/DEMO_VIDEOS.md)

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
* Gather all the serial numbers of every device and module.
* Sort and count things, such as compile and count the number and type of wireless access points installed
* Drill down searches to level of specificity required. Example: Once all types of wireless access points are discovered list all the instances and locations of a particular type of AP.
* During an outage, you can query and trouble shoot the device as if it was still operating.
* Run a complete configuration backup on all of your campus devices in a few seconds.
* Find all unused ports on all tors
* Verify the consistent mlag configs on all devices
* Display all VLANS defined on all TORS and Spines.
* Display all unique version of code running and then identify devices that are not running the standard
