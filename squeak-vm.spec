%define major   3.10
%define minor   4
%define vmver   %{major}-%{minor}
%define source  Squeak-%{vmver}

Name:           squeak-vm
Version:        %{major}.%{minor}
Release:        %mkrel 1
Summary:        The Squeak virtual machine

Group:          Development/Other
License:        MIT
URL:            http://squeakvm.org/unix
Source0:        http://ftp.squeak.org/%{major}/unix-linux/%{source}.src.tar.gz
Source2:        squeak-desktop-files.tar.gz
Patch0:         squeak-vm-rpath.patch
Patch1:         squeak-vm-install-inisqueak.patch
Patch2:         squeak-vm-imgdir.patch
Patch3:         squeak-vm-tail-options.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

BuildRequires: libaudiofile-devel
BuildRequires: X11-devel
BuildRequires: x11-proto-devel
BuildRequires: libx11-devel
BuildRequires: gcc
BuildRequires: desktop-file-utils
BuildRequires: libalsa-devel
BuildRequires: dbus-devel
Requires:       zenity

#
# define nonXOplugins to be non-zero if you would like the plugins that
# are unnecessary on the XO to be moved into a separate sub-package
# to save space on the XO.  The list of plugins that are split out is
# listed below in the nonXOplugins files section
#
%define nonXOplugins 1


%description
Squeak is a full-featured implementation of the Smalltalk programming
language and environment based on (and largely compatible with) the original
Smalltalk-80 system.

This package contains just the Squeak virtual machine.

%if 0%{?nonXOplugins}
%package nonXOplugins
Summary:        Non-XO Plugins for the Squeak virtual machine
Group:          Development/Languages
Requires:       squeak-vm = %{version}-%{release}
%description nonXOplugins
Plugins for the Squeak virtual machine.
These plugins are unnecessary on the XO, and so are moved into a separate
sub-package to save space.
%endif


%prep
%setup -q -n %{source} -a 2

# The source files chmod'd here have the execute bit set in the upstream tarball
# which bothers rpmlint, need submit a request upstream to have this changed
find platforms -name '*.[ch]' -exec chmod ug=rw,o=r {} \;
##chmod ug=rw,o=r platforms/Cross/plugins/JPEGReadWriter2Plugin/*
##chmod ug=rw,o=r platforms/Cross/plugins/Mpeg3Plugin/libmpeg/*
##chmod ug=rw,o=r platforms/Cross/plugins/Mpeg3Plugin/libmpeg/audio/*
##chmod ug=rw,o=r platforms/Cross/plugins/Mpeg3Plugin/libmpeg/vidio/*
##chmod ug=rw,o=r platforms/unix/vm/osExports.c
##chmod ug=rw,o=r platforms/Cross/plugins/RePlugin/internal.h
##chmod ug=rw,o=r platforms/Cross/plugins/FilePlugin/sqFilePluginBasicPrims.c

%patch0 -p1 -b .rpath
%patch1 -p1 -b .install-inisqueak
%patch2 -p1 -b .imgdir
%patch3 -p1 -b .tail-options

%build
mkdir -p bld
cd bld

CPPFLAGS=-DSUGAR ../platforms/unix/config/configure --prefix=%{_prefix} --mandir=%{_mandir} --datadir=%{_datadir} --libdir=%{_libdir}

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make -C bld install ROOT=%{buildroot}

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
cd %{buildroot}%{_libdir}/squeak/%{vmver}
DOTDOTS=$(echo %{_libdir}/squeak/%{vmver} | sed -e 's:/[^/]\+:../:g')
ln -s ${DOTDOTS}%{_datadir}/squeak/SqueakV39.sources .
ln -s ${DOTDOTS}%{_datadir}/squeak/SqueakV3.sources .


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
%defattr(-,root,root)
%doc platforms/unix/ChangeLog platforms/unix/doc/{README*,LICENSE,*RELEASE_NOTES}
%{_bindir}/*
%dir %{_libdir}/squeak
%dir %{_libdir}/squeak/%{vmver}
%if 0 == 0%{?nonXOplugins}
%{_libdir}/squeak/%{vmver}/FileCopyPlugin
%{_libdir}/squeak/%{vmver}/B3DAcceleratorPlugin
%{_libdir}/squeak/%{vmver}/PseudoTTYPlugin
%{_libdir}/squeak/%{vmver}/UnixOSProcessPlugin
%{_libdir}/squeak/%{vmver}/XDisplayControlPlugin
%{_libdir}/squeak/%{vmver}/Mpeg3Plugin
%{_libdir}/squeak/%{vmver}/vm-sound-NAS
%ifarch i686
%{_libdir}/squeak/%{vmver}/SqueakFFIPrims
%endif
%ifarch ppc
%{_libdir}/squeak/%{vmver}/SqueakFFIPrims
%endif
%else
%{_libdir}/squeak/%{vmver}/AioPlugin
%{_libdir}/squeak/%{vmver}/ClipboardExtendedPlugin
%{_libdir}/squeak/%{vmver}/DBusPlugin
%{_libdir}/squeak/%{vmver}/GStreamerPlugin
%{_libdir}/squeak/%{vmver}/ImmX11Plugin
%{_libdir}/squeak/%{vmver}/KedamaPlugin
%{_libdir}/squeak/%{vmver}/KedamaPlugin2
%{_libdir}/squeak/%{vmver}/MIDIPlugin
%{_libdir}/squeak/%{vmver}/OggPlugin
%{_libdir}/squeak/%{vmver}/RomePlugin
%{_libdir}/squeak/%{vmver}/Squeak3D
%{_libdir}/squeak/%{vmver}/UUIDPlugin
%{_libdir}/squeak/%{vmver}/VideoForLinuxPlugin

%{_libdir}/squeak/%{vmver}/SqueakV3.sources
%{_libdir}/squeak/%{vmver}/SqueakV39.sources
%{_libdir}/squeak/%{vmver}/npsqueak.so
%{_libdir}/squeak/%{vmver}/squeak
%{_libdir}/squeak/%{vmver}/vm-display-X11
%{_libdir}/squeak/%{vmver}/vm-display-fbdev
%{_libdir}/squeak/%{vmver}/vm-display-null
%{_libdir}/squeak/%{vmver}/vm-sound-ALSA
%{_libdir}/squeak/%{vmver}/vm-sound-OSS
%{_libdir}/squeak/%{vmver}/vm-sound-null
%endif
%{_mandir}/man*/*
%dir %{_datadir}/squeak
%{_datadir}/squeak/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/*
%{_datadir}/icons/gnome/*/mimetypes/*.png


%if 0%{?nonXOplugins}
%files nonXOplugins
%defattr(-,root,root,-)
%{_libdir}/squeak/%{vmver}/FileCopyPlugin
%{_libdir}/squeak/%{vmver}/B3DAcceleratorPlugin
%{_libdir}/squeak/%{vmver}/PseudoTTYPlugin
%{_libdir}/squeak/%{vmver}/UnixOSProcessPlugin
%{_libdir}/squeak/%{vmver}/XDisplayControlPlugin
%{_libdir}/squeak/%{vmver}/Mpeg3Plugin
%ifarch %{ix86} ppc
%{_libdir}/squeak/%{vmver}/SqueakFFIPrims
%endif
%endif
