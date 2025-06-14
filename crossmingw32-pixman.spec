Summary:	Pixel manipulation library - cross MinGW32
Summary(pl.UTF-8):	Biblioteka operacji na pikselach - wersja skrośna MinGW32
Name:		crossmingw32-pixman
Version:	0.46.2
Release:	1
License:	MIT
Group:		Development/Libraries
Source0:	https://www.cairographics.org/releases/pixman-%{version}.tar.gz
# Source0-md5:	60ec2d0e718c31510f2000ada530e51b
URL:		https://pixman.org/
BuildRequires:	crossmingw32-gcc >= 1:4.2
BuildRequires:	meson >= 1.3.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 2.042
BuildRequires:	sed >= 4.0
Requires:	crossmingw32-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1
%define		_enable_debug_packages	0

%define		target			i386-mingw32
%define		target_platform 	i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_docdir			%{_sysprefix}/share/doc
%define		_dlldir			/usr/share/wine/windows/system
%define		__pkgconfig_provides	%{nil}
%define		__pkgconfig_requires	%{nil}
# for meson 0.50+, keep __cc/__cxx as host compiler and pass %{target}-* in meson-cross.txt

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker, most of -f options are Linux-specific
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-f[-a-z0-9=]*

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

%{__sed} -i -e 's#<pixman-version.h>#"pixman-version.h"#' pixman/pixman.h

cat > meson-cross.txt <<'EOF'
[host_machine]
system = 'windows'
cpu_family = 'x86'
cpu = 'i386'
endian='little'
[binaries]
c = '%{target}-gcc'
cpp = '%{target}-g++'
ar = '%{target}-ar'
windres = '%{target}-windres'
pkg-config = 'pkg-config'
[build-in options]
c_args = ['%(echo %{rpmcflags} | sed -e "s/ \+/ /g;s/ /', '/g")', '-DWINVER=0x0600']
EOF

%build
export PKG_CONFIG_LIBDIR=%{_pkgconfigdir}
%meson \
	--cross-file meson-cross.txt \
	-Da64-neon=disabled \
	-Darm-simd=disabled \
	-Ddemos=disabled \
	-Dgnu-inline-asm=enabled \
	-Dgtk=disabled \
	-Dlibpng=disabled \
	-Dloongson-mmi=disabled \
	-Dmips-dspr2=disabled \
	-Dneon=disabled \
	-Dopenmp=disabled \
	-Drvv=disabled \
	-Dsse2=enabled \
	-Dssse3=enabled \
	-Dtests=disabled \
	-Dtls=enabled \
	-Dvmx=disabled

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

install -d $RPM_BUILD_ROOT%{_dlldir}
%{__mv} $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc COPYING README
%{_libdir}/libpixman-1.dll.a
%{_includedir}/pixman-1
%{_pkgconfigdir}/pixman-1.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpixman-1.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpixman-1-*.dll
