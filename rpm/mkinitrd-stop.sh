#!/bin/bash
#
#%stage: setup
#%provides: killprogs
#
#%if: "$root_dcbd" -a "$root_fcoe"
#%dontshow
#
##### kill fcoe
##
## Because we will run and use the dcbd daemon from the new root
## the old one has to be killed. During that time no DCB
## exceptions should occur!
##
## Command line parameters
## -----------------------
##

# kill dcbd, will be restarted from the real root
lldpad_pid=$(pidof lldpad)
[ "$lldpad_pid" ] && kill -TERM $lldpad_pid
