# See this for all pyproject macros: https://src.fedoraproject.org/rpms/pyproject-rpm-macros
# New guidelines: https://fedoraproject.org/wiki/Changes/PythonPackagingGuidelines202x

# Enabled by default
# If the package needs to download data for the test which cannot be done in
# koji, these can be disabled in koji by using `bcond_with` instead, but the
# tests must be validated in mock with network enabled like so:
# mock -r fedora-rawhide-x86_64 rebuild <srpm> --enable-network --rpmbuild-opts="--with tests"
%bcond_without tests

# Replace "tiny-proxy" with the appropriate value using your editor's
# search and replace function. It is preferred to using macros like %{pypi_name}
# because they make the spec harder to read especially in cases where the
# canonical ("pretty name") of the module is different from its name on pypi


# for github etc. use the forgemacros
# https://docs.fedoraproject.org/en-US/packaging-guidelines/SourceURL/#_using_forges_hosted_revision_control

%global _description %{expand:
Simple proxy (SOCKS4(a), SOCKS5(h), HTTP tunnel) server built with anyio. It is
used for testing python-socks, aiohttp-socks and httpx-socks packages.}

Name:           python-tiny-proxy
Version:        0.2.0
Release:        %{autorelease}
Summary:        Simple proxy server (SOCKS4(a), SOCKS5(h), HTTP tunnel)

# https://fedoraproject.org/wiki/Licensing:Main?rd=Licensing#Good_Licenses
License:
URL:            https://pypi.org/pypi/tiny-proxy
Source0:        %{pypi_source tiny-proxy}

BuildArch:      noarch

%description %_description

%package -n python3-tiny-proxy
Summary:        %{summary}
# pyproject-rpm-macros is also pulled in by python3-devel
BuildRequires:  python3-devel

%description -n python3-tiny-proxy %_description

%prep
%autosetup -n tiny-proxy-%{version}

# Comment out to remove /usr/bin/env shebangs
# Can use something similar to correct/remove /usr/bin/python shebangs also
# find . -type f -name "*.py" -exec sed -i '/^#![  ]*\/usr\/bin\/env.*$/ d' {} 2>/dev/null ';'

%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel

%install
%pyproject_install
%pyproject_save_files tiny-proxy

%check
%if %{with tests}
%{pytest}
# or %%{tox}
%endif

# LICENSE/COPYING are included in the dist-info, so we do not need to
# explicitly list them again
%files -n python3-tiny-proxy -f %{pyproject_files}
%doc README.rst

%changelog
%autochangelog
