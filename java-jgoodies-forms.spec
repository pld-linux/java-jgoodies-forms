#
# Conditional build:
%bcond_without	javadoc		# don't build javadoc

%define		shortname forms
%define		srcname		jgoodies-%{shortname}
%define		ver	%(echo %{version} | tr . _)
%include	/usr/lib/rpm/macros.java
Summary:	Framework to lay out and implement elegant Swing panels in Java
Name:		java-jgoodies-forms
Version:	1.2.0
Release:	3
License:	BSD
Group:		Libraries/Java
URL:		http://www.jgoodies.com/freeware/forms/
Source0:	http://www.jgoodies.com/download/libraries/%{shortname}/%{shortname}-%{ver}.zip
# Source0-md5:	756de0bee840592cdc12ef0cd5d8332e
Patch0:		build.patch
BuildRequires:	ant
BuildRequires:	jdk
BuildRequires:	jpackage-utils >= 1.6
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.533
BuildRequires:	sed >= 4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The JGoodies Forms framework helps you lay out and implement elegant
Swing panels quickly and consistently. It makes simple things easy and
the hard stuff possible, the good design easy and the bad difficult.

Main Benefits:

- Powerful, flexible and precise layout
- Easy to work with and quite easy to learn
- Faster UI production
- Better UI code readability
- Leads to better style guide compliance

%package javadoc
Summary:	Javadoc documentation for JGoodies Forms
Group:		Documentation

%description javadoc
The JGoodies Forms framework helps you lay out and implement elegant
Swing panels quickly and consistently. It makes simple things easy and
the hard stuff possible, the good design easy and the bad difficult.

This package contains the Javadoc documentation for JGoodies Forms.

%package doc
Summary:	Manual for %{srcname}
Summary(fr.UTF-8):	Documentation pour %{srcname}
Summary(it.UTF-8):	Documentazione di %{srcname}
Summary(pl.UTF-8):	Podręcznik dla %{srcname}
Group:		Documentation

%description doc
Documentation for %{srcname}.

%description doc -l fr.UTF-8
Documentation pour %{srcname}.

%description doc -l it.UTF-8
Documentazione di %{srcname}.

%description doc -l pl.UTF-8
Dokumentacja do %{srcname}.

%package demo
Summary:	Demo for %{srcname}
Summary(pl.UTF-8):	Pliki demonstracyjne dla pakietu %{srcname}
Group:		Documentation
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description demo
Demonstrations and samples for %{srcname}.

%description demo -l pl.UTF-8
Pliki demonstracyjne i przykłady dla pakietu %{srcname}.

%prep
%setup -q -n %{shortname}-%{version}
%undos build.xml
%patch0 -p1
rm %{shortname}-%{version}.jar
rm -r docs/api

# Fix the line endings and the encodings
for file in *.txt *.html docs/*.* docs/reference/* docs/tutorial/* \
        src/tutorial/com/jgoodies/forms/tutorial/*.java \
        src/tutorial/com/jgoodies/forms/tutorial/*/*.java; do
	sed -i 's/\r//' $file
done

for file in docs/reference/*.html docs/tutorial/*.html; do
	iconv --from=ISO-8859-1 --to=UTF-8 $file > $file.new
	sed -i 's/iso-8859-1/utf-8/' $file.new
	mv $file.new $file
done

%build
%ant compile jar %{?with_javadoc:javadoc}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_javadir}
install -p build/%{shortname}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}-%{version}.jar
ln -s %{srcname}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{srcname}.jar

# javadoc
%if %{with javadoc}
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
cp -a build/docs/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{srcname}-%{version}
ln -s %{srcname}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{srcname} # ghost symlink
%endif

# demo
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a src/tutorial/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -nfs %{srcname}-%{version} %{_javadocdir}/%{srcname}

%files
%defattr(644,root,root,755)
%doc RELEASE-NOTES.txt LICENSE.txt README.html
%{_javadir}/%{srcname}-%{version}.jar
%{_javadir}/%{srcname}.jar

%files doc
%defattr(644,root,root,755)
%doc docs/*

%files demo
%defattr(644,root,root,755)
%{_examplesdir}/%{name}-%{version}

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{srcname}-%{version}
%ghost %{_javadocdir}/%{srcname}
%endif
