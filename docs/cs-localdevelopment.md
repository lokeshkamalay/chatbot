# Local Development

## Obtaining Your API key for Authentication

To use the Cloudsmith API or any tools and integrations that rely on it, you’ll need to first retrieve your API Key via cloudsmith UI. Here’s how you can do that:

1. **Login to Cloudsmith:**
   - Visit the [Cloudsmith website](https://cloudsmith.io/orgs/american-airlines/saml/login/) and log in using your SAML credentials.

2. **Navigate to Your Profile:**
   - Click on your profile icon in the top right corner of the screen to access your profile settings. select "API Settings" from the dropdown menu.

   ![API Settings](assets/apisettings.png)

3. **API Key page:**
   - In this page, you will find your API Key. You can copy the key to your clipboard or click on the "Refresh" button to generate a new key.
   - we have 90 day API key policy enforcement for the Org, so please ensure to refresh and use the new token before it expires.

   ![API Key](assets/apikey.png)   

With your API Key in hand, you can now configure authentication for each package type. Please refer to the **Local Development** section below to see the steps and commands required for authentication with your username and API Key.   

## Instructions for Local Setup

To find out how to use cloudsmith for local development, please refer to the "Set me up" button found after clicking into either the `nonprod` or `prod` repositories.

![set me up](assets/setmeup.png)

Once clicked into a package type (maven in this example), there will be instructions on how to authenticate with cloudsmith and download the artifacts.

![alt text](assets/maven-example.png)

Please find additional setup instructions below for different package types. 

#### Maven
In the pom.xml and settings.xml files below, both prod and nonprod repositories are added, you can add only one of them depending your requirement and from where you are intending to fetch your dependencies

***pom.xml:***
You need to update the repositories in your pom.xml with the details below.

```xml
<repositories>
  <repository>
    <id>american-airlines-nonprod</id>
    <url>https://package-manager.aa.com/basic/nonprod/maven/</url>
    <releases>
      <enabled>true</enabled>
      <updatePolicy>always</updatePolicy>
    </releases>
    <snapshots>
      <enabled>true</enabled>
      <updatePolicy>always</updatePolicy>
    </snapshots>
  </repository>
  <repository>
    <id>american-airlines-prod</id>
    <url>https://package-manager.aa.com/basic/prod/maven/</url>
    <releases>
      <enabled>true</enabled>
      <updatePolicy>always</updatePolicy>
    </releases>
    <snapshots>
      <enabled>true</enabled>
      <updatePolicy>always</updatePolicy>
    </snapshots>
  </repository>
</repositories>
```

***settings.xml:***
The following details need to be added into your settings.xml file for authenticating into cloudsmith

```xml
<settings>
  <servers>
    <server>
      <id>american-airlines-nonprod</id>
      <username>cloudsmith-username</username>
      <password>YOUR-API-KEY</password>
    </server>
    <server>
      <id>american-airlines-prod</id>
      <username>cloudsmith-username</username>
      <password>YOUR-API-KEY</password>
    </server>
  </servers>
</settings>
```

After updating your pom and settings files, you can run the mvn commands to test your package build locally

#### Docker

You should be able to access cloudsmith documentation when selecting **docker** as the package type under `Set Me Up` dropdown

you can login using the following command

```
docker login docker.aa.com
Username: cloudmsith-username
Password: YOUR-API-KEY
```

To pull a docker image locally, here are the urls,

nonprod: docker.aa.com/nonprod
prod: docker.aa.com/prod

example command to pull a docker image
`docker pull docker.aa.com/nonprod/your-image:latest`

***Dockerfile example (using an image from cloudsmith):***
`FROM docker.aa.com/prod/aa.com/python:3.12.5-dev@sha256:e8742f7efb1170fab3a4f6d402a6151242e5b322116ae9e51ffdf0ce4267449b as python-builder`

#### NPM

You should be able to access cloudsmith documentation when selecting **npm** as the package type under `Set Me Up` dropdown following directions above.

***.npmrc:***
Recommended way is to create or update your .npmrc file in your project repository to point to Cloudsmith. 

 **⚠️ WARNING:** Do not put your authentication credentials in repo level .npmrc or push it to remote GitHub repo.

```
registry=https://npm.aa.com/prod/
always-auth=true
engine-strict=true
```

Run `npm login` and follow the prompts. This will update your local .npmrc with Cloudsmith credentials (not the project .npmrc). Use <<CLOUDSMITH-USERNAME>> for Username and <<CLOUDSMITH-API-KEY>> for `Password:`. After successful login, output in commandline would look like below

```
npm login
npm notice Log in on https://npm.aa.com/prod/
Username: jonny-doe
Password: 

Logged in on https://npm.aa.com/prod/.
```

You can verify login was successful using `npm whoami --registry=https://npm.aa.com/prod/`. 

```
npm whoami --registry https://npm.aa.com/prod/
jonny-doe

```

You can also run `npm config ls` to see the contents of local .npmrc at /home/jdoe/.npmrc.

```
npm config ls
; "user" config from /home/sprasai/.npmrc

//npm.aa.com/prod/:_authToken = (protected) 

; "project" config from /home/jdoe/projects/my_node_project/.npmrc

always-auth = true 
engine-strict = true 
registry = "https://npm.aa.com/prod/" 

; node bin location = /home/jdoe/.nvm/versions/node/v18.20.3/bin/node
; node version = v18.20.3
; npm local prefix = /home/jdoe/projects/my_node_project
; npm version = 10.7.0
; cwd = /home/jdoe/projects/my_node_project
; HOME = /home/jdoe
; Run `npm config ls -l` to show all defaults.

```

If this is the first time you are pointing to Cloudsmith, you may also need to

- Run `npm update` command to update **packages-lock.json** file with Cloudsmith registry urls.

- Run `npm install`, to download dependencies from Cloudsmith. 

- Run other npm commands to verify your project successfully builds and runs.


**Helpful tips:**
> Note: In most cases, your dependencies will be in prod. If your package is in non prod, update the registry to nonprod.

> Note: If `npm audit` returns `npm warn audit 403 Forbidden` error, temporary solution is to use ` npm audit --registry https://registry.npmjs.org/` and `npm audit fix --registry https://registry.npmjs.org/` . We are working with Cloudsmith to find a better solution.
