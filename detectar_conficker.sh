#!/usr/bin/bash

# Detectar conficker via nmap
nmap -PN -T4 -p139,445 -n -v --script smb-check-vulns,smb-os-discovery --script-args=unsafe=1 192.168.0.0/21 > nmap_conficker.txt
