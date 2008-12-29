%define major 8

Summary:       Squeak Virtual Machine
Name:          squeak-vm
Version:       3.9
Release:       %mkrel 7
License:       Free with restrictions (http://www.squeak.org/download/license.html)
Group:         Development/Other
Source0:       ftp://st.cs.uiuc.edu/Smalltalk/Squeak/%version/unix-linux/src/Squeak-%version-%major.src.tar.gz
Source1:       linex.tar.bz2
Source2:       startsqueak
Patch0:         Squeak-3.9-8.src.patch
Patch1:         Squeak-3.9-8-avoid-depth-32-visuals.patch
URL:           http://www.squeak.org
BuildRequires: libaudiofile-devel
BuildRequires: X11-devel
BuildRequires: x11-proto-devel
BuildRequires: libx11-devel
BuildRequires: gcc
BuildRequires: desktop-file-utils
BuildRequires: libalsa2-devel
Requires:       zenity
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

ExclusiveArch: i586

%description
Squeak is an open, highly-portable Smalltalk-80 implementation whose virtual
machine is written entirely in Smalltalk, making it easy to debug, analyze, and
change. To achieve practical performance, a translator produces an equivalent C
program whose performance is comparable to commercial Smalltalks.

%prep
%setup -q -n Squeak-%version-%major -a 1
%patch0
%patch1 -p1
mkdir build; cd build; ../platforms/unix/config/configure --prefix=/usr --mandir=/usr/share/man

%build
cd build; %make; %make squeak.1; mv squeak.1 squeakvm.1

%install
cd build
%make prefix=%{buildroot}/usr mandir=%{buildroot}/usr/share/man plgdir=%{buildroot}/usr/lib/squeak/%{version}-%{major} install
cd ..
mkdir -p {%buildroot/usr/share/doc,%{buildroot}/usr/share/icons/gnome/48x48/mimetypes,%{buildroot}/usr/share/pixmaps,%{buildroot}/usr/share/mime/packages,%{buildroot}/usr/share/mime-info,%{buildroot}/usr/lib/mime/packages/squeak,%{buildroot}/usr/share/application-registry,%{buildroot}/usr/share/applications}
install -m 0644 linex/gnome-mime-application-squeak*.png  %{buildroot}/usr/share/icons/gnome/48x48/mimetypes
install -m 0644 linex/squeak.png  %{buildroot}/usr/share/pixmaps
install -m 0644 linex/squeak.xml %{buildroot}/usr/share/mime/packages
install -m 0644 linex/squeak.mime %{buildroot}/usr/share/mime-info
install -m 0644 linex/squeak.keys %{buildroot}/usr/share/mime-info
install -m 0644 linex/squeakmime.mandriva %{buildroot}/usr/lib/mime/packages
mv %{buildroot}/usr/lib/mime/packages/squeakmime.mandriva %{buildroot}/usr/lib/mime/packages/squeak
install linex/squeak.applications %{buildroot}/usr/share/application-registry
install linex/squeak.desktop %{buildroot}/usr/share/applications
strip -s --remove-section=.comment %{buildroot}/usr/lib/squeak/%{version}-%{major}/*
install -m 0755 %{SOURCE2} %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/doc/squeak
#mv %{buildroot}/usr/share/doc/squeak/Squeak/* %{buildroot}/usr/share/doc/squeak/

#menu

desktop-file-install \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %name

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post
%update_menus
%update_desktop_database
%update_mime_database
%update_icon_cache gnome
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%clean_desktop_database
%clean_mime_database
%clean_icon_cache hicolor
%endif

%files -f %name.lang
%defattr(-,root,root)
%{_docdir}/squeak/*.gz
%{_bindir}/*
%{_libdir}/mime/packages/squeak/*
%{_libdir}/squeak/*
%{_datadir}/application-registry/squeak.applications
%{_datadir}/applications/squeak.desktop
%{_datadir}/icons/gnome/*/mimetypes/*.png
%{_mandir}/man1/*.lzma
%{_datadir}/mime-info/*
%{_datadir}/mime/packages/squeak.xml
%{_datadir}/pixmaps/squeak.png
