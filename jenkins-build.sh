#!/bin/bash
set -e

rpm -iv --replacepkgs rpm/RPMS/x86_64/kazoo-librabbitmq-* rpm/RPMS/x86_64/kazoo-json-c* || echo ok

yum install -y bison flex redhat-rpm-config lksctp-tools-devel libxml2-devel net-snmp-devel libevent-devel libcurl-devel pcre-devel net-snmp-devel
 
rm -rf ${WORKSPACE}/kamailio-qa
git clone git://github.com/2600hz/kamailio-qa.git
cd ${WORKSPACE}/Kazoo-Kamailio
git apply ${WORKSPACE}/kamailio-qa/db_kazoo-blf-reg.patch

mkdir -p ${WORKSPACE}/rpm/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

cat <<'EOF' > ${WORKSPACE}/Kazoo-Kamailio/pkg/kamailio/centos/6/kamailio.init
#!/bin/bash
#
# Startup script for Kamailio
#
# chkconfig: 345 85 15
# description: Kamailio (OpenSER) - the Open Source SIP Server
#
# processname: kamailio
# pidfile: /var/run/kamailio.pid
# config: /etc/kamailio/kamailio.cfg
#
### BEGIN INIT INFO
# Provides: kamailio
# Required-Start: $local_fs $network
# Short-Description: Kamailio (OpenSER) - the Open Source SIP Server
# Description: Kamailio (former OpenSER) is an Open Source SIP Server released
#       under GPL, able to handle thousands of call setups per second.
### END INIT INFO

# Source function library.
. /etc/rc.d/init.d/functions

kam=/usr/sbin/kamailio
prog=kamailio
RETVAL=0

[ -f /etc/sysconfig/$prog ] && . /etc/sysconfig/$prog

start() {
        echo -n $"Starting $prog: "
        # there is something at end of this output which is needed to
        # report proper [ OK ] status in CentOS scripts
        daemon $kam $OPTIONS 2>/dev/null | tail -1
        RETVAL=$?
        echo
        [ $RETVAL = 0 ] && touch /var/lock/subsys/$prog
}

stop() {
        echo -n $"Stopping $prog: "
        killproc $kam
        RETVAL=$?
        echo
        [ $RETVAL = 0 ] && rm -f /var/lock/subsys/$prog /var/run/$prog.pid
}

MEMORY=$((`echo $MEMORY | sed -e 's/[^0-9]//g'`))
PKG_MEMORY=$((`echo $PKG_MEMORY | sed -e 's/[^0-9]//g'`))
[ -z "$USER" ]  && USER=kamailio
[ -z "$GROUP" ] && GROUP=kamailio
[ $MEMORY -le 0 ] && MEMORY=32
[ $PKG_MEMORY -le 0 ] && PKG_MEMORY=4

OPTIONS="-P /var/run/$prog.pid -m $MEMORY -M $PKG_MEMORY -u $USER -g $GROUP"

# See how we were called.
case "$1" in
        start)
                start
                ;;
        stop)
                stop
                ;;
        status)
                status $kam
                RETVAL=$?
                ;;
        restart)
                stop
                start
                ;;
        condrestart)
                if [ -f /var/run/$prog.pid ] ; then
                        stop
                        start
                fi
                ;;
        *)
                echo $"Usage: $prog {start|stop|reload|restart|condrestart|status|help}"
                exit 1
esac

exit $RETVAL
EOF

tar cf ${WORKSPACE}/rpm/SOURCES/Kazoo-Kamailio.tar --directory=${WORKSPACE} Kazoo-Kamailio --exclude .git

cat <<'EOF' > ${WORKSPACE}/rpm/SPECS/kazoo-kamailio.spec
%define packagelayout   FH
%define PREFIX          %{_prefix}
%define SYSCONFDIR      %{_sysconfdir}/kazoo/kamailio
%define DOCDIR          %{_defaultdocdir}/kamailio
%define DATADIR         %{_datadir}/kamailio
%define LIBDIR          %{_libdir}/kamailio
%define SBINDIR         %{_sbindir}
%define MODINSTDIR      %{LIBDIR}/modules

Name:           kazoo-kamailio
Summary:        Kamailio (former OpenSER) - the Open Source SIP Server
License:        GPL
Group:          Productivity/Telephony/Servers
Version:        %{_version}
Release:        %{_release}%{dist}
URL:            http://kamailio.org/
Packager:       Karl Anderson
Vendor:         kamailio.org
Requires:       openssl
Requires:       lksctp-tools
Requires:       kazoo-librabbitmq
Requires:       kazoo-json-c
Requires:       kazoo-configs

Source0:        Kazoo-Kamailio.tar
BuildRoot:      %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  lksctp-tools-devel

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
like Asterisk#, FreeSWITCH# or SEMS.


######################################################################################################################
# Prepare for the build
######################################################################################################################
%prep
%setup -b0 -q -n Kazoo-Kamailio

######################################################################################################################
# Bootstrap, Configure and Build the whole enchilada
######################################################################################################################
%build

# pike
# permissions
# db_text
EXCLUDE_MODULES="alias_db \
path \
cfg_rpc \
corex \
mi_rpc \
async \
auth_diameter \
avpops \
avp \
benchmark \
blst \
call_control \
cfg_db \
counters \
db2_ops \
db_cluster \
db_flatstore \
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
mqueue \
msilo \
msrp \
mtree \
nat_traversal \
pdb \
pdt \
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

INCLUDE_MODULES="pua_dialoginfo \
presence \
presence_dialoginfo \
snmpstats \
tls"

make FLAVOUR=kamailio cfg\
  skip_modules="${EXCLUDE_MODULES}"\
  include_modules="${INCLUDE_MODULES}"\
  prefix=%{PREFIX}\
  cfg_prefix=%{buildroot}\
  cfg_target=%{SYSCONFDIR}/\
  basedir=%{buildroot}\
  modules_dirs="modules"\
  SCTP=1\
  STUN=1

make

######################################################################################################################
# Install it to the build root
######################################################################################################################
%install

make install

rm -rf %{buildroot}/etc/kamailio
rm -rf %{buildroot}/usr/share/kamailio/dbtext

mkdir -p %{buildroot}/%{_sysconfdir}/rc.d/init.d
install -m755 pkg/kamailio/centos/%{?centos}/kamailio.init \
        %{buildroot}/%{_sysconfdir}/rc.d/init.d/kamailio

mkdir -p %{buildroot}/%{_sysconfdir}/sysconfig
install -m644 pkg/kamailio/centos/%{?centos}/kamailio.sysconfig \
        %{buildroot}/%{_sysconfdir}/sysconfig/kamailio

######################################################################################################################
# Scripts for when the RPM is installed
######################################################################################################################
%pre
# create user only if it doesn't already exist
if ! getent passwd kamailio >/dev/null 2>&1; then
        useradd -r \
        -M -d %{LIBDIR} \
        -s /sbin/nologin \
        kamailio || %logmsg "User \"kamailio\" could not be created."
fi

%post
chkconfig --add kamailio
service kamailio start

######################################################################################################################
# Scripts for when the RPM is update/remove
######################################################################################################################
%preun
if [ $1 -eq 0 ]; then
    service kamailio stop
    chkconfig --del kamailio
fi

%postun
if [ $1 -eq 0 ]; then
    userdel kamailio || %logmsg "User \"kamailio\" could not be deleted."
fi

######################################################################################################################
# List of files/directories to include the RPM
######################################################################################################################
%files
%defattr(-,kamailio,kamailio)
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
%{MODINSTDIR}/pua_dialoginfo.so
%{MODINSTDIR}/presence.so
%{MODINSTDIR}/presence_dialoginfo.so
%{MODINSTDIR}/snmpstats.so
%{MODINSTDIR}/pike.so
%{MODINSTDIR}/permissions.so
%{MODINSTDIR}/db_text.so
%{MODINSTDIR}/tls.so

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
%{LIBDIR}/kamctl/kamctl.dbtext
%{LIBDIR}/kamctl/kamdbctl.dbtext
%{LIBDIR}/kamctl/dbtextdb

%dir %{DATADIR}

%defattr(-,kamailio,kamailio)
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
%{DOCDIR}/modules/README.presence
%{DOCDIR}/modules/README.presence_dialoginfo
%{DOCDIR}/modules/README.pua_dialoginfo
%{DOCDIR}/modules/README.snmpstats
%{DOCDIR}/modules/README.pike
%{DOCDIR}/modules/README.permissions
%{DOCDIR}/modules/README.db_text
%{DOCDIR}/modules/README.tls

%{_mandir}/man5/*
%{_mandir}/man8/*

######################################################################################################################
# Clean the build environment
######################################################################################################################
%clean
rm -rf "%{buildroot}"
EOF

cd ${WORKSPACE}/rpm/
rpmbuild --define '_topdir '`pwd` --define "_version ${GIT_BRANCH/origin\/}" --define "_release `/opt/redis-bash/release_num.sh Kazoo-Kamailio`" -bb SPECS/kazoo-kamailio.spec
