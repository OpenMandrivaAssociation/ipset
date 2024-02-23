%define major 13
%define oldlibname %mklibname ipset 13
%define libname %mklibname ipset
%define devname %mklibname ipset -d

%define _disable_rebuild_configure 1

# (tpg) optimize it a bit
%global optflags %{optflags} -Oz
%global build_ldflags %{build_ldflags} -Wl,--undefined-version

Summary:	Tools for managing sets of IP or ports with iptables
Name:		ipset
Version:	7.21
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://ipset.netfilter.org/
Source0:	http://ipset.netfilter.org/%{name}-%{version}.tar.bz2
BuildRequires:	pkgconfig(libmnl)

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

%package -n %{libname}
Summary:	Shared library for managing sets of IP or ports with iptables
Group:		System/Libraries
%rename %{oldlibname}

%description -n %{libname}
IP sets are a framework inside the Linux 2.4.x and 2.6.x kernel, which can be
administered by the ipset utility. Depending on the type, currently an IP set
may store IP addresses, (TCP/UDP) port numbers or IP addresses with MAC
addresses in a way, which ensures lightning speed when matching an entry
against a set.

This package provides the shared library for managing sets of IP or ports with
iptables.

%package -n %{devname}
Summary:	Headers and static lib for ipset development
Group:		Development/C
%rename		ipset-devel

%description -n %{devname}
IP sets are a framework inside the Linux 2.4.x and 2.6.x kernel, which can be
administered by the ipset utility. Depending on the type, currently an IP set
may store IP addresses, (TCP/UDP) port numbers or IP addresses with MAC
addresses in a way, which ensures lightning speed when matching an entry
against a set.

Install this package if you want do compile applications using the ipset
library.

%prep
%autosetup -p1

%build
%configure \
    --enable-static=no \
    --enable-shared \
    --with-kmod=no

# Just to make absolutely sure we are not building the bundled kernel module
# I have to do it after the configure run unfortunately
rm -fr kernel
 
# Prevent libtool from defining rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%make_build

%install
%make_install

install -d %{buildroot}%{_libdir}/ipset

%files
%doc ChangeLog ChangeLog.ippool
%{_sbindir}/ipset
%{_sbindir}/ipset-translate
%doc %{_mandir}/man8/ipset.8*
%doc %{_mandir}/man8/ipset-translate.8*

%files -n %{libname}
%dir %{_libdir}/ipset
%{_libdir}/libipset.so.%{major}*

%files -n %{devname}
%dir %{_includedir}/libipset
%{_includedir}/libipset/*
%{_libdir}/libipset.so
%{_libdir}/pkgconfig/libipset.pc
%doc %{_mandir}/man3/libipset.3*
