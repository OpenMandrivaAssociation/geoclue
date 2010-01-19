%define major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d
%define snapshot 20100119

%if %{snapshot}
%define rel %mkrel 0.%{snapshot}.1
%define src %{name}-%{snapshot}.tar.xz
%else
%define rel %mkrel 1
%define src %{name}-%{version}.tar.gz
%endif

Summary:	The geoinformation service
Name:		geoclue
Version:	0.11.1.1
Release:	%{rel}
License:	LGPLv2+
Group:		Networking/Other
Url:		http://www.freedesktop.org/wiki/Software/GeoClue
Source0:	http://folks.o-hand.com/jku/geoclue-releases/%{src}
Patch0:		geoclue-0.11.1.1-hostip-api.patch
BuildRequires:	dbus-glib-devel
BuildRequires:	libxml2-devel
BuildRequires:	libGConf2-devel
BuildRequires:	gtk+2-devel
BuildRequires:	gpsd-devel
BuildRequires:	xsltproc
%if %{snapshot}
BuildRequires:	gtk-doc
%endif
Requires:	%{libname} = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Geoclue is a modular geoinformation service built on top of the D-Bus
messaging system.The goal of the Geoclue project is to make creating
location-aware applications as simple as possible.

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n %{libname}
Main library for %{name}.

%package -n %{develname}
Summary:	Developmnet libraries for %{name}
Group:		System/Libraries
Requires:	%{libname} = %{version}-%{release}
Provides:	lib%name-devel = %version-%release

%description -n %{develname}
Developmnet files and headers for %{name}.

%prep
%setup -q -n %{name}
%patch0 -p1 -b .api

%build
./autogen.sh
%configure2_5x --disable-static --enable-gtk-doc
%make

%install
rm -rf %{buildroot}
%makeinstall_std

# Install the test gui as it seems the test isn't installed any more
mkdir %{buildroot}%{_bindir}
cp test/.libs/geoclue-test-gui %{buildroot}%{_bindir}/
%find_lang %{name}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS README
%dir %{_datadir}/geoclue-providers
%{_bindir}/%{name}*
%{_libdir}/%{name}-*
%{_datadir}/dbus-1/services/*.service
%{_datadir}/geoclue-providers/%{name}-*.provider
%{_datadir}/gtk-doc/html/%{name}

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*%{name}.so.%{major}*

%files -n %{develname}
%defattr(-,root,root)
%{_includedir}/%{name}
%{_libdir}/*%{name}.*a
%{_libdir}/*%{name}.so
%{_libdir}/pkgconfig/%{name}.pc
