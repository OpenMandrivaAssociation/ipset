%define major 2
%define libname %mklibname ipset %{major}
%define develname %mklibname ipset -d

%ifarch %{arm}
%define kflavour kirkwood
%else
%define kflavour desktop
%endif

Summary:	Tools for managing sets of IP or ports with iptables
Name:		ipset
Version:	6.12.1
Release:	1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://ipset.netfilter.org/
Source0:	http://ipset.netfilter.org/%{name}-%{version}.tar.bz2
BuildRequires:	mnl-devel
BuildRequires:	autoconf automake libtool
BuildRequires:	libtool-devel
BuildRequires:	kernel-%{kflavour}-devel > 3.1.5

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

%package -n	%{develname}
Summary:	Headers and static lib for ipset development
Group:		Development/C
Obsoletes:	ipset-devel
Provides:	ipset-devel = %{version}-%{release}

%description -n	%{develname}
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
rm -rf autom4te.cache
aclocal -I m4
autoreconf -fi
KPKG=kernel-%{kflavour}-devel
KDIR=$(rpm -ql $KPKG | grep '/usr/src/devel/[^/]*$')
%configure2_5x \
    --with-kbuild=$KDIR \
    --disable-static \
    --enable-shared \
    --disable-ltdl-install \
    --enable-settype-modules

%make

%install
rm -rf %{buildroot}

%makeinstall_std

rm -f %{buildroot}%{_libdir}/*.la

%files
%doc ChangeLog ChangeLog.ippool
%{_sbindir}/*
%{_mandir}/man8/*.8*

%files -n %{libname}
%dir %{_libdir}/ipset
%{_libdir}/lib*.so.%{major}*

%files -n %{develname}
%dir %{_includedir}/libipset
%{_includedir}/libipset/*
%{_libdir}/*.so
