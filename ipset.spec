%define major 3
%define libname %mklibname ipset %{major}
%define devname %mklibname ipset -d

%define _disable_rebuild_configure 1

Summary:	Tools for managing sets of IP or ports with iptables
Name:		ipset
Version:	6.29
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://ipset.netfilter.org/
Source0:	http://ipset.netfilter.org/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(libmnl)
BuildRequires:	kernel-release-devel

%track
prog %name = {
	url = http://ipset.netfilter.org/install.html
	regex = %name-(__VER__)\.tar\.bz2
	version = %version
}

%description
IP sets are a framework inside the Linux 2.4.x and 2.6.x kernel, which can be
administered by the ipset utility. Depending on the type, currently an IP set
may store IP addresses, (TCP/UDP) port numbers or IP addresses with MAC
addresses in a way, which ensures lightning speed when matching an entry
against a set.

ipset may be the proper tool for you, if you want to

 o store multiple IP addresses or port numbers and match against the collection
   by iptables at one swoop;

 o dynamically update iptables rules against IP addresses or ports without
   performance penalty;

 o express complex IP address and ports based rulesets with one single iptables
   rule and benefit from the speed of IP sets 

%package -n	%{libname}
Summary:	Shared library for managing sets of IP or ports with iptables
Group:		System/Libraries

%description -n	%{libname}
IP sets are a framework inside the Linux 2.4.x and 2.6.x kernel, which can be
administered by the ipset utility. Depending on the type, currently an IP set
may store IP addresses, (TCP/UDP) port numbers or IP addresses with MAC
addresses in a way, which ensures lightning speed when matching an entry
against a set.

This package provides the shared library for managing sets of IP or ports with
iptables.

%package -n	%{devname}
Summary:	Headers and static lib for ipset development
Group:		Development/C
%rename		ipset-devel

%description -n	%{devname}
IP sets are a framework inside the Linux 2.4.x and 2.6.x kernel, which can be
administered by the ipset utility. Depending on the type, currently an IP set
may store IP addresses, (TCP/UDP) port numbers or IP addresses with MAC
addresses in a way, which ensures lightning speed when matching an entry
against a set.

Install this package if you want do compile applications using the ipset
library.

%prep
%setup -q

%build
KERNEL=`ls -1d --sort=time %{_usrsrc}/linux-*-*-* |head -n1`
%configure \
    --with-kbuild=$KERNEL \
    --disable-static \
    --enable-shared \
    --disable-ltdl-install \
    --enable-settype-modules \
    --with-kmod=yes

%make

%install
%makeinstall_std

install -d %{buildroot}%{_libdir}/ipset

%files
%doc ChangeLog ChangeLog.ippool
%{_sbindir}/ipset
%{_mandir}/man8/ipset.8*

%files -n %{libname}
%dir %{_libdir}/ipset
%{_libdir}/libipset.so.%{major}*

%files -n %{devname}
%dir %{_includedir}/libipset
%{_includedir}/libipset/*
%{_libdir}/libipset.so
%{_libdir}/pkgconfig/libipset.pc
