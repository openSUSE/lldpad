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
Version:        0.9.43
Release:        0.5
License:        GPL v2 only
Group:          System/Daemons
BuildRequires:  bison flex libnl-devel pkgconfig
AutoReqProv:    On
Url:            http://www.open-lldp.org 
Source:         http://www.open-lldp.org/open-lldp/downloads/%{name}-0.9.43.tar.bz2
Patch0:         %{name}-%{version}-sles11-sp2.diff.bz2
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
%setup -q -n %{name}-%{version}
%patch0 -p1

%build
touch NEWS
touch libconfig-1.3.2/NEWS
autoreconf --install
%configure --disable-cxx --bindir=/bin --sbindir=/sbin
make %{?_smp_mflags}

%install
mkdir -p ${RPM_BUILD_ROOT}/var/lib/lldpad
%makeinstall
install -d ${RPM_BUILD_ROOT}/lib/mkinitrd/scripts/
install -m 755 rpm/mkinitrd-boot.sh ${RPM_BUILD_ROOT}/lib/mkinitrd/scripts/boot-lldpad.sh
install -m 755 rpm/mkinitrd-stop.sh ${RPM_BUILD_ROOT}/lib/mkinitrd/scripts/boot-killlldpad.sh
install -m 755 rpm/mkinitrd-setup.sh ${RPM_BUILD_ROOT}/lib/mkinitrd/scripts/setup-lldpad.sh
mkdir -p ${RPM_BUILD_ROOT}/usr/sbin
ln -s /etc/init.d/boot.lldpad ${RPM_BUILD_ROOT}/usr/sbin/rclldpad

%post
[ -x /sbin/mkinitrd_setup ] && mkinitrd_setup
%{fillup_and_insserv -n -i boot.lldpad}

%preun
%{stop_on_removal boot.lldpad}

%postun
[ -x /sbin/mkinitrd_setup ] && mkinitrd_setup
%{insserv_cleanup boot.lldpad}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc COPYING
%doc README
%doc ChangeLog
%dir /var/lib/lldpad
/sbin/*
/etc/init.d/boot.lldpad
%{_mandir}/man8/*
/lib/mkinitrd
/usr/sbin/rclldpad

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/pkgconfig/*.pc

%changelog
