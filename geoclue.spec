Summary:	The geoinformation service
Name:		geoclue
Version:	0.12.0
Release:	5
License:	LGPLv2+
Group:		Networking/Other
Url:		http://www.freedesktop.org/wiki/Software/GeoClue
Source0:	http://folks.o-hand.com/jku/geoclue-releases/%{name}-%{version}.tar.gz
Patch0:		geoclue-0.12.0-gcc46.patch
Patch1:		geoclue-0.12.0-str-fmt.patch
Patch2:		geoclue-0.12.0-networkmanager-pkgconfig-typo.patch
BuildRequires:	dbus-glib-devel
BuildRequires:	libxml2-devel
BuildRequires:	libGConf2-devel GConf2
BuildRequires:	gtk+2-devel
BuildRequires:	gpsd-devel >= 2.91
BuildRequires:	xsltproc
BuildRequires:	gtk-doc
BuildRequires:	NetworkManager-devel NetworkManager-glib-devel
BuildRequires:	gypsy-devel

%description
Geoclue is a modular geoinformation service built on top of the D-Bus
messaging system.The goal of the Geoclue project is to make creating
location-aware applications as simple as possible.

%define	major	0
%define	libname	%mklibname %{name} %{major}
%package -n	%{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Main library for %{name}.

%define	devname	%mklibname -d %{name}
%package -n	%{devname}
Summary:	Development libraries for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
Development files and headers for %{name}.

%prep
%setup -q
%patch0 -p0 -b .gcc46~
%patch1 -p0 -b .str_fmt~
%patch2 -p1 -b .nm_pkgconf~
autoreconf -fi

%build
%configure2_5x	--disable-static \
		--disable-gtk-doc \
		--enable-gtk=yes \
		--enable-conic=no \
		--enable-networkmanager=yes \
		--enable-gypsy=yes \
		--enable-gpsd=yes \
		--enable-skyhook=yes
%make

%install
%makeinstall_std

# Install the test gui as it seems the test isn't installed any more
install -m755 test/.libs/geoclue-test-gui -D %{buildroot}%{_bindir}/geoclue-test-gui
%find_lang %{name}

%files -f %{name}.lang
%doc AUTHORS README
%dir %{_datadir}/geoclue-providers
%{_bindir}/%{name}*
%{_libdir}/%{name}-*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/geoclue-providers/%{name}-*.provider
%{_datadir}/gtk-doc/html/%{name}

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

%files -n %{devname}
%{_includedir}/%{name}
%{_libdir}/lib%{name}.*a
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
