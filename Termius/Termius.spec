#
# spec file for package Termius
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


Name:           Termius
Version:        8.12.1
Release:        2%{?dist}
Summary:        SSH remote access terminal for sysadmins and network engineers
License:        NonFree
URL:            https://termius.com
Source:         https://autoupdate.termius.com/linux/%{name}.deb
BuildRequires:  bsdtar
BuildRequires:  desktop-file-utils
BuildRequires:  fdupes
BuildRequires:  hicolor-icon-theme
BuildRequires:  shared-mime-info
Requires:       pkgconfig(systemd)
Requires:       alsa
Requires:       alsa-oss
Requires:       dbus-1-common
Requires:       expat
Requires:       glibc
Requires:       Mesa
Requires:       mozilla-nspr

%global debug_package %{nil}
%global __strip "/bin/true"

%description
Termius is described as more than a mere SSH client –
It is a complete command-line solution that’s redefining remote access for sysadmins and network engineers.

%prep
mkdir -p "%{_builddir}/%{name}-%{version}/"
bsdtar -xf "%{_sourcedir}/%{name}.deb" -C %{_builddir}
bsdtar -xf "%{_builddir}/data.tar.xz" -C "%{_builddir}/%{name}-%{version}/"
echo " -> Removing unnecessary file properties from the DEB binary package: "
rm -vfdr "%{_builddir}/%{name}-%{version}/etc/"

%build

%install
export NO_BRP_CHECK_RPATH='true'
cp -a %{_builddir}/%{name}-%{version}/* -t %{buildroot}
install -D "%{buildroot}/%{_datadir}/icons/hicolor/512x512/apps/termius-app.png" -t "%{buildroot}/%{_datadir}/pixmaps/"
install -D "%{buildroot}/opt/%{name}/LICENSE.electron.txt" -t "%{buildroot}/%{_datadir}/licenses/%{name}/"
install -D "%{buildroot}/opt/%{name}/LICENSES.chromium.html" -t "%{buildroot}/%{_datadir}/licenses/%{name}/"
install -D "%{buildroot}/%{_datadir}/doc/termius-app/changelog.gz" -t "%{buildroot}/%{_datadir}/doc/packages/%{name}/"
echo " -> Removing redundant file - changelog.gz:"
rm -vfdr "%{buildroot}/%{_datadir}/doc/termius-app/"

%post
echo " -> Linking binaries from SOURCE to the system:"
ln -sf '/opt/%{name}/termius-app' '/usr/bin/termius'

echo " -> Imposing sandboxing by modifying SUID properties for Electron 5+:"
chmod 4755 '/opt/%{name}/chrome-sandbox' || true

update-mime-database '/usr/share/mime' || true
update-desktop-database '/usr/share/applications' || true

%postun
echo " -> Removing binary link from the system:"
rm -vf '/usr/bin/termius'

%files
%dir "/opt/"
%dir "/opt/%{name}"
%dir %{_datadir}

/opt/%{name}/*
%{_datadir}/*

%changelog
