%define build_geoip	0

%define url_ver %(echo %{version} | cut -d. -f1,2)

%define api 2.0

Name:			geoclue
Version:		2.4.10
Release:		1
Summary:		A modular geoinformation service
Group:			Networking/Other
License:		GPLv2+
URL:			http://geoclue.freedesktop.org/
Source0:		http://www.freedesktop.org/software/geoclue/releases/%{url_ver}/geoclue-%{version}.tar.xz

BuildRequires:	intltool
BuildRequires:	itstool
BuildRequires:	libxml2-utils
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libpng16)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(mm-glib) >= 1.6
BuildRequires:	pkgconfig(libnm-glib) >= 0.9.8.0
BuildRequires:	pkgconfig(libnm-glib-vpn)
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	gtk-doc
BuildRequires:	gobject-introspection
BuildRequires:	pkgconfig(gobject-introspection-1.0)

# for demo agent
BuildRequires:	pkgconfig(libnotify)

%if %{build_geoip}
BuildRequires:	pkgconfig(geoip) >= 1.5.1
Requires:	geoip-database >= 1.5.1
Conflicts:	geocode-glib < 0.99.2
%endif

%libpackage geoclue-2 0

%description
Geoclue is a D-Bus service that provides location information. The
primary goal of the Geoclue project is to make creating location-aware
applications as simple as possible, while the secondary goal is to
ensure that no application can access location information without
explicit permission from user.

Geoclue used to also do (reverse-)geocoding but that functionality has
been dropped in favor of geocode-glib library.

However project is in the early stages of development and hence
lacking essential features. Currently it can only determine your
location based on your IP (i-e city-level accuracy) and does not have
any permission control.

%files
%doc NEWS README
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf
%dir %{_sysconfdir}/%{name}/
%{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service
%{_datadir}/dbus-1/interfaces/*.xml
%{_sysconfdir}/xdg/autostart/geoclue-demo-agent.desktop
%{_datadir}/applications/geoclue-demo-agent.desktop
%{_datadir}/applications/geoclue-where-am-i.desktop
%{_libexecdir}/geoclue-2.0/
%{_libexecdir}/geoclue
%{_unitdir}/geoclue.service
%if %{build_geoip}
%{_bindir}/geoip-update
%{_bindir}/geoip-lookup
%endif

#--------------------------------------------------------------------

%package devel
Summary:	Development files for geoclue2
Group:		Development/Other
Obsoletes:	libgeoclue1.0-devel < 1.99.2
Obsoletes:	lib64geoclue1.0-devel < 1.99.2
# (tv) fix "No rule to make target '/usr/share/dbus-1/interfaces/org.freedesktop.GeoClue2.xml', needed by 'geoclue.h'":
Requires: geoclue
Requires: %mklibname geoclue-2 0

%description devel
This package contains the development files for geoclue2.

%files devel
%{_includedir}/libgeoclue-%{api}
%{_libdir}/pkgconfig/%{name}-%{api}.pc
%{_libdir}/pkgconfig/lib%{name}-%{api}.pc
%{_libdir}/girepository-1.0/Geoclue-2.0.typelib
%{_datadir}/gir-1.0/Geoclue-2.0.gir
%{_libdir}/*.so

#--------------------------------------------------------------------
%prep
%setup -q
%apply_patches

%build
#autoreconf -vfi
%configure \
	--enable-demo-agent \
%if %{build_geoip}
        --enable-geoip-server=yes \
%else
	--enable-geoip-server=no \
%endif
	--disable-static \
	--with-systemdsystemunitdir=%{_unitdir}
%make

%install
%makeinstall_std
