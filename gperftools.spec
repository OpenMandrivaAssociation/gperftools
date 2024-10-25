%define major	0
%define maj4	4
%define	libprofiler			%mklibname profiler
%define	oldlibprofiler			%mklibname profiler 0
%define	libtcmalloc_minimal		%mklibname tcmalloc_minimal
%define	oldlibtcmalloc_minimal		%mklibname tcmalloc_minimal 4
%define	libtcmalloc_minimal_debug	%mklibname tcmalloc_minimal_debug
%define	oldlibtcmalloc_minimal_debug	%mklibname tcmalloc_minimal_debug 4
%define	libtcmalloc_debug		%mklibname tcmalloc_debug
%define	oldlibtcmalloc_debug		%mklibname tcmalloc_debug 4
%define	libtcmalloc_and_profiler	%mklibname tcmalloc_and_profiler
%define	oldlibtcmalloc_and_profiler	%mklibname tcmalloc_and_profiler 4
%define	libtcmalloc			%mklibname tcmalloc
%define	oldlibtcmalloc			%mklibname tcmalloc 4
%define devname				%mklibname %{name} -d

%define _disable_rebuild_configure 1
%define _disable_lto 1

Summary:	Very fast malloc and performance analysis tools
Name:		gperftools
Version:	2.16
Release:	1
License:	BSD
Group:		Development/Other
Url:		  https://github.com/gperftools/gperftools
Source0:	https://github.com/gperftools/gperftools/archive/gperftools-gperftools-%{version}.tar.gz

%description
Perf Tools is a collection of performance analysis tools, including a
high-performance multi-threaded malloc() implementation that works
particularly well with threads and STL, a thread-friendly heap-checker,
a heap profiler, and a cpu-profiler.

%package -n	%{libprofiler}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2
%rename %{oldlibprofiler}

%description -n %{libprofiler}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc_minimal}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2
%rename %{oldlibtcmalloc_minimal}

%description -n %{libtcmalloc_minimal}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc_minimal_debug}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2
%rename %{oldlibtcmalloc_minimal_debug}

%description -n %{libtcmalloc_minimal_debug}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc_debug}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2
%rename %{oldlibtcmalloc_debug}

%description -n %{libtcmalloc_debug}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc_and_profiler}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2
%rename %{oldlibtcmalloc_and_profiler}

%description -n %{libtcmalloc_and_profiler}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2
%rename %{oldlibtcmalloc}

%description -n %{libtcmalloc}
This package contains a shared library for %{name}.

%package -n	%{devname}
Summary:	Development libraries and headers for gperftools
Group:		Development/C
Requires:	%{libprofiler} = %{version}-%{release}
Requires:	%{libtcmalloc_minimal} = %{version}-%{release}
Requires:	%{libtcmalloc_minimal_debug} = %{version}-%{release}
Requires:	%{libtcmalloc_debug} = %{version}-%{release}
Requires:	%{libtcmalloc_and_profiler} = %{version}-%{release}
Requires:	%{libtcmalloc} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Libraries and headers for developing applications that use gperftools.

%package -n pprof
Summary:	CPU and Heap Profiler tool
Group:		Development/Other
BuildArch:	noarch
Requires:	gv
Requires:	graphviz
Provides:	google-perftools = %{version}-%{release}

%description -n pprof
Pprof is a heap and CPU profiler tool, part of the gperftools suite.

%prep
%autosetup -p1 -n %{name}-%{name}-%{version}

# Fix end-of-line encoding
sed -i 's/\r//' README_windows.txt

# No need to have exec permissions on source code
chmod -x src/sampler.h src/sampler.cc Makefile.am

#[ -e configure ] || ./autogen.sh

%build
CXXFLAGS=`echo $RPM_OPT_FLAGS -DTCMALLOC_LARGE_PAGES| sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`
%configure --enable-frame-pointers

# Bad rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Can't build with smp_mflags
%make_build

%install
%make_install docdir=%{_docdir}/%{name}-%{version}/ 

# Zero files
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}/NEWS

# Delete useless files
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}/INSTALL

%check
# http://code.google.com/p/google-perftools/issues/detail?id=153
# Their test suite is junk. Disabling.
# LD_LIBRARY_PATH=./.libs make check

%files -n pprof
%{_bindir}/pprof
%{_bindir}/pprof-symbolize
%{_mandir}/man1/*

%files -n %{libprofiler}
%{_libdir}/libprofiler.so.%{major}*

%files -n %{libtcmalloc_minimal}
%{_libdir}/libtcmalloc_minimal.so.%{maj4}*

%files -n %{libtcmalloc_minimal_debug}
%{_libdir}/libtcmalloc_minimal_debug.so.%{maj4}*

%files -n %{libtcmalloc_debug}
%{_libdir}/libtcmalloc_debug.so.%{maj4}*

%files -n %{libtcmalloc_and_profiler}
%{_libdir}/libtcmalloc_and_profiler.so.%{maj4}*

%files -n %{libtcmalloc}
%{_libdir}/libtcmalloc.so.%{maj4}*

%files -n %{devname}
%{_docdir}/%{name}-%{version}/
%{_includedir}/google/
%{_includedir}/gperftools/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
