#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define	module	chai
Summary:	Easy to use mocking/stub/spy framework
Name:		python-%{module}
Version:	1.0.0
Release:	1
License:	BSD
Group:		Development/Libraries
Source0:	http://pypi.python.org/packages/source/c/%{module}/%{module}-%{version}.tar.gz
# Source0-md5:	fce8d1deb08ef6c1fb2b56eea7ae7b67
URL:		http://pypi.python.org/pypi/chai
BuildRequires:	python-devel
BuildRequires:	python-nose
BuildArch:	noarch
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-nose
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Chai provides a very easy to use API for mocking/stubbing your Python
objects, patterned after the Mocha <http://mocha.rubyforge.org/>
library for Ruby.

%package -n python3-%{module}
Summary:	Easy to use mocking/stub framework
Group:		Development/Libraries

%description -n python3-%{module}
Chai provides a very easy to use API for mocking/stubbing your python
objects, patterned after the Mocha <http://mocha.rubyforge.org/>
library for Ruby.

%prep
%setup -q -n %{module}-%{version}

# Remove bundled egg-info in case it exists
rm -r %{module}.egg-info

%build
%if %{with python2}
%{__python} setup.py build --build-base build-2 %{?with_tests:test}
%endif

%if %{with python3}
# Remove python2 compatibility files
# Makes tests fail and are not needed on python3
rm chai/python2.py
rm tests/comparator_py2.py
# signature mismatch
rm tests/stub_test.py

%{__python3} setup.py build --build-base build-3 %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%{__python} setup.py \
	build --build-base build-2 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
	build --build-base build-3 \
	install --skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.rst LICENSE.txt
%{py_sitescriptdir}/chai
%{py_sitescriptdir}/chai-%{version}-py*.egg-info

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc README.rst LICENSE.txt
%{py3_sitescriptdir}/chai
%{py3_sitescriptdir}/chai-%{version}-py*.egg-info
%endif
