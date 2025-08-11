Name:           python-docx2txt
Version:        0.11
Release:        1%{?dist}
Summary:        A pure python-based utility to extract text and images from docx files.

License:        MIT
URL:            https://github.com/ryan-blakley/python-docx2txt
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools

Requires:       python3

%description
A pure python-based utility to extract text and images from docx files.

%prep
%autosetup -n %{name}-%{version}

%build
%py3_build

%install
%py3_install

%files
%license LICENSE.txt
%doc README.md
%{_bindir}/*
%{python3_sitelib}/*

%changelog
* Mon Aug 11 2025 Ryan Blakley <rblakley@redhat.com> 0.11-1
- Switch how images are extracted (rblakley@redhat.com)

* Wed Aug 06 2025 Ryan Blakley <rblakley@redhat.com> 0.10-1
- new package built with tito

* Wed Aug 06 2025 Ryan Blakley <rblakley@redhat.com> - 0.9-1
- Initial fork and rework to be able to build as an RPM.