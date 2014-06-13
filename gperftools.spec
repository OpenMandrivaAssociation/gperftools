%define major	0
%define maj4	4
%define	libprofiler			%mklibname profiler %{major}
%define	libtcmalloc_minimal		%mklibname tcmalloc_minimal %{maj4}
%define	libtcmalloc_minimal_debug	%mklibname tcmalloc_minimal_debug %{maj4}
%define	libtcmalloc_debug		%mklibname tcmalloc_debug %{maj4}
%define	libtcmalloc_and_profiler	%mklibname tcmalloc_and_profiler %{maj4}
%define	libtcmalloc			%mklibname tcmalloc %{maj4}
%define devname				%mklibname %{name} -d

Summary:	Very fast malloc and performance analysis tools
Name:		gperftools
Version:	2.0
Release:	7
License:	BSD
Group:		Development/Other
Url:		http://code.google.com/p/gperftools/
Source0:	http://gperftools.googlecode.com/files/%{name}-%{version}.tar.gz
# http://code.google.com/p/gperftools/issues/detail?id=444
Patch0:		gperftools-2.0-glibc216.patch
# ppc64 still broken, bz 238390
ExclusiveArch:	%{ix86} x86_64 ppc %{arm} aarch64
%ifnarch ppc ppc64
BuildRequires:	libunwind-devel
%endif

%description
Perf Tools is a collection of performance analysis tools, including a
high-performance multi-threaded malloc() implementation that works
particularly well with threads and STL, a thread-friendly heap-checker,
a heap profiler, and a cpu-profiler.

%package -n	%{libprofiler}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2

%description -n %{libprofiler}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc_minimal}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2

%description -n %{libtcmalloc_minimal}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc_minimal_debug}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2

%description -n %{libtcmalloc_minimal_debug}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc_debug}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2

%description -n %{libtcmalloc_debug}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc_and_profiler}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2

%description -n %{libtcmalloc_and_profiler}
This package contains a shared library for %{name}.

%package -n	%{libtcmalloc}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Obsoletes:	%{_lib}gperftools1 < 2.0-2

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
%setup -q
%apply_patches

# Fix end-of-line encoding
sed -i 's/\r//' README_windows.txt

# No need to have exec permissions on source code
chmod -x src/sampler.h src/sampler.cc

%build
autoreconf -fiv
CXXFLAGS=`echo $RPM_OPT_FLAGS -DTCMALLOC_LARGE_PAGES| sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`
%configure2_5x --disable-static

# Bad rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Can't build with smp_mflags
make

%install
%makeinstall_std docdir=%{_docdir}/%{name}-%{version}/ 

# Zero files
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}/NEWS

# Delete useless files
rm -rf %{buildroot}%{_docdir}/%{name}-%{version}/INSTALL

%check
# http://code.google.com/p/google-perftools/issues/detail?id=153
%ifnarch ppc
# Their test suite is junk. Disabling.
# LD_LIBRARY_PATH=./.libs make check
%endif

%files -n pprof
%{_bindir}/pprof
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

