%define	major 0
%define	libname %mklibname gnomescan %major
%define	develname %mklibname gnomescan -d

Summary:	Gnome solution for scanning in the desktop on top of libsane
Name:		gnome-scan
Version:	0.6
Release:	%mkrel 1
Group:		Graphical desktop/GNOME
License:	LGPLv2+
URL:		http://www.gnome.org/projects/gnome-scan/index
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.6/%{name}-%{version}.tar.bz2
Patch0:		gnome-scan-cursor_fix.patch
BuildRequires:	gtk2-devel libgnomeui2-devel sane-devel
BuildRequires:	gegl-devel gimp-devel
BuildRequires:	gettext perl(XML::Parser) pkgconfig
BuildRequires:	desktop-file-utils gtk-doc gnome-doc-utils
BuildRequires:	libglade2-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
Requires:	gimp
Provides:	flegita = %{version}-%{release}
Provides:	gnomescan = %{version}-%{release}

%description
Gnome Scan provide a library for use by applications (e.g. using
plugins) as well as a tiny standalone application, called flegita,
which allow to simply save scan to file.

%package -n %libname
Summary:	Gnome-scan library
Group:		System/Libraries

%description -n %libname
Libraries for using gnome-scan

%package -n %develname
Summary:	Development files for gnome-scan
Group:		Development/GNOME and GTK+
Requires:	%{libname} = %{version}-%{release}
Requires:	pkgconfig gtk2-devel
Provides:	gnomescan-devel

%description -n %develname
Contains development headers and libraries for gnome-scan

%prep
%setup -q
%patch0 -p0 -b .fix

%build
%configure --disable-static
# Disable rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags} 

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

desktop-file-install					\
	--remove-category Application			\
	--dir %{buildroot}%{_datadir}/applications	\
	--mode 0644					\
	%{buildroot}%{_datadir}/applications/flegita.desktop


%find_lang %{name}

find %{buildroot} -type f -name "*.la" -exec rm -f {} ';'
rm -rf %{buildroot}%{_prefix}/doc

%clean
rm -rf %{buildroot}

%post 
touch --no-create %{_datadir}/icons/hicolor
%{update_menus}

%if %mdkversion < 200900
%post -n %libname -p /sbin/ldconfig
%endif

%postun 
touch --no-create %{_datadir}/icons/hicolor
%{clean_menus}

%if %mdkversion < 200900
%postun -n %libname -p /sbin/ldconfig
%endif


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/flegita
%{_libdir}/gimp/2.0/plug-ins/flegita-gimp
%{_datadir}/applications/flegita.desktop
%{_datadir}/icons/hicolor/*/*/*.svg
%{_datadir}/gnome-scan/

%files -n %libname
%defattr(-,root,root,-)
%{_libdir}/libgnomescan.so.%{major}
%{_libdir}/libgnomescan.so.%{major}.*
%{_libdir}/gnome-scan-1.0/

%files -n %develname
%defattr(-,root,root,-)
%{_includedir}/gnome-scan-1.0/
%{_libdir}/libgnomescan.so
%{_libdir}/pkgconfig/gnome-scan.pc
%doc %{_datadir}/gtk-doc/html/gnome-scan*/
