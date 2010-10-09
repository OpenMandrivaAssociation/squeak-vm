%define vmver	4.0.3-2202
Name:		squeak-vm
Version:	4.0.3.2202
Release:	%mkrel 1
Summary:	The Squeak virtual machine
Group:		Development/Other
License:	MIT
URL:            http://squeakvm.org/unix
Source0:	http://ftp.squeak.org/%{major}/unix-linux/Squeak-%{version}-src.tar.gz
Source2:	squeak-desktop-files.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires(post):	desktop-file-utils
Requires(postun): desktop-file-utils

BuildRequires:	cmake
BuildRequires:	libaudiofile-devel
BuildRequires:	X11-devel
BuildRequires:	x11-proto-devel
BuildRequires:	libx11-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libalsa-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libtheora-devel
BuildRequires:	speex-devel
BuildRequires:	dbus-devel
BuildRequires:	pango-devel
BuildRequires:	gstreamer0.10-devel
BuildRequires:	libice-devel
BuildRequires:	libsm-devel
BuildRequires:	libxext-devel
BuildRequires:	e2fsprogs-devel
BuildRequires:	dbus-devel
Requires:	zenity

Obsoletes:	squeak-vm-nonXOplugins

Patch0:		squeak-vm-rpath.patch
Patch1:		squeak-vm-imgdir.patch
Patch2:		squeak-vm-tail-options.patch

%description
Squeak is a full-featured implementation of the Smalltalk programming
language and environment based on (and largely compatible with) the original
Smalltalk-80 system.

This package contains just the Squeak virtual machine.

%prep
%setup -q -n Squeak-%{version}-src -a 2

# The source files chmod'd here have the execute bit set in the upstream tarball
# which bothers rpmlint, need submit a request upstream to have this changed
find . -name '*.[ch]' -exec chmod ug=rw,o=r {} \;

%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
mkdir -p bld
cd bld
CPPFLAGS=-DSUGAR ../unix/cmake/configure --prefix=%{_prefix} --libdir=%{_libdir}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make -C bld install ROOT=%{buildroot} DESTDIR=%{buildroot}
cp -f unix/config/inisqueak.in %{buildroot}%{_bindir}/inisqueak
perl -pi					\
	-e 's|\@SQ_MAJOR\@|41|;'		\
	-e 's|\@SQ_VERSION\@|4.1|;'		\
	-e 's|\@prefix\@|%{_prefix}|;'		\
	-e 's|\@exec_prefix\@|%{_prefix}|;'	\
	-e 's|\@bindir\@|%{_bindir}|;'		\
	-e 's|\@imgdir\@|%{_datadir}/squeak|;'	\
	-e 's|\@plgdir\@|%{_datadir}/squeak|;'	\
	%{buildroot}%{_bindir}/inisqueak
perl -pi					\
	-e 's|/lib/squeak|/%{_lib}/squeak|;'	\
	%{buildroot}%{_bindir}/squeak.sh

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

%ifarch x86_64 ppc64
    mkdir -p %{buildroot}%{_libdir}/squeak/%{vmver}
    mv -f %{buildroot}%{_prefix}/{lib,%{_lib}}/squeak/%{vmver}/*
%endif

# If an image cant find the .sources in the current directory it will look
# in %{_libdir}/squeak/%{vmver}
cd %{buildroot}%{_libdir}/squeak/%{vmver}
DOTDOTS=$(echo %{_libdir}/squeak/%{vmver} | sed -e 's:/[^/]\+:../:g')
ln -s ${DOTDOTS}%{_datadir}/squeak/SqueakV41.sources .

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

%files
%defattr(-,root,root,-)
%doc unix/ChangeLog unix/doc/{README*,LICENSE,*RELEASE_NOTES}
%{_bindir}/*
%{_datadir}/applications/*
%{_datadir}/icons/gnome/*/*/*
%{_datadir}/mime/packages/*
%{_datadir}/pixmaps/*
%dir %{_libdir}/squeak
%{_libdir}/squeak/*
%{_mandir}/man*/*
