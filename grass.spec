Summary:	The Geographic Resources Analysis Support System
Summary(pl):	System obs³uguj±cy analizê zasobów geograficznych
Name:		grass
Version:	6.0.1
Release:	1
Epoch:		1
License:	GPL
Group:		X11/Applications
Source0:	ftp://grass.itc.it/pub/grass/grass60/source/%{name}-%{version}.tar.gz
# Source0-md5:	5225e816895d5e6b28bca623f76acaad
Patch0:		%{name}-tk85.patch
Patch1:		%{name}-soname.patch
URL:		http://grass.itc.it/
BuildRequires:	OpenGL-devel
BuildRequires:	awk
BuildRequires:	bison
BuildRequires:	blas-devel
BuildRequires:	fftw-devel
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
BuildRequires:	motif-devel
BuildRequires:	mysql-devel
BuildRequires:	ncurses-devel
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	proj-devel
BuildRequires:	proj-progs
BuildRequires:	readline-devel
BuildRequires:	sed >= 4.0
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	unixODBC-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautoreqdep   libGL.so.1 libGLU.so.1
%define		_sysconfdir	/etc/X11
%define		_target_platform %(echo %{_target_cpu}-%{_target_vendor}-%{_host_os} | sed -e 's/athlon/i686/;s/ppc/powerpc/')

%description
GRASS (the Geographic Resources Analysis Support System) is a software
raster- and vector-based GIS (Geographic Information System), image
processing system, graphics production system, and spatial modeling
system. GRASS contains many modules for raster data manipulation,
vector data manipulation, rendering images on the monitor or paper,
multispectral image processing, point data management and general data
management. It also has tools for interfacing with digitizers,
scanners, and the RIM, Informix, Postgres, and Oracle databases.

%description -l pl
GRASS (System Wspierania Analiz Zasobów Geograficznych) jest rastrowym
oraz wektorowym systemem GIS (System Informacji Geograficznej),
obróbki obrazów, tworzenia grafiki oraz modelowania przestrzennego.
GRASS zawiera wiele modu³ów wspomagaj±cych manipulacjê danymi
rastrowymi i wektorowymi, renderowanie obrazów na monitorze lub
papierze, obróbkê multispektralnych obrazów, punktowe oraz ogólne
zarz±dzanie danymi. Zawiera równie¿ narzêdzia do wspó³pracy z
digitizerami, skanerami oraz bazami RIM, Informix, Postgres oraz
Oracle.

%package OpenGL
Summary:	NVIZ - a 3D-tool for GRASS
Summary(pl):	NVIZ - narzêdzie 3D dla GRASSa
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}

%description OpenGL
Package contains nviz, which is a GRASS module-in-progress which
allows users to realistically render multiple surfaces in a 3D space,
optionally using thematic coloring, draping GRASS vector files over
the surfaces, and displaying GRASS site files either draped on the
surfaces or as 3D point locations.

%description OpenGL -l pl
Pakiet zawiera modu³ nviz, który rozszerza funkcjonalno¶æ systemu
GRASS o mo¿liwo¶æ realistycznego renderowania wielu powierzchni w
trójwymiarowej przestrzeni. Na renderowanych powierzchniach, które
mog± byæ tematycznie kolorowane, mo¿na zawieszaæ pliki wektorowe
GRASSa.

%package pg
Summary:	PostgreSQL database interface
Summary(pl):	Interfejs do bazy PostgreSQL
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}

%description pg
PostgreSQL database interface for GRASS.

%description pg -l pl
Interfejs do bazy PostgreSQL dla GRASSa.

%package odbc
Summary:	ODBC database interface
Summary(pl):	Interfejs ODBC dla GRASSa
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}

%description odbc
ODBC database interface for GRASS.

%description odbc -l pl
Interfejs ODBC dla GRASSa.

%package devel
Summary:	Header files and static libraries for GRASS
Summary(pl):	Pliki nag³ówkowe i biblioteki statyczne systemu GRASS
Group:		X11/Development/Libraries

%description devel
Header files and static libraries for GRASS.

%description devel -l pl
Pliki nag³ówkowe i biblioteki statyczne systemu GRASS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"; export CFLAGS
CPPFLAGS="-I/usr/include/ncurses -I/usr/X11R6/include"; export CPPFLAGS
%configure2_13 \
	--with-includes=%{_includedir} \
	--with-libs=%{_libdir} \
	--with-blas \
	--with-cxx \
	--with-freetype \
	--with-freetype-includes=/usr/include/freetype2 \
	--with-lapack \
	--with-motif \
	--with-mysql \
	--with-mysql-includes=/usr/include/mysql \
	--with-nls \
	--with-odbc \
	--with-postgres-includes=/usr/include/postgresql/server \
	--with-readline
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	prefix=$RPM_BUILD_ROOT%{_libdir} \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	PREFIX=$RPM_BUILD_ROOT%{_libdir}

install -d $RPM_BUILD_ROOT{%{_datadir},%{_includedir}/grass60}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/include/* $RPM_BUILD_ROOT%{_includedir}/grass60
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/lib/* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/locale $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/man $RPM_BUILD_ROOT%{_datadir}

sed -i -e 's,^GISBASE=.*,GISBASE=%{_libdir}/grass-%{version},' $RPM_BUILD_ROOT%{_bindir}/grass60

cp -f lib/external/bwidget/CHANGES.txt bwidget.CHANGES.TXT
cp -f lib/external/bwidget/README.grass bwidget.README.grass

rm -rf $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/{bwidget/{*.txt,README.grass},docs}

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
%dir %{_libdir}/grass-%{version}
%attr(755,root,root) %{_libdir}/grass-%{version}/bin
%dir %{_libdir}/grass-%{version}/bwidget
%{_libdir}/grass-%{version}/bwidget/*.tcl
%{_libdir}/grass-%{version}/bwidget/images
%dir %{_libdir}/grass-%{version}/bwidget/lang
%lang(de) %{_libdir}/grass-%{version}/bwidget/lang/de.rc
%{_libdir}/grass-%{version}/bwidget/lang/en.rc
%lang(es) %{_libdir}/grass-%{version}/bwidget/lang/es.rc
%lang(fr) %{_libdir}/grass-%{version}/bwidget/lang/fr.rc
%attr(755,root,root) %{_libdir}/grass-%{version}/driver
%dir %{_libdir}/grass-%{version}/etc
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/c[!e]*
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/d[.b]*
%{_libdir}/grass-%{version}/etc/d[ai]*
%dir %{_libdir}/grass-%{version}/etc/dm
%{_libdir}/grass-%{version}/etc/dm/*.gif
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/dm/*.tcl
%dir %{_libdir}/grass-%{version}/etc/dm/script
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/dm/script/*
%dir %{_libdir}/grass-%{version}/etc/form
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/form/form
%{_libdir}/grass-%{version}/etc/form/*.tcl
%{_libdir}/grass-%{version}/etc/gtcltk
%dir %{_libdir}/grass-%{version}/etc/msgs
%lang(ru) %{_libdir}/grass-%{version}/etc/msgs/ru.msg
%{_libdir}/grass-%{version}/etc/nad
%dir %{_libdir}/grass-%{version}/etc/nviz2.2
%{_libdir}/grass-%{version}/etc/nviz2.2/bitmaps
%dir %{_libdir}/grass-%{version}/etc/nviz2.2/scripts
%{_libdir}/grass-%{version}/etc/nviz2.2/scripts/[!ns]*
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/nviz2.2/scripts/nviz2.2_script
%{_libdir}/grass-%{version}/etc/nviz2.2/scripts/nviz_init.tcl
%{_libdir}/grass-%{version}/etc/nviz2.2/scripts/s[!c]*
%{_libdir}/grass-%{version}/etc/nviz2.2/scripts/script_support.tcl
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/nviz2.2/scripts/script_[!s]*
%{_libdir}/grass-%{version}/etc/ogr_csv
%dir %{_libdir}/grass-%{version}/etc/paint
%{_libdir}/grass-%{version}/etc/paint/prolog.ps
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/water
%{_libdir}/grass-%{version}/etc/FIPS.code
%{_libdir}/grass-%{version}/etc/VERSION*
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/[Iilv]*
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/echo
%{_libdir}/grass-%{version}/etc/el*
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/epsg_option.tcl
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/frame.*
%{_libdir}/grass-%{version}/etc/freetypecap
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/g.mapsets.tcl
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/gis_set.tcl
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/grass-run.sh
%{_libdir}/grass-%{version}/etc/grass_intro
%{_libdir}/grass-%{version}/etc/gui.tcl
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/help.tcl
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/mon.*
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/make_location_epsg.sh
%{_libdir}/grass-%{version}/etc/monitorcap
%{_libdir}/grass-%{version}/etc/projections
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/r[!g]*
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/photo.*
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/s[!t]*
%{_libdir}/grass-%{version}/etc/state*
%{_libdir}/grass-%{version}/etc/welcome
%{_libdir}/grass-%{version}/fonts
%attr(755,root,root) %{_libdir}/grass-%{version}/scripts
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/grass60
%{_libdir}/*.a
