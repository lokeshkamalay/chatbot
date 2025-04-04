## Download Action

This action will download a package from the Cloudsmith repository in the American Airlines organization. It can be used to retrieve Docker, npm, or other package types as needed. The action simplifies the process of authenticating and downloading packages directly from Cloudsmith.

### Cloudsmith Repository

Always downloads from the appropriate nonprod repository in the American Airlines Cloudsmith organization.

### Migration Note

#### **Old Action:** [AAInternal/artifactory-actions/download](https://github.com/AAInternal/artifactory-actions/blob/main/download/README.md#usage)

```yaml
jobs:
  direct-download-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4 # Check out repo
      - name: Direct Download or Upload package to Artifactory Outside Build (packages.aa.com)
        id: direct-download-upload-artifacts
        uses: AAInternal/artifactory-actions/download@direct-upload-download
        with:
          BUILD_TYPE: "maven" #${{ inputs.build-type }}
          ARTIFACTORY_REPO_NAME: "dev-releases"
          ARTIFACTORY_GROUP_ID: "com.aa.flighthub.mte"
          ARTIFACTORY_ARTIFACT_ID: "mte-all"
          ARTIFACTORY_ARTIFACT_VERSION: "5.0.0"
          ARTIFACTORY_ACCESS_TOKEN: ${{ secrets.ARTIFACTORY_CRED_PAT }}
          ARTIFACTORY_ID_USR: ${{ secrets.ARTIFACTORY_CRED_USR }}
          BASE_FOLDER: "./"
      - name: Checking Downloads
        run: |
          cd dev-releases/com/aa/flighthub/mte/mte-all/5.0.0/
          ls
```

#### **New Action:** [AAInternal/download-package-action](https://github.com/AAInternal/download-package-action?tab=readme-ov-file#usage)

```yaml
jobs:
  download-package:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read    
    steps:
      - uses: actions/checkout@v4 # Check out repo
      - name: Download Package from Cloudsmith
        id: download-package
        uses: AAInternal/download-package-action@v0
        with:
          PACKAGE_NAME: "example-package"
          PACKAGE_VERSION: "1.0.0"
          PACKAGE_REPOSITORY: "nonprod"
          DOWNLOADED_PACKAGE_PATH: ${{ github.workspace }}
```                    

#### **GIT DIFF**
# ![](../assets/diff-download.png)

[![Next: RAW Package Upload Action →](https://img.shields.io/badge/NEXT-RAW_Package_Upload_Action-%23007ACC?style=for-the-badge&logo=cloudsmith)](upload.md)

