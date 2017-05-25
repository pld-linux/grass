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
Version:	7.0.3
Release:	3
Epoch:		1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://grass.osgeo.org/grass70/source/%{name}-%{version}.tar.gz
# Source0-md5:	dfbd39829036ee2d59b13c35a183ec0e
Patch0:		%{name}-soname.patch
Patch1:		%{name}-ac.patch
Patch2:		%{name}-format.patch
Patch3:		%{name}-ctypesgen.patch
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
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	python-wxPython
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.0
%{?with_odbc:BuildRequires:	unixODBC-devel}
BuildRequires:	wxGTK2-unicode-devel >= 2.8.1
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	zlib-devel
# R language?
Requires:	proj >= 4.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gver	%{version}
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%{__sed} -i -e '1s,/usr/bin/env perl,%{__perl},' \
	display/d.text/test.pl
	raster/r.topidx/gridatb.to.arc.pl \
	raster/r.topidx/arc.to.gridatb.pl

find general gui imagery lib/python/pygrass lib/init raster scripts temporal tools -name '*.py' | xargs grep -l '/usr/bin/env python' | xargs %{__sed} -i -e '1s,/usr/bin/env python,%{__python},'

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%configure \
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
	--with-wxwidgets=/usr/bin/wx-gtk2-unicode-config

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_libdir} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	PREFIX=$RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT{%{_datadir},%{_includedir}/grass70}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/include/* $RPM_BUILD_ROOT%{_includedir}/grass70
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/lib/* $RPM_BUILD_ROOT%{_libdir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/locale $RPM_BUILD_ROOT%{_datadir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/docs/man $RPM_BUILD_ROOT%{_datadir}
%{__mv} $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/share/{appdata,applications,icons} $RPM_BUILD_ROOT%{_datadir}

# these manual cover topics, not programs, so shouldn't exist in section 1
# (maybe in section 7, but names are too common anyway); keep HTML version only
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{cairodriver,database,databaseintro,display,displaydrivers,full_index,general,helptext,htmldriver,imagery,imageryintro,index,keywords,misc,pngdriver,postscript,projectionintro,psdriver,raster,rasterintro,raster3d,raster3dintro,sql,temporal,temporalintro,topics,variables,vector,vectorascii,vectorintro}.1

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/docs

%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{pt_br,pt_BR}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/locale/{zh,zh_CN}

%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/AUTHORS
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/CHANGES
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/COPYING
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/GPL.TXT
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/REQUIREMENTS.html

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CHANGES COPYING README TODO
#%attr(755,root,root) %{_bindir}/grass70
%attr(755,root,root) %{_libdir}/libgrass_*.%{version}.so
%dir %{_libdir}/grass-%{gver}
%dir %{_libdir}/grass-%{gver}/*.csv
%attr(755,root,root) %{_libdir}/grass-%{gver}/config.status
%attr(755,root,root) %{_libdir}/grass-%{gver}/bin
%attr(755,root,root) %{_libdir}/grass-%{gver}/driver
%dir %{_libdir}/grass-%{gver}/etc
%{_libdir}/grass-%{gver}/etc/VERSIONNUMBER
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/clean_temp
%{_libdir}/grass-%{gver}/etc/colors
%{_libdir}/grass-%{gver}/etc/colors.desc
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/current_time_s_ms
%{_libdir}/grass-%{gver}/etc/d.polar
%{_libdir}/grass-%{gver}/etc/db.test
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/echo
%{_libdir}/grass-%{gver}/etc/element_list
%{_libdir}/grass-%{gver}/etc/fontcap
%{_libdir}/grass-%{gver}/etc/grass70.py
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/i.find
%{_libdir}/grass-%{gver}/etc/license
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/lister
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/lock
%{_libdir}/grass-%{gver}/etc/paint
%{_libdir}/grass-%{gver}/etc/proj
%{_libdir}/grass-%{gver}/etc/psdriver.ps
%{_libdir}/grass-%{gver}/etc/python
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.in.wms
%dir %{_libdir}/grass-%{gver}/etc/r.watershed
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.watershed/ram
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.watershed/seg
%{_libdir}/grass-%{gver}/etc/renamed_options
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/run
%{_libdir}/grass-%{gver}/etc/sql
%{_libdir}/grass-%{gver}/etc/symbol
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/wxpyimgview_gui.py
%{_libdir}/grass-%{gver}/fonts
%dir %{_libdir}/grass-%{gver}/gui
%{_libdir}/grass-%{gver}/gui/icons
%{_libdir}/grass-%{gver}/gui/images
%dir %{_libdir}/grass-%{gver}/gui/scripts
%attr(755,root,root) %{_libdir}/grass-%{gver}/gui/scripts/d.*
%dir %{_libdir}/grass-%{gver}/gui/wxpython
%{_libdir}/grass-%{gver}/gui/wxpython/README
%{_libdir}/grass-%{gver}/gui/wxpython/animation
%{_libdir}/grass-%{gver}/gui/wxpython/core
%{_libdir}/grass-%{gver}/gui/wxpython/dbmgr
%{_libdir}/grass-%{gver}/gui/wxpython/gcp
%{_libdir}/grass-%{gver}/gui/wxpython/gmodeler
%{_libdir}/grass-%{gver}/gui/wxpython/gui_core
%{_libdir}/grass-%{gver}/gui/wxpython/iclass
%{_libdir}/grass-%{gver}/gui/wxpython/icons
%{_libdir}/grass-%{gver}/gui/wxpython/iscatt
%{_libdir}/grass-%{gver}/gui/wxpython/lmgr
%{_libdir}/grass-%{gver}/gui/wxpython/location_wizard
%{_libdir}/grass-%{gver}/gui/wxpython/mapdisp
%{_libdir}/grass-%{gver}/gui/wxpython/mapswipe
%{_libdir}/grass-%{gver}/gui/wxpython/mapwin
%{_libdir}/grass-%{gver}/gui/wxpython/modules
%{_libdir}/grass-%{gver}/gui/wxpython/nviz
%{_libdir}/grass-%{gver}/gui/wxpython/psmap
%{_libdir}/grass-%{gver}/gui/wxpython/rlisetup
%{_libdir}/grass-%{gver}/gui/wxpython/timeline
%{_libdir}/grass-%{gver}/gui/wxpython/tplot
%{_libdir}/grass-%{gver}/gui/wxpython/vdigit
%{_libdir}/grass-%{gver}/gui/wxpython/vnet
%{_libdir}/grass-%{gver}/gui/wxpython/web_services
%{_libdir}/grass-%{gver}/gui/wxpython/wxplot
%{_libdir}/grass-%{gver}/gui/wxpython/xml
%{_libdir}/grass-%{gver}/gui/wxpython/gis_set*.py*
%{_libdir}/grass-%{gver}/gui/wxpython/wxgui.py*
%{_libdir}/grass-%{gver}/gui/xml
%attr(755,root,root) %{_libdir}/grass-%{gver}/scripts
%dir %{_libdir}/grass-%{gver}/tools
%attr(755,root,root) %{_libdir}/grass-%{gver}/tools/g.echo
%attr(755,root,root) %{_libdir}/grass-%{gver}/tools/g.html2man.py
%{_libdir}/grass-%{gver}/tools/groff.py*
%{_libdir}/grass-%{gver}/tools/html.py*
%attr(755,root,root) %{_libdir}/grass-%{gver}/tools/mkhtml.py
%{_libdir}/grass-%{gver}/translation_status.json
# default (demo?) database - subpackage?
%{_libdir}/grass-%{gver}/demolocation
%{_datadir}/appdata/grass.appdata.xml
%{_desktopdir}/grass.desktop
%{_iconsdir}/hicolor/*x*/apps/grass70.png
%{_iconsdir}/hicolor/scalable/apps/grass70.svg
%{_mandir}/man1/d.*.1*
%{_mandir}/man1/db.*.1*
%{_mandir}/man1/g.*.1*
%{_mandir}/man1/grass7.1*
%{_mandir}/man1/grass-*.1*
%{_mandir}/man1/i.*.1*
%{_mandir}/man1/lrs.1*
%{_mandir}/man1/m.*.1*
%{_mandir}/man1/ps.map.1*
%{_mandir}/man1/r.*.1*
%{_mandir}/man1/r3.*.1*
%{_mandir}/man1/t.*.1*
%{_mandir}/man1/topic_*.1*
%{_mandir}/man1/v.*.1*
%{_mandir}/man1/wximgview.1*
%{_mandir}/man1/wxpyimgview.1*
%{_mandir}/man1/wxGUI*.1*
%{_mandir}/man1/ximgview.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgrass_*[!0-9].so
%attr(755,root,root) %{_libdir}/libgrass_btree2.so
%attr(755,root,root) %{_libdir}/libgrass_dig2.so
%{_libdir}/libgrass_iostream.%{version}.a
%{_includedir}/grass70

%files doc
%defattr(644,root,root,755)
%doc dist.*/docs/html/*
