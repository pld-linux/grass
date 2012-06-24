#
# Conditional build, see http://grass.itc.it/grass61/source/REQUIREMENTS.html
# for description of optional requirements.
%bcond_without	tcl		# disable gui and nviz
%bcond_without	mysql	# disable mysql support
%bcond_without	odbc	# disable unixODBC support
%bcond_without	xanim	# disable xanim module
#
Summary:	The Geographic Resources Analysis Support System
Summary(pl):	System obs�uguj�cy analiz� zasob�w geograficznych
Name:		grass
Version:	6.2.1
Release:	1
Epoch:		1
License:	GPL
Group:		X11/Applications
Source0:	http://grass.itc.it/grass62/source/%{name}-%{version}.tar.gz
# Source0-md5:	cbe14d34503a75e8102d2f56c7b527a7
Patch0:		%{name}-soname.patch
Patch1:		%{name}-link.patch
URL:		http://grass.itc.it/
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

%define         _noautoreqdep   libGL.so.1 libGLU.so.1
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

%description -l pl
GRASS (System Wspierania Analiz Zasob�w Geograficznych) jest rastrowym
oraz wektorowym systemem GIS (System Informacji Geograficznej),
obr�bki obraz�w, tworzenia grafiki oraz modelowania przestrzennego.
GRASS zawiera wiele modu��w wspomagaj�cych manipulacj� danymi
rastrowymi i wektorowymi, renderowanie obraz�w na monitorze lub
papierze, obr�bk� multispektralnych obraz�w, punktowe oraz og�lne
zarz�dzanie danymi. Zawiera r�wnie� narz�dzia do wsp�pracy z
digitizerami, skanerami oraz bazami RIM, Informix, Postgres oraz
Oracle.

%package OpenGL
Summary:	NVIZ - a 3D-tool for GRASS
Summary(pl):	NVIZ - narz�dzie 3D dla GRASSa
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description OpenGL
Package contains nviz, which is a GRASS module-in-progress which
allows users to realistically render multiple surfaces in a 3D space,
optionally using thematic coloring, draping GRASS vector files over
the surfaces, and displaying GRASS site files either draped on the
surfaces or as 3D point locations.

%description OpenGL -l pl
Pakiet zawiera modu� nviz, kt�ry rozszerza funkcjonalno�� systemu
GRASS o mo�liwo�� realistycznego renderowania wielu powierzchni w
tr�jwymiarowej przestrzeni. Na renderowanych powierzchniach, kt�re
mog� by� tematycznie kolorowane, mo�na zawiesza� pliki wektorowe
GRASSa.

%package pg
Summary:	PostgreSQL database interface
Summary(pl):	Interfejs do bazy PostgreSQL
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description pg
PostgreSQL database interface for GRASS.

%description pg -l pl
Interfejs do bazy PostgreSQL dla GRASSa.

%package odbc
Summary:	ODBC database interface
Summary(pl):	Interfejs ODBC dla GRASSa
Group:		X11/Applications
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description odbc
ODBC database interface for GRASS.

%description odbc -l pl
Interfejs ODBC dla GRASSa.

%package devel
Summary:	Header files and static libraries for GRASS
Summary(pl):	Pliki nag��wkowe i biblioteki statyczne systemu GRASS
Group:		X11/Development/Libraries

%description devel
Header files and static libraries for GRASS.

%description devel -l pl
Pliki nag��wkowe i biblioteki statyczne systemu GRASS.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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

install -d $RPM_BUILD_ROOT{%{_datadir},%{_includedir}/grass62}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/include/* $RPM_BUILD_ROOT%{_includedir}/grass62
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/lib/* $RPM_BUILD_ROOT%{_libdir}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/locale $RPM_BUILD_ROOT%{_datadir}
mv $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/man $RPM_BUILD_ROOT%{_datadir}

sed -i -e 's,^GISBASE=.*,GISBASE=%{_libdir}/grass-%{version},' $RPM_BUILD_ROOT%{_bindir}/grass62

cp -f lib/external/bwidget/CHANGES.txt bwidget.CHANGES.TXT
cp -f lib/external/bwidget/README.grass bwidget.README.grass

rm -rf $RPM_BUILD_ROOT%{_libdir}/grass-%{version}/{bwidget/{*.txt,README.grass},docs}

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
%{_libdir}/grass-%{version}/etc/gintro.gif
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/grass-xterm-wrapper
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/file_option.tcl
%{_libdir}/grass-%{version}/etc/gem
%{_libdir}/grass-%{version}/etc/grass_write_ascii.style
%dir %{_libdir}/grass-%{version}/etc/gui
%{_libdir}/grass-%{version}/etc/gui/icons
%{_libdir}/grass-%{version}/etc/gtcltk
%dir %{_libdir}/grass-%{version}/etc/msgs
%lang(cs) %{_libdir}/grass-%{version}/etc/msgs/cs.msg
%lang(de) %{_libdir}/grass-%{version}/etc/msgs/de.msg
%lang(fr) %{_libdir}/grass-%{version}/etc/msgs/fr.msg
%lang(it) %{_libdir}/grass-%{version}/etc/msgs/it.msg
%lang(ja) %{_libdir}/grass-%{version}/etc/msgs/ja.msg
%lang(pl) %{_libdir}/grass-%{version}/etc/msgs/pl.msg
%lang(pt_BR) %{_libdir}/grass-%{version}/etc/msgs/pt_br.msg
%lang(ru) %{_libdir}/grass-%{version}/etc/msgs/ru.msg
%lang(tr) %{_libdir}/grass-%{version}/etc/msgs/tr.msg
%lang(vi) %{_libdir}/grass-%{version}/etc/msgs/vi.msg
%{_libdir}/grass-%{version}/etc/nad
%{_libdir}/grass-%{version}/etc/ogr_csv
%dir %{_libdir}/grass-%{version}/etc/paint
%{_libdir}/grass-%{version}/etc/paint/patterns
%{_libdir}/grass-%{version}/etc/paint/prolog.ps
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/prompt.sh
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

%if %{with tcl}
%dir %{_libdir}/grass-%{version}/etc/dm
%{_libdir}/grass-%{version}/etc/dm/*.gif
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/dm/*.tcl
%dir %{_libdir}/grass-%{version}/etc/dm/script
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/dm/script/*
%dir %{_libdir}/grass-%{version}/etc/form
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/form/form
%{_libdir}/grass-%{version}/etc/form/*.tcl
%dir %{_libdir}/grass-%{version}/etc/gm
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/gm/*.tcl
%{_libdir}/grass-%{version}/etc/gm/*.gif
%dir %{_libdir}/grass-%{version}/etc/gm/script
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/gm/script/*
%dir %{_libdir}/grass-%{version}/etc/gui/menus
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/gui/menus/menu.tcl
%dir %{_libdir}/grass-%{version}/etc/nviz2.2
%{_libdir}/grass-%{version}/etc/nviz2.2/bitmaps
%dir %{_libdir}/grass-%{version}/etc/nviz2.2/scripts
%{_libdir}/grass-%{version}/etc/nviz2.2/scripts/[!ns]*
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/nviz2.2/scripts/nviz2.2_script
%{_libdir}/grass-%{version}/etc/nviz2.2/scripts/nviz_init.tcl
%{_libdir}/grass-%{version}/etc/nviz2.2/scripts/nviz_params
%{_libdir}/grass-%{version}/etc/nviz2.2/scripts/s[!c]*
%{_libdir}/grass-%{version}/etc/nviz2.2/scripts/script_support.tcl
%attr(755,root,root) %{_libdir}/grass-%{version}/etc/nviz2.2/scripts/script_[!s]*
%endif

%files devel
%defattr(644,root,root,755)
%{_includedir}/grass62
%{_libdir}/*.a
