#!/bin/sh

# Modify /etc/network/interfaces file for VM3
echo "source /etc/network/interfaces.d/*
auto lo eth0
iface lo inet loopback
iface eth0 inet static
        address 192.168.2.4
        netmask 255.255.255.0
        gateway 192.168.2.254" | sudo tee /etc/network/interfaces > /dev/null

# Display success message
echo "VM4 configuration updated successfully!"

