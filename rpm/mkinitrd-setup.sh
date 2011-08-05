#!/bin/bash
#
#%stage: device
#%depends: fcoe
#

#
# Check if DCBX is active for FCoE traffic
#
dcbd_check_dcb() {
    local if=$1

    dcbtool gc $if dcb 2> /dev/null | sed -n 's/DCB State:\s*\(.*\)/\1/p'
}

dcbd_check_app_fcoe() {
    local if=$1

    dcbtool gc $if app:fcoe 2> /dev/null | sed -n 's/Enable:\s*\(.*\)/\1/p'
}

if [ "${root_fcoe}" ] ; then
    dcb_status=$(dcbd_check_app_fcoe $fcoe_if)
    if [ "$dcb_status" = "true" ] ; then
        root_dcbd=1
    fi
    fcoe_status=$(dcbd_check_app_fcoe $fcoe_if)
    if [ "$fcoe_status" = "true" ] ; then
	root_app_fcoe=1
    fi
fi

save_var root_dcbd
save_var root_app_fcoe
if [ "${root_dcbd}" ] ; then
    mkdir -p ${tmp_mnt}/var/lib/lldpad
    if [ -f /var/lib/lldpad/lldpad.conf ] ; then
        # copy lldpad configuration
	cp -p /var/lib/lldpad/lldpad.conf ${tmp_mnt}/var/lib/lldpad
    fi
fi
