%bcond_without check

# A daemon that manages a pool of block devices to create flexible filesystems
%global __cargo_is_lib() false
%global udevdir %(pkg-config --variable=udevdir udev)
%global dracutdir %(pkg-config --variable=dracutdir dracut)

Name:           stratisd
Version:        2.4.2
Release:        2%{?dist}
Summary:        Daemon that manages block devices to create filesystems

License:        MPLv2.0
URL:            https://github.com/stratis-storage/stratisd
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/%{name}-%{version}-vendor.tar.gz

ExclusiveArch:  %{rust_arches}
ExcludeArch:    i686
BuildRequires:  rust-toolset
BuildRequires:  systemd-devel
BuildRequires:  dbus-devel
BuildRequires:  libblkid-devel
BuildRequires:  cryptsetup-devel
BuildRequires:  clang
BuildRequires:  dracut
BuildRequires:  %{_bindir}/a2x

Requires:       xfsprogs
Requires:       device-mapper-persistent-data
Requires:       systemd-libs
Requires:       dbus-libs
Requires:       cryptsetup >= 2.3.0

Recommends:     clevis-luks >= 15

%description
%{summary}.

%package dracut


Summary: Dracut modules for use with stratisd

ExclusiveArch: ${rust_arches}

Requires:     stratisd
Requires:     dracut >= 049-136
Requires:     plymouth

%description dracut

This package contains dracut modules to be used with stratisd
to enable using Stratis filesystems as the root filesystem for
a Linux install.

%prep
%setup -q -n %{name}-%{version}

# Source1 is vendored dependencies
%cargo_prep -V 1

%build
%cargo_build --bin=stratisd
%cargo_build --bin=stratis-min --bin=stratisd-min --bin=stratis-utils --no-default-features --features min,systemd_compat
a2x -f manpage docs/stratisd.txt

%install
%{__install} -Dpm0644 -t %{buildroot}%{_datadir}/dbus-1/system.d stratisd.conf
# Daemon should be really private
mkdir -p %{buildroot}/developer_tools
%{__install} -Dpm0755 -t %{buildroot}%{_libexecdir} target/release/stratisd
%{__install} -Dpm0644 -t %{buildroot}%{_mandir}/man8 docs/stratisd.8
%{__install} -Dpm0644 -t %{buildroot}%{_udevrulesdir} udev/61-stratisd.rules
%{__install} -Dpm0644 -t %{buildroot}%{_unitdir} systemd/stratisd.service
%{__install} -Dpm0644 -t %{buildroot}%{dracutdir}/dracut.conf.d dracut/90-stratis.conf
mkdir -p %{buildroot}%{dracutdir}/modules.d/90stratis
%{__install} -Dpm0755 -t %{buildroot}%{dracutdir}/modules.d/90stratis dracut/90stratis/module-setup.sh
%{__install} -Dpm0755 -t %{buildroot}%{dracutdir}/modules.d/90stratis dracut/90stratis/stratis-rootfs-setup
%{__install} -Dpm0644 -t %{buildroot}%{dracutdir}/modules.d/90stratis dracut/90stratis/stratisd-min.service
%{__install} -Dpm0644 -t %{buildroot}%{dracutdir}/modules.d/90stratis dracut/90stratis/61-stratisd.rules
mkdir -p %{buildroot}%{dracutdir}/modules.d/90stratis-clevis
%{__install} -Dpm0755 -t %{buildroot}%{dracutdir}/modules.d/90stratis-clevis dracut/90stratis-clevis/module-setup.sh
%{__install} -Dpm0755 -t %{buildroot}%{dracutdir}/modules.d/90stratis-clevis dracut/90stratis-clevis/stratis-clevis-rootfs-setup
%{__install} -Dpm0644 -t %{buildroot}%{_unitdir} systemd/stratisd-min-postinitrd.service
%{__install} -Dpm0644 -t %{buildroot}%{_unitdir} systemd/stratis-fstab-setup\@.service

mkdir -p %{buildroot}%{udevdir}
cp target/release/stratis-utils target/release/stratis-str-cmp
%{__install} -Dpm0755 -t %{buildroot}%{udevdir} target/release/stratis-str-cmp
ln %{buildroot}%{udevdir}/stratis-str-cmp %{buildroot}%{udevdir}/stratis-base32-decode
mkdir -p %{buildroot}%{_bindir}
ln %{buildroot}%{udevdir}/stratis-str-cmp %{buildroot}%{_bindir}/stratis-predict-usage
mkdir -p %{buildroot}%{_systemdgeneratordir}
ln %{buildroot}%{udevdir}/stratis-str-cmp %{buildroot}%{_systemdgeneratordir}/stratis-clevis-setup-generator
ln %{buildroot}%{udevdir}/stratis-str-cmp %{buildroot}%{_systemdgeneratordir}/stratis-setup-generator
%{__install} -Dpm0755 -t %{buildroot}%{_bindir} target/release/stratis-min
%{__install} -Dpm0755 -t %{buildroot}%{_libexecdir} target/release/stratisd-min
%{__install} -Dpm0755 -t %{buildroot}%{_usr}/lib/systemd systemd/stratis-fstab-setup


%if %{with check}
%check
%cargo_test -- --skip real_ --skip loop_ --skip travis_
%endif

%post
%systemd_post stratisd.service

%preun
%systemd_preun stratisd.service

%postun
%systemd_postun_with_restart stratisd.service

%files
%license LICENSE
%doc README.md
%{_libexecdir}/stratisd
%dir %{_datadir}/dbus-1
%{_datadir}/dbus-1/system.d/stratisd.conf
%{_mandir}/man8/stratisd.8*
%{_unitdir}/stratisd.service
%config %{_udevrulesdir}/61-stratisd.rules
%{udevdir}/stratis-str-cmp
%{udevdir}/stratis-base32-decode
%{_bindir}/stratis-predict-usage
%{_unitdir}/stratisd-min-postinitrd.service
%{_unitdir}/stratis-fstab-setup@.service
%{_bindir}/stratis-min
%{_libexecdir}/stratisd-min
%{_usr}/lib/systemd/stratis-fstab-setup

%files dracut
%license LICENSE
%{dracutdir}/dracut.conf.d/90-stratis.conf
%{dracutdir}/modules.d/90stratis-clevis/module-setup.sh
%{dracutdir}/modules.d/90stratis-clevis/stratis-clevis-rootfs-setup
%{dracutdir}/modules.d/90stratis/61-stratisd.rules
%{dracutdir}/modules.d/90stratis/module-setup.sh
%{dracutdir}/modules.d/90stratis/stratis-rootfs-setup
%{dracutdir}/modules.d/90stratis/stratisd-min.service
%{_systemdgeneratordir}/stratis-clevis-setup-generator
%{_systemdgeneratordir}/stratis-setup-generator

%changelog
* Fri Aug 20 2021  Bryan Gurney <bgurney@redhat.com> - 2.4.2-2
- Add stratisd to requires for stratisd-dracut
- Resolves: rhbz#1995916

* Wed Jun 02 2021  Bryan Gurney <bgurney@redhat.com> - 2.4.2-1
- Update to 2.4.2
- Resolves: rhbz#1931671
- Ensure that binaries are installed with proper features enabled
- Split dracut modules out to subpackage
- Add additional dependencies in dracut module

* Wed May 12 2021  Bryan Gurney <bgurney@redhat.com> - 2.4.0-3
- Update to 2.4.0
- Resolves: rhbz#1931671
- Improve stratis by adding Multi-threading
- Resolves: rhbz#1927485
- Dump stratis configuration on demand or in debug
- Resolves: rhbz#1735475
- Add noalign option to XFS creation on MDV
- Resolves: rhbz#1908318
- Cap thinpool metadata device size at devicemapper-set limit
- Resolves: rhbz#1707461

* Tue Dec 08 2020  Dennis Keefe <dkeefe@redhat.com> - 2.3.0-2
- Update to 2.3.0
- Resolves: rhbz#1885328
- Stratis devices inhabit an existing root directory path
- Resolves: rhbz#1798244
- Add Clevis Support
- Resolves: rhbz#1868100
- Improve stratisd log levels
- Resolves: rhbz#1757976
 
* Sat Jun 06 2020  Dennis Keefe <dkeefe@redhat.com> - 2.1.0-1
- Update to 2.1.0
- Resolves: rhbz#1791473
- Update Stratis RPM Spec File
- Resolves: rhbz#1828487
- Support per-pool encryption of the devices that form a pool's data tier
- Resolves: rhbz#1768580
- Improve systemd unit file description
- Resolves: rhbz#1756525

* Tue Nov 12 2019  Dennis Keefe <dkeefe@redhat.com> - 2.0.0-4
- Update to 2.0.0
- Resolves: rhbz#1760906
- Fix a bug where last update time for variable length metadata was not set
  properly on startup:
- Resolves: rhbz#1720399
- Specify path of PID file as "/run/stratisd.pid" instead of 
  "/var/run/stratisd.pid".
- Resolves: rhbz#1754649
- For a particular log entry, reduce log level from INFO to DEBUG and make the
  log message more detailed:
- Resolves: rhbz#1680052
 
* Mon Jun 3 2019 Dennis Keefe <dkeefe@redhat.com> - 1.0.4-2
- update to 1.0.4

* Wed Jan 9 2019 Andy Grover <agrover@redhat.com> - 1.0.3-1
- Update to 1.0.3

* Tue Dec 11 2018 Andy Grover <agrover@redhat.com> - 1.0.2-1
- Update to 1.0.2

* Tue Nov 6 2018 Andy Grover <agrover@redhat.com> - 1.0.1-1
- Update to 1.0.1

* Mon Oct 8 2018 Andy Grover <agrover@redhat.com> - 1.0.0-2
- Fix for non-Dbus activation

* Tue Oct 2 2018 Andy Grover <agrover@redhat.com> - 1.0.0-1
- Update to 1.0.0

* Wed Aug 08 2018 Josh Stone <jistone@redhat.com> - 0.5.5-2
- Rebuild with rust-toolset-1.26

* Thu Aug 2 2018 Andy Grover <agrover@redhat.com> - 0.5.5-1
- Update to 0.5.5

* Fri Jul 13 2018 Andy Grover <agrover@redhat.com> - 0.5.4-1
- Update to 0.5.4

* Thu May 24 2018 Andy Grover <agrover@redhat.com> - 0.5.2-1
- Initial packaging for RHEL 8
- Update to 0.5.2
