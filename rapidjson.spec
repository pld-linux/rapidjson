Summary:	Fast JSON parser and generator for C++
Name:		rapidjson
Version:	1.1.0
Release:	1
License:	MIT
Group:		Libraries
Source0:	https://github.com/miloyip/rapidjson/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	badd12c511e081fec6c89c43a7027bce
Patch0:		%{name}-1.1.0-do_not_include_gtest_src_dir.patch
URL:		http://miloyip.github.io/rapidjson
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	gtest-devel
BuildRequires:	valgrind
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
RapidJSON is a fast JSON parser and generator for C++. It was inspired
by RapidXml.

RapidJSON is small but complete. It supports both SAX and DOM style
API. The SAX parser is only a half thousand lines of code.

RapidJSON is fast. Its performance can be comparable to strlen(). It
also optionally supports SSE2/SSE4.1 for acceleration.

RapidJSON is self-contained. It does not depend on external libraries
such as BOOST. It even does not depend on STL.

RapidJSON is memory friendly. Each JSON value occupies exactly 16/20
bytes for most 32/64-bit machines (excluding text string). By default
it uses a fast memory allocator, and the parser allocates memory
compactly during parsing.

RapidJSON is Unicode friendly. It supports UTF-8, UTF-16, UTF-32 (LE &
BE), and their detection, validation and transcoding internally. For
example, you can read a UTF-8 file and let RapidJSON transcode the
JSON strings into UTF-16 in the DOM. It also supports surrogates and
"\u0000" (null character).

JSON(JavaScript Object Notation) is a light-weight data exchange
format. RapidJSON should be in fully compliance with RFC4627/ECMA-404.

%package devel
Summary:	Fast JSON parser and generator for C++
Group:		Development/Libraries
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description devel
RapidJSON is a fast JSON parser and generator for C++. It was inspired
by RapidXml.

RapidJSON is small but complete. It supports both SAX and DOM style
API. The SAX parser is only a half thousand lines of code.

RapidJSON is fast. Its performance can be comparable to strlen(). It
also optionally supports SSE2/SSE4.1 for acceleration.

RapidJSON is self-contained. It does not depend on external libraries
such as BOOST. It even does not depend on STL.

RapidJSON is memory friendly. Each JSON value occupies exactly 16/20
bytes for most 32/64-bit machines (excluding text string). By default
it uses a fast memory allocator, and the parser allocates memory
compactly during parsing.

RapidJSON is Unicode friendly. It supports UTF-8, UTF-16, UTF-32 (LE &
BE), and their detection, validation and transcoding internally. For
example, you can read a UTF-8 file and let RapidJSON transcode the
JSON strings into UTF-16 in the DOM. It also supports surrogates and
"\u0000" (null character).

JSON(JavaScript Object Notation) is a light-weight data exchange
format. RapidJSON should be in fully compliance with RFC4627/ECMA-404.

%package doc
Summary:	Documentation-files for %{name}
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description doc
This package contains the documentation-files for %{name}.

%prep
%setup -q
%patch0 -p1

# Disable -Werror.
find . -type f -name 'CMakeLists.txt' -print0 | \
	xargs -0 %{__sed} -i -e's![ \t]*-march=native!!g' -e's![ \t]*-Werror!!g'

%build
install -d build
cd build
%cmake .. \
	-DGTESTSRC_FOUND=TRUE \
	-DGTEST_SOURCE_DIR=.

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

# Move pkgconfig und CMake-stuff to generic datadir.
%{__mv} -f $RPM_BUILD_ROOT%{_prefix}/lib/* $RPM_BUILD_ROOT%{_datadir}

cp -a example/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc CHANGELOG.md readme*.md
%{_datadir}/cmake
%{_npkgconfigdir}/*.pc
%{_includedir}/%{name}

%files doc
%defattr(644,root,root,755)
%doc build/doc/html
%{_examplesdir}/%{name}-%{version}
