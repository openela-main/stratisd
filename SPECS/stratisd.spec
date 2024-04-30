%bcond_without check

%global udevdir %(pkg-config --variable=udevdir udev)
%global dracutdir %(pkg-config --variable=dracutdir dracut)

Name:           stratisd
Version:        3.6.2
Release:        1%{?dist}
Summary:        Daemon that manages block devices to create filesystems

License:        MPL-2.0
URL:            https://github.com/stratis-storage/stratisd
Source0:        %{url}/archive/stratisd-v%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/stratisd-v%{version}/%{name}-%{version}-vendor.tar.gz
Source2:        %{crates_source}


ExclusiveArch:  %{rust_arches}
%if 0%{?rhel}
ExcludeArch:    i686
%endif

%if 0%{?rhel}
BuildRequires:  rust-toolset
%else
BuildRequires:  rust-packaging
%endif
BuildRequires:  rust-srpm-macros
BuildRequires:  systemd-devel
BuildRequires:  dbus-devel
BuildRequires:  libblkid-devel
BuildRequires:  cryptsetup-devel
BuildRequires:  clang
BuildRequires:  glibc-static
BuildRequires:  device-mapper-devel
BuildRequires:  %{_bindir}/a2x

# Required to calculate install directories
BuildRequires:  systemd
BuildRequires:  dracut

Requires:       xfsprogs
Requires:       device-mapper-persistent-data
Requires:       systemd-libs
Requires:       dbus-libs
Requires:       cryptsetup-libs
Requires:       libblkid

# stratisd does not require clevis; it can be used in restricted environments
# where clevis is not available.
# If using encryption via clevis, stratisd requires the instance of clevis
# that it uses to have been built in an environment with cryptsetup >= 2.6.0.
Recommends:     clevis-luks >= 18

Provides: bundled(crate(aho-corasick)) = 1.0.2
Provides: bundled(crate(anstream)) = 0.3.2
Provides: bundled(crate(anstyle)) = 1.0.1
Provides: bundled(crate(anstyle-parse)) = 0.2.1
Provides: bundled(crate(anstyle-query)) = 1.0.0
Provides: bundled(crate(assert_cmd)) = 2.0.11
Provides: bundled(crate(assert_matches)) = 1.5.0
Provides: bundled(crate(async-trait)) = 0.1.68
Provides: bundled(crate(autocfg)) = 1.1.0
Provides: bundled(crate(bindgen)) = 0.59.2
Provides: bundled(crate(bit-set)) = 0.5.3
Provides: bundled(crate(bit-vec)) = 0.6.3
Provides: bundled(crate(bitflags)) = 2.4.0
Provides: bundled(crate(bitflags)) = 1.3.2
Provides: bundled(crate(block-buffer)) = 0.10.4
Provides: bundled(crate(bstr)) = 1.5.0
Provides: bundled(crate(byteorder)) = 1.4.3
Provides: bundled(crate(cc)) = 1.0.79
Provides: bundled(crate(cexpr)) = 0.6.0
Provides: bundled(crate(cfg-if)) = 1.0.0
Provides: bundled(crate(cfg-if)) = 0.1.10
Provides: bundled(crate(chrono)) = 0.4.26
Provides: bundled(crate(clang-sys)) = 1.6.1
Provides: bundled(crate(clap)) = 4.3.5
Provides: bundled(crate(clap_builder)) = 4.3.5
Provides: bundled(crate(clap_lex)) = 0.5.0
Provides: bundled(crate(colorchoice)) = 1.0.0
Provides: bundled(crate(cpufeatures)) = 0.2.8
Provides: bundled(crate(crc)) = 3.0.1
Provides: bundled(crate(crc-catalog)) = 2.2.0
Provides: bundled(crate(crypto-common)) = 0.1.6
Provides: bundled(crate(data-encoding)) = 2.4.0
Provides: bundled(crate(dbus)) = 0.9.7
Provides: bundled(crate(dbus-tree)) = 0.9.2
Provides: bundled(crate(devicemapper)) = 0.34.0
Provides: bundled(crate(devicemapper-sys)) = 0.2.0
Provides: bundled(crate(difflib)) = 0.4.0
Provides: bundled(crate(digest)) = 0.10.7
Provides: bundled(crate(doc-comment)) = 0.3.3
Provides: bundled(crate(either)) = 1.8.1
Provides: bundled(crate(env_logger)) = 0.10.0
Provides: bundled(crate(errno)) = 0.3.1
Provides: bundled(crate(errno)) = 0.2.8
Provides: bundled(crate(fastrand)) = 1.9.0
Provides: bundled(crate(float-cmp)) = 0.9.0
Provides: bundled(crate(futures)) = 0.3.28
Provides: bundled(crate(futures-channel)) = 0.3.28
Provides: bundled(crate(futures-core)) = 0.3.28
Provides: bundled(crate(futures-executor)) = 0.3.28
Provides: bundled(crate(futures-io)) = 0.3.28
Provides: bundled(crate(futures-macro)) = 0.3.28
Provides: bundled(crate(futures-sink)) = 0.3.28
Provides: bundled(crate(futures-task)) = 0.3.28
Provides: bundled(crate(futures-util)) = 0.3.28
Provides: bundled(crate(generic-array)) = 0.14.7
Provides: bundled(crate(getrandom)) = 0.2.10
Provides: bundled(crate(glob)) = 0.3.1
Provides: bundled(crate(humantime)) = 2.1.0
Provides: bundled(crate(iana-time-zone)) = 0.1.57
Provides: bundled(crate(io-lifetimes)) = 1.0.11
Provides: bundled(crate(iocuddle)) = 0.1.1
Provides: bundled(crate(is-terminal)) = 0.4.7
Provides: bundled(crate(itertools)) = 0.11.0
Provides: bundled(crate(itertools)) = 0.10.5
Provides: bundled(crate(itoa)) = 1.0.6
Provides: bundled(crate(lazy_static)) = 1.4.0
Provides: bundled(crate(lazycell)) = 1.3.0
Provides: bundled(crate(libblkid-rs)) = 0.3.1
Provides: bundled(crate(libblkid-rs-sys)) = 0.2.0
Provides: bundled(crate(libc)) = 0.2.149
Provides: bundled(crate(libcryptsetup-rs)) = 0.9.1
Provides: bundled(crate(libcryptsetup-rs-sys)) = 0.3.0
Provides: bundled(crate(libdbus-sys)) = 0.2.5
Provides: bundled(crate(libloading)) = 0.7.4
Provides: bundled(crate(libm)) = 0.2.7
Provides: bundled(crate(libmount)) = 0.1.15
Provides: bundled(crate(libudev)) = 0.3.0
Provides: bundled(crate(libudev-sys)) = 0.1.4
Provides: bundled(crate(linux-raw-sys)) = 0.3.8
Provides: bundled(crate(log)) = 0.4.19
Provides: bundled(crate(loopdev)) = 0.4.0
Provides: bundled(crate(memchr)) = 2.5.0
Provides: bundled(crate(memoffset)) = 0.7.1
Provides: bundled(crate(minimal-lexical)) = 0.2.1
Provides: bundled(crate(mio)) = 0.8.8
Provides: bundled(crate(nix)) = 0.26.2
Provides: bundled(crate(nix)) = 0.14.1
Provides: bundled(crate(nom)) = 7.1.3
Provides: bundled(crate(normalize-line-endings)) = 0.3.0
Provides: bundled(crate(num-traits)) = 0.2.15
Provides: bundled(crate(num_cpus)) = 1.15.0
Provides: bundled(crate(once_cell)) = 1.18.0
Provides: bundled(crate(peeking_take_while)) = 0.1.2
Provides: bundled(crate(pin-project-lite)) = 0.2.9
Provides: bundled(crate(pin-utils)) = 0.1.0
Provides: bundled(crate(pkg-config)) = 0.3.27
Provides: bundled(crate(ppv-lite86)) = 0.2.17
Provides: bundled(crate(predicates)) = 3.0.3
Provides: bundled(crate(predicates-core)) = 1.0.6
Provides: bundled(crate(predicates-tree)) = 1.0.9
Provides: bundled(crate(pretty-hex)) = 0.3.0
Provides: bundled(crate(proc-macro2)) = 1.0.66
Provides: bundled(crate(proptest)) = 1.2.0
Provides: bundled(crate(quick-error)) = 1.2.3
Provides: bundled(crate(quote)) = 1.0.28
Provides: bundled(crate(rand)) = 0.8.5
Provides: bundled(crate(rand_chacha)) = 0.3.1
Provides: bundled(crate(rand_core)) = 0.6.4
Provides: bundled(crate(rand_xorshift)) = 0.3.0
Provides: bundled(crate(regex)) = 1.8.4
Provides: bundled(crate(regex-automata)) = 0.1.10
Provides: bundled(crate(regex-syntax)) = 0.7.2
Provides: bundled(crate(regex-syntax)) = 0.6.29
Provides: bundled(crate(retry)) = 1.3.1
Provides: bundled(crate(rustc-hash)) = 1.1.0
Provides: bundled(crate(rustix)) = 0.37.25
Provides: bundled(crate(rusty-fork)) = 0.3.0
Provides: bundled(crate(ryu)) = 1.0.13
Provides: bundled(crate(semver)) = 1.0.17
Provides: bundled(crate(serde)) = 1.0.188
Provides: bundled(crate(serde_derive)) = 1.0.188
Provides: bundled(crate(serde_json)) = 1.0.97
Provides: bundled(crate(sha2)) = 0.10.7
Provides: bundled(crate(shlex)) = 1.1.0
Provides: bundled(crate(signal-hook-registry)) = 1.4.1
Provides: bundled(crate(slab)) = 0.4.8
Provides: bundled(crate(socket2)) = 0.4.9
Provides: bundled(crate(static_assertions)) = 1.1.0
Provides: bundled(crate(stratisd_proc_macros)) = 0.2.1
Provides: bundled(crate(strsim)) = 0.10.0
Provides: bundled(crate(syn)) = 2.0.29
Provides: bundled(crate(syn)) = 1.0.109
Provides: bundled(crate(tempfile)) = 3.6.0
Provides: bundled(crate(termcolor)) = 1.2.0
Provides: bundled(crate(termios)) = 0.3.3
Provides: bundled(crate(termtree)) = 0.4.1
Provides: bundled(crate(tokio)) = 1.28.2
Provides: bundled(crate(tokio-macros)) = 2.1.0
Provides: bundled(crate(typenum)) = 1.16.0
Provides: bundled(crate(unarray)) = 0.1.4
Provides: bundled(crate(unicode-ident)) = 1.0.9
Provides: bundled(crate(utf8parse)) = 0.2.1
Provides: bundled(crate(uuid)) = 1.3.4
Provides: bundled(crate(version_check)) = 0.9.4
Provides: bundled(crate(void)) = 1.0.2
Provides: bundled(crate(wait-timeout)) = 0.2.0

%description
%{summary}.

%package dracut
Summary: Dracut modules for use with stratisd

ExclusiveArch:  %{rust_arches}
%if 0%{?rhel}
ExcludeArch:    i686
%endif

Requires:     stratisd
Requires:     dracut >= 051
Requires:     systemd

%description dracut
%{summary}.

%package tools
Summary: Tools that support Stratis operation

ExclusiveArch:  %{rust_arches}
%if 0%{?rhel}
ExcludeArch:    i686
%endif

Requires:     stratisd

%description tools
%{summary}.

%prep
# Rename SOURCE0's top-level directory because it starts with
# stratisd-stratisd-v. GitHub calculates the directory name from the repo name
# + the tag. Extract the upstream crate on top of the extracted GitHub release,
# overwriting changed files. The primary purpose of this step is to ensure that
# the Cargo.toml that is used in building is the one that is generated by
# cargo-publish and cargo-package, not the file with path dependencies that
# GitHub packs up. Tar the overwritten files back up again into a tar file
# with the format and top-level directory that %setup expects cleaning up the
# previously extracted directory and its contents at the same time. Move the
# newly created tar file to the SOURCE0 location.
tar --transform="s/^stratisd\-stratisd-v/stratisd-/" --extract --file %{SOURCE0}
tar --directory=./stratisd-%{version} --strip-components=1 --extract --overwrite --file %{SOURCE2}
tar --create --gzip --file %{SOURCE0}.newfile ./stratisd-%{version} --remove-files
mv %{SOURCE0}.newfile %{SOURCE0}

%setup -q

%if 0%{?rhel}
%cargo_prep -V 1
%else
%cargo_prep
%generate_buildrequires
%cargo_generate_buildrequires -f engine,dbus_enabled,min,systemd_compat,extras,udev_scripts
%endif

%build
%if 0%{?rhel}
%{__cargo} build %{?_smp_mflags} --release --bin=stratisd
%{__cargo} build %{?_smp_mflags} --release --bin=stratis-min --bin=stratisd-min --bin=stratis-utils --no-default-features --features engine,min,systemd_compat
%{__cargo} rustc %{?_smp_mflags} --release --bin=stratis-str-cmp --no-default-features --features udev_scripts -- -Ctarget-feature=+crt-static
%{__cargo} rustc %{?_smp_mflags} --release --bin=stratis-base32-decode --no-default-features --features udev_scripts -- -Ctarget-feature=+crt-static
%{__cargo} build %{?_smp_mflags} --release --bin=stratis-dumpmetadata --no-default-features --features engine,extras,min
%else
%{cargo_license -f engine,dbus_enabled,min,systemd_compat,extras,udev_scripts} > LICENSE.dependencies
%{__cargo} build %{?__cargo_common_opts} --release --bin=stratisd
%{__cargo} build %{?__cargo_common_opts} --release --bin=stratis-min --bin=stratisd-min --bin=stratis-utils --no-default-features --features engine,min,systemd_compat
%{__cargo} rustc %{?__cargo_common_opts} --release --bin=stratis-str-cmp --no-default-features --features udev_scripts -- -Ctarget-feature=+crt-static
%{__cargo} rustc %{?__cargo_common_opts} --release --bin=stratis-base32-decode --no-default-features --features udev_scripts -- -Ctarget-feature=+crt-static
%{__cargo} build %{?__cargo_common_opts} --release --bin=stratis-dumpmetadata --no-default-features --features engine,extras,min
%endif
a2x -f manpage docs/stratisd.txt
a2x -f manpage docs/stratis-dumpmetadata.txt

%install
%make_install DRACUTDIR=%{dracutdir} PROFILEDIR=release

%if %{with check}
%check
# Compile stratisd tests only where package does not use vendoring.
# This is a temporary step, to address the problem of loopdev crate
# 0.4.0 failing to build properly in some situations due to a failure of
# bindgen 0.59.0.
# See https://github.com/stratis-storage/project/issues/607
%if !0%{?rhel}
%cargo_test -- --no-run
%endif
%endif

%post
%systemd_post stratisd.service

%preun
%systemd_preun stratisd.service

%postun
%systemd_postun_with_restart stratisd.service

%files
%license LICENSE
%if 0%{?rhel}
%else
%license LICENSE.dependencies
%endif
%doc README.md
%{_libexecdir}/stratisd
%dir %{_datadir}/dbus-1
%dir %{_datadir}/dbus-1/system.d
%{_datadir}/dbus-1/system.d/stratisd.conf
%{_mandir}/man8/stratisd.8*
%{_unitdir}/stratisd.service
%{_udevrulesdir}/61-stratisd.rules
%{udevdir}/stratis-str-cmp
%{udevdir}/stratis-base32-decode
%{_bindir}/stratis-predict-usage
%{_unitdir}/stratisd-min-postinitrd.service
%{_unitdir}/stratis-fstab-setup@.service
%{_bindir}/stratis-min
%{_libexecdir}/stratisd-min
%{_systemd_util_dir}/stratis-fstab-setup


%files dracut
%license LICENSE
%{dracutdir}/modules.d/90stratis-clevis/module-setup.sh
%{dracutdir}/modules.d/90stratis-clevis/stratis-clevis-rootfs-setup
%{dracutdir}/modules.d/90stratis/61-stratisd.rules
%{dracutdir}/modules.d/90stratis/module-setup.sh
%{dracutdir}/modules.d/90stratis/stratis-rootfs-setup
%{dracutdir}/modules.d/90stratis/stratisd-min.service
%{_systemd_util_dir}/system-generators/stratis-clevis-setup-generator
%{_systemd_util_dir}/system-generators/stratis-setup-generator

%files tools
%license LICENSE
%{_bindir}/stratis-dumpmetadata
%{_mandir}/man8/stratis-dumpmetadata.8*

%changelog
* Mon Nov 20 2023 Bryan Gurney <bgurney@redhat.com> - 3.6.2-1
- Ensure proper alignment of flex devices
- Resolves: RHEL-16736

* Mon Nov 06 2023 Bryan Gurney <bgurney@redhat.com> - 3.6.1-1
- Update to version 3.6.1
- Resolves: RHEL-2278
- Add filesystem growth limits
- Resolves: RHEL-12898

* Mon Jul 31 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.8-1
- Refine handling of partially-set-up pools
- Resolves: rhbz#2223409

* Thu Jun 08 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.7-1
- Increase libcryptsetup-rs dependency lower bound to 0.8.0
- Resolves: rhbz#2213277

* Tue May 16 2023 Bryan Gurney <bgurney@redhat.com> - 3.5.5-1
- Update to version 3.5.5
- Resolves: rhbz#2167463
- Take into account the sector size of crypt devices
- Resolves: rhbz#2170318
- Add stratisd-tools package with stratis-dumpmetadata program
- Resolves: rhbz#2173726
- Support key description key in kernel keyring
- Resolves: rhbz#2038492

* Tue Jan 03 2023 Bryan Gurney <bgurney@redhat.com> - 3.4.4-1
- Use devicemapper-rs version 0.32.3
- Resolves: rhbz#2155689

* Fri Dec 16 2022 Bryan Gurney <bgurney@redhat.com> - 3.4.3-1
- Migrate pool for start pool by name functionality
- Resolves: rhbz#2153593

* Tue Dec 06 2022 Bryan Gurney <bgurney@redhat.com> - 3.4.2-1
- Increase amount of space allocated for thin pool metadata
- Resolves: rhbz#2150109

* Wed Nov 23 2022 Bryan Gurney <bgurney@redhat.com> - 3.4.0-1
- Update to version 3.4.0
- Resolves: rhbz#2124976
- Allow a pool to make use of added capacity of a block device
- Resolves: rhbz#2039955
- Enforce per-pool consistency of block device sector sizes
- Resolves: rhbz#2039957
- Do not read data from device specified in udev remove event
- Resolves: rhbz#2124681
- Specify pool to start by its name
- Resolves: rhbz#2125012

* Wed Aug 24 2022 Bryan Gurney <bgurney@redhat.com> - 3.2.2-1
- Fix assertion for migrating from greedy to lazy allocation
- Resolves: rhbz#2119537

* Mon Aug 01 2022 Bryan Gurney <bgurney@redhat.com> - 3.2.1-1
- Set a per-command ioctl version in device-mapper header
- Resolves: rhbz#2112461

* Fri Jul 08 2022 Bryan Gurney <bgurney@redhat.com> - 3.2.0-1
- Add the ability to stop and start pools
- Resolves: rhbz#2039960

* Wed Jun 08 2022 Bryan Gurney <bgurney@redhat.com> - 3.1.0-2
- Increment release number to include bugs fixed in 3.1.0
- Resolves: rhbz#2039946
- Pass optional size parameter for new filesystem
- Resolves: rhbz#1990905
- Unify rollback to refresh Clevis info on Clevis bind command
- Resolves: rhbz#2005110
- Retarget thinpool to cache device when initializing cache
- Resolves: rhbz#2007018
- Improve thin provisioning implementation
- Resolves: rhbz#2040352
- Verify udev info with libblkid before overwriting
- Resolves: rhbz#2041624

* Tue May 31 2022 Bryan Gurney <bgurney@redhat.com> - 3.1.0-1
- Update to 3.1.0
- Resolves: rhbz#2039946
- Revise stratisd.spec file to unified format
- Remove old rust2rpm config file

* Fri Aug 20 2021 Bryan Gurney <bgurney@redhat.com> - 2.4.2-3
- Add stratisd to requires for stratisd-dracut
- Resolves: rhbz#1996104

* Tue Aug 10 2021 Mohan Boddu <mboddu@redhat.com> - 2.4.2-2
- Rebuilt for IMA sigs, glibc 2.34, aarch64 flags
  Related: rhbz#1991688

* Fri Jun 11 2021 Bryan Gurney <bgurney@redhat.com> - 2.4.2-1
- Update to 2.4.2
- Resolves: rhbz#1914315
- Add boot from root support
- Resolves: rhbz#1869768
- Ensure that binaries are installed with proper features enabled
- Split dracut modules out to subpackage
- Add additional dependencies in dracut module


* Fri Apr 16 2021 Mohan Boddu <mboddu@redhat.com> - 2.3.0-9
- Rebuilt for RHEL 9 BETA on Apr 15th 2021. Related: rhbz#1947937

* Wed Jan 27 2021 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Fri Jan 15 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.3.0-7
- Fix build on ELN

* Fri Jan 15 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.3.0-6
- Make package compatible without violating guidelines

* Fri Jan 15 2021 mulhern <amulhern@redhat.com> - 2.3.0-5
- Add both sources at the same time

* Fri Jan 15 2021 mulhern <amulhern@redhat.com> - 2.3.0-4
- Restore RHEL/Fedora compatible spec file, adding some additional changes

* Fri Jan 15 2021 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.3.0-3
- Partially revert previous commit

* Thu Jan 14 2021 mulhern <amulhern@redhat.com> - 2.3.0-2
- Make RHEL/Fedora compatible spec file

* Tue Jan 12 2021 mulhern <amulhern@redhat.com> - 2.3.0-1
- Update to 2.3.0

* Mon Dec 28 13:34:26 CET 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.2.1-3
- Rebuild

* Sun Dec 27 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.2.1-2
- Rebuild

* Mon Nov 9 2020 mulhern <amulhern@redhat.com> - 2.2.1-1
- Update to 2.2.1

* Mon Oct 19 2020 mulhern <amulhern@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jul 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 07 2020 John Baublitz <jbaublitz@redhat.com> - 2.1.0-1
- Update to 2.1.0

* Wed Feb 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.0.1-2
- Fixup license

* Wed Feb 19 2020 Igor Raits <ignatenkobrain@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Fri Jan 31 2020 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Nov 07 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Fri Sep 06 20:52:06 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.5-1
- Update to 1.0.5

* Sat Jul 27 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jun 04 2019 Josh Stone <jistone@redhat.com> - 1.0.4-2
- Bump nix to 0.14

* Tue May 07 08:16:24 CEST 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.4-1
- Update to 1.0.4

* Wed Mar 06 2019 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.3-1
- Update to 1.0.3

* Wed Dec 12 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.2-1
- Update to 1.0.2

* Fri Nov 02 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.1-1
- Update to 1.0.1

* Thu Sep 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.0.0-1
- Update to 1.0.0

* Wed Sep 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-4
- Add missing systemd scriptlets

* Wed Sep 19 2018 Tony Asleson <tasleson@redhat.com> - 0.9.0-3
- Add systemd unit file
- Remove systemd activation file

* Tue Sep 18 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-2
- Rebuild to workaround pungi bug

* Sat Sep 01 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.9.0-1
- Update to 0.9.0

* Fri Aug 3 2018 Andy Grover <agrover@redhat.com> - 0.5.5-2
- Disable a failing but noncritical test

* Fri Aug 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.5-1
- Update to 0.5.5

* Thu Jul 19 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.4-3
- Upgrade dependencies

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.5.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Jul 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.4-1
- Update to 0.5.4

* Fri Jun 22 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.3-2
- Add -init version of daemon
- Own dbus-1 directory

* Mon Jun 4 2018 Andy Grover <agrover@redhat.com> - 0.5.3-1
- Update to 0.5.3

* Fri May 4 2018 Andy Grover <agrover@redhat.com> - 0.5.2-2
- Add 0002-Prefix-commands-with-entire-path.patch

* Tue May 1 2018 Andy Grover <agrover@redhat.com> - 0.5.2-1
- Update to 0.5.2

* Tue Apr 03 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.1-1
- Update to 0.5.1

* Tue Mar 13 2018 Andy Grover <agrover@redhat.com> - 0.5.0-2
- Add stratisd manpage

* Thu Mar 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.5.0-1
- Update to 0.5.0

* Thu Feb 15 2018 Andy Grover <agrover@redhat.com> - 0.1.5-2
- Require packages that contain binaries that we exec: xfsprogs and
  device-mapper-persistent-data

* Sun Feb 11 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.5-1
- Update to 0.1.5

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.4-3
- Rebuild for rust-packaging v5

* Mon Jan 08 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.4-2
- Move binary under %%{_libexecdir}
- Add dbus service (so it is activatable)
- Fix rand's version bump

* Sun Jan 07 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.1.4-1
- Initial package
