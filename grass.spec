#
# Conditional build, see http://grass.itc.it/grass61/source/REQUIREMENTS.html
# for description of optional requirements.
%bcond_without	tcl		# disable gui and nviz
%bcond_without	mysql	# disable mysql support
%bcond_without	odbc	# disable unixODBC support
%bcond_without	xanim	# disable xanim module
#

%define		rcver	RC6
Summary:	The Geographic Resources Analysis Support System
Summary(pl.UTF-8):	System obsługujący analizę zasobów geograficznych
Name:		grass
Version:	6.3.0
Release:	0.%{rcver}.1
Epoch:		1
License:	GPL
Group:		X11/Applications
Source0:	http://grass.osgeo.org/grass63/source/%{name}-%{version}%{rcver}.tar.gz
# Source0-md5:	16c70918f0f92fe1edb787f4bf2f4177
Patch0:		%{name}-soname.patch
Patch1:		%{name}-link.patch
Patch2:		%{name}-ffmpeg.patch
URL:		http://grass.osgeo.org/
%{?with_tcl:BuildRequires:	OpenGL-GLU-devel}
BuildRequires:	awk
BuildRequires:	bison
BuildRequires:	blas-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	fftw3-devel
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gcc-g77
BuildRequires:	gdal-devel
BuildRequires:	gdbm-devel
BuildRequires:	gd-devel
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
BuildRequires:	zlib-devel
# R language?
Requires:	proj >= 4.4.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		gver	%{version}%{rcver}
%define		_noautoreqdep   libGL.so.1 libGLU.so.1
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
%setup -q -n %{name}-%{gver}
%patch0 -p1
%patch1 -p1
#%patch2 -p1

%build
CPPFLAGS="-I/usr/include/ncurses"; export CPPFLAGS
%configure2_13 \
	--enable-largefile \
	--with-includes=%{_includedir} \
	--with-libs=%{_libdir} \
	--with-blas \
	--with-cxx \
	--with-ffmpeg \
	--with-ffmpeg-includes=/usr/include/ffmpeg \
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
	--with%{!?with_tcl:out}-tcltk
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_libdir} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	PREFIX=$RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT{%{_datadir},%{_includedir}/grass63}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/include/* $RPM_BUILD_ROOT%{_includedir}/grass63
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/lib/* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/locale $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/man $RPM_BUILD_ROOT%{_datadir}

sed -i -e 's,^GISBASE=.*,GISBASE=%{_libdir}/grass-%{gver},' $RPM_BUILD_ROOT%{_bindir}/grass63

cp -f lib/external/bwidget/CHANGES.txt bwidget.CHANGES.TXT
cp -f lib/external/bwidget/README.grass bwidget.README.grass

rm -rf $RPM_BUILD_ROOT%{_libdir}/grass-%{gver}/{bwidget/{*.txt,README.grass},docs}

mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{pt_br,pt_BR}
mv -f $RPM_BUILD_ROOT%{_datadir}/locale/{zh,zh_CN}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS CHANGES COPYING README TODO bwidget.CHANGES.TXT bwidget.README.grass dist.%{_target_platform}/docs/html
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/*.so
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
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/bmif_to_cell
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/c[!e]*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/d[.b]*
%{_libdir}/grass-%{gver}/etc/d[ai]*
%{_libdir}/grass-%{gver}/etc/gintro.gif
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/grass-xterm-wrapper
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/file_option.tcl
%{_libdir}/grass-%{gver}/etc/fontcap
%{_libdir}/grass-%{gver}/etc/gem
%{_libdir}/grass-%{gver}/etc/grass_write_ascii.style
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/grocat
%dir %{_libdir}/grass-%{gver}/etc/gui
%{_libdir}/grass-%{gver}/etc/gui/icons
%{_libdir}/grass-%{gver}/etc/gtcltk
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/mod*
%dir %{_libdir}/grass-%{gver}/etc/msgs
%lang(cs) %{_libdir}/grass-%{gver}/etc/msgs/cs.msg
%lang(de) %{_libdir}/grass-%{gver}/etc/msgs/de.msg
%lang(es) %{_libdir}/grass-%{gver}/etc/msgs/es.msg
%lang(fr) %{_libdir}/grass-%{gver}/etc/msgs/fr.msg
%lang(it) %{_libdir}/grass-%{gver}/etc/msgs/it.msg
%lang(ja) %{_libdir}/grass-%{gver}/etc/msgs/ja.msg
%lang(lv) %{_libdir}/grass-%{gver}/etc/msgs/lv.msg
%lang(pl) %{_libdir}/grass-%{gver}/etc/msgs/pl.msg
%lang(pt_BR) %{_libdir}/grass-%{gver}/etc/msgs/pt_br.msg
%lang(ru) %{_libdir}/grass-%{gver}/etc/msgs/ru.msg
%lang(tr) %{_libdir}/grass-%{gver}/etc/msgs/tr.msg
%lang(vi) %{_libdir}/grass-%{gver}/etc/msgs/vi.msg
%{_libdir}/grass-%{gver}/etc/nad
%{_libdir}/grass-%{gver}/etc/ogr_csv
%dir %{_libdir}/grass-%{gver}/etc/paint
%{_libdir}/grass-%{gver}/etc/paint/patterns
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/poly_to_bmif
%{_libdir}/grass-%{gver}/etc/paint/prolog.ps
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/prompt.sh
#%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/water
%{_libdir}/grass-%{gver}/etc/proj-*
%{_libdir}/grass-%{gver}/etc/psdriver.ps
%{_libdir}/grass-%{gver}/etc/FIPS.code
%{_libdir}/grass-%{gver}/etc/VERSION*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/[Iilv]*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/echo
%{_libdir}/grass-%{gver}/etc/el*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/epsg_option.tcl
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/frame.*
#%{_libdir}/grass-%{gver}/etc/freetypecap
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/g.mapsets.tcl
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/gis_set.tcl
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/grass-run.sh
%{_libdir}/grass-%{gver}/etc/grass_intro
%{_libdir}/grass-%{gver}/etc/gui.tcl
#%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/help.tcl
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/mon.*
#%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/make_location_epsg.sh
%{_libdir}/grass-%{gver}/etc/monitorcap
%{_libdir}/grass-%{gver}/etc/projections
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/r[!g]*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/photo.*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/s[!t]*
%{_libdir}/grass-%{gver}/etc/state*
%{_libdir}/grass-%{gver}/etc/welcome
%{_libdir}/grass-%{gver}/fonts
%attr(755,root,root) %{_libdir}/grass-%{gver}/scripts
%{_mandir}/man1/*

%if %{with tcl}
%dir %{_libdir}/grass-%{gver}/etc/dm
%{_libdir}/grass-%{gver}/etc/dm/*.gif
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/dm/*.tcl
%dir %{_libdir}/grass-%{gver}/etc/dm/script
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/dm/script/*
%dir %{_libdir}/grass-%{gver}/etc/form
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/form/form
%{_libdir}/grass-%{gver}/etc/form/*.tcl
%dir %{_libdir}/grass-%{gver}/etc/gm
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/gm/*.tcl
%{_libdir}/grass-%{gver}/etc/gm/*.gif
%dir %{_libdir}/grass-%{gver}/etc/gm/script
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/gm/script/*
%dir %{_libdir}/grass-%{gver}/etc/gui/menus
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/gui/menus/menu.tcl
%dir %{_libdir}/grass-%{gver}/etc/nviz2.2
%{_libdir}/grass-%{gver}/etc/nviz2.2/bitmaps
%dir %{_libdir}/grass-%{gver}/etc/nviz2.2/scripts
%{_libdir}/grass-%{gver}/etc/nviz2.2/scripts/[!ns]*
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/nviz2.2/scripts/nviz2.2_script
%{_libdir}/grass-%{gver}/etc/nviz2.2/scripts/nviz_init.tcl
%{_libdir}/grass-%{gver}/etc/nviz2.2/scripts/nviz_params
%{_libdir}/grass-%{gver}/etc/nviz2.2/scripts/s[!c]*
%{_libdir}/grass-%{gver}/etc/nviz2.2/scripts/script_support.tcl
%attr(755,root,root) %{_libdir}/grass-%{gver}/etc/nviz2.2/scripts/script_[!s]*
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/grass63
%{_libdir}/*.a
