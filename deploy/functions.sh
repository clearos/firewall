#!/bin/sh

# TODO/KLUDGE: remove stray configs from anaconda installer.
# This should be moved somewhere else (anaconda patch, syswatch).
function anaconda_kludge
{
    for config in $(ls /etc/sysconfig/network-scripts/ifcfg-* 2>/dev/null); do
        NM_CONTROLLED=""
        ONBOOT=""
        source $CONFIG
        if [ "$NM_CONTROLLED" = "yes" -a "$ONBOOT" = "no" ]; then
            rm -f "$CONFIG"
        fi
    done
}

# Start firewall.
function firewall_start
{
    if [ ! -f "/etc/clearos/firewall.conf" ]; then
        echo "No firewall configuration found."
        return 1
    fi

    if [ "$(basename $1)" == "iptables" ]; then
        /usr/sbin/firewall-start >/dev/null 2>&1 || exit 1
    else
        /usr/sbin/firewall-start6 >/dev/null 2>&1 || exit 1
    fi

}

# Stop firewall, set default policies to ACCEPT.
function firewall_stop
{
    if [ "$(basename $1)" == "iptables" ]; then
        tables="$(cat /proc/net/ip_tables_names 2>/dev/null)"
    else
        tables="$(cat /proc/net/ip6_tables_names 2>/dev/null)"
    fi

    for table in ${tables}; do
        $1 -w -t ${table} -F || return 1
        $1 -w -t ${table} -X || return 1

        if [ "${table}" == "filter" ]; then
            $1 -w -t ${table} -P INPUT ACCEPT || return 1
            $1 -w -t ${table} -P OUTPUT ACCEPT || return 1
            $1 -w -t ${table} -P FORWARD ACCEPT || return 1
        elif [ "${table}" == "nat" ]; then
            $1 -w -t ${table} -P PREROUTING ACCEPT || return 1
            $1 -w -t ${table} -P POSTROUTING ACCEPT || return 1
            $1 -w -t ${table} -P OUTPUT ACCEPT || return 1
        elif [ "${table}" == "mangle" ]; then
            $1 -w -t ${table} -P PREROUTING ACCEPT  || return 1
            $1 -w -t ${table} -P OUTPUT ACCEPT || return 1
        fi
    done
}

# vi: expandtab shiftwidth=4 softtabstop=4 tabstop=4
