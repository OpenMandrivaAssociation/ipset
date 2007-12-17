%define name ipset
%define version 2.2.9a
%define cvsdate 20061009
%define release %mkrel 1

Summary: Tools for managing sets of IP or ports with iptables
Name: %{name}
Version: %{version}
Release: %{release}
Source0: http://ipset.netfilter.org/%{name}-%{version}-%{cvsdate}.tar.bz2
Source1: %{name}-kernel-headers.tar.bz2

License: GPL
Group: System/Kernel and hardware
Url: http://ipset.netfilter.org/

%description
IP sets are a framework inside the Linux 2.4.x and 2.6.x kernel,
which can be administered by the ipset utility.
Depending on the type, currently an IP set may store IP addresses,
(TCP/UDP) port numbers or IP addresses with MAC addresses in a way,
which ensures lightning speed when matching an entry against a set.

ipset may be the proper tool for you, if you want to
 * store multiple IP addresses or port numbers and match against the
   collection by iptables at one swoop;
 * dynamically update iptables rules against IP addresses or ports
   without performance penalty;
 * express complex IP address and ports based rulesets with one single
   iptables rule and benefit from the speed of IP sets 

%prep
%setup -q -a 1

%build
make all KERNEL_DIR=$PWD/linux-2.6 PREFIX=/usr LIBDIR=%{_libdir}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std PREFIX=/usr MANDIR=%{_mandir} LIBDIR=%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc ChangeLog ChangeLog.ippool
%defattr(-,root,root,0755)
%{_sbindir}/*
%{_libdir}/%{name}/*
%{_mandir}/man8/*.8*
