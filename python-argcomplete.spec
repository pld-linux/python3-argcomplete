#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		module		argcomplete
%define		egg_name	argcomplete
%define		pypi_name	argcomplete
Summary:	Bash tab completion for argparse
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów dla argparse
Name:		python-%{pypi_name}
Version:	1.11.1
Release:	2
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://github.com/kislyuk/argcomplete/releases
Source0:	https://github.com/kislyuk/argcomplete/archive/v%{version}/%{pypi_name}-%{version}.tar.gz
# Source0-md5:	603117954aad0f5c94197fc283edc605
URL:		https://github.com/kislyuk/argcomplete
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-importlib_metadata >= 0.23
BuildRequires:	python-importlib_metadata < 2
BuildRequires:	python-pexpect
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.5
BuildRequires:	python3-setuptools
%if %{with tests}
%if "%{py3_ver}" < "3.8"
BuildRequires:	python3-importlib_metadata >= 0.23
BuildRequires:	python3-importlib_metadata < 2
%endif
BuildRequires:	python3-pexpect
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with doc}
BuildRequires:	python3-guzzle_sphinx_theme
BuildRequires:	sphinx-pdg-3
%endif
%if %{with tests}
BuildRequires:	bash
BuildRequires:	fish
BuildRequires:	pip
BuildRequires:	tcsh
%endif
%if %{without python3}
# pkg_resources module is used from python-argcomplete-check-easy-install-script
Requires:	python-setuptools
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

%description -l pl.UTF-8
Argcomplete zapewnia łatwe, rozszerzalne dopełnianie tabem argumentów
scriptów Pythona w wierszu poleceń.

Czyni dwa założenia:
- powłoką jest bash
- skrypt używa argparse do zarządzania argumentami/opcjami linii
  poleceń

Argcomplete jest przydatne szczególnie wtedy, gdy program ma wiele
opcji lub podparserów, albo gdy może dynamicznie podpowiadać
dopełnienia wartości argumentów/opcji (np. kiedy użytkownik przegląda
zasoby sieciowe).

%package -n python3-%{pypi_name}
Summary:	Bash tab completion for argparse
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów dla argparse
Group:		Libraries/Python
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

%description -n python3-%{pypi_name} -l pl.UTF-8
Argcomplete zapewnia łatwe, rozszerzalne dopełnianie tabem argumentów
scriptów Pythona w wierszu poleceń.

Czyni dwa założenia:
- powłoką jest bash
- skrypt używa argparse do zarządzania argumentami/opcjami linii
  poleceń

Argcomplete jest przydatne szczególnie wtedy, gdy program ma wiele
opcji lub podparserów, albo gdy może dynamicznie podpowiadać
dopełnienia wartości argumentów/opcji (np. kiedy użytkownik przegląda
zasoby sieciowe).

%package -n bash-completion-python-argcomplete
Summary:	Bash completion for argparse
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów dla argparse
Group:		Applications/Shells
Requires:	bash-completion >= 2.0
Suggests:	%{name} = %{version}-%{release}
Suggests:	python3-%{pypi_name} = %{version}-%{release}

%description -n bash-completion-python-argcomplete
Bash completion for argparse based Python scripts.

%description -n bash-completion-python-argcomplete -l pl.UTF-8
Bashowe dopełnianie parametrów dla skryptów Pythona opartych na
argparse.

%prep
%setup -q -n %{pypi_name}-%{version}

%package apidocs
Summary:	API documentation for Python argcomplete module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona argcomplete
Group:		Documentation

%description apidocs
API documentation for Python argcomplete module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona argcomplete.

%build
export LC_ALL=C.UTF-8
%if %{with python2}
%py_build

%if %{with tests}
%{__python} test/test.py
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} test/test.py
%endif
%endif

%if %{with doc}
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT
%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%{__rm} -r $RPM_BUILD_ROOT%{_bindir}
%py3_install
%endif

install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p argcomplete/bash_completion.d/python-argcomplete $RPM_BUILD_ROOT%{bash_compdir}

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc Authors.rst Changes.rst README.rst
%if %{without python3}
%attr(755,root,root) %{_bindir}/activate-global-python-argcomplete
%attr(755,root,root) %{_bindir}/python-argcomplete-check-easy-install-script
%attr(755,root,root) %{_bindir}/python-argcomplete-tcsh
%attr(755,root,root) %{_bindir}/register-python-argcomplete
%endif
%{py_sitescriptdir}/%{module}
%{py_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{pypi_name}
%defattr(644,root,root,755)
%doc Authors.rst Changes.rst README.rst
%attr(755,root,root) %{_bindir}/activate-global-python-argcomplete
%attr(755,root,root) %{_bindir}/python-argcomplete-check-easy-install-script
%attr(755,root,root) %{_bindir}/python-argcomplete-tcsh
%attr(755,root,root) %{_bindir}/register-python-argcomplete
%{py3_sitescriptdir}/%{module}
%{py3_sitescriptdir}/%{egg_name}-%{version}-py*.egg-info
%endif

%files -n bash-completion-python-argcomplete
%defattr(644,root,root,755)
%{bash_compdir}/python-argcomplete

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
