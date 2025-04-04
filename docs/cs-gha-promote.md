## Promote Reusable Workflow

The Promote Reusable Workflow facilitates the transfer of packages between repositories in Cloudsmith. For example, it can be used to move a package from the non-production repository to the production repository. Before promoting, ensure that the package exists in the nonprod repository. This action will then transfer the package from the nonprod to the prod repository. This workflow is designed for integration into CI/CD pipelines, making it a reusable solution for package promotion steps.

### Migration Note

#### **Old Action:** [AAInternal/artifactory-actions/promote](https://github.com/AAInternal/artifactory-actions/blob/main/promote/README.md#usage)

```yaml
   - name: Promote Maven Package in Artifactory
     uses: AAInternal/artifactory-actions/promote@v7 # use latest versions
     with:
       username: ${{ secrets.ARTIFACTORY_CRED_USR }}
       apikey: ${{ secrets.ARTIFACTORY_CRED_PAT }}
       buildName: "my-application" # if not the same as your repo
       buildNumber: 1.0.8          # version
       repository: prod-releases
```       

#### **New Reusable Workflow:** [AAInternal/promote-package-action](https://github.com/AAInternal/promote-package-action?tab=readme-ov-file#usage) 

```yaml
jobs:
  promote-job:   # This is a reusable workflow to promote docker images from nonprod to prod in Cloudsmith.
    permissions:
      id-token: write
      contents: write
    uses: AAInternal/promote-package-action/.github/workflows/rw_promote.yaml@v0  ## Use latest release version or sha
    with:
      APPLICATION_NAME: "example-app"
      APPLICATION_VERSION: "1.0.0"
      PACKAGE_TYPE: "docker"
```

```yaml
jobs:
  promote-job:   # This is a reusable workflow to promote npm packages from nonprod to prod in Cloudsmith.
    permissions:
      id-token: write
      contents: write
    uses: AAInternal/promote-package-action/.github/workflows/rw_promote.yaml@v0  ## Use current release version
    with:
      APPLICATION_NAME: "example-app"
      APPLICATION_VERSION: "1.0.0"
      PACKAGE_TYPE: "npm" # defaults to docker if not provided, other options are npm.
```

#### **GIT DIFF**
# ![](../assets/diff-promote.png)


[![Next: NPM Action →](https://img.shields.io/badge/NEXT-NPM_Action-%23007ACC?style=for-the-badge&logo=npm)](npm.md)
