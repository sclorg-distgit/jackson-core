%global pkg_name jackson-core
%{?scl:%scl_package %{pkg_name}}
%{?java_common_find_provides_and_requires}
Name:          %{?scl_prefix}jackson-core
Version:       2.5.0
Release:       2.3%{?dist}
Summary:       Core part of Jackson
License:       ASL 2.0
URL:           http://wiki.fasterxml.com/JacksonHome
Source0:       https://github.com/FasterXML/jackson-core/archive/%{pkg_name}-%{version}.tar.gz

# test deps
BuildRequires: %{?scl_prefix_java_common}mvn(junit:junit)

BuildRequires: %{?scl_prefix_java_common}maven-local

BuildArch:     noarch

%description
Core part of Jackson that defines Streaming API as well
as basic shared abstractions.

%package javadoc
Summary:       Javadoc for %{pkg_name}

%description javadoc
This package contains javadoc for %{pkg_name}.

%prep

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%setup -q -n %{pkg_name}-%{pkg_name}-%{version}

# remove unavailable com.google.doclava doclava 1.0.3
%pom_xpath_remove "pom:reporting/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:configuration"
%pom_xpath_inject "pom:reporting/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']" '
<configuration>
  <encoding>${project.reporting.outputEncoding}</encoding>
  <quiet>true</quiet>
  <source>${javac.src.version}</source>
</configuration>'

%pom_xpath_remove "pom:build/pom:plugins/pom:plugin[pom:artifactId='maven-javadoc-plugin']/pom:executions"

cp -p src/main/resources/META-INF/LICENSE .
cp -p src/main/resources/META-INF/NOTICE .
sed -i 's/\r//' LICENSE NOTICE

%mvn_file : %{pkg_name}

%pom_remove_parent

%pom_xpath_inject "pom:build/pom:plugins" '
        <plugin>
          <groupId>org.apache.felix</groupId>
          <artifactId>maven-bundle-plugin</artifactId>
          <extensions>true</extensions>
          <version>1.0.0</version>
          <configuration>
            <instructions>
              <_nouses>true</_nouses>
              <_removeheaders>Include-Resource,JAVA_1_3_HOME,JAVA_1_4_HOME,JAVA_1_5_HOME,JAVA_1_6_HOME,JAVA_1_7_HOME</_removeheaders>
              <_versionpolicy>${osgi.versionpolicy}</_versionpolicy>
              <Bundle-Name>${project.name}</Bundle-Name>
              <Bundle-SymbolicName>${project.groupId}.${project.artifactId}</Bundle-SymbolicName>
              <Bundle-Description>${project.description}</Bundle-Description>
              <Export-Package>${osgi.export}</Export-Package>
              <Private-Package>${osgi.private}</Private-Package>
              <Import-Package>${osgi.import}</Import-Package>
              <DynamicImport-Package>${osgi.dynamicImport}</DynamicImport-Package>
              <Bundle-DocURL>${project.url}</Bundle-DocURL>
              <Bundle-RequiredExecutionEnvironment>${osgi.requiredExecutionEnvironment}</Bundle-RequiredExecutionEnvironment>

              <Implementation-Build-Date>${maven.build.timestamp}</Implementation-Build-Date>
              <X-Compile-Source-JDK>${javac.src.version}</X-Compile-Source-JDK>
              <X-Compile-Target-JDK>${javac.target.version}</X-Compile-Target-JDK>

              <Implementation-Title>${project.name}</Implementation-Title>
              <Implementation-Version>${project.version}</Implementation-Version>
              <Implementation-Vendor-Id>${project.groupId}</Implementation-Vendor-Id>
              <Implementation-Vendor>${project.organization.name}</Implementation-Vendor>

              <Specification-Title>${project.name}</Specification-Title>
              <Specification-Version>${project.version}</Specification-Version>
              <Specification-Vendor>${project.organization.name}</Specification-Vendor>
            </instructions>
          </configuration>
        </plugin>'

# Avoid using the replacer-plugin
%pom_remove_plugin com.google.code.maven-replacer-plugin:replacer

file=`find -name PackageVersion.java.in`
gid=`grep "<groupId>" pom.xml | head -1 | sed 's/.*>\(.*\)<.*/\1/'`
aid=`grep "<artifactId>" pom.xml | head -1 | sed 's/.*>\(.*\)<.*/\1/'`
v=`grep "<version>" pom.xml | head -1 | sed 's/.*>\(.*\)<.*/\1/'`
pkg=`echo ${file} | cut -d/ -f5- | rev | cut -d/ -f2- | rev | tr '/' '\.'`

sed -i "s/@projectversion@/${v}/
        s/@projectgroupid@/${gid}/
        s/@package@/${pkg}/
        s/@projectartifactid@/${aid}/" ${file}

cp ${file} ${file%.in}

%{?scl:EOF}

%build

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}

%mvn_build -- -Dmaven.test.skip=true

%{?scl:EOF}

%install

%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
%mvn_install

%{?scl:EOF}

%files -f .mfiles
%doc README.md release-notes/* LICENSE NOTICE

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%changelog
* Tue Jul 28 2015 Alexander Kurtakov <akurtako@redhat.com> 2.5.0-2.3
- Drop Provides/Obsoletes outside of dts namespace.

* Fri Jul 03 2015 Roland Grunberg <rgrunber@redhat.com> - 2.5.0-2.2
- Replace %%license with %%doc.

* Thu Jul 02 2015 Roland Grunberg <rgrunber@redhat.com> - 2.5.0-2.1
- SCL-ize.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Jan 31 2015 gil cattaneo <puntogil@libero.it> 2.5.0-1
- update to 2.5.0

* Sat Sep 20 2014 gil cattaneo <puntogil@libero.it> 2.4.2-1
- update to 2.4.2

* Wed Jul 23 2014 gil cattaneo <puntogil@libero.it> 2.4.1.1-1
- update to 2.4.1.1

* Wed Jul 02 2014 gil cattaneo <puntogil@libero.it> 2.4.1-1
- update to 2.4.1

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Mar 28 2014 Michael Simacek <msimacek@redhat.com> - 2.2.2-4
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jul 22 2013 gil cattaneo <puntogil@libero.it> 2.2.2-2
- review fixes

* Tue Jul 16 2013 gil cattaneo <puntogil@libero.it> 2.2.2-1
- 2.2.2
- renamed jackson-core

* Tue May 07 2013 gil cattaneo <puntogil@libero.it> 2.2.1-1
- 2.2.1

* Wed Oct 24 2012 gil cattaneo <puntogil@libero.it> 2.1.0-1
- update to 2.1.0
- renamed jackson2-core

* Thu Sep 13 2012 gil cattaneo <puntogil@libero.it> 2.0.6-1
- initial rpm
