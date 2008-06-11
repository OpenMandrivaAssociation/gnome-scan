%define	major 0
%define	libname %mklibname gnomescan %major
%define	develname %mklibname gnomescan -d

Summary:	Gnome solution for scanning in the desktop on top of libsane
Name:		gnome-scan
Version:	0.6
Release:	%mkrel 2
Group:		Graphical desktop/GNOME
License:	LGPLv2+
URL:		http://www.gnome.org/projects/gnome-scan/index
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.6/%{name}-%{version}.tar.bz2
Patch0:		gnome-scan-cursor_fix.patch
# (fc) 0.6-2mdv fix with non-UTF8 locale
Patch1:		gnome-scan-0.6-utf8.patch
# (fc) 0.6-2mdv fix module building
Patch2:		gnome-scan-0.6-fixmodule.patch
BuildRequires:	libgnomeui2-devel sane-devel
BuildRequires:	gegl-devel gimp-devel
BuildRequires:	perl(XML::Parser) 
BuildRequires:	desktop-file-utils gtk-doc gnome-doc-utils
BuildRequires:	libglade2-devel
BuildRequires:	gnome-common
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
%patch1 -p1 -b .utf8
%patch2 -p1 -b .fixmodule

#needed by patch2
autoreconf

%build
%configure2_5x --disable-static

%make

%install
rm -rf %{buildroot}
%makeinstall_std

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
