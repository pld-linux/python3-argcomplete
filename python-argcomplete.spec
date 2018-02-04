#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		argcomplete
%define		egg_name	argcomplete
%define		pypi_name	argcomplete
Summary:	Bash tab completion for argparse
Name:		python-%{pypi_name}
Version:	1.9.3
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/kislyuk/argcomplete/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	18afda95a2726eb24df810645bef4b38
URL:		https://github.com/kislyuk/argcomplete
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with check}
BuildRequires:	tcsh
%endif
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Argcomplete provides easy, extensible command line tab completion of
arguments for your Python script.

It makes two assumptions:

 - You are using bash as your shell
 - You are using argparse to manage your command line arguments/options

Argcomplete is particularly useful if your program has lots of options
or subparsers, and if your program can dynamically suggest completions
for your argument/option values (for example, if the user is browsing
resources over the network).

%package -n python3-%{pypi_name}
Summary:	%{summary}
Group:		Libraries/Python
BuildRequires:	python3-devel
BuildRequires:	python3-setuptools
%if %{with check}
BuildRequires:	python3-pexpect
%endif
# pkg_resources module is used from python-argcomplete-check-easy-install-script
Requires:	python3-setuptools

%description -n python3-%{pypi_name}
Argcomplete provides easy, extensible command line tab completion of
arguments for your Python script.

It makes two assumptions:

 - You are using bash as your shell
 - You are using argparse to manage your command line arguments/options

Argcomplete is particularly useful if your program has lots of options
or subparsers, and if your program can dynamically suggest completions
for your argument/option values (for example, if the user is browsing
resources over the network).

%prep
%setup -q -n %{pypi_name}-%{version}

# Remove useless BRs
sed -i -r -e '/tests_require = /s/"(coverage|flake8|wheel)"[, ]*//g' setup.py

%build
export LC_ALL=C.UTF-8
%if %{with python2}
%py_build %{?with_tests:test}
%endif

%if %{with python3}
%py3_build %{?with_tests:test}
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

install -d $RPM_BUILD_ROOT%{bash_compdir}
install -p $RPM_BUILD_ROOT%{py3_sitescriptdir}/%{pypi_name}/bash_completion.d/python-argcomplete.sh \
	$RPM_BUILD_ROOT%{bash_compdir}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.rst LICENSE.rst
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc README.rst LICENSE.rst
%attr(755,root,root) %{_bindir}/activate-global-python-argcomplete
%attr(755,root,root) %{_bindir}/python-argcomplete-check-easy-install-script
%attr(755,root,root) %{_bindir}/python-argcomplete-tcsh
%attr(755,root,root) %{_bindir}/register-python-argcomplete
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%{bash_compdir}/python-argcomplete.sh
%endif
