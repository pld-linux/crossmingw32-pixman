Summary:	Pixel manipulation library - cross MinGW32
Summary(pl.UTF-8):	Biblioteka operacji na pikselach - wersja skrośna MinGW32
Name:		crossmingw32-pixman
Version:	0.20.0
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	http://xorg.freedesktop.org/archive/individual/lib/pixman-%{version}.tar.bz2
# Source0-md5:	512ec766a911142b901157ba581f6e75
URL:		http://xorg.freedesktop.org/
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	crossmingw32-gcc
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*

%description
pixman is a pixel manipulation library.

This package contains the cross version for Win32.

%description -l pl.UTF-8
pixman to biblioteka do operacji na pikselach.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static pixman library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka pixman (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static pixman library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka pixman (wersja skrośna MinGW32).

%package dll
Summary:	DLL pixman library for Windows
Summary(pl.UTF-8):	Biblioteka DLL pixman dla Windows
Group:		Applications/Emulators
Requires:	wine

%description dll
DLL pixman library for Windows.

%description dll -l pl.UTF-8
Biblioteka DLL pixman dla Windows.

%prep
%setup -q -n pixman-%{version}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--target=%{target} \
	--host=%{target} \
	--disable-gtk \
	--disable-silent-rules

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

sed -i -e 's#<pixman-version.h>#<pixman-1/pixman-version.h>#g' $RPM_BUILD_ROOT%{_includedir}/pixman-1/pixman.h

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README TODO
%{_libdir}/libpixman-1.dll.a
%{_libdir}/libpixman-1.la
%{_includedir}/pixman-1
%{_pkgconfigdir}/pixman-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpixman-1.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpixman-1-*.dll
