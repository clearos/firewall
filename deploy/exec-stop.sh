#!/bin/sh

source /usr/libexec/firewall/functions.sh

firewall_stop /usr/sbin/iptables
firewall_stop /usr/sbin/ip6tables

# vi: expandtab shiftwidth=4 softtabstop=4 tabstop=4
