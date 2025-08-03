# TODO
# - openDWG
#
# Conditional build, see http://grass.itc.it/grass61/source/REQUIREMENTS.html
# for description of optional requirements.
%bcond_without	mysql	# MySQL support
%bcond_without	odbc	# unixODBC support

Summary:	The Geographic Resources Analysis Support System
Summary(pl.UTF-8):	System obsługujący analizę zasobów geograficznych
Name:		grass
Version:	8.4.0
%define		gver	%(echo %{version} | awk -F. '{ print $1$2 }')
Release:	2
Epoch:		1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://grass.osgeo.org/grass84/source/%{name}-%{version}.tar.gz
# Source0-md5:	2dac2ae5e69655b9825c34cce433a793
URL:		http://grass.osgeo.org/
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	autoconf >= 2.13
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	blas-devel
BuildRequires:	cairo-devel
BuildRequires:	fftw3-devel >= 3
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gcc-fortran
BuildRequires:	gd-devel
BuildRequires:	gdal-devel
BuildRequires:	gdbm-devel
BuildRequires:	geos-devel
BuildRequires:	lapack-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
# man or man-db
BuildRequires:	/usr/bin/man
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	pkgconfig
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	proj-devel >= 4.4.6
BuildRequires:	proj-progs
BuildRequires:	python3-devel
BuildRequires:	python3-wxPython
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.0
%{?with_odbc:BuildRequires:	unixODBC-devel}
BuildRequires:	wxGTK3-unicode-devel >= 2.8.1
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zlib-devel
# R language?
Requires:	proj >= 4.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_sysconfdir	/etc/X11

%description
GRASS (the Geographic Resources Analysis Support System) is a software
raster- and vector-based GIS (Geographic Information System), image
processing system, graphics production system, and spatial modeling
system. GRASS contains many modules for raster data manipulation,
vector data manipulation, rendering images on the monitor or paper,
multispectral image processing, point data management and general data
management. It also has tools for interfacing with digitizers,
scanners, and the RIM, Informix, Postgres, and Oracle databases.

%description -l pl.UTF-8
GRASS (System Wspierania Analiz Zasobów Geograficznych) jest rastrowym
oraz wektorowym systemem GIS (System Informacji Geograficznej),
obróbki obrazów, tworzenia grafiki oraz modelowania przestrzennego.
GRASS zawiera wiele modułów wspomagających manipulację danymi
rastrowymi i wektorowymi, renderowanie obrazów na monitorze lub
papierze, obróbkę multispektralnych obrazów, punktowe oraz ogólne
zarządzanie danymi. Zawiera również narzędzia do współpracy z
digitizerami, skanerami oraz bazami RIM, Informix, Postgres oraz
Oracle.

%package OpenGL
Summary:	NVIZ - a 3D-tool for GRASS
Summary(pl.UTF-8):	NVIZ - narzędzie 3D dla GRASSa
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description OpenGL
Package contains nviz, which is a GRASS module-in-progress which
allows users to realistically render multiple surfaces in a 3D space,
optionally using thematic coloring, draping GRASS vector files over
the surfaces, and displaying GRASS site files either draped on the
surfaces or as 3D point locations.

%description OpenGL -l pl.UTF-8
Pakiet zawiera moduł nviz, który rozszerza funkcjonalność systemu
GRASS o możliwość realistycznego renderowania wielu powierzchni w
trójwymiarowej przestrzeni. Na renderowanych powierzchniach, które
mogą być tematycznie kolorowane, można zawieszać pliki wektorowe
GRASSa.

%package pg
Summary:	PostgreSQL database interface
Summary(pl.UTF-8):	Interfejs do bazy PostgreSQL
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description pg
PostgreSQL database interface for GRASS.

%description pg -l pl.UTF-8
Interfejs do bazy PostgreSQL dla GRASSa.

%package odbc
Summary:	ODBC database interface
Summary(pl.UTF-8):	Interfejs ODBC dla GRASSa
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description odbc
ODBC database interface for GRASS.

%description odbc -l pl.UTF-8
Interfejs ODBC dla GRASSa.

%package devel
Summary:	Header files and static libraries for GRASS
Summary(pl.UTF-8):	Pliki nagłówkowe i biblioteki statyczne systemu GRASS
Group:		X11/Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description devel
Header files and static libraries for GRASS.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki statyczne systemu GRASS.

%prep
%setup -q

find general gui imagery lib/init raster scripts temporal utils -name '*.py' | xargs %{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,'

%build
%configure2_13 \
%if "%{_lib}" == "lib64"
        --enable-64bit \
%endif
	--enable-largefile \
	--with-includes=%{_includedir} \
	--with-libs=%{_libdir} \
	--with-blas \
	--with-cairo \
	--with-cxx \
	--with-freetype \
	--with-freetype-includes=/usr/include/freetype2 \
	--with-geos=/usr/bin/geos-config \
	--with-lapack \
	%{?with_mysql:--with-mysql} \
	%{?with_mysql:--with-mysql-includes=/usr/include/mysql} \
	--with-nls \
	%{?with_odbc:--with-odbc} \
	--with-opengl \
	--with-postgres \
	--with-postgres-includes=/usr/include/postgresql/server \
	--with-proj-share=/usr/share/proj \
	--with-readline \
	--with-sqlite \
	--without-pdal \
	--with-wxwidgets=/usr/bin/wx-gtk2-unicode-config

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_libdir} \
	UNIX_BIN=$RPM_BUILD_ROOT%{_bindir}

install -d $RPM_BUILD_ROOT{%{_datadir},%{_includedir}/grass%{gver}}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass%{gver}/include/* $RPM_BUILD_ROOT%{_includedir}/grass%{gver}/
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass%{gver}/lib/* $RPM_BUILD_ROOT%{_libdir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass%{gver}/locale $RPM_BUILD_ROOT%{_datadir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass%{gver}/docs/man $RPM_BUILD_ROOT%{_datadir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass%{gver}/share/{metainfo,applications,icons} $RPM_BUILD_ROOT%{_datadir}

# these manual cover topics, not programs, so shouldn't exist in section 1
# (maybe in section 7, but names are too common anyway); keep HTML version only
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{cairodriver,database,databaseintro,display,displaydrivers,full_index,general,helptext,htmldriver,imagery,imageryintro,index,keywords,pngdriver,postscript,projectionintro,psdriver,raster,rasterintro,raster3d,raster3dintro,sql,temporal,temporalintro,topics,variables,vector,vectorascii,vectorintro}.1

# non-standard icons
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/40x40

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/grass%{gver}/docs

%{__mv} $RPM_BUILD_ROOT%{_localedir}/{id_ID,id}
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/zh_CN
%{__mv} $RPM_BUILD_ROOT%{_localedir}/{zh,zh_CN}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}%{gver}/{AUTHORS,CHANGES,CITING,COPYING,GPL.TXT,INSTALL.md,REQUIREMENTS.md}

%{__sed} -i -e "s|$RPM_BUILD_ROOT||g" \
	$RPM_BUILD_ROOT%{_libdir}/grass%{gver}/etc/fontcap \
	$RPM_BUILD_ROOT%{_libdir}/grass%{gver}/demolocation/.grassrc%{gver} \
	$RPM_BUILD_ROOT%{_bindir}/grass \
	$RPM_BUILD_ROOT%{_includedir}/grass%{gver}/Make/Grass.make \
	$RPM_BUILD_ROOT%{_includedir}/grass%{gver}/Make/Platform.make

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CHANGES CITING COPYING README.md TODO
%attr(755,root,root) %{_bindir}/grass
%attr(755,root,root) %{_libdir}/libgrass_*.*.*.so
%dir %{_libdir}/grass%{gver}
%{_libdir}/grass%{gver}/*.csv
%attr(755,root,root) %{_libdir}/grass%{gver}/bin
%attr(755,root,root) %{_libdir}/grass%{gver}/driver
%dir %{_libdir}/grass%{gver}/etc
%{_libdir}/grass%{gver}/etc/VERSIONNUMBER
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/clean_temp
%{_libdir}/grass%{gver}/etc/colors
%{_libdir}/grass%{gver}/etc/colors.desc
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/current_time_s_ms
%{_libdir}/grass%{gver}/etc/d.mon
%{_libdir}/grass%{gver}/etc/d.polar
%{_libdir}/grass%{gver}/etc/db.test
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/echo
%{_libdir}/grass%{gver}/etc/element_list
%{_libdir}/grass%{gver}/etc/fontcap
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/i.find
%{_libdir}/grass%{gver}/etc/i.band.library
%{_libdir}/grass%{gver}/etc/license
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/lister
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/lock
%{_libdir}/grass%{gver}/etc/paint
%{_libdir}/grass%{gver}/etc/proj
%{_libdir}/grass%{gver}/etc/psdriver.ps
%{_libdir}/grass%{gver}/etc/python
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/r.in.wms
%dir %{_libdir}/grass%{gver}/etc/r.watershed
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/r.watershed/ram
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/r.watershed/seg
%{_libdir}/grass%{gver}/etc/renamed_options
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/run
%{_libdir}/grass%{gver}/etc/sql
%{_libdir}/grass%{gver}/etc/symbol
%attr(755,root,root) %{_libdir}/grass%{gver}/etc/wxpyimgview_gui.py
%{_libdir}/grass%{gver}/fonts
%dir %{_libdir}/grass%{gver}/gui
%{_libdir}/grass%{gver}/gui/icons
%{_libdir}/grass%{gver}/gui/images
%dir %{_libdir}/grass%{gver}/gui/scripts
%attr(755,root,root) %{_libdir}/grass%{gver}/gui/scripts/d.*
%{_libdir}/grass%{gver}/gui/wxpython
%{_libdir}/grass%{gver}/gui/xml
%attr(755,root,root) %{_libdir}/grass%{gver}/scripts
%{_libdir}/grass%{gver}/utils/__pycache__
%dir %{_libdir}/grass%{gver}/utils
%attr(755,root,root) %{_libdir}/grass%{gver}/utils/g.echo
%attr(755,root,root) %{_libdir}/grass%{gver}/utils/g.html2man.py
%attr(755,root,root) %{_libdir}/grass%{gver}/utils/generate_last_commit_file.py
%{_libdir}/grass%{gver}/utils/ggroff.py*
%{_libdir}/grass%{gver}/utils/ghtml.py*
%attr(755,root,root) %{_libdir}/grass%{gver}/utils/mkhtml.py
%{_libdir}/grass%{gver}/translation_status.json
# default (demo?) database - subpackage?
%{_libdir}/grass%{gver}/demolocation
%{_datadir}/metainfo/org.osgeo.grass.appdata.xml
%{_desktopdir}/grass.desktop
%{_iconsdir}/hicolor/*x*/apps/grass.png
%{_iconsdir}/hicolor/scalable/apps/grass.svg
%{_mandir}/man1/d.*.1*
%{_mandir}/man1/db.*.1*
%{_mandir}/man1/g.*.1*
%{_mandir}/man1/*_graphical.1*
%{_mandir}/man1/graphical_index.1*
%{_mandir}/man1/grass*.1*
%{_mandir}/man1/i.*.1*
%{_mandir}/man1/lrs.1*
%{_mandir}/man1/m.*.1*
%{_mandir}/man1/manual_gallery.1*
%{_mandir}/man1/miscellaneous.1*
%{_mandir}/man1/parser_standard_options.1*
%{_mandir}/man1/ps.map.1*
%{_mandir}/man1/r.*.1*
%{_mandir}/man1/r3.*.1*
%{_mandir}/man1/t.*.1*
%{_mandir}/man1/topic_*.1*
%{_mandir}/man1/v.*.1*
%{_mandir}/man1/wxGUI.1*
%{_mandir}/man1/wxGUI.*.1*
%{_mandir}/man1/wxpyimgview.1*
%{_mandir}/man1/ximgview.1*

%files devel
%defattr(644,root,root,755)
%doc dist.*/docs/html/*
%attr(755,root,root) %{_libdir}/libgrass_*[!0-9].so
%attr(755,root,root) %{_libdir}/libgrass_btree2.so
%attr(755,root,root) %{_libdir}/libgrass_dig2.so
%{_includedir}/grass%{gver}
