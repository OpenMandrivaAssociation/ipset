# (tmb) temp linking fix
%define _disable_ld_as_needed 1
%define _disable_ld_no_undefined 1

# (tmb) hack to get it to build against correct kernel config (not running one)
%define kflavour desktop
%define kver	2.6.38.4
%define krel	1mnb2

Summary:	Tools for managing sets of IP or ports with iptables
Name:		ipset
Version:	6.4
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Kernel and hardware
Url:		http://ipset.netfilter.org/
Source0:	http://ipset.netfilter.org/%{name}-%{version}.tar.bz2
Requires:	libmnl
BuildRequires:	mnl-devel
BuildRequires:	kernel-%{kflavour}-devel-%{kver}-%{krel}

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

%prep
%setup -q

%build
aclocal -I m4
autoreconf -fi
%configure2_5x --with-kbuild=/usr/src/linux-%{kver}-%{kflavour}-%{krel}
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc ChangeLog ChangeLog.ippool
%{_sbindir}/*
%{_libdir}/*
%{_mandir}/man8/*.8*
