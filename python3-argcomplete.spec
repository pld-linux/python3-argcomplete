#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests

%define		module		argcomplete
Summary:	Bash tab completion for argparse
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów dla argparse
Name:		python3-%{module}
Version:	2.1.2
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://github.com/kislyuk/argcomplete/releases
Source0:	https://github.com/kislyuk/argcomplete/archive/v%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	455a332fdbb651d9715e4d6f7576d11e
URL:		https://github.com/kislyuk/argcomplete
%if %(locale -a | grep -q '^C\.utf8$'; echo $?)
BuildRequires:	glibc-localedb-all
%endif
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
%if %{with tests}
%if "%{py3_ver}" == "3.6" || "%{py3_ver}" == "3.7"
BuildRequires:	python3-importlib_metadata >= 0.23
BuildRequires:	python3-importlib_metadata < 6
%endif
BuildRequires:	python3-pexpect
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
%endif
# pkg_resources module is used from python-argcomplete-check-easy-install-script
Requires:	python3-setuptools
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

%package -n bash-completion-python3-argcomplete
Summary:	Bash completion for argparse
Summary(pl.UTF-8):	Bashowe dopełnianie parametrów dla argparse
Group:		Applications/Shells
Requires:	bash-completion >= 2.0
Requires:	python3-%{module} = %{version}-%{release}
Obsoletes:	bash-completion-python-argcomplete < 2

%description -n bash-completion-python3-argcomplete
Bash completion for argparse based Python scripts.

%description -n bash-completion-python3-argcomplete -l pl.UTF-8
Bashowe dopełnianie parametrów dla skryptów Pythona opartych na
argparse.

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

%build
%py3_build

%if %{with tests}
%{__python3} test/test.py
%endif

%if %{with doc}
PYTHONPATH=$(pwd) \
sphinx-build-3 -b html docs docs/_build/html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

install -d $RPM_BUILD_ROOT%{bash_compdir}
cp -p argcomplete/bash_completion.d/python-argcomplete $RPM_BUILD_ROOT%{bash_compdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Authors.rst Changes.rst README.rst
%attr(755,root,root) %{_bindir}/activate-global-python-argcomplete
%attr(755,root,root) %{_bindir}/python-argcomplete-check-easy-install-script
%attr(755,root,root) %{_bindir}/register-python-argcomplete
%{py3_sitescriptdir}/argcomplete
%{py3_sitescriptdir}/argcomplete-%{version}-py*.egg-info

%files -n bash-completion-python3-argcomplete
%defattr(644,root,root,755)
%{bash_compdir}/python-argcomplete

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_static,*.html,*.js}
%endif
