Summary:	The Geographic Resources Analysis Support System
Summary(pl):	System Obs³uguj±cy Analizê Zasobów Geograficznych
Name:		grass
Version:	5.0.0pre3
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	http://grass.itc.it/grass5/source/%{name}%{version}.tar.gz
URL:		http://grass.itc.it/
BuildRequires:	blas-devel
#BuildRequires:	gdal-devel
BuildRequires:	OpenGL-devel
BuildRequires:	fftw-devel
BuildRequires:	freetype-devel
BuildRequires:	gd-devel
BuildRequires:	gdbm-devel
BuildRequires:	lapack-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	motif-devel
BuildRequires:	postgresql-devel
BuildRequires:	tcl-devel
BuildRequires:	tk-devel
BuildRequires:	unixODBC-devel
BuildRequires:	zlib-devel
BuildRequires:	gcc-g77
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _noautoreqdep   libGL.so.1 libGLU.so.1
%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
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

%description -l pl
GRASS (System Wspierania Analiz Zasobów Geograficznych) jest rastrowym
oraz wektorowym systemem GIS (System Informacji Geograficznej), system
obróbki obrazów, tworzeniem grafiki oraz system modelowania
przestrzennego. GRASS zawiera wiele modu³ów do manipulacji danych
rastrowych, wektorowych, renderowania obrazów na monitorze lub
papierze, obróbkê multispektralnych obrazów, punktowe oraz ogólne
zarz±dzanie danymi. Zawiera równie¿ narzêdzia do wspó³pracy z
digitizerami, skanerami oraz bazami RIM, Informix, Postgres oraz
Oracle.

%package OpenGL
Summary:	NVIZ - a 3D-tool for grass
Summary(pl):	NVIZ - narzêdzie 3D dla GRASSa
Group:		X11/Applications
Requires:	%{name} = %{version}

%description OpenGL
nviz is a GRASS module-in-progress which allows users to realistically
render multiple surfaces in a 3D space, optionally using thematic
coloring, draping GRASS vector files over the surfaces, and displaying
GRASS site files either draped on the surfaces or as 3D point
locations.

%package pg
Summary:	postgres database interface
Summary(pl):	Interfejs do bazy PostgreSQL
Group:		X11/Applications
Requires:	%{name} = %{version}

%description pg
Postgres database interface for GRASS.

%dewscription pg -l pl
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

%prep
%setup -q -n %{name}%{version}

%build
if [ -f %{_pkgconfigdir}/libpng12.pc ] ; then
        CPPFLAGS="`pkg-config libpng12 --cflags`"; export CPPFLAGS
fi
CFLAGS="%{rpmcflags} -I/usr/include/ncurses"; export CFLAGS
%configure2_13 \
	--with-lapack \
	--with-motif \
	--with-freetype \
	--with-includes=%{_includedir} \
	--with-libs=%{_libdir} \
	--with-postgres-includes=/usr/include/postgresql/server \
	--with-freetype-includes=/usr/include/freetype2
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{makeinstall}

#%{__make} install \
#	DESTDIR=$RPM_BUILD_ROOT

gzip -9nf AUTHORS BUGS COPYING NEWS.html ONGOING TODO.txt documents/*.*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz */*.gz
%attr(755,root,root) %{_bindir}/*
