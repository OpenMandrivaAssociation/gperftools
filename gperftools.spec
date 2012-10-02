%define major           1
%define oname           gperftools
%define libname         %mklibname %{oname} %major
%define develname       %mklibname %{oname} -d

Name:		gperftools
Version:	2.0
Release:	1
License:	BSD
Group:		Development/Other
Summary:	Very fast malloc and performance analysis tools
URL:		http://code.google.com/p/gperftools/
Source0:	http://gperftools.googlecode.com/files/%{name}-%{version}.tar.gz
# http://code.google.com/p/gperftools/issues/detail?id=444
Patch0:		gperftools-2.0-glibc216.patch
# ppc64 still broken, bz 238390
ExclusiveArch:	%{ix86} x86_64 ppc %{arm}
%ifnarch ppc ppc64
BuildRequires:	libunwind-devel
%endif

%description
Perf Tools is a collection of performance analysis tools, including a
high-performance multi-threaded malloc() implementation that works
particularly well with threads and STL, a thread-friendly heap-checker,
a heap profiler, and a cpu-profiler.

%package -n	%{develname}
Summary:	Development libraries and headers for gperftools
Group:		Development/C
Requires:	%{name}-libs%{?_isa} = %{version}-%{release}
Provides:	google-perftools-devel = %{version}-%{release}
Obsoletes:	google-perftools-devel < 2.0

%description -n %{develname}
Libraries and headers for developing applications that use gperftools.

%package -n	%{libname}
Group:		System/Libraries
Summary:	Libraries provided by gperftools
Provides:	google-perftools-libs = %{version}-%{release}
Obsoletes:	google-perftools-libs < 2.0

%description -n %{libname}
Libraries provided by gperftools, including libtcmalloc and libprofiler.

%package -n pprof
Summary:	CPU and Heap Profiler tool
Group:		Development/Other
Requires:	gv, graphviz
BuildArch:	noarch
Provides:	google-perftools = %{version}-%{release}
Obsoletes:	google-perftools < 2.0

%description -n pprof
Pprof is a heap and CPU profiler tool, part of the gperftools suite.

%prep
%setup -q
%patch0 -p1 -b .glibc216

# Fix end-of-line encoding
sed -i 's/\r//' README_windows.txt

# No need to have exec permissions on source code
chmod -x src/sampler.h src/sampler.cc

%build
CXXFLAGS=`echo $RPM_OPT_FLAGS -DTCMALLOC_LARGE_PAGES| sed -e 's/-Wp,-D_FORTIFY_SOURCE=2//g'`
%configure2_5x --disable-static

# Bad rpath!
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# Can't build with smp_mflags
make

%install
make DESTDIR=%{buildroot} docdir=%{_docdir}/%{name}-%{version}/ install
find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'

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

%files -n %{develname}
%{_docdir}/%{name}-%{version}/
%{_includedir}/google/
%{_includedir}/gperftools/
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%files -n %{libname}
%{_libdir}/*.so.*
