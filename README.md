# OSCP-TunnelMonitor

Have you had trouble with ligolo dropping your tunnel?  Has it cost you precious minutes on your OSCP?  ME TOO!!
I wrote this script to monitor my connection to a remote system in the background and use the gnome builtin notification system to alert me when it drops.

I hope this helps you like it helped me.

Monitor based on ICMP
python ./tunnelcheck.py 172.16.100.200

Monitor based on open tcp port 139
python ./tunnelcheck.py 172.16.100.200 139
