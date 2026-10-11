Name:           anki
Version:        26.09.3
Release:        2%{?dist}
Summary:        Flashcard program for using space repetition learning
License:        AGPL-3.0-or-later AND GPL-3.0-or-later AND LGPL-3.0-or-later AND MIT AND BSD-3-Clause AND CC-BY-SA-3.0 AND CC-BY-3.0 AND Apache-2.0 AND CC-BY-2.5
URL:            https://apps.ankiweb.net/
Packager:       madonuko <mado@fyralabs.com>
BuildRequires:  python3-devel >= 3.12
BuildRequires:  pyproject-rpm-macros >= 1.23.0
BuildRequires:  python3-pip python3-installer python3-packaging rpm_macro(fdupes) desktop-file-utils
BuildRequires:  make cargo git rsync ninja-build libxcrypt-compat gcc gcc-c++ just
Requires:       hicolor-icon-theme sox libxcrypt-compat python3-pyqt6 python3-pyqt6-webengine
Recommends:     (mpv or mpv-nightly)
Obsoletes:      anki <= 2.1.15
Conflicts:      anki-qt5
Patch0:         0001-No-update.patch

%description
Anki is a program designed to help you remember facts (such as words and
phrases in a foreign language) as easily, quickly and efficiently as possible.
Anki is based on a theory called spaced repetition.

%prep
%git_clone https://github.com/ankitects/anki
%patch -P 0 -p1

%build
# Build the Python wheels without invoking upstream's release tooling.
export RELEASE=1
just wheels

%install
mkdir -p %{_pyproject_wheeldir}
cp out/wheels/*.whl %{_pyproject_wheeldir}
%pyproject_install
%pyproject_save_files -D anki anki
%pyproject_save_files -D aqt aqt _aqt

install -Dm644 'qt/installer/linux-template/{{ cookiecutter.format }}/{{ cookiecutter.app_name }}/anki.desktop' %{buildroot}/%{_datadir}/applications/anki.desktop
install -Dm644 qt/aqt/data/qt/icons/anki.png %{buildroot}/%{_datadir}/pixmaps/anki.png

%fdupes %{buildroot}%{python3_sitelib}/_aqt/data/

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/anki.desktop

%files -f %{pyproject_files}-anki -f %{pyproject_files}-aqt
%license LICENSE*
%doc README*
%{_bindir}/anki
%{_bindir}/ankiw
%{_datadir}/applications/anki.desktop
%{_datadir}/pixmaps/anki.png

%changelog
* Sat Oct 10 2026 Terra Packaging Team <terra@fyralabs.com> - 26.09.3-2
- Update the source build and wheel installation for current Anki releases

* Tue Jan 3 2023 madonuko <mado@fyralabs.com> - 2.1.60
- Initial package
