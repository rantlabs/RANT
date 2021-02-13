# Some sample queries
Once you have an output file, open it up in your favorite editor or display it using unix more to take a look at your output. You will quickly get
an idea of what you may want to search.

### Display the number of connected interfaces on all of your devices

*grep "show interface status" outputfile.txt | grep connected | awk '{print $1}' | uniq -c | sort -rn*

Explanation: search for the text "show interface status" in the output file, then pipe to a search for the word connected to extract only the connected
interfaces; then use awk to print only the first column (tagged device name); print only each unique device name BUT count the number of times it appeared ; 
then sort that resulting list to present the numbers in decending order.....

Sounds like a mouth full! But it's very easy. If that seemed too difficult, you can just start with the first part of the query and it will still be useful.

*grep "show interface status" outputfile.txt*

### Record every serial number in your network 

*grep "show inventory" outputfile.txt | grep PID | awk '{print $NF}'*

Explanation: Search the text "show inventory" in the output file, then focus your search on the PID key word, then print only the last field, which 
is the serial number. You can then simply upload this output into your vendors support tool (Cisco has one) to list the support status of your entire network.

### Search for anything specific

*grep "show running" outputfile.txt | grep -i password* 

In one query you can audit every running config on your network no matter how enormous your company is and quickly find all the little surprises in 
your local usernames. 

### Audit and verify all of config registers are correctly set

*grep "show version" outputfile.txt | grep -i "Configuration register"*

###  Count how many phones are connected to your network

*grep "show cdp" outputfile.txt | grep SEP | grep -v detail | wc -l*

I removed any line from containing detail because I wanted to remove the output of the the show cdp neighbor detail command.

### Display every wireless AP on campus

*grep "show cdp neighbor detail" outputfile.txt | grep -i platform | grep -i air*

#### Its very easy after you do a couple of searches to realize the potential of having all of your permanent and semi permanent network information in one easily searchable file.
