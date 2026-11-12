#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests

%define		module		argcomplete
Summary:	Bash tab completion for argparse
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów dla argparse
Name:		python3-%{module}
Version:	3.7.2
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/argcomplete/
Source0:	https://files.pythonhosted.org/packages/source/a/argcomplete/%{module}-%{version}.tar.gz
# Source0-md5:	b6553ad23016cb210399570522f90223
URL:		https://github.com/kislyuk/argcomplete
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-hatchling
BuildRequires:	python3-installer
%if %{with tests}
BuildRequires:	python3-pexpect
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	python3-furo
BuildRequires:	python3-sphinx_copybutton
BuildRequires:	python3-sphinxext.opengraph
BuildRequires:	sphinx-pdg-3
%endif
%if %{with tests}
BuildRequires:	bash
BuildRequires:	fish
BuildRequires:	pip
%endif
Requires:	python3-modules >= 1:3.10
Obsoletes:	bash-completion-python-argcomplete < 3
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

%package apidocs
Summary:	API documentation for Python argcomplete module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona argcomplete
Group:		Documentation

%description apidocs
API documentation for Python argcomplete module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona argcomplete.

%prep
%setup -q -n %{module}-%{version}

%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' argcomplete/scripts/register_python_argcomplete.py

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} test/test.py
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

install -d $RPM_BUILD_ROOT{%{bash_compdir},%{zsh_compdir}}
%{__mv} $RPM_BUILD_ROOT%{py3_sitescriptdir}/argcomplete/bash_completion.d/_python-argcomplete $RPM_BUILD_ROOT%{zsh_compdir}
ln $RPM_BUILD_ROOT%{zsh_compdir}/_python-argcomplete $RPM_BUILD_ROOT%{bash_compdir}/python-argcomplete
rmdir $RPM_BUILD_ROOT%{py3_sitescriptdir}/argcomplete/bash_completion.d

# script for copying completions to system location
%{__rm} $RPM_BUILD_ROOT%{py3_sitescriptdir}/argcomplete/scripts/activate_global_python_argcomplete.py
%{__rm} $RPM_BUILD_ROOT%{_bindir}/activate-global-python-argcomplete

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Authors.rst Changes.rst NOTICE README.rst SECURITY.md
%attr(755,root,root) %{_bindir}/register-python-argcomplete
%{py3_sitescriptdir}/argcomplete
%{py3_sitescriptdir}/argcomplete-%{version}.dist-info
%{bash_compdir}/python-argcomplete
%{zsh_compdir}/_python-argcomplete

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
