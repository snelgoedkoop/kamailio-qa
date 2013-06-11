%define name    kazoo-kamailio
%define ver     4.0.0
%define rel     0%{dist}



Summary:       Kamailio (former OpenSER) - the Open Source SIP Server
Name:          %name
Version:       %ver
Release:       %rel
Packager:      Peter Dunkley <peter@dunkley.me.uk>
License:       GPL
Group:         System Environment/Daemons
Source:        http://kamailio.org/pub/kamailio/%{ver}/src/%{name}-%{ver}_src.tar.gz
URL:           http://kamailio.org/
Vendor:        kamailio.org
BuildRoot:     %{_tmppath}/%{name}-%{ver}-buildroot
Conflicts:     kamailio-mysql < %ver, kamailio-postgresql < %ver
Conflicts:     kamailio-unixODBC < %ver, kamailio-bdb < %ver
Conflicts:     kamailio-sqlite < %ver, kamailio-utils < %ver
Conflicts:     kamailio-cpl < %ver, kamailio-snmpstats < %ver
Conflicts:     kamailio-presence < %ver, kamailio-xmpp < %ver
Conflicts:     kamailio-purple < %ver, kamailio-ldap < %ver
Conflicts:     kamailio-xmlrpc < %ver, kamailio-perl < %ver, kamailio-lua < %ver
Conflicts:     kamailio-python < %ver, kamailio-regex < %ver
Conflicts:     kamailio-dialplan < %ver, kamailio-lcr < %ver
Conflicts:     kamailio-xmlops < %ver, kamailio-cdp < %ver
Conflicts:     kamailio-websocket < %ver, kamailio-xhttp-pi < %ver
Conflicts:     kamailio-outbound < %ver, kamailio-ims < %ver
Conflicts:     kamailio-auth-identity < %ver
%if 0%{?fedora}
Conflicts:     kamailio-radius < %ver, kamailio-carrierroute < %ver
Conflicts:     kamailio-redis < %ver, kamailio-json < %ver
Conflicts:     kamailio-mono < %ver, kamailio-GeoIP < %ver
%endif
Requires:      openssl lksctp-tools
BuildRequires: bison flex gcc make redhat-rpm-config openssl-devel
BuildRequires: lksctp-tools-devel
%if 0%{?fedora}
BuildRequires: docbook2X
%endif

%description
Kamailio (former OpenSER) is an Open Source SIP Server released under GPL, able
to handle thousands of call setups per second. Among features: asynchronous TCP,
UDP and SCTP, secure communication via TLS for VoIP (voice, video); IPv4 and
IPv6; SIMPLE instant messaging and presence with embedded XCAP server and MSRP
relay; ENUM; DID and least cost routing; load balancing; routing fail-over;
accounting, authentication and authorization; support for many backend systems
such as MySQL, Postgres, Oracle, Radius, LDAP, Redis, Cassandra; XMLRPC control
interface, SNMP monitoring. It can be used to build large VoIP servicing
platforms or to scale up SIP-to-PSTN gateways, PBX systems or media servers
like Asterisk™, FreeSWITCH™ or SEMS.


%package utils
Summary:       Non-SIP utitility functions for Kamailio.
Group:         System Environment/Daemons
Requires:      libcurl, libxml2, kamailio = %ver
BuildRequires: libcurl-devel, libxml2-devel

%description utils
Non-SIP utitility functions for Kamailio.


%package snmpstats
Summary:       SNMP management interface (scalar statistics) for Kamailio.
Group:         System Environment/Daemons
%if 0%{?fedora}
Requires:      net-snmp-agent-libs, kamailio = %ver
%else
Requires:      net-snmp-libs, kamailio = %ver
%endif
BuildRequires: net-snmp-devel

%description snmpstats
SNMP management interface (scalar statistics) for Kamailio.


%package presence
Summary:       SIP Presence (and RLS, XCAP, etc) support for Kamailio.
Group:         System Environment/Daemons
Requires:      libxml2, libcurl, kamailio = %ver, kamailio-xmpp = %ver
BuildRequires: libxml2-devel, libcurl-devel

%description presence
SIP Presence (and RLS, XCAP, etc) support for Kamailio.


%package  auth-identity
Summary:  Functions for secure identification of originators of SIP messages for Kamailio.
Group:    System Environment/Daemons
Requires: libcurl, kamailio = %ver
BuildRequires: libcurl-devel

%description auth-identity
Functions for secure identification of originators of SIP messages for Kamailio.


%package json
Summary:       json string operation and rpc support for Kamailio.
Group:         System Environment/Daemons
Requires:      json-c, libevent, kamailio = %ver
BuildRequires: json-c-devel, libevent-devel

%description json
json string operation and rpc support for Kamailio.


%prep
%setup -n %{name}-%{ver}



%build
make FLAVOUR=kamailio cfg prefix=/usr cfg_prefix=$RPM_BUILD_ROOT\
  basedir=$RPM_BUILD_ROOT cfg_target=/%{_sysconfdir}/kamailio/\
  modules_dirs="modules" SCTP=1 STUN=1
make
%if 0%{?fedora}
make every-module skip_modules="db_cassandra iptrtpproxy db_oracle memcached \
  mi_xmlrpc osp" \
  group_include="kstandard kmysql kpostgres kcpl kxml kradius kunixodbc \
  kperl ksnmpstats kxmpp kcarrierroute kberkeley kldap kutils kpurple \
  ktls kwebsocket kpresence klua kpython kgeoip ksqlite kjson kredis \
  kmono kims koutbound"
%else
make every-module skip_modules="db_cassandra iptrtpproxy db_oracle memcached \
  mi_xmlrpc osp" \
  group_include="kstandard kmysql kpostgres kcpl kxml kunixodbc \
  kperl ksnmpstats kxmpp kberkeley kldap kutils kpurple \
  ktls kwebsocket kpresence klua kpython ksqlite \
  kims koutbound"
%endif
make utils



%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf "$RPM_BUILD_ROOT"

make install
%if 0%{?fedora}
make install-modules-all skip_modules="db_cassandra iptrtpproxy db_oracle \
  memcached mi_xmlrpc osp" \
  group_include="kstandard kmysql kpostgres kcpl kxml kradius kunixodbc \
  kperl ksnmpstats kxmpp kcarrierroute kberkeley kldap kutils kpurple \
  ktls kwebsocket kpresence klua kpython kgeoip ksqlite kjson kredis \
  kmono kims koutbound"

mkdir -p $RPM_BUILD_ROOT/%{_unitdir}
install -m644 pkg/kamailio/fedora/%{?fedora}/kamailio.service \
	$RPM_BUILD_ROOT/%{_unitdir}/kamailio.service

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
install -m644 pkg/kamailio/fedora/%{?fedora}/kamailio.sysconfig \
	$RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/kamailio
%else
make install-modules-all skip_modules="db_cassandra iptrtpproxy db_oracle \
  memcached mi_xmlrpc osp" \
  group_include="kstandard kmysql kpostgres kcpl kxml kunixodbc \
  kperl ksnmpstats kxmpp kberkeley kldap kutils kpurple \
  ktls kwebsocket kpresence klua kpython ksqlite \
  kims koutbound"

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d
install -m755 pkg/kamailio/centos/%{?centos}/kamailio.init \
	$RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/kamailio

mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig
install -m644 pkg/kamailio/centos/%{?centos}/kamailio.sysconfig \
	$RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/kamailio
%endif



%pre
/usr/sbin/groupadd -r kamailio 2> /dev/null || :
/usr/sbin/useradd -r -g kamailio -s /bin/false -c "Kamailio daemon" -d \
	%{_libdir}/kamailio kamailio 2> /dev/null || :



%clean
rm -rf "$RPM_BUILD_ROOT"



%post
%if 0%{?fedora}
/bin/systemctl --system daemon-reload
%else
/sbin/chkconfig --add kamailio
%endif



%preun
if [ $1 = 0 ]; then
%if 0%{?fedora}
  /bin/systemctl stop kamailio.service
  /bin/systemctl disable kamailio.service 2> /dev/null
%else
  /sbin/service kamailio stop > /dev/null 2>&1
  /sbin/chkconfig --del kamailio
%endif
fi



%postun
%if 0%{?fedora}
/bin/systemctl --system daemon-reload
%endif



%files
%defattr(-,root,root)
%dir %{_docdir}/kamailio
%doc %{_docdir}/kamailio/AUTHORS
%doc %{_docdir}/kamailio/NEWS
%doc %{_docdir}/kamailio/INSTALL
%doc %{_docdir}/kamailio/README
%doc %{_docdir}/kamailio/README-MODULES

%dir %{_docdir}/kamailio/modules
%doc %{_docdir}/kamailio/modules/README.acc
%doc %{_docdir}/kamailio/modules/README.auth
%doc %{_docdir}/kamailio/modules/README.auth_db
%doc %{_docdir}/kamailio/modules/README.cfgutils
%doc %{_docdir}/kamailio/modules/README.ctl
%doc %{_docdir}/kamailio/modules/README.dialog
%doc %{_docdir}/kamailio/modules/README.dispatcher
%doc %{_docdir}/kamailio/modules/README.htable
%doc %{_docdir}/kamailio/modules/README.kex
%doc %{_docdir}/kamailio/modules/README.maxfwd
%doc %{_docdir}/kamailio/modules/README.mi_fifo
%doc %{_docdir}/kamailio/modules/README.nathelper
%doc %{_docdir}/kamailio/modules/README.outbound
%doc %{_docdir}/kamailio/modules/README.path
%doc %{_docdir}/kamailio/modules/README.pv
%doc %{_docdir}/kamailio/modules/README.registrar
%doc %{_docdir}/kamailio/modules/README.rr
%doc %{_docdir}/kamailio/modules/README.sanity
%doc %{_docdir}/kamailio/modules/README.siputils
%doc %{_docdir}/kamailio/modules/README.sl
%doc %{_docdir}/kamailio/modules/README.textops
%doc %{_docdir}/kamailio/modules/README.textopsx
%doc %{_docdir}/kamailio/modules/README.tm
%doc %{_docdir}/kamailio/modules/README.tmx
%doc %{_docdir}/kamailio/modules/README.uac_redirect
%doc %{_docdir}/kamailio/modules/README.usrloc
%doc %{_docdir}/kamailio/modules/README.xlog

%dir %attr(-,kamailio,kamailio) %{_sysconfdir}/kamailio
%config(noreplace) %{_sysconfdir}/kamailio/*
%if 0%{?fedora}
%config %{_unitdir}/*
%else
%config %{_sysconfdir}/rc.d/init.d/*
%endif
%config %{_sysconfdir}/sysconfig/*

%dir %{_libdir}/kamailio
%{_libdir}/kamailio/libkcore.so
%{_libdir}/kamailio/libkcore.so.1
%{_libdir}/kamailio/libkcore.so.1.0
%{_libdir}/kamailio/libkmi.so
%{_libdir}/kamailio/libkmi.so.1
%{_libdir}/kamailio/libkmi.so.1.0
%{_libdir}/kamailio/libsrdb1.so
%{_libdir}/kamailio/libsrdb1.so.1
%{_libdir}/kamailio/libsrdb1.so.1.0
%{_libdir}/kamailio/libsrdb2.so
%{_libdir}/kamailio/libsrdb2.so.1
%{_libdir}/kamailio/libsrdb2.so.1.0
%{_libdir}/kamailio/libsrutils.so
%{_libdir}/kamailio/libsrutils.so.1
%{_libdir}/kamailio/libsrutils.so.1.0

%dir %{_libdir}/kamailio/modules
%{_libdir}/kamailio/modules/acc.so
%{_libdir}/kamailio/modules/auth.so
%{_libdir}/kamailio/modules/auth_db.so
%{_libdir}/kamailio/modules/cfgutils.so
%{_libdir}/kamailio/modules/ctl.so
%{_libdir}/kamailio/modules/db_kazoo.so
%{_libdir}/kamailio/modules/dialog.so
%{_libdir}/kamailio/modules/dispatcher.so
%{_libdir}/kamailio/modules/htable.so
%{_libdir}/kamailio/modules/kex.so
%{_libdir}/kamailio/modules/maxfwd.so
%{_libdir}/kamailio/modules/mi_fifo.so
%{_libdir}/kamailio/modules/nathelper.so
%{_libdir}/kamailio/modules/outbound.so
%{_libdir}/kamailio/modules/path.so
%{_libdir}/kamailio/modules/pv.so
%{_libdir}/kamailio/modules/registrar.so
%{_libdir}/kamailio/modules/rr.so
%{_libdir}/kamailio/modules/sanity.so
%{_libdir}/kamailio/modules/siputils.so
%{_libdir}/kamailio/modules/sl.so
%{_libdir}/kamailio/modules/textops.so
%{_libdir}/kamailio/modules/textopsx.so
%{_libdir}/kamailio/modules/tm.so
%{_libdir}/kamailio/modules/tmx.so
%{_libdir}/kamailio/modules/uac_redirect.so
%{_libdir}/kamailio/modules/usrloc.so
%{_libdir}/kamailio/modules/xlog.so

%{_sbindir}/kamailio
%{_sbindir}/kamctl
%{_sbindir}/kamdbctl
%{_sbindir}/kamcmd

%dir %{_libdir}/kamailio/kamctl
%{_libdir}/kamailio/kamctl/kamctl.base
%{_libdir}/kamailio/kamctl/kamctl.ctlbase
%{_libdir}/kamailio/kamctl/kamctl.fifo
%{_libdir}/kamailio/kamctl/kamctl.ser
%{_libdir}/kamailio/kamctl/kamctl.ser_mi
%{_libdir}/kamailio/kamctl/kamctl.sqlbase
%{_libdir}/kamailio/kamctl/kamctl.unixsock
%{_libdir}/kamailio/kamctl/kamdbctl.base

%{_mandir}/man5/*
%if 0%{?fedora}
%{_mandir}/man7/*
%endif
%{_mandir}/man8/*

%dir %{_datadir}/kamailio


%if 0%{?fedora}
%files radius
%defattr(-,root,root)
%{_docdir}/kamailio/modules/README.acc_radius
%{_docdir}/kamailio/modules/README.auth_radius
%{_docdir}/kamailio/modules/README.misc_radius
%{_docdir}/kamailio/modules/README.peering
%{_libdir}/kamailio/modules/acc_radius.so
%{_libdir}/kamailio/modules/auth_radius.so
%{_libdir}/kamailio/modules/misc_radius.so
%{_libdir}/kamailio/modules/peering.so


%files carrierroute
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.carrierroute
%{_libdir}/kamailio/modules/carrierroute.so


%files redis
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.ndb_redis
%{_libdir}/kamailio/modules/ndb_redis.so


%files json
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.json
%doc %{_docdir}/kamailio/modules/README.jsonrpc-c
%{_libdir}/kamailio/modules/json.so
%{_libdir}/kamailio/modules/jsonrpc-c.so


%files mono
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.app_mono
%{_libdir}/kamailio/modules/app_mono.so


%files GeoIP
%defattr(-,root,root)
%doc %{_docdir}/kamailio/modules/README.geoip
%{_libdir}/kamailio/modules/geoip.so
%endif



%changelog
* Thu Mar 7 2013 Peter Dunkley <peter@dunkley.me.uk>
  - Changed rel from rc1 to 0 in preparation for 4.0.0 release
  - Added build requirement for docbook2X for Fedora builds
* Wed Mar 6 2013 Peter Dunkley <peter@dunkley.me.uk>
  - Restored perl related files
* Tue Mar 5 2013 Peter Dunkley <peter@dunkley.me.uk>
  - Updated pre1 to rc1
  - Re-ordered file to make it internally consistent
  - Updated make commands to match updated module groups
  - Added auth_identity back in
  - Temporarily commented out perl related files as perl modules do not appear
    to be working
* Sun Jan 20 2013 Peter Dunkley <peter@dunkley.me.uk>
  - Updated rel to pre1
  - Moved modules from modules_k/ to modules/
  - Renamed perl modules
* Fri Jan 11 2013 Peter Dunkley <peter@dunkley.me.uk>
  - Updated rel to pre0
* Thu Jan 10 2013 Peter Dunkley <peter@dunkley.me.uk>
  - More IMS updates
* Tue Jan 8 2013 Peter Dunkley <peter@dunkley.me.uk>
  - Changed dialog2 to dialog_ng
  - Renamed all IMS modules (prepended ims_)
* Sun Jan 6 2013 Peter Dunkley <peter@dunkley.me.uk>
  - Updated ver to 4.0.0 and rel to dev8
* Mon Dec 31 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added dialog2 and IMS modules to the build
* Fri Dec 21 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added db2_ldap, db2_ops, and timer to the build
  - Added uid_auth_db, uid_avp_db, uid_domain, uid_gflags, uid_uri_db, print,
    and print_lib to the build
* Thu Dec 13 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added xhttp_pi framework examples to the installation
  - Added xhttp_pi README to the installation
* Wed Dec 12 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added mangler module to the build
  - Tidied up make commands used to build and install
* Sun Dec 9 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Updated rel to dev7
  - Added avp, sca, and xprint modules to the build
  - Moved xlog from modules_k to modules
* Fri Nov 9 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Updated rel to dev5
* Tue Oct 30 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added xhttp_pi module to RPM builds
* Fri Oct 20 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Set ownership of /etc/kamailio to kamailio.kamailio
  - Added installation of auth.7.gz for Fedora now that manpages are built for
    Fedora
  - Added "make utils" to the build section (when it's not there utils get
    built during the install - which isn't right)
  - SCTP and STUN now included in this build
  - Removed kamailio-tls package - tls module now in main kamailio RPM as that
    has openssl as a dependency for STUN
* Sun Sep 17 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added corex module to RPM builds
  - Updated rel to dev4
* Sun Aug 19 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Updated rel to dev3
* Mon Aug 13 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added Outbound module
* Fri Jul 13 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Updated rel to dev2
* Thu Jul 5 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added kamailio-cdp RPM for cdp and cdp_avp modules
* Tue Jul 3 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Updates to websocket module
* Sat Jun 30 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Updated rel to dev1
  - Removed %_sharedir and replaced with standard macro %_datadir
* Sat Jun 23 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added websocket module
* Mon Jun 11 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Updated ver to 3.4.0 and rel to dev0
* Mon Jun 4 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added a number of %dir lines to make sure the RPMs are properly cleaned up
    on uninstall
* Sat Jun 2 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added %postun section to reload systemd on Fedora after uninstall
  - Added build requirement for redhat-rpm-config so debuginfo RPMs get built
* Fri Jun 1 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Tweak to the pkg/kamailio/fedora directory structure
  - Tested with Fedora 17
* Thu May 31 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Updated rel to pre3
  - Combined Fedora/CentOS .spec in preparation for Fedora 17
* Sun May 20 2012 Peter Dunkley <peter@dunkley.me.uk>
  - First version created for Kamailio 3.3.0. Based on spec-file for Fedora
    created by myself (in turn based on an older spec-file for CentOS created
    by Ovidiu Sas).
  - Tested with CentOS 6.2 x86_64.
  - Builds all Kamailio 3.3.0 modules (modules/modules_k) except:
    - modules/app_mono: Requires mono which is not in the CentOS 6 repo
    - modules/auth_identity: Conflicts with TLS unless statically linked (which
      requires changes to Makefile and is impractical for generic RPM building)
    - modules/db_cassandra: Requires Cassandra and Thrift which are not in the
      CentOS 6 repo
    - modules/geoip: Requires GeoIP which is not in the CentOS 6 repo
    - modules/iptrtpproxy: Needs local copy of iptables source to build
      (impractical for generic RPM building)
    - modules/json: Requires json-c whish is not in the CentOS 6 repo
    - modules/jsonrpc-c: Requires json-c whish is not in the CentOS 6 repo
    - modules/ndb_redis: Requires hiredis which is not in the CentOS 6 repo
    - modules/peering: Requires radiusclient-ng which is not in the CentOS 6
      repo
    - modules_k/acc_radius: Requires radiusclient-ng which is not in the CentOS
      6 repo
    - modules_k/auth_radius: Required radiusclient-ng which is not in the
      CentOS 6 repo
    - modules_k/carrierroute: Requires libconfuse which is not in the CentOS 6
      repo
    - modules_k/db_oracle: Requires Oracle which is not in the CentOS 6 repo
      (and is closed-source)
    - modules_k/memcached: Module compilation appears to require an older
      version of libmemcached-devel than the one in the CentOS 6 repo
    - modules_k/mi_xmlrpc: Requires libxmlrpc-c3 which is not in the CentOS 6
      repo
    - modules_k/misc_radius: Requires radiusclient-ng which is not in the
      CentOS 6 repo
    - modules_k/osp: Requires OSP Toolkit which is not in the CentOS 6 repo
* Fri May 18 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Added missing BuildRequires (gcc).
  - Added .fc16 to rel.  This makes it easy to tell which distribution the RPMs
    are built for.
* Thu May 17 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Updated rel to pre2.
* Mon May 7 2012 Peter Dunkley <peter@dunkley.me.uk>
  - Changed to use systemd instead of SysV init.
* Sun May 6 2012 Peter Dunkley <peter@dunkley.me.uk>
  - First version created for Kamailio 3.3.0. Based on spec-file for CentOS
    created by Ovidiu Sas.
  - Tested with Fedora 16 x86_64.
  - Builds all Kamailio 3.3.0 modules (modules/modules_k) except:
    - modules/auth_identity: Conflicts with TLS unless statically linked (which
      requires changes to Makefile and is impractical for generic RPM building)
    - modules/db_cassandra: Requires Thrift which is not in the F16 repo
    - modules/iptrtpproxy: Needs local copy of iptables source to build
      (impractical for generic RPM building)
    - modules_k/db_oracle: Requires Oracle which is not in the F16 repo
      (and is closed-source)
    - modules_k/memcached: Module compilation appears to require an older
      version of libmemcached-devel than the one in the F16 repo
    - modules_k/mi_xmlrpc: The F16 repo contains an unsupported version of
      libxmlrpc-c3, and there is an compilation error due to the module code
      using an unknown type ('TString')
    - modules_k/osp: Requires OSP Toolkit which is not in the F16 repo
