#!/bin/sh

# CLEAN PREVIOUS CONFIG
iptables -F
# REFUSE CONNECTIONS BY DEFAULT
iptables -P INPUT DROP
# ALLOW INCOMING SSH CONNECTIONS
iptables -A INPUT -p tcp --dport 22 -j ACCEPT