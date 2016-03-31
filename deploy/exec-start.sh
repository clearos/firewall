#!/bin/sh

source /usr/libexec/firewall/functions.sh

firewall_start /usr/sbin/iptables
firewall_start /usr/sbin/ip6tables

# vi: expandtab shiftwidth=4 softtabstop=4 tabstop=4
