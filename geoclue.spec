%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

Summary:	The geoinformation service
Name:		geoclue
Version:	0.12.0
Release:	9
License:	LGPLv2+
Group:		Networking/Other
Url:		http://www.freedesktop.org/wiki/Software/GeoClue
Source0:	http://folks.o-hand.com/jku/geoclue-releases/%{name}-%{version}.tar.gz
Patch0:		geoclue-0.12.0-gcc46.patch
Patch1:		geoclue-0.12.0-str-fmt.patch
Patch2:		geoclue-0.12.0-networkmanager-pkgconfig-typo.patch

BuildRequires:	GConf2
BuildRequires:	gtk-doc
BuildRequires:	xsltproc
BuildRequires:	pkgconfig(dbus-glib-1)
BuildRequires:	pkgconfig(gconf-2.0)
BuildRequires:	pkgconfig(gtk+-2.0)
BuildRequires:	pkgconfig(gypsy)
BuildRequires:	pkgconfig(libgpsd) >= 2.91
BuildRequires:	pkgconfig(libnm-glib)
BuildRequires:	pkgconfig(libxml-2.0)

%description
Geoclue is a modular geoinformation service built on top of the D-Bus
messaging system.The goal of the Geoclue project is to make creating
location-aware applications as simple as possible.

%package -n	%{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
Main library for %{name}.

%package -n	%{devname}
Summary:	Development libraries for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n	%{devname}
Development files and headers for %{name}.

%prep
%setup -q
%apply_patches
sed -i 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/g' configure.ac
autoreconf -fi

%build
%configure2_5x	\
	--disable-static \
	--disable-gtk-doc \
	--enable-gtk=yes \
	--enable-conic=no \
	--enable-networkmanager=yes \
	--enable-gypsy=yes \
	--enable-gpsd=yes \
	--enable-skyhook=no
%make

%install
%makeinstall_std

# Install the test gui as it seems the test isn't installed any more
install -m755 test/.libs/geoclue-test-gui -D %{buildroot}%{_bindir}/geoclue-test-gui

%files 
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
%{_libdir}/lib%{name}.so
%{_libdir}/pkgconfig/%{name}.pc

