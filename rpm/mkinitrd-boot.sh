#!/bin/bash
#%stage: device
#%depends: network
#%programs: /sbin/lldpad /sbin/dcbtool
#%if: "$root_dcbd"
#
##### DCBD initialization
##
## This script initializes DCBD (Data Center Bridging Exchange protocol daemon)

/sbin/lldpad -d
# Check EDD info for FCoE interface
for edd in /sys/firmware/edd/int13_dev* ; do
    fc=$(sed -n '/FIBRE/p' ${edd}/interface 2> /dev/null)
    [ -z "$fc" ] && continue
    [ -d "${edd}/pci_dev/net" ] || continue
    edd_if=$(ls $edd/pci_dev/net)
    break
done
if [ -n "$edd_if" ] && [ "$edd_if" != "$interface" ] ; then
    echo "FCoE boot interface $edd_if not configured"
    ip link set $edd_if up
else
    edd_if=
fi
/sbin/dcbtool sc $interface dcb on
/sbin/dcbtool sc $interface app:fcoe e:1

fcoe_if=$interface
if [ -n "$edd_if" ] ; then
    /sbin/dcbtool sc $edd_if dcb on
    /sbin/dcbtool sc $edd_if app:fcoe e:1
fi
