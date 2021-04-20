# GATHER DEMO VIDEOS RANT - Really Awesome New Tools

### Introduction

Gather is a simple tool to that gathers a large amount of searchable information from your IT infrastructure. Gather requires a list of your infrastructure
devices and a list of commands you want to issue to the devices to extract data.

[![Inroduction Video One](https://github.com/rantlabs/RANT/blob/main/IMAGES/Intro_Part_One.png)](https://youtu.be/lZmfDHwVsKo)

[![Inroduction Video Two](https://github.com/rantlabs/RANT/blob/main/IMAGES/Intro_Part_Two.png)](https://youtu.be/0Xc2h0t-1HU)

### Command File Example

The command file is a text file consisting of commands you want to issue on your infrastructure devices.

[![Command File](https://github.com/rantlabs/RANT/blob/main/IMAGES/ShowCommands_Three.png)](https://youtu.be/JSP8Ef6HdXM)

### Target File Example

The target file consists of a list of devices that Gather will ssh to and issue the commands specified in the...command file ;)

[![Target File](https://github.com/rantlabs/RANT/blob/main/IMAGES/TargetFile_Four.png)](https://youtu.be/-JytrAvQgmM)

### Gathering Data - Running Gather

Gathering data is as simple as following the prompts

[![Gathering Data](https://github.com/rantlabs/RANT/blob/main/IMAGES/Gather_Data_Five.png)](https://youtu.be/sfBNBznNknU)

### A Closer Look at the Output File - Tagging Data is the Secret Sauce

The output file is a simply the output of the commands issued on each device. Gather's secret sauce is how the data is tagged.
Each line of the output is tagged with the device name and the command name. The tags added to the command enable the output information to be searched and 
consolidated in an infinite amount of combinations.

[![Output File Details](https://github.com/rantlabs/RANT/blob/main/IMAGES/OutputFile_Six.png)](https://youtu.be/kkuWTvwc_TM)

### Search Example: Searching for Image Versions

In this example, we will search for the type and number of each type of OS image in your infrastructure. The unix search we use in this example is:

grep "show version" output.txt | grep "Software image version" | awk '{print $NF}' | uniq -c

[![Show Version Search](https://github.com/rantlabs/RANT/blob/main/IMAGES/ShowVersion_Seven.png)](https://youtu.be/QDratnd8-ok)

### Search Example: Searching Your Network for Physical Layer Errors

In this example, we will search for physical layer errors across the entire network infrastructure. The unix search we use in this example is:

grep "show interface counters error" output.txt | grep -v "0        0        0        0        0        0        0"

[![Physical Layer Error Search](https://github.com/rantlabs/RANT/blob/main/IMAGES/L2Error_Check_Eight.png)](https://youtu.be/P5jdh5_YVkk)

### Search Example: Audit Local Usernames Configured on Netwrok Devices

In this example we search the running configuration of every network device to audit the local usernames. The unix search we use in this example is:

grep "show running" output.txt | grep -i user

[![Local Username Audit](https://github.com/rantlabs/RANT/blob/main/IMAGES/LocalAccountAudit_Nine.png)](https://youtu.be/cnhE56RA40k)


