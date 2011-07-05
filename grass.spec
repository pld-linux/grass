#
# Conditional build, see http://grass.itc.it/grass61/source/REQUIREMENTS.html
# for description of optional requirements.
%bcond_without	tcl	# disable gui and nviz
%bcond_without	mysql	# disable MySQL support
%bcond_without	odbc	# disable unixODBC support
%bcond_without	xanim	# disable xanim module

Summary:	The Geographic Resources Analysis Support System
Summary(pl.UTF-8):	System obsługujący analizę zasobów geograficznych
Name:		grass
Version:	6.4.1
Release:	1
Epoch:		1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://grass.osgeo.org/grass64/source/%{name}-%{version}.tar.gz
# Source0-md5:	d8ca83d416b5b0cf2aa9d36c81a77b23
Patch0:		%{name}-soname.patch
Patch1:		ncurses.patch
URL:		http://grass.osgeo.org/
BuildRequires:	Mesa-libGLw-devel
%{?with_tcl:BuildRequires:	OpenGL-GLU-devel}
BuildRequires:	bison
BuildRequires:	blas-devel
BuildRequires:	cairo-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	fftw3-devel
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
BuildRequires:	man
%{?with_xanim:BuildRequires:	motif-devel}
%{?with_mysql:BuildRequires:	mysql-devel}
BuildRequires:	ncurses-devel
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	proj-devel >= 4.4.6
BuildRequires:	proj-progs
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel >= 3.0
%{?with_tcl:BuildRequires:	tcl-devel >= 8.4}
%{?with_tcl:BuildRequires:	tk-devel >= 8.4}
%{?with_odbc:BuildRequires:	unixODBC-devel}
BuildRequires:	wxGTK2-unicode-devel
BuildRequires:	zlib-devel
# R language?
Requires:	proj >= 4.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gver	%{version}
%define		_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_sysconfdir	/etc/X11
%define		_target_platform %(echo %{_target_cpu}-%{_target_vendor}-%{_host_os} | sed -e 's/athlon/i686/;s/ppc/powerpc/;s/amd64/x86_64/')

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

%description devel
Header files and static libraries for GRASS.

%description devel -l pl.UTF-8
Pliki nagłówkowe i biblioteki statyczne systemu GRASS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

cp -f lib/external/bwidget/CHANGES.txt bwidget.CHANGES.TXT
cp -f lib/external/bwidget/README.grass bwidget.README.grass

%build
%if 0
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%endif
CPPFLAGS="-I/usr/include/ncurses"
%configure2_13 \
%if "%{_lib}" != "lib"
        --enable-64bit \
%endif
	--enable-largefile \
	--with-includes=%{_includedir} \
	--with-libs=%{_libdir} \
	--with-blas \
	--with-cairo \
	--with-cxx \
	--with-ffmpeg \
	--with-ffmpeg-includes='/usr/include/libavcodec /usr/include/libavformat /usr/include/libswscale' \
	--with-freetype \
	--with-freetype-includes=/usr/include/freetype2 \
	--with-lapack \
	%{?with_xanim:--with-motif} \
	%{?with_mysql:--with-mysql} \
	%{?with_mysql:--with-mysql-includes=/usr/include/mysql} \
	--with-nls \
	%{?with_odbc:--with-odbc} \
	--with%{!?with_tcl:out}-opengl \
	--with-postgres \
	--with-postgres-includes=/usr/include/postgresql/server \
	--with-proj-share=/usr/share/proj \
	--with-python \
	--with-readline \
	--with-sqlite \
	--with%{!?with_tcl:out}-tcltk \
	--with-wxwidgets=/usr/bin/wx-gtk2-unicode-config
# --with-glw requires Motif parts in -lGLw or -lGLwM
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_libdir} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	PREFIX=$RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT{%{_datadir},%{_includedir}/grass64}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/include/* $RPM_BUILD_ROOT%{_includedir}/grass64
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/lib/* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/locale $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/man $RPM_BUILD_ROOT%{_datadir}

sed -i -e 's,^GISBASE=.*,GISBASE=%{_libdir}/grass-%{gver},' $RPM_BUILD_ROOT%{_bindir}/grass64

%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/{bwidget/{*.txt,README.grass},docs}

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{pt_br,pt_BR}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{zh,zh_CN}

rm $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/AUTHORS
rm $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/CHANGES
rm $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/COPYING
rm $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/GPL.TXT
rm $RPM_BUILD_ROOT%{_libdir}/%{name}-%{version}/REQUIREMENTS.html

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CHANGES COPYING README TODO bwidget.CHANGES.TXT bwidget.README.grass
#%doc dist.%{_target_platform}/docs/html
%attr(755,root,root) %{_bindir}/gem64
%attr(755,root,root) %{_bindir}/grass64
%attr(755,root,root) %{_libdir}/libgrass_*.so
%dir %{_libdir}/grass-%{gver}
%attr(755,root,root) %{_libdir}/grass-%{gver}/bin
%dir %{_libdir}/grass-%{gver}/bwidget
%{_libdir}/grass-%{gver}/bwidget/*.tcl
%{_libdir}/grass-%{gver}/bwidget/images
%dir %{_libdir}/grass-%{gver}/bwidget/lang
%lang(de) %{_libdir}/grass-%{gver}/bwidget/lang/de.rc
%{_libdir}/grass-%{gver}/bwidget/lang/en.rc
%lang(es) %{_libdir}/grass-%{gver}/bwidget/lang/es.rc
%lang(fr) %{_libdir}/grass-%{gver}/bwidget/lang/fr.rc
%attr(755,root,root) %{_libdir}/grass-%{gver}/driver
%dir %{_libdir}/grass-%{gver}/etc
%{_libdir}/grass-%{gver}/etc/FIPS.code
%{_libdir}/grass-%{gver}/etc/VERSIONNUMBER
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/Init.sh
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/bmif_to_cell
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/clean_temp
%{_libdir}/grass-%{gver}/etc/colors
%{_libdir}/grass-%{gver}/etc/colors.desc
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/current_time_s_ms
%{_libdir}/grass-%{gver}/etc/d.polar
%{_libdir}/grass-%{gver}/etc/d.rast.edit.tcl
%{_libdir}/grass-%{gver}/etc/datum*.table
%{_libdir}/grass-%{gver}/etc/db.test
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/echo
%{_libdir}/grass-%{gver}/etc/element_list
%{_libdir}/grass-%{gver}/etc/ellipse.table
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/epsg_option.tcl
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/file_option.tcl
%{_libdir}/grass-%{gver}/etc/fontcap
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/frame.*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/g.mapsets.tcl
%{_libdir}/grass-%{gver}/etc/gem
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/gis_set.tcl
%{_libdir}/grass-%{gver}/etc/grass-interface.dtd
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/grass-run.sh
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/grass-xterm-wrapper
%{_libdir}/grass-%{gver}/etc/grass_intro
%{_libdir}/grass-%{gver}/etc/grass_write_ascii.style
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/grocat
%{_libdir}/grass-%{gver}/etc/gtcltk
%dir %{_libdir}/grass-%{gver}/etc/gui
%{_libdir}/grass-%{gver}/etc/gui/icons
%{_libdir}/grass-%{gver}/etc/gui/images
%dir %{_libdir}/grass-%{gver}/etc/gui/scripts
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/gui/scripts/*
%{_libdir}/grass-%{gver}/etc/gui.tcl
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/i.ask
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/i.find
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/i.oif
%{_libdir}/grass-%{gver}/etc/license
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/lister
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/lock
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/modcats
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/modcolr
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/modhead
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/modhist
%{_libdir}/grass-%{gver}/etc/monitorcap
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/mon.*
%dir %{_libdir}/grass-%{gver}/etc/msgs
%lang(am) %{_libdir}/grass-%{gver}/etc/msgs/am.msg
%lang(ar) %{_libdir}/grass-%{gver}/etc/msgs/ar.msg
%lang(cs) %{_libdir}/grass-%{gver}/etc/msgs/cs.msg
%lang(de) %{_libdir}/grass-%{gver}/etc/msgs/de.msg
%lang(el) %{_libdir}/grass-%{gver}/etc/msgs/el.msg
%lang(es) %{_libdir}/grass-%{gver}/etc/msgs/es.msg
%lang(fr) %{_libdir}/grass-%{gver}/etc/msgs/fr.msg
%lang(hi) %{_libdir}/grass-%{gver}/etc/msgs/hi.msg
%lang(id) %{_libdir}/grass-%{gver}/etc/msgs/id.msg
%lang(it) %{_libdir}/grass-%{gver}/etc/msgs/it.msg
%lang(ja) %{_libdir}/grass-%{gver}/etc/msgs/ja.msg
%lang(ko) %{_libdir}/grass-%{gver}/etc/msgs/ko.msg
%lang(lv) %{_libdir}/grass-%{gver}/etc/msgs/lv.msg
%lang(mr) %{_libdir}/grass-%{gver}/etc/msgs/mr.msg
%lang(pl) %{_libdir}/grass-%{gver}/etc/msgs/pl.msg
%lang(pt) %{_libdir}/grass-%{gver}/etc/msgs/pt.msg
%lang(pt_BR) %{_libdir}/grass-%{gver}/etc/msgs/pt_br.msg
%lang(ru) %{_libdir}/grass-%{gver}/etc/msgs/ru.msg
%lang(sl) %{_libdir}/grass-%{gver}/etc/msgs/sl.msg
%lang(th) %{_libdir}/grass-%{gver}/etc/msgs/th.msg
%lang(tr) %{_libdir}/grass-%{gver}/etc/msgs/tr.msg
%lang(vi) %{_libdir}/grass-%{gver}/etc/msgs/vi.msg
%lang(zh_CN) %{_libdir}/grass-%{gver}/etc/msgs/zh.msg
%{_libdir}/grass-%{gver}/etc/nad
%{_libdir}/grass-%{gver}/etc/ogr_csv
%{_libdir}/grass-%{gver}/etc/paint
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/photo.*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/poly_to_bmif
%{_libdir}/grass-%{gver}/etc/proj-*.table
%{_libdir}/grass-%{gver}/etc/projections
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/prompt.sh
%{_libdir}/grass-%{gver}/etc/psdriver.ps
%{_libdir}/grass-%{gver}/etc/python
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.in.wms
%dir %{_libdir}/grass-%{gver}/etc/r.li.setup
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.li.setup/area_query
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.li.setup/masked_area_selection
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.li.setup/r.li.*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.li.setup/sample_area_vector.sh
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.li.setup/square_*
%{_libdir}/grass-%{gver}/etc/r.li.setup/*.txt
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r.watershed.*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/run
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/set_data
%{_libdir}/grass-%{gver}/etc/state*
%{_libdir}/grass-%{gver}/etc/symbol
%{_libdir}/grass-%{gver}/etc/v.digit
%{_libdir}/grass-%{gver}/etc/welcome
%dir %{_libdir}/grass-%{gver}/etc/wxpython
%{_libdir}/grass-%{gver}/etc/wxpython/README
%{_libdir}/grass-%{gver}/etc/wxpython/compat
%{_libdir}/grass-%{gver}/etc/wxpython/gis_set.py
%{_libdir}/grass-%{gver}/etc/wxpython/gui_modules
%{_libdir}/grass-%{gver}/etc/wxpython/icons
%{_libdir}/grass-%{gver}/etc/wxpython/images
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/wxpython/scripts
%{_libdir}/grass-%{gver}/etc/wxpython/wxgui.py
%{_libdir}/grass-%{gver}/etc/wxpython/xml
%{_libdir}/grass-%{gver}/fonts
%attr(755,root,root) %{_libdir}/grass-%{gver}/scripts
%dir %{_libdir}/grass-%{gver}/tools
%attr(755,root,root) %{_libdir}/grass-%{gver}/tools/mkhtml.sh
%{_mandir}/man1/cairodriver.1*
%{_mandir}/man1/d.*.1*
%{_mandir}/man1/databaseintro.1*
%{_mandir}/man1/db.*.1*
%{_mandir}/man1/displaydrivers.1*
%{_mandir}/man1/g.*.1*
%{_mandir}/man1/gis.m.1*
%{_mandir}/man1/gm_*.1*
%{_mandir}/man1/grass6.1*
%{_mandir}/man1/grass-*.1*
%{_mandir}/man1/helptext.1*
%{_mandir}/man1/htmlmapdriver.1*
%{_mandir}/man1/i.*.1*
%{_mandir}/man1/imageryintro.1*
%{_mandir}/man1/lrs.1*
%{_mandir}/man1/m.*.1*
%{_mandir}/man1/mkftcap.1*
%{_mandir}/man1/modcats.1*
%{_mandir}/man1/modcolr.1*
%{_mandir}/man1/modhead.1*
%{_mandir}/man1/modhist.1*
%{_mandir}/man1/nviz.1*
%{_mandir}/man1/nviz_cmd.1*
%{_mandir}/man1/p.out.vrml.1*
%{_mandir}/man1/photo.*.1*
%{_mandir}/man1/pngdriver.1*
%{_mandir}/man1/projectionintro.1*
%{_mandir}/man1/psdriver.1*
%{_mandir}/man1/ps.map.1*
%{_mandir}/man1/r.*.1*
%{_mandir}/man1/r3.*.1*
%{_mandir}/man1/raster3dintro.1*
%{_mandir}/man1/rasterintro.1*
%{_mandir}/man1/sql.1*
%{_mandir}/man1/v.*.1*
%{_mandir}/man1/variables.1*
%{_mandir}/man1/vectorintro.1*
%{_mandir}/man1/wxGUI*.1*
%{_mandir}/man1/xdriver.1*
%{_mandir}/man1/xganim.1*

%if %{with tcl}
%dir %{_libdir}/grass-%{gver}/etc/dm
%{_libdir}/grass-%{gver}/etc/dm/*.gif
%{_libdir}/grass-%{gver}/etc/dm/[!d]*.tcl
%{_libdir}/grass-%{gver}/etc/dm/d[!.]*.tcl
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/dm/d.m.tcl
%dir %{_libdir}/grass-%{gver}/etc/dm/script
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/dm/script/*
%dir %{_libdir}/grass-%{gver}/etc/form
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/form/form
%{_libdir}/grass-%{gver}/etc/form/*.tcl
%dir %{_libdir}/grass-%{gver}/etc/gm
%{_libdir}/grass-%{gver}/etc/gm/intro.gif
%{_libdir}/grass-%{gver}/etc/gm/*.tcl
%dir %{_libdir}/grass-%{gver}/etc/nviz2.2
%{_libdir}/grass-%{gver}/etc/nviz2.2/bitmaps
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/nviz2.2/nviz
%dir %{_libdir}/grass-%{gver}/etc/nviz2.2/scripts
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/nviz2.2/scripts/*
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/libgrass_iostream.a
%{_libdir}/libgrass_ismap.a
%{_libdir}/libgrass_manage.a
%{_includedir}/grass64
