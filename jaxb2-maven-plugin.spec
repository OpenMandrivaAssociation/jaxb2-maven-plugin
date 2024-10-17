%{?_javapackages_macros:%_javapackages_macros}
Name:          jaxb2-maven-plugin
Version:       1.5
Release:       3.0%{?dist}
Summary:       JAXB-2 Maven Plugin
License:       ASL 2.0
Url:           https://mojo.codehaus.org/jaxb2-maven-plugin/
# svn export https://svn.codehaus.org/mojo/tags/jaxb2-maven-plugin-1.5
# tar czf jaxb2-maven-plugin-1.5-src-svn.tar.gz jaxb2-maven-plugin-1.5
Source0:       http://repo2.maven.org/maven2/org/codehaus/mojo/%{name}/%{version}/%{name}-%{version}-source-release.zip
# jaxb2-maven-plugin package don't include the license file
Source1:       http://www.apache.org/licenses/LICENSE-2.0.txt

BuildRequires: java-devel
BuildRequires: mojo-parent

BuildRequires: glassfish-jaxb
BuildRequires: mvn(org.apache.maven:maven-artifact)
BuildRequires: mvn(org.apache.maven:maven-compat)
BuildRequires: mvn(org.apache.maven:maven-core)
BuildRequires: mvn(org.apache.maven:maven-model)
BuildRequires: mvn(org.apache.maven:maven-plugin-api)
#BuildRequires: mvn(org.apache.maven:maven-project)
#BuildRequires: mvn(org.codehaus.plexus:plexus-build-api)
BuildRequires: mvn(org.codehaus.plexus:plexus-compiler-api)
BuildRequires: mvn(org.codehaus.plexus:plexus-utils)
BuildRequires: mvn(org.sonatype.plexus:plexus-build-api)

# test deps
BuildRequires: aopalliance
BuildRequires: cglib
BuildRequires: junit
BuildRequires: maven-plugin-testing-harness
BuildRequires: xmlunit

BuildRequires: maven-local
BuildRequires: maven-invoker-plugin
BuildRequires: maven-plugin-plugin
BuildRequires: maven-surefire-provider-junit4

BuildArch:     noarch

%description
Mojo's JAXB-2 Maven plugin is used to create an object graph from
XSDs based on the JAXB 2.1 implementation and to generate XSDs from
JAXB-annotated Java classes.

%package javadoc
Summary:       Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

cp -p %{SOURCE1} .
sed -i 's/\r//' LICENSE-2.0.txt
# updated plexus-build-api refs
#%%pom_xpath_remove "pom:dependencies/pom:dependency[pom:artifactId ='plexus-build-api']/pom:groupId"
#%%pom_xpath_inject "pom:dependencies/pom:dependency[pom:artifactId ='plexus-build-api']" "<groupId>org.sonatype.plexus</groupId>"
# used only mvn3 apis
%pom_remove_dep org.apache.maven:maven-project
%pom_add_dep org.apache.maven:maven-compat
%pom_add_dep org.apache.maven:maven-core
# missing build deps
%pom_add_dep com.sun.xml.bind:jaxb-impl

# missing test deps
%pom_add_dep aopalliance:aopalliance::test
%pom_add_dep net.sf.cglib:cglib::test

# Disable integration tests
%pom_xpath_remove "pom:profiles"

%build

%mvn_file :%{name} %{name}
%mvn_build -- -Dmaven.test.failure.ignore=true

%install
%mvn_install

%files -f .mfiles
%doc LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE-2.0.txt

%changelog
* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 09 2013 gil cattaneo <puntogil@libero.it> 1.5-2
- switch to XMvn
- minor changes to adapt to current guideline

* Thu May 09 2013 gil cattaneo <puntogil@libero.it> 1.5-1
- initial rpm