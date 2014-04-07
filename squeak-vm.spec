%define vmver 4.10.2
%define svntag 2614

Summary:	The Squeak virtual machine
Name:		squeak-vm
Version:	%{vmver}.%{svntag}
Release:	7
License:	MIT
Group:		Development/Other
Url:		http://squeakvm.org/unix
Source0:	http://squeakvm.org/unix/release/Squeak-%{version}-src.tar.gz
Source2:	squeak-desktop-files.tar.gz
Patch0:		squeak-vm-dprintf.patch
Patch1:		alsa-fixes.patch
Patch2:		squeak-vm-4.10.2-fix-cmake.patch
Patch3:		squeak-vm-4.10.2-squeak-init-fix.patch
Patch4:		squeak-vm-4.10.2-format-security.patch

BuildRequires:	cmake
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(audiofile)
BuildRequires:	pkgconfig(dbus-1)
BuildRequires:	pkgconfig(ext2fs)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(gl)
BuildRequires:	pkgconfig(gstreamer-0.10)
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libpulse)
BuildRequires:	pkgconfig(pango)
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(speex)
BuildRequires:	pkgconfig(theora)
BuildRequires:	pkgconfig(vorbis)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xt)
Requires:	zenity

%description
Squeak is a full-featured implementation of the Smalltalk programming
language and environment based on (and largely compatible with) the original
Smalltalk-80 system.

This package contains just the Squeak virtual machine.

%files
%doc unix/ChangeLog unix/doc/{README*,LICENSE,*RELEASE_NOTES}
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/icons/gnome/*/*/*
%{_datadir}/mime/packages/*
%{_datadir}/pixmaps/*
%dir %{_libdir}/squeak
%{_libdir}/squeak/*
%{_mandir}/man*/*

#----------------------------------------------------------------------------

%prep
%setup -q -n Squeak-%{version}-src -a 2
%patch0 -p1 -b .dprintf
%patch1 -p2 -b .alsa-fixes
%patch2 -p1 -b .fix-cmake
%patch3 -p1 -b .squeak-init-fix
%patch4 -p1 -b .format-security

sed -i 's|SET\s*\(imgdir\s+.+\)|SET (imgdir share/squeak)|i;
s|SET\s*\(plgdir\s+.+\)|SET (plgdir %{_lib}/squeak/${version}${versionsuffix})|i' \
unix/CMakeLists.txt

sed -i 's|^libdir=.*$|libdir="%{_libdir}/squeak"|' unix/cmake/squeak.in
sed -i 's|^libdir=.*$|libdir="%{_libdir}/squeak"|' unix/cmake/squeak.sh.in

# The source files chmod'd here have the execute bit set in the upstream tarball
# which bothers rpmlint, need submit a request upstream to have this changed
find . -name '*.[ch]' -exec chmod ug=rw,o=r {} \;

%build
pushd unix
%cmake -DVM_HOST="%{_host}" -DVM_VERSION="%{vmver}-%{svntag}" -DPLATFORM_SOURCE_VERSION="%{svntag}"
%make
popd

%install
pushd unix
%makeinstall_std -C build
popd

# these files will be put in std RPM doc location
rm -rf %{buildroot}%{_prefix}/doc/squeak

# install the desktop stuff
install -D --mode=u=rwx,go=rx mysqueak %{buildroot}%{_bindir}/mysqueak
install -D --mode=u=rw,go=r mysqueak.1 %{buildroot}%{_mandir}/man1/mysqueak.1
install -D --mode=u=rw,go=r squeak.xml %{buildroot}%{_datadir}/mime/packages/squeak.xml
install -D --mode=u=rw,go=r squeak.desktop %{buildroot}%{_datadir}/applications/squeak.desktop
install -D --mode=u=rw,go=r squeak.png %{buildroot}%{_datadir}/pixmaps/squeak.png

%define icons_dir %{buildroot}%{_datadir}/icons/gnome
for size in 16 24 32 48 64 72 96
do
  mkdir -p %{icons_dir}/${size}x${size}/mimetypes
  install -m0644 squeak${size}.png %{icons_dir}/${size}x${size}/mimetypes/application-x-squeak-image.png
  install -m0644 squeaksource${size}.png %{icons_dir}/${size}x${size}/mimetypes/application-x-squeak-source.png
done

# If an image cant find the .sources in the current directory it will look
# in %{_libdir}/squeak/%{vmver}
cd %{buildroot}%{_libdir}/squeak/%{vmver}-%{svntag}
DOTDOTS=$(echo %{_libdir}/squeak/%{vmver}-%{svntag} | sed -e 's:/[^/]\+:../:g')
ln -s ${DOTDOTS}%{_datadir}/squeak/SqueakV41.sources .

