%define packagelayout   FH
%define PREFIX          %{_prefix}
%define SYSCONFDIR      %{_sysconfdir}/kazoo/kamailio
%define DOCDIR          %{_defaultdocdir}/kamailio
%define MODINSTDIR      %{LIBDIR}/modules
%define DATADIR         %{_datadir}/kamailio
%define LIBDIR          %{_libdir}/kamailio
%define SBINDIR         %{_sbindir}

Name:          kazoo-kamailio
Summary:       Kamailio (former OpenSER) - the Open Source SIP Server
License:       GPL
Group:         System Environment/Daemons
Version:       4.0.0
Release:       0%{dist}
URL:           http://kamailio.org/
Packager:      Karl Anderson
Vendor:        kamailio.org

Source0:       Kazoo-Kamailio.tar
BuildRoot:     %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

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

Requires:      openssl lksctp-tools
BuildRequires: bison flex gcc make openssl-devel lksctp-tools-devel
#BuildRequires: lksctp-tools-devel redhat-rpm-config

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


######################################################################################################################
# Prepare for the build
######################################################################################################################
%prep
%setup -b0 -q -n Kazoo-Kamailio

######################################################################################################################
# Configure and Build the whole enchilada
######################################################################################################################
%build

export EXCLUDE="alias_db \
async \
auth_diameter \
avpops \
avp \
benchmark \
blst \
call_control \
cfg_db \
cfg_rpc \
corex \
counters \
db2_ops \
db_cluster \
db_flatstore \
db_text \
debugger \
diversion \
dmq \
domainpolicy \
domain \
drouting \
enum \
exec \
group \
imc \
ipops \
malloc_test \
mangler \
matrix \
mediaproxy \
mi_datagram \
mi_rpc \
mqueue \
msilo \
msrp \
mtree \
nat_traversal \
pdb \
pdt \
permissions \
pike \
pipelimit \
prefix_route \
print_lib \
print \
p_usrloc \
qos \
ratelimit \
rtimer \
rtpproxy \
sca \
sdpops \
seas \
sipcapture \
siptrace \
sms \
speeddial \
sqlops \
sst \
statistics \
timer \
tmrec \
topoh \
uid_auth_db \
uid_avp_db \
uid_domain \
uid_gflags \
uid_uri_db \
uri_db \
userblacklist \
xhttp_rpc \
xhttp \
xprint"

make FLAVOUR=kamailio cfg\
  skip_modules="${EXCLUDE}"\
  prefix=%{PREFIX}\
  cfg_prefix=%{buildroot}\
  cfg_target=%{SYSCONFDIR}/\
  basedir=%{buildroot}\
  modules_dirs="modules"\
  SCTP=1\
  STUN=1

make

%install

make install
rm -rf %{buildroot}/etc/kamailio

mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/init.d
install -m755 pkg/kamailio/centos/%{?centos}/kamailio.init \
        %{buildroot}/%{_sysconfdir}/rc.d/init.d/kamailio

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
install -m644 pkg/kamailio/centos/%{?centos}/kamailio.sysconfig \
        %{buildroot}/%{_sysconfdir}/sysconfig/kamailio

%pre
/usr/sbin/groupadd -r kamailio 2> /dev/null || :
/usr/sbin/useradd -r -g kamailio -s /bin/false -c "Kamailio daemon" -d \
        %{LIBDIR} kamailio 2> /dev/null || :


%clean
rm -rf "%{buildroot}"


%post
/sbin/chkconfig --add kamailio


%preun
if [ $1 = 0 ]; then
  /sbin/service kamailio stop > /dev/null 2>&1
  /sbin/chkconfig --del kamailio
fi


%postun


%files
%defattr(-,root,root)
%config %{_sysconfdir}/rc.d/init.d/*
%config(noreplace) %{_sysconfdir}/sysconfig/*

%dir %{LIBDIR}
%{LIBDIR}/libkcore.so
%{LIBDIR}/libkcore.so.1
%{LIBDIR}/libkcore.so.1.0
%{LIBDIR}/libkmi.so
%{LIBDIR}/libkmi.so.1
%{LIBDIR}/libkmi.so.1.0
%{LIBDIR}/libsrdb1.so
%{LIBDIR}/libsrdb1.so.1
%{LIBDIR}/libsrdb1.so.1.0
%{LIBDIR}/libsrdb2.so
%{LIBDIR}/libsrdb2.so.1
%{LIBDIR}/libsrdb2.so.1.0
%{LIBDIR}/libsrutils.so
%{LIBDIR}/libsrutils.so.1
%{LIBDIR}/libsrutils.so.1.0

%dir %{MODINSTDIR}
%{MODINSTDIR}/acc.so
%{MODINSTDIR}/auth.so
%{MODINSTDIR}/auth_db.so
%{MODINSTDIR}/uac.so
%{MODINSTDIR}/cfgutils.so
%{MODINSTDIR}/ctl.so
%{MODINSTDIR}/db_kazoo.so
%{MODINSTDIR}/dialog.so
%{MODINSTDIR}/dispatcher.so
%{MODINSTDIR}/htable.so
%{MODINSTDIR}/kex.so
%{MODINSTDIR}/maxfwd.so
%{MODINSTDIR}/mi_fifo.so
%{MODINSTDIR}/nathelper.so
%{MODINSTDIR}/path.so
%{MODINSTDIR}/pv.so
%{MODINSTDIR}/registrar.so
%{MODINSTDIR}/rr.so
%{MODINSTDIR}/sanity.so
%{MODINSTDIR}/siputils.so
%{MODINSTDIR}/sl.so
%{MODINSTDIR}/textops.so
%{MODINSTDIR}/textopsx.so
%{MODINSTDIR}/tm.so
%{MODINSTDIR}/tmx.so
%{MODINSTDIR}/uac_redirect.so
%{MODINSTDIR}/usrloc.so
%{MODINSTDIR}/xlog.so

%{SBINDIR}/kamailio
%{SBINDIR}/kamctl
%{SBINDIR}/kamdbctl
%{SBINDIR}/kamcmd

%dir %{LIBDIR}/kamctl
%{LIBDIR}/kamctl/kamctl.base
%{LIBDIR}/kamctl/kamctl.ctlbase
%{LIBDIR}/kamctl/kamctl.fifo
%{LIBDIR}/kamctl/kamctl.ser
%{LIBDIR}/kamctl/kamctl.ser_mi
%{LIBDIR}/kamctl/kamctl.sqlbase
%{LIBDIR}/kamctl/kamctl.unixsock
%{LIBDIR}/kamctl/kamdbctl.base

%dir %{DATADIR}

%defattr(-,root,root)
%dir %{DOCDIR}
%doc %{DOCDIR}/AUTHORS
%doc %{DOCDIR}/NEWS
%doc %{DOCDIR}/INSTALL
%doc %{DOCDIR}/README
%doc %{DOCDIR}/README-MODULES

%dir %{DOCDIR}/modules
%{DOCDIR}/modules/README.acc
%{DOCDIR}/modules/README.auth
%{DOCDIR}/modules/README.auth_db
%{DOCDIR}/modules/README.cfgutils
%{DOCDIR}/modules/README.ctl
%{DOCDIR}/modules/README.dialog
%{DOCDIR}/modules/README.dispatcher
%{DOCDIR}/modules/README.htable
%{DOCDIR}/modules/README.kex
%{DOCDIR}/modules/README.maxfwd
%{DOCDIR}/modules/README.mi_fifo
%{DOCDIR}/modules/README.nathelper
%{DOCDIR}/modules/README.path
%{DOCDIR}/modules/README.pv
%{DOCDIR}/modules/README.registrar
%{DOCDIR}/modules/README.rr
%{DOCDIR}/modules/README.sanity
%{DOCDIR}/modules/README.siputils
%{DOCDIR}/modules/README.sl
%{DOCDIR}/modules/README.textops
%{DOCDIR}/modules/README.textopsx
%{DOCDIR}/modules/README.tm
%{DOCDIR}/modules/README.tmx
%{DOCDIR}/modules/README.uac
%{DOCDIR}/modules/README.uac_redirect
%{DOCDIR}/modules/README.usrloc
%{DOCDIR}/modules/README.xlog

%{_mandir}/man5/*
%{_mandir}/man8/*
