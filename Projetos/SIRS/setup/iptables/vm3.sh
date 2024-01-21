#!/bin/sh

# CLEAN CONFIG
iptables -F 
# DROP ALL OTHER INCOMING CONNECTIONS
iptables -P INPUT DROP
# ALLOW INCOMING HTTP CONNECTIONS FROM BOTH INTERNAL AND EXTERNAL NETWORKS
iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
# ALLOW INCOMING SSH CONNECTIONS FROM THE INTERNAL NETWORK
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --sport 22 -j ACCEPT

