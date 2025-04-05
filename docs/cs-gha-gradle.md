## Gradle Action

This action uploads a Gradle package from the local environment to the Cloudsmith repository in the American Airlines organization. It simplifies the process of authenticating and publishing Gradle packages directly to Cloudsmith

### Cloudsmith Repository

Always uploads to nonprod repository in the American Airlines Cloudsmith organization.

### Migration Note

##### There is no gradle action in artifactory actions. This action is a new addition to the GitHub Actions.


#### **New Action:** [AAInternal/publish-gradle-action](https://github.com/AAInternal/publish-gradle-action?tab=readme-ov-file#usage)

```yaml
jobs:
  example-job:
    permissions:
      id-token: write
      contents: read
    runs-on: ubuntu-latest
    steps:
      - name: checkout this repo
        uses: actions/checkout@v4 # Checks out the repository

      - name: build with gradle and publish
        id: build-and-publish
        uses: AAInternal/publish-gradle-action@v0 # check for the latest version before copy pasting this
        with:
          VERSION: v1.0.0 # build version
          BASE_FOLDER: ${{ github.workspace }}/test/
```   

## Next Steps

Explore detailed migration guides for ADO Pipelines

[![Azure DevOps Pipelines →](https://img.shields.io/badge/Azure_DevOps_Pipelines-%23007ACC?style=for-the-badge&logo=azure-devops)](../ado-pipelines/overview.md)