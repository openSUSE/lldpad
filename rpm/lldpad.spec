#
# spec file for package lldpad
#
# Copyright (c) 2011 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#



Name:           lldpad
Summary:        Link Layer Discovery Protocol (LLDP) Agent
Version:        0.9.42.1107011030
Release:        0.5
License:        GPL v2 only
Group:          System/Daemons
BuildRequires:  bison flex libnl-devel pkgconfig
AutoReqProv:    On
Url:            http://www.intel.com/network/connectivity/products/server_adapters.htm
Source:         http://downloads.sourceforge.net/e1000/%{name}-0.9.42.tar.bz2
Source20:       mkinitrd-boot.sh
Source21:       mkinitrd-stop.sh
Source22:       mkinitrd-setup.sh
Patch0:         %{name}-0.9.42-git-update
Patch1:         %{name}-lldptool-fix-statistics-segfault
Patch2:         %{name}-Change-the-client-interface-to-use-an-abstract-names
Patch3:         %{name}-makefile-fixup
Patch4:         %{name}-init-script-fixup
#Patch5:         %{name}-0.9.32-compile-fixes
Patch6:         lldpad-include-builtin-libconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Provides:       dcbd
Obsoletes:      dcbd

%description
This package contains the Link Layer Discovery Protocol (LLDP) Agent
with Data Center Bridging (DCB) for Intel(R) Network Connections
'lldpad' plus the configuration tools 'dcbtool' and 'lldptool'.



Authors:
--------
    e1000-eedc Mailing List <e1000-eedc@lists.sourceforge.net>
    Intel Corporation, 5200 N.E. Elam Young Parkway, Hillsboro, OR 97124-6497

%package devel
License:        GPL v2 only
Summary:        Link Layer Discovery Protocol (LLDP) Agent
Group:          System/Daemons
Requires:       %{name} = %{version}

%description devel
This package contains the Link Layer Discovery Protocol (LLDP) Agent
with Data Center Bridging (DCB) for Intel(R) Network Connections
'lldpad' plus the configuration tools 'dcbtool' and 'lldptool'.



Authors:
--------
    e1000-eedc Mailing List <e1000-eedc@lists.sourceforge.net>
    Intel Corporation, 5200 N.E. Elam Young Parkway, Hillsboro, OR 97124-6497

%prep
%setup -q -n lldpad-0.9.42
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
#%patch5 -p1
%patch6 -p1

%build
autoreconf --install
%configure --disable-cxx --bindir=/bin --sbindir=/sbin
make %{?_smp_mflags}

%install
mkdir -p ${RPM_BUILD_ROOT}/var/lib/lldpad
%makeinstall
install -d ${RPM_BUILD_ROOT}/lib/mkinitrd/scripts/
install -m 755 %{S:20} ${RPM_BUILD_ROOT}/lib/mkinitrd/scripts/boot-lldpad.sh
install -m 755 %{S:21} ${RPM_BUILD_ROOT}/lib/mkinitrd/scripts/boot-killlldpad.sh
install -m 755 %{S:22} ${RPM_BUILD_ROOT}/lib/mkinitrd/scripts/setup-lldpad.sh
mkdir -p ${RPM_BUILD_ROOT}/usr/sbin
ln -s /etc/init.d/lldpad ${RPM_BUILD_ROOT}/usr/sbin/rclldpad

%post
[ -x /sbin/mkinitrd_setup ] && mkinitrd_setup
%{fillup_and_insserv -n -i lldpad}

%preun
%{stop_on_removal lldpad}

%postun
[ -x /sbin/mkinitrd_setup ] && mkinitrd_setup
%{insserv_cleanup lldpad}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%doc README
%doc ChangeLog
%dir /var/lib/lldpad
/sbin/*
/etc/init.d/lldpad
%{_mandir}/man8/*
/lib/mkinitrd
/usr/sbin/rclldpad

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%changelog
