#!/bin/sh

# CLEAN CURRENT CONFIG
iptables -F          # Flush all rules in the filter table
iptables -t nat -F   # Flush all rules in the nat table
# REROUTING HTTP CONNECTIONS ON PORT 80 TO VM3
iptables -t nat -A PREROUTING -p tcp --dport 5000 -j DNAT --to-destination 192.168.1.1:5000
iptables -t nat -A POSTROUTING -p tcp -d 192.168.1.1 --dport 5000 -j SNAT --to-source 192.168.0.10
iptables -A FORWARD -p tcp -d 192.168.1.1 --dport 5000 -j ACCEPT
# REROUTING SSH CONNECTIONS ON PORT 22 TO VM4
iptables -t nat -A PREROUTING -p tcp -s 192.168.1.1 --dport 22 -j DNAT --to-destination 192.168.2.4:22
iptables -t nat -A POSTROUTING -p tcp -d 192.168.2.4 --dport 22 -j SNAT --to-source 192.168.1.254
iptables -A FORWARD -p tcp -s 192.168.1.1 -d 192.168.2.4 --dport 22 -j ACCEPT
# ALLOW ESTABLISHED AND RELATED CONNECTIONS 
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
# REJECT ALL OTHER TRAFFIC
iptables -P FORWARD DROP
