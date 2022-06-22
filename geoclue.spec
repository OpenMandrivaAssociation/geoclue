%define major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define build_geoip	0
%define url_ver %(echo %{version} | cut -d. -f1,2)
%define api 2.0


Summary:	The geoinformation service
Name:		geoclue
Version:	2.6.0
Release:	4
License:	LGPLv2+
Group:		Networking/Other
Url:		http://www.freedesktop.org/wiki/Software/GeoClue
Source0:	https://gitlab.freedesktop.org/geoclue/geoclue/-/archive/%{version}/%{name}-%{version}.tar.bz2

BuildRequires:	itstool
BuildRequires:	libxml2-utils
BuildRequires:	pkgconfig(gio-2.0)
BuildRequires:	pkgconfig(gio-unix-2.0)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(json-glib-1.0)
BuildRequires:	pkgconfig(libpng16)
BuildRequires:	pkgconfig(libsoup-2.4)
BuildRequires:	pkgconfig(mm-glib) >= 1.6
BuildRequires:	pkgconfig(avahi-client)
BuildRequires:	pkgconfig(avahi-glib)
BuildRequires:	pkgconfig(ModemManager)
BuildRequires:	avahi-common-devel
BuildRequires:	gtk-doc
BuildRequires:	gobject-introspection
BuildRequires:	xmlto docbook-dtds
BuildRequires:	pkgconfig(gobject-introspection-1.0)
BuildRequires:	meson
BuildRequires:	pkgconfig(systemd)
# for demo agent
BuildRequires:	pkgconfig(libnotify)

%if %{build_geoip}
BuildRequires:	pkgconfig(geoip) >= 1.5.1
Requires:	geoip-database >= 1.5.1
Conflicts:	geocode-glib < 0.99.2
%endif

Requires:	%{libname} = %{EVRD}

%description
Geoclue is a modular geoinformation service built on top of the D-Bus
messaging system.The goal of the Geoclue project is to make creating
location-aware applications as simple as possible.

%files
%doc NEWS README.md
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.conf
%{_sysconfdir}/dbus-1/system.d/org.freedesktop.GeoClue2.Agent.conf
%dir %{_sysconfdir}/%{name}/
%{_sysconfdir}/%{name}/%{name}.conf
%{_datadir}/dbus-1/system-services/org.freedesktop.GeoClue2.service
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/polkit-1/rules.d/org.freedesktop.GeoClue2.rules
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

#----------------------------------------------------------------------------

%package -n	%{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

Obsoletes:	%{libname} < %{EVRD}

%description -n %{libname}
Main library for %{name}.

%files -n %{libname}
%{_libdir}/lib%{name}-2.so.%{major}*


#--------------------------------------------------------------------

%package vala
Summary:	Vala integration for geoclue
Group:		Development/Other
Requires:	geoclue = %{EVRD}
BuildRequires:	vala

%description vala
Vala integration for geoclue

%files vala
%{_datadir}/vala/vapi/*

#----------------------------------------------------------------------------

%package gir
Summary:	GObject Introspection interface description for geoclue2
Group:		System/Libraries

%description gir
GObject Introspection interface description for geoclue2.

%files gir
%{_libdir}/girepository-1.0/Geoclue-2.0.typelib

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Development libraries for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{EVRD}
Provides:	%{name}-devel = %{EVRD}
Requires:	%{name} = %{EVRD}

%description -n %{devname}
Development files and headers for %{name}.

%files -n %{devname}
%doc %{_datadir}/gtk-doc/html/*
%{_includedir}/libgeoclue-%{api}
%{_libdir}/pkgconfig/%{name}-%{api}.pc
%{_libdir}/pkgconfig/lib%{name}-%{api}.pc
%{_datadir}/gir-1.0/Geoclue-2.0.gir
%{_libdir}/*.so
%{_mandir}/man5/geoclue.5.*

#----------------------------------------------------------------------------

%prep
%setup -q
%autopatch -p1

%build
%meson \
	-Dlibgeoclue=true \
	-Dintrospection=true \
	-Dgtk-doc=true \
	-D3g-source=true \
	-Dcdma-source=true \
	-Dmodem-gps-source=true \
	-Dnmea-source=true \
	-Denable-backend=true \
	-Ddemo-agent=true

%meson_build

%install
%meson_install

