Name: firewall
Summary: ClearOS Firewall Engine
Version: 1.4.21
Release: 1%{?dist}
Vendor: ClearFoundation
Source: firewall-%{version}.tar.gz
Group: System Environment/Base
URL: http://www.clearfoundation.com/
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
License: GPLv2
BuildRequires: libselinux-devel
BuildRequires: kernel-headers
BuildRequires: lua-devel
BuildRequires: iptables-devel = %{version}
BuildRequires: autoconf >= 2.63
BuildRequires: automake
BuildRequires: libtool
Conflicts: kernel < 2.4.20
Requires: iptables = %{version}

%description
The ClearOS Firewall Engine.  This is a customized version of iptables combined with the LUA interpreter.

%prep
%setup -q
./autogen.sh
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" \
./configure --bindir=/bin --sbindir=/sbin --sysconfdir=/etc --libdir=/%{_lib} --libexecdir=/%{_lib} --mandir=%{_mandir} --includedir=%{_includedir}

%build
# do not use rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make

%install
rm -rf %{buildroot}

make install DESTDIR=%{buildroot} 
mv %{buildroot}/sbin/firewall  %{buildroot}/sbin/app-firewall
mv %{buildroot}/sbin/firewall6  %{buildroot}/sbin/app-firewall6

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/sbin/app-firewall
/sbin/app-firewall6

%changelog

* Tue Mar 22 2016 Darryl Sokoloski <dsokoloski@clearfoundation.com> - v1.4.21-3
- Removed changelog, updating dynamically from Git. : Commit 0bf12d3

* Tue Mar 22 2016 Darryl Sokoloski <dsokoloski@clearfoundation.com> - v1.4.21-2
- Changed IPv6 firewall name to firewall6.  Clean-up. : Commit ae40406

* Tue Jul 07 2015 Shad L. Lords <slords@lordsfam.net> - list, tag
- Update .gitignore : Commit 31028fc
- Added spec to repo. : Commit ddbab2d
- Combined ipv4 and ipv6 in to the same package (as per latest iptables RPM). : Commit e43857a
- Removed auto-generated files.  Added autoconf/make/libtool to build requires. : Commit 29e1b31
- Fixed bogus changelog dates, bumped release. : Commit 01eae5a
- Added missing ip6tables-multi.h to EXTRA_DIST. : Commit c6367d7
- Updated to iptables 1.4.19.1 : Commit ac550a9
- Added a directory iterator for LUA. : Commit 505ca8f
- Unified exit from main() and retabbed sources.  Bumped release. : Commit 5614d3a
- Removed fatal return from if_exists() -- bad copy/paste. : Commit 5a98ace
- Switched from using inet_addr(3) to int inet_aton(3).  As /32 netmasks return -1 (INADDR_ANY) which is confusing. : Commit a1dfccc
