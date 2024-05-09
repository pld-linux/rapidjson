Summary:	Fast JSON parser and generator for C++
Summary(pl.UTF-8):	Szybki parser i generator JSON-a dla C++
Name:		rapidjson
Version:	1.1.0
Release:	2
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/Tencent/rapidjson/releases
Source0:	https://github.com/miloyip/rapidjson/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	badd12c511e081fec6c89c43a7027bce
Patch0:		%{name}-1.1.0-do_not_include_gtest_src_dir.patch
Patch1:		git-fixes.patch
URL:		http://miloyip.github.io/rapidjson
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	gtest-devel
BuildRequires:	rpmbuild(macros) >= 1.752
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

JSON (JavaScript Object Notation) is a light-weight data exchange
format. RapidJSON should be in fully compliance with RFC4627/ECMA-404.

%description -l pl.UTF-8
RapidJSON to szybki parser i generator JSON-a dla C++. Został
zainspirowany przez RapidXml.

RapidJSON jest mały, ale kompletny. Obsługuje API zarówno w stylu SAX,
jak i DOM. Parser SAX ma jedynie pięćset linii kodu.

RapidJSON jest szybki, Wydajność jest porównywalna ze strlen().
Opcjonalnie obsługuje także SSE2/SSE4.1.

RapidJSON jest samodzielny. Nie zależy od zewnętrznych bibliotek,
takich jak BOOST. Nie wymaga nawet STL-a.

JSON (JavaScript Object Notation) to lekki format wymiany danych.
RapidJSON powinien być w pełni zgodny z RFC4627/ECMA-404.

%package devel
Summary:	Fast JSON parser and generator for C++
Summary(pl.UTF-8):	Szybki parser i generator JSON-a dla C++
Group:		Development/Libraries
BuildArch:	noarch

%description devel
RapidJSON is a fast JSON parser and generator for C++. It was inspired
by RapidXml.

RapidJSON is small but complete. It supports both SAX and DOM style
API. The SAX parser is only a half thousand lines of code.

RapidJSON is fast. Its performance can be comparable to strlen(). It
also optionally supports SSE2/SSE4.1 for acceleration.

RapidJSON is self-contained. It does not depend on external libraries
such as BOOST. It even does not depend on STL.

JSON (JavaScript Object Notation) is a light-weight data exchange
format. RapidJSON should be in fully compliance with RFC4627/ECMA-404.

%description devel -l pl.UTF-8
RapidJSON to szybki parser i generator JSON-a dla C++. Został
zainspirowany przez RapidXml.

RapidJSON jest mały, ale kompletny. Obsługuje API zarówno w stylu SAX,
jak i DOM. Parser SAX ma jedynie pięćset linii kodu.

RapidJSON jest szybki, Wydajność jest porównywalna ze strlen().
Opcjonalnie obsługuje także SSE2/SSE4.1.

RapidJSON jest samodzielny. Nie zależy od zewnętrznych bibliotek,
takich jak BOOST. Nie wymaga nawet STL-a.

JSON (JavaScript Object Notation) to lekki format wymiany danych.
RapidJSON powinien być w pełni zgodny z RFC4627/ECMA-404.

%package doc
Summary:	Documentation files for RapidJSON
Summary(pl.UTF-8):	Dokumentacja do biblioteki RapidJSON
Group:		Documentation
BuildArch:	noarch

%description doc
This package contains the documentation files for RapidJSON.

%description doc -l pl.UTF-8
Dokumentacja do biblioteki RapidJSON.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
%{__mv} $RPM_BUILD_ROOT%{_prefix}/lib/* $RPM_BUILD_ROOT%{_datadir}

cp -a example/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc CHANGELOG.md license.txt readme.md
%lang(zh_CN) %doc readme.zh-cn.md
%{_datadir}/cmake
%{_npkgconfigdir}/RapidJSON.pc
%{_includedir}/rapidjson

%files doc
%defattr(644,root,root,755)
%doc build/doc/html
%{_examplesdir}/%{name}-%{version}
