## NuGet Action

This action is used to publish NuGet packages to Cloudsmith.

### Migration Note

#### **Old Action:** [AAInternal/artifactory-actions/nuget](https://github.com/AAInternal/artifactory-actions/blob/main/nuget/README.md#usage)

```yaml
name: Artifactory Actions Nuget Demo
on: push
jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4 # Checks out the repository
      - name: Publish Nuget Package to Artifactory
        uses: AAInternal/artifactory-actions/nuget@v7 # use latest versions
        with:
          username: ${{ secrets.ARTIFACTORY_CRED_USR }} # AAInternal Artifactory User Credential
          apikey: ${{ secrets.ARTIFACTORY_CRED_PAT }} # AAInternal Artifactory Access Token
          buildName: welcomemessage # OPTIONAL - Artifactory build name
          buildVersion: 1.0.0 # OPTIONAL - Optional parameter to control build versioning
          nugetPath: '${{ github.workspace }}/bin/Debug' # REQUIRED - Path to the location of the .nuget file to be uploaded
```          

#### **New Action:** [publish-nuget-action](https://github.com/AAInternal/publish-nuget-action?tab=readme-ov-file#usage)

```yaml
name: Nuget Build and Publish
jobs:
  test-nuget-publish:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - uses: actions/setup-dotnet@v4 ## setup dotnet action need for publish action to work
        with:
          dotnet-version: "8.0.x" ## Use whichever version needed        

      - name: publish-nuget-action
        id: publish-nuget
        uses: AAInternal/publish-nuget-action@v0 # use the latest versions
        with:
          APP_NAME: "ReusableExample" # If not provided, the action will use either the PackageID or AssemblyName tags within the .csproj file. Otherwise, the name of the .csproj file is used
          APP_VERSION: "1.0.0" # If not provided, it will use whatever is in the Version, PackageVersion, AssemblyVersion, or FileVersion tags within the .csproj file, otherwise if not found the action will fail
          BASE_FOLDER: ./example-nuget # Path to the .csproj file. Default is .
```


[![Next: MAVEN Action →](https://img.shields.io/badge/NEXT-MAVEN_Action-%23007ACC?style=for-the-badge&logo=apache-maven)](maven.md)