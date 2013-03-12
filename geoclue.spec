%define	major	0
%define	libname	%mklibname %{name} %{major}
%define	devname	%mklibname -d %{name}

Summary:	The geoinformation service
Name:		geoclue
Version:	0.12.0
Release:	8
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
%patch0 -p0 -b .gcc46~
%patch1 -p0 -b .str_fmt~
%patch2 -p1 -b .nm_pkgconf~

%build
sed -i 's/AM_CONFIG_HEADER/AC_CONFIG_HEADERS/g' configure.ac
autoreconf -fi
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



%changelog
* Sun Dec 11 2011 Matthew Dawkins <mattydaw@mandriva.org> 0.12.0-6
+ Revision: 740197
- removed find_lang
- rebuild
- cleaned up spec
- removed .la files
- converted BRs to pkgconfig provides

* Tue May 10 2011 Per Øyvind Karlsen <peroyvind@mandriva.org> 0.12.0-5
+ Revision: 673330
- disable skyhook
- fix typo
- add gypsy-devel to buildrequires
- perform some further cleanups
- fix build with networkmanager support
- cleanups
- force various options to ensure they're support is built
- fix dependency loops

* Sun May 08 2011 Funda Wang <fwang@mandriva.org> 0.12.0-4
+ Revision: 672403
- br gtk-doc
- fix build with gcc 4.6
- cleanup br

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 0.12.0-2mdv2011.0
+ Revision: 605446
- rebuild

* Sun Apr 04 2010 Emmanuel Andry <eandry@mandriva.org> 0.12.0-1mdv2010.1
+ Revision: 531453
- always need BR gtk-doc
- New version 0.12.0
- drop patches (merged upstream)

* Wed Mar 03 2010 Emmanuel Andry <eandry@mandriva.org> 0.11.1.1-0.20100119.2mdv2010.1
+ Revision: 513890
- diff p1 to fix build with gpsd-2.91

* Tue Jan 19 2010 Emmanuel Andry <eandry@mandriva.org> 0.11.1.1-0.20100119.1mdv2010.1
+ Revision: 493842
- New svn snapshot
- fix geoclue-test-gui packaging

* Sun Sep 27 2009 Frederik Himpe <fhimpe@mandriva.org> 0.11.1.1-0.20090310.2mdv2010.0
+ Revision: 450018
- Add patch fixing hostip provider for new API
  (freedesktop.org bug #24058)
- Update to 20090310 snapshot used by Fedora: fixes geoclue-master segfault
  when Empathy starts up

* Wed Aug 26 2009 Götz Waschk <waschk@mandriva.org> 0.11.1-2mdv2010.0
+ Revision: 421343
- fix devel provides

* Sun Jul 26 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 0.11.1-1mdv2010.0
+ Revision: 400470
- add buildrequires on xsltproc
- disable parallel make
- add spec and source files
- create geoclue

