## Maven Action

This action is used to build and publish Maven packages to Cloudsmith.

### Migration Note

#### **Old Action:** [AAInternal/artifactory-actions/maven](https://github.com/AAInternal/artifactory-actions/blob/main/maven/README.md#usage)

```yaml
name: Build-Maven-And-Publish
jobs:
  example-ci-job:
    runs-on: ubuntu-latest
    steps:
      - name: checkout this repo
        uses: actions/checkout@v4

      - name: build with maven and publish
        id: build-and-publish
        uses: AAInternal/artifactory-actions/maven@v7 
        with:
          APPLICATION_VERSION: '2.0.0' # If no version is passed in - it will be extracted from the pom.xml
          ARTIFACTORY_ID_USR: ${{ secrets.ARTIFACTORY_CRED_USR }} 
          ARTIFACTORY_ACCESS_TOKEN: ${{ secrets.ARTIFACTORY_CRED_PAT }}
```                  

#### **New Action:** [AAInternal/publish-maven-action](https://github.com/AAInternal/publish-maven-action?tab=readme-ov-file#usage)
    
```yaml
name: Build-Maven-And-Publish
jobs:
  example-ci-job:  
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read          
    steps:
      - name: checkout this repo
        uses: actions/checkout@v4

      - name: build with maven and publish
        id: build-and-publish
        uses: AAInternal/publish-maven-action@v0
        with:
          APPLICATION_VERSION: '2.0.0' # If no version is passed in - it will be extracted from the pom.xml
```

#### **GIT DIFF**
DO NOT forget to add the permission section, it is needed in order to read the token
```yml
permissions:
  id-token: write
  contents: read   
```
# ![](../assets/diff-maven.png)

#### Things to consider
#### Discontinued Inputs
Following inputs are discontinued.  Please have them removed if being used in your workflow for maven action
  - USE_MAVEN_PUBLIC
  - IS_DEPENDENCY
  - RepoDeployReleases
  - RepoDeploySnapshots
  - USE_JFROG_CLI

##### pom.xml
There are two different URLs, one for download which goes under plugins and repositories section and another one for upload under Distribution section.  The reason behind 2 URLs is, download URL is much faster than upload.

Your repositories/plugins section needs to be updated to point to `package-manager.aa.com/basic/nonprod/maven`
```xml
<repositories>
    <repository>
        <id>nonprod-releases</id>
        <snapshots>
            <enabled>true</enabled>
        </snapshots>
        <url>https://package-manager.aa.com/basic/nonprod/maven/</url>
    </repository>
</repositories>
```

Your all distribution section must be pointing to `https://maven.cloudsmith.io/american-airlines/nonprod/`
```xml
<distributionManagement>
    <repository>
        <id>nonprod-releases</id>
        <name>releases</name>
        <url>https://maven.cloudsmith.io/american-airlines/nonprod/</url>
    </repository>
    <snapshotRepository>
        <id>snapshots</id>
        <name>snapshots</name>
        <url>https://maven.cloudsmith.io/american-airlines/nonprod/</url>
    </snapshotRepository>
</distributionManagement>
```

The ID `<id>nonprod-releases</id>` should be one of the below, otherwise you may see latency or failures in your job.  If you are planning to use multiple repository section under `repositories` or `Distribution` then please keep the IDs Unique like shown above in distribution section
- central
- cloudsmith
- american-airlines-prod
- american-airlines-nonprod
- snapshots
- releases
- nonprod-releases
- prod-releases

#### settings.xml
All DTE Maven actions come with a default settings.xml file, so you may just delete or rename if you have one in your repo.

#### URLs
- snapshots: 	https://package-manager.aa.com/basic/nonprod/maven
- releases :  https://package-manager.aa.com/basic/nonprod/maven
- thirdparty: https://package-manager.aa.com/basic/nonprod/maven
- prod-releases: https://package-manager.aa.com/basic/prod/maven
- central: https://package-manager.aa.com/basic/nonprod/maven
- maven-public: https://package-manager.aa.com/basic/nonprod/maven
- Publish/upload: https://maven.cloudsmith.io/american-airlines/nonprod

Note: If you have a custom repository then please update to above nonprod/maven url.

[![Next: Download Action →](https://img.shields.io/badge/NEXT-Download_Action-%23007ACC?style=for-the-badge&logo=download)](download.md)
