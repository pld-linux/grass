#
# todo: 1. see %install section :-\
#
Summary:	The Geographic Resources Analysis Support System
Summary(pl):	System obs³uguj±cy analizê zasobów geograficznych
Name:		grass
Version:	5.0.0
Release:	5
Epoch:		1
License:	GPL
Group:		X11/Applications
Source0:	http://grass.itc.it/grass5/source/%{name}-%{version}_src.tar.gz
Patch1:		grass-athlon.patch
URL:		http://grass.itc.it/
BuildRequires:	OpenGL-devel
BuildRequires:	awk
BuildRequires:	bison
BuildRequires:	blas-devel
BuildRequires:	fftw-devel
BuildRequires:	flex
BuildRequires:	freetype-devel >= 2.0.0
BuildRequires:	gcc-g77
#BuildRequires:	gdal-devel
BuildRequires:	gdbm-devel
BuildRequires:	gd-devel
BuildRequires:	lapack-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	man
BuildRequires:	motif-devel
BuildRequires:	ncurses-devel
BuildRequires:	postgresql-backend-devel
BuildRequires:	postgresql-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	unixODBC-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautoreqdep   libGL.so.1 libGLU.so.1
%define		_sysconfdir	/etc/X11
%define		_target_platform %{_target_cpu}-%{_target_vendor}-%{_host_os}

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
Requires:	%{name} = %{version}

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
Requires:	%{name} = %{version}

%description pg
PostgreSQL database interface for GRASS.

%description pg -l pl
Interfejs do bazy PostgreSQL dla GRASSa.

%package odbc
Summary:	ODBC database interface
Summary(pl):	Interfejs ODBC dla GRASSa
Group:		X11/Applications
Requires:	%{name} = %{version}

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
%patch1 -p0

%build
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"; export CFLAGS
CPPFLAGS="-I/usr/include/ncurses"; export CPPFLAGS
%configure2_13 \
	--with-lapack \
	--with-nls \
	--with-motif \
	--with-blas \
	--with-freetype \
	--with-includes=%{_includedir} \
	--with-libs=%{_libdir} \
	--with-postgres-includes=/usr/include/postgresql/server \
	--with-freetype-includes=/usr/include/freetype2
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_mandir}/man1,%{_includedir}/grass5,%{_libdir}/grass5,%{_bindir},%{_datadir}}

#due to uncompatibilty $ARCH and %%{_target_platform} on ppc
%ifarch ppc
%define _target_platform powerpc-pld-linux-gnu
%endif

cd bin.%{_target_platform}
mv grass5 grass5.in
awk '// {if (/^GISBASE/) { print "GISBASE=%{_libdir}/grass5" } else { print $0 }}' < grass5.in > grass5
install grass5 $RPM_BUILD_ROOT%{_bindir}
cd ..

cd dist.%{_target_platform}

find . -type d -name CVS | xargs rm -rf

# etc: it is a big mess; do not move the content of "etc" dir to /etc
# txt: move to %docdir?
# tcltkgrass: separate package?
# bwidget: move to devel or separate package?
# dev: move the content to /dev or leave it as below?
cp -a bin bwidget etc dev driver fonts scripts tcltkgrass txt $RPM_BUILD_ROOT%{_libdir}/grass5

install man/man1/* $RPM_BUILD_ROOT%{_mandir}/man1
install lib/* $RPM_BUILD_ROOT%{_libdir}
install include/* $RPM_BUILD_ROOT%{_includedir}/grass5
cp -rf locale $RPM_BUILD_ROOT%{_datadir}

mv -f bwidget/CHANGES.txt ../bwidget.CHANGES.TXT
mv -f bwidget/README.grass ../bwidget.README.grass
mv -f tcltkgrass/docs ../tcltkgrass-docs
cd ..

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS BUGS COPYING NEWS.html ONGOING TODO.txt documents/*.*
%doc bwidget.CHANGES.TXT bwidget.README.grass
%doc dist.%{_target_platform}/bwidget/BWman tcltkgrass-docs
%attr(755,root,root) %{_bindir}/*
#%attr(-,root,root) %{_libdir}/grass5
%dir %{_libdir}/grass5
%attr(755,root,root) %{_libdir}/grass5/bin
%dir %{_libdir}/grass5/bwidget
%{_libdir}/grass5/bwidget/*.tcl
%dir %{_libdir}/grass5/bwidget/demo
%{_libdir}/grass5/bwidget/demo/*.xbm
%{_libdir}/grass5/bwidget/demo/[^d]*.tcl
%{_libdir}/grass5/bwidget/demo/d[^e]*.tcl
%attr(755,root,root) %{_libdir}/grass5/bwidget/demo/demo.tcl
%{_libdir}/grass5/bwidget/images
%dir %{_libdir}/grass5/bwidget/lang
%lang(de) %{_libdir}/grass5/bwidget/lang/de.rc
%{_libdir}/grass5/bwidget/lang/en.rc
%lang(es) %{_libdir}/grass5/bwidget/lang/es.rc
%lang(fr) %{_libdir}/grass5/bwidget/lang/fr.rc
%dir %{_libdir}/grass5/dev
%attr(755,root,root) %{_libdir}/grass5/dev/create_fifos.sh
%{_libdir}/grass5/dev/fifo*
%attr(755,root,root) %{_libdir}/grass5/driver
%dir %{_libdir}/grass5/etc
%{_libdir}/grass5/etc/Gcolortab
%attr(755,root,root) %{_libdir}/grass5/etc/agnps50
%attr(755,root,root) %{_libdir}/grass5/etc/bin
%attr(755,root,root) %{_libdir}/grass5/etc/b.*
%{_libdir}/grass5/etc/census.docs
%attr(755,root,root) %{_libdir}/grass5/etc/c[^e]*
%attr(755,root,root) %{_libdir}/grass5/etc/d[.b]*
%{_libdir}/grass5/etc/d[ai]*
%{_libdir}/grass5/etc/help
%{_libdir}/grass5/etc/nad
%attr(755,root,root) %{_libdir}/grass5/etc/nad2bin
%dir %{_libdir}/grass5/etc/nviz2.2
%attr(755,root,root) %{_libdir}/grass5/etc/nviz2.2/NVWISH2.2
%{_libdir}/grass5/etc/nviz2.2/bitmaps
%dir %{_libdir}/grass5/etc/nviz2.2/scripts
%{_libdir}/grass5/etc/nviz2.2/scripts/[^nps]*
%attr(755,root,root) %{_libdir}/grass5/etc/nviz2.2/scripts/nviz2.2_script
%{_libdir}/grass5/etc/nviz2.2/scripts/nviz_init.tcl
%{_libdir}/grass5/etc/nviz2.2/scripts/p[^a]*
%{_libdir}/grass5/etc/nviz2.2/scripts/panelIndex
%{_libdir}/grass5/etc/nviz2.2/scripts/panel_[^m]*
%{_libdir}/grass5/etc/nviz2.2/scripts/panel_m[^k]*
%attr(755,root,root) %{_libdir}/grass5/etc/nviz2.2/scripts/panel_mkdspf.tcl
%{_libdir}/grass5/etc/nviz2.2/scripts/s[^c]*
%{_libdir}/grass5/etc/nviz2.2/scripts/script_support.tcl
%attr(755,root,root) %{_libdir}/grass5/etc/nviz2.2/scripts/script_[^s]*
%dir %{_libdir}/grass5/etc/paint
%attr(755,root,root) %{_libdir}/grass5/etc/paint/driver*
%{_libdir}/grass5/etc/paint/ps.devices
%attr(755,root,root) %{_libdir}/grass5/etc/paint/*.test
%attr(755,root,root) %{_libdir}/grass5/etc/paint/patcc
%{_libdir}/grass5/etc/paint/header
%{_libdir}/grass5/etc/paint/patterns*
%{_libdir}/grass5/etc/paint/prolog.ps
%attr(755,root,root) %{_libdir}/grass5/etc/water
%{_libdir}/grass5/etc/FIPS.code
%attr(755,root,root) %{_libdir}/grass5/etc/[Iilv]*
%attr(755,root,root) %{_libdir}/grass5/etc/echo
%{_libdir}/grass5/etc/el*
%{_libdir}/grass5/etc/font.bin
%attr(755,root,root) %{_libdir}/grass5/etc/font_2_bin
%attr(755,root,root) %{_libdir}/grass5/etc/frame.*
%{_libdir}/grass5/etc/freetypecap
%attr(755,root,root) %{_libdir}/grass5/etc/front.end
%attr(755,root,root) %{_libdir}/grass5/etc/ge*
%{_libdir}/grass5/etc/grass_intro
%attr(755,root,root) %{_libdir}/grass5/etc/mod*
%attr(755,root,root) %{_libdir}/grass5/etc/mon.*
%{_libdir}/grass5/etc/monitorcap
%attr(755,root,root) %{_libdir}/grass5/etc/permut
%{_libdir}/grass5/etc/projections
%attr(755,root,root) %{_libdir}/grass5/etc/r[^g]*
%{_libdir}/grass5/etc/rgb.txt
%attr(755,root,root) %{_libdir}/grass5/etc/s[^t]*
%{_libdir}/grass5/etc/state*
%{_libdir}/grass5/fonts
%attr(755,root,root) %{_libdir}/grass5/scripts
%dir %{_libdir}/grass5/tcltkgrass
%dir %{_libdir}/grass5/tcltkgrass/main
%{_libdir}/grass5/tcltkgrass/main/[^t]*.tcl
%attr(755,root,root) %{_libdir}/grass5/tcltkgrass/main/pause
%{_libdir}/grass5/tcltkgrass/main/t[^k]*.tcl
%attr(755,root,root) %{_libdir}/grass5/tcltkgrass/main/tksys.tcl
%dir %{_libdir}/grass5/tcltkgrass/module
%{_libdir}/grass5/tcltkgrass/module/[cdginprsv]*
%{_libdir}/grass5/tcltkgrass/module/m[^i]*
%attr(755,root,root) %{_libdir}/grass5/tcltkgrass/module/missing_modules.sh
%dir %{_libdir}/grass5/tcltkgrass/script
%attr(755,root,root) %{_libdir}/grass5/tcltkgrass/script/[^g]*
%attr(755,root,root) %{_libdir}/grass5/tcltkgrass/script/g.*
%{_libdir}/grass5/tcltkgrass/script/gis_set.tcl
%{_libdir}/grass5/txt
%{_mandir}/man1/*

%files devel
%defattr(644,root,root,755)
%{_includedir}/grass5
%{_libdir}/*.a
