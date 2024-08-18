%global srcname keycloak-httpd-client-install
%global summary Tools to configure Apache HTTPD as Keycloak client

%if (0%{?fedora} > 0 && 0%{?fedora} < 30) || (0%{?rhel} > 0 && 0%{?rhel} <= 7)
  %bcond_without python2
  %bcond_without python3
%endif

%if 0%{?fedora} >= 30 || 0%{?rhel} >= 8
  %bcond_with python2
  %bcond_without python3
%endif

Name:           %{srcname}
Version:        1.2
Release:        %{?release_string}%{!?release_string: 1}%{?dist}
Summary:        %{summary}


License:        GPL-3.0-or-later
URL:            https://github.com/lachset/keycloak-httpd-client-install
Source0:        https://github.com/lachset/keycloak-httpd-client-install/releases/download/%{version}/keycloak-httpd-client-install-%{version}.tar.gz
BuildArch:      noarch

%if %{with python2}
BuildRequires:  python2-devel
%endif
# ^^^ with_python2

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  (python3-setuptools if python3-devel >= 3.12)
%endif

Requires:       %{_bindir}/keycloak-httpd-client-install

%description
Keycloak is a federated Identity Provider (IdP). Apache HTTPD supports
a variety of authentication modules which can be configured to utilize
a Keycloak IdP to perform authentication. This package contains
libraries and tools which can automate and simplify configuring an
Apache HTTPD authentication module and registering as a client of a
Keycloak IdP.

%if %{with python2}
%package -n python2-%{srcname}
Summary:        %{summary}

%{?python_provide:%python_provide python2-%{srcname}}

Requires:       %{name} = %{version}-%{release}
Requires:       python2-requests
Requires:       python2-requests-oauthlib
Requires:       python2-jinja2
Requires:       %{_bindir}/keycloak-httpd-client-install

%description -n python2-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.
%endif
# ^^^ with_python2

%if 0%{?with_python3}
%package -n python3-%{srcname}
Summary:        %{summary}

%{?python_provide:%python_provide python3-%{srcname}}

Requires:       %{name} = %{version}-%{release}
Requires:       python3-requests
Requires:       python3-requests-oauthlib
Requires:       python3-jinja2
Requires:       python3-lxml

%description -n python3-%{srcname}
Keycloak is an authentication server. This package contains libraries and
programs which can invoke the Keycloak REST API and configure clients
of a Keycloak server.

%endif

%prep
%autosetup -n %{srcname}-%{version} -p1

%build
%if %{with python2}
%py2_build
%endif
# ^^^ with_python2

%if 0%{?with_python3}
%py3_build
%endif

%install
%if %{with python2}
# Must do the python2 install first because the scripts in /usr/bin are
# overwritten with every setup.py install, and in general we want the
# python3 version to be the default.
%py2_install
%endif
# ^^^ with_python2

%if 0%{?with_python3}
# py3_install won't overwrite files if they have a timestamp greater-than
# or equal to the py2 installed files. If both the py2 and py3 builds execute
# quickly the files end up with the same timestamps thus leaving the py2
# version in the py3 install. Therefore remove any files susceptible to this.
%if %{with python2}
rm %{buildroot}%{_bindir}/keycloak-httpd-client-install
%endif
# ^^^ with_python2
%py3_install
%endif

install -d -m 755 %{buildroot}/%{_mandir}/man8
install -c -m 644 doc/keycloak-httpd-client-install.8 %{buildroot}/%{_mandir}/man8

%files
%license LICENSE.txt
%doc README.md doc/ChangeLog
%{_datadir}/%{srcname}/

%if %{with python2}
# Note that there is no %%files section for the unversioned python module if we are building for several python runtimes
%files -n python2-%{srcname}
%{python2_sitelib}/*

%if ! 0%{?with_python3}
%{_bindir}/keycloak-httpd-client-install
%{_bindir}/keycloak-rest
%{_mandir}/man8/*
%endif
%endif
# ^^^ with_python2

%if 0%{?with_python3}
%files -n python3-%{srcname}
%{python3_sitelib}/*
%{_bindir}/keycloak-httpd-client-install
%{_bindir}/keycloak-rest
%{_mandir}/man8/*
%endif

%changelog
* Mon Aug 19 2024 Tomas Halman <tomas@halman.net> - 1.2-1
  Repository cleanup, preparing for new version
  Spec file is adopted from Fedora.
