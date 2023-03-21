# Micro-Blog

Micro-Blog provides an environment to users which allows read, write and share their opinion.

### Table of Contents

- [Micro-Blog](#micro-blog)
  - [Table of Contents](#table-of-contents)
  - [Repository](#repository)
- [Server](#server)
  - [Run](#run)
  - [Folder Structure](#folder-structure)
  - [API References](#api-references)
  - [Authentication](#authentication)
    - [Register user](#register-user)
    - [Login user](#login-user)
  - [User Listing](#user-listing)
    - [Get all users](#get-all-users)
    - [Get user by id](#get-user-by-id)
    - [Get user posts by user id](#get-user-posts-by-user-id)
  - [Blog Post Endpoints](#blog-post-endpoints)
    - [Get all posts](#get-all-posts)
    - [Post new blog-post](#post-new-blog-post)
    - [Get post by id](#get-post-by-id)
    - [Update post by id](#update-post-by-id)
    - [Delete post by id](#delete-post-by-id)
    - [Get all categories](#get-all-categories)
  - [Comment Endpoints](#comment-endpoints)
    - [Get all comments](#get-all-comments)
    - [Post new comment](#post-new-comment)
    - [Delete comment by id](#delete-comment-by-id)
  - [Vote Endpoints](#vote-endpoints)
    - [Post new vote](#post-new-vote)
- [Client](#client)
  - [Recommended System Environment](#recommended-system-environment)
  - [Project setup](#project-setup)
    - [Install dependencies](#install-dependencies)
    - [Compiles and hot-reloads for development](#compiles-and-hot-reloads-for-development)
    - [Compiles and minifies for production](#compiles-and-minifies-for-production)
    - [Lints and fixes files](#lints-and-fixes-files)
    - [Customize configuration](#customize-configuration)
  - [Folder Structure](#folder-structure-1)
  - [Project Plan](#project-plan)
    - [Pages](#pages)
- [Appendix](#appendix)
  - [Status Codes](#status-codes)
- [Guide for pull requests](#guide-for-pull-requests)
  - [Creating Pull Requests](#creating-pull-requests)
    - [Example Pull Request](#example-pull-request)
  - [Reviewing and Merging The Pull Requests](#reviewing-and-merging-the-pull-requests)
    - [Example merge process](#--example-merge-process--)
- [Guide for Dockerization on Ubuntu 20.04](#guide-for-dockerization-on-ubuntu-2004)
  - [Docker Installation](#docker-installation)
    - [Install Docker Engine](#install-docker-engine)
  - [Dockerization](#dockerization)
    - [Vue App](#vue-app)
    - [Flask App](#flask-app)
    - [MongoDB](#mongodb)
    - [Docker Compose](#docker-compose)
    - [Blockers, issues and solutions](#blockers--issues-and-solutions)
      - [Issue 1](#issue-1)
      - [Issue 2](#issue-2)
    - [Conclusion](#conclusion)

<br>

### Repository

git: git clone <https://github.com/ardabzlk/Micro-Blog-Playground.git>

There are two working directory.

server (backend / Flask)

client (frontend / Vue.js)

# Server

Server side contains application files and test files. App.py is the main file of the application. It contains all the routes and functions of the application. Test files are used to test the application. You can run the tests by writing `pytest` to terminal.

To work in server-side put `cd server` to terminal

To access virtual environment

- On windows write `env\Scripts\activate.bat` to terminal
- On linux write `source env/bin/activate` to terminal
- On mac write `source env/bin/activate` to terminal

Install packages:

```bash
pip install -r requirements.txt
```

config.json must be created under the server directory

You can use code the snippet below as a template for config.json

```json
{
  "APP_NAME": "example_app",
  "DEBUG": true,
  "TESTING": true,
  "SECRET_KEY": "example_secret_key",
  "DB_NAME": "example_db",
  "WTF_CSRF_ENABLED": false,
  "DB_URI": "mongodb+srv://{example_user_name}:{example_password}@cluster0.ldccoab.mongodb.net/{example_db}?retryWrites=true&w=majority",

  "MONGODB_SETTINGS": {
    "db": "example_db",
    "host": "example_host"
  }
}
```

First, you need to create a database in MongoDB Atlas. Then, you need to create a user for the database. After that, you need to replace the example_user_name, example_password, example_db and example_host with your own information. You can find the information in the MongoDB Atlas dashboard.

### Run

To run the application write `python app.py` to terminal

<br>

## Folder Structure

- src
  - models
    - Mongoengine model; eg. Users, BlogPosts
  - routes
    - endpoint methods; eg. post_management for "blog-posts/<param_post_id>" endpoint
  - services
    - global functions; eg. JWT_service.py
- tests
  - unit tests; eg. test_database_models.py
  - integration tests; eg. test_authentication.py
  - conftest.py
    - fixtures; eg. client, db, user, post
- app.py
  - main file of the application which contains all the routes and functions of the application and also the configuration of the application such as database connection.
- config.json (not included in the repository)
  - configuration file of the application (the example is given above)
- requirements.txt
  - packages that are used in the application

# API References

## Authentication

#### Register user

```http
  POST /api/register
```

| Parameter  | Type     | Description                                   |
| :--------- | :------- | :-------------------------------------------- |
| `name`     | `string` | **Required**. Name of the new user            |
| `surname`  | `string` | **Required**. Surname of the new user         |
| `email`    | `string` | **Required**. Email of the new user           |
| `password` | `string` | **Required**. Hashed password of the new user |

register new user and return the token

#### Login user

```http
  POST /api/login
```

| Parameter  | Type     | Description                               |
| :--------- | :------- | :---------------------------------------- |
| `email`    | `string` | **Required**. Email of the user           |
| `password` | `string` | **Required**. Hashed password of the user |

login user and return the token and user information

## User Listing

#### Get all users

```http
  GET /api/users
```

it returns all users in the database as a list of dictionaries.

#### Get user by id

```http
  GET /api/users/<uid>
```

| Parameter | Type     | Description                  |
| :-------- | :------- | :--------------------------- |
| `uid`     | `string` | **Required**. Id of the user |

it returns the user information as a dictionary.

#### Get user posts by user id

```http
  GET /api/users/<uid>/blog_posts
```

| Parameter | Type     | Description                  |
| :-------- | :------- | :--------------------------- |
| `uid`     | `string` | **Required**. Id of the user |

it returns the user posts as a list of dictionaries.

## Blog Post Endpoints

#### Get all posts

```http
  GET /api/blog-posts
```

it returns all posts in the database as a list of dictionaries.

#### Post new blog-post

```http
  POST /api/blog-posts
```

| Parameter     | Type     | Description                                  |
| :------------ | :------- | :------------------------------------------- |
| `title`       | `string` | **Required**. Title of the new post          |
| `content`     | `string` | **Required**. Content of the new post        |
| `user_id`     | `string` | **Required**. Author of the new post         |
| `username`    | `string` | **Required**. author username                |
| `category_id` | `int`    | **Required**. Category id                    |
| `date`        | `date`   | **Required**. Publish date of the new post   |
| `img_base64`  | `string` | **Required**. Image of the new post (base64) |

it adds the new posty.

#### Get post by id

```http
  GET /api/blog-posts/<post_id>
```

| Parameter | Type     | Description                  |
| :-------- | :------- | :--------------------------- |
| `post_id` | `string` | **Required**. Id of the post |

it returns the post information as a dictionary.

#### Update post by id

```http
  PUT /api/blog-posts/<post_id>
```

| Parameter     | Type     | Description                                  |
| :------------ | :------- | :------------------------------------------- |
| `post_id`     | `string` | **Required**. Id of the post.                |
| `title`       | `string` | **Required**. Title of the new post          |
| `content`     | `string` | **Required**. Content of the new post        |
| `category_id` | `int`    | **Required**. Category id                    |
| `img_base64`  | `string` | **Required**. Image of the new post (base64) |

it updates the post.

#### Delete post by id

```http
  DELETE /api/blog-posts/<post_id>
```

| Parameter | Type     | Description                   |
| :-------- | :------- | :---------------------------- |
| `post_id` | `string` | **Required**. Id of the post. |

it deletes the post.

#### Get all categories

```http
  GET /api/blog-posts/categories
```

it returns all categories in the database as a list of dictionaries.

## Comment Endpoints

#### Get all comments

```http
  GET /api/comment/<post_id>
```

| Parameter | Type     | Description                  |
| :-------- | :------- | :--------------------------- |
| `post_id` | `string` | **Required**. Id of the post |

it returns all comments belongs to a particular post

#### Post new comment

```http
  POST /api/comment/<post_id>
```

| Parameter         | Type     | Description                               |
| :---------------- | :------- | :---------------------------------------- |
| `user_id`         | `string` | **Required**. Author of the comment       |
| `username`        | `string  | **Required**. Author username             |
| `post_id`         | `string` | **Required**. Id of the post              |
| `comment_content` | `string` | **Required**. Content of the comment      |
| `date`            | `date`   | **Required**. Publish date of the comment |

it adds the new comment.

#### Delete comment by id

```http
  DELETE /api/comment/<comment_id>
```

| Parameter    | Type     | Description                      |
| :----------- | :------- | :------------------------------- |
| `comment_id` | `string` | **Required**. Id of the comment. |

it deletes the comment.

## Vote Endpoints

#### Post new vote

```http
  POST /api/vote/<post_id>
```

| Parameter | Type     | Description                      |
| :-------- | :------- | :------------------------------- |
| `user_id` | `string` | **Required**. Author of the vote |
| `post_id` | `string` | **Required**. Id of the post     |
| `vote`    | `int`    | **Required**. Vote of the post   |

it adds or updates the vote.

# Client

Client-side contains Vue application which runs through node local server. Before starting to work on the client, dependencies should be installed. To do that first open the terminal and navigate to "/client" folder and run a command "yarn install" to install client dependencies.

### Recommended System Environment

- npm 8.4 or higher (npm -v)
- node 16.14.2 or higher (node -v)

### Project setup

Project needs a environment files before run. They have to be created under `client/` directory. The name of the files should be `".env.production"` and `".env.development"`. They should contain the following code:

```.env
# Development
NODE_ENV= development
VUE_APP_API_BASE_URL="http://your-api-url"
PROD_TYPE_PRODUCTION = false
```

After that, you can install dependencies and run the project.

##### Install dependencies

```
yarn install
```

##### Compiles and hot-reloads for development

```
yarn serve
```

##### Compiles and minifies for production

```
yarn build
```

##### Lints and fixes files

```
yarn lint
```

##### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

### Folder Structure

- public
  - It contains static files such as index.html, favicon.ico
- src
  - It contains the source code of the project such as assets, components, router etc.
  - src/components
    - It contains the component codes of the pages. Components has been separated by their pages. It consist of .vue files.
  - src/core
    - It is the place that where scripts, vuex store files has been conserved.
  - src/layout
    - Directory to keep global layout components e.g. Layout.vue and Footer.vue
  - src/router
    - Router script file of the project. Protected routes has been used on this project.
  - src/main.js
    - It is an important file to initialize packages such as axios, vuetify, router etc..

### Project Plan

#### Pages

- Login
- Register
- Start Page
- Posts
  - It is the place where all blog posts can be viewed or new blog post can be added. It can be filtered by their title. Details about a post can be viewed by clicking the explore button on a blog post card.
- Post Detail
  - Users can read the post, leave comment, like or dislike the post on that page
- New post
- Users
  - It is the pages that lists all users that saved on the system. To view the blog posts from a particular user it should be navigated from that page.
- Profile page
  - To see the details about a user

# Appendix

### Status Codes

```Python
class StatusCodeEnums:
    success = {"msg": "Success", "code": 200}
    not_found = {"msg": "Not found", "code": 404}
    bad_request = {"msg": "Bad Request", "code": 400}
    unauthorized = {"msg": "Unauthorized", "code": 401}
    gone = {"msg": "Gone", "code": 410}

```

# Guide for pull requests

## Creating Pull Requests

Creating the pull requests is an important part of git-flow. A good PR should be easy-to-review, be helpful to the new developers' onboarding and has a positive effect on product development.

Here are some key points that developers should follow before creating their pull requests

1. **Write descriptive and consistent names**

   - Variable names, file names, folder structure etc...

2. **Create a clear PR title and description**

   - Titles and descriptions must meet conventional commit standards. Learn more about [conventional commits](https://www.conventionalcommits.org/en/v1.0.0/)
   - Do not hesitate to enrich the description with more context

3. **Manage PR disagreements through direct communication**

   - Please ask questions and disagreements.

4. **Always sync the branch**

   - Developers must pull/push changes on every opening and closing of their IDE

5. **Prefer Smaller Requests**

   - Crowded "changed lists" cause conflicts and slow Merge operations down. Developers should commit their changes more often with related parts of their tasks instead of pushing all changes together and creating PRs with a long changed list.

6. **Package links**

   - Developers should give the link of the newly implemented package if any. There should be a detailed description of the package on the commit message.

### Example Pull Request

1.  **Commit changes**
2.  **Publish/push branch into master** -`git push -u origin 'feature-branch'`
3.  **Create a PR from GitHub**

## Reviewing and Merging The Pull Requests

Merge a pull request into the upstream branch when work is completed. Anyone with push access to the repository can complete the merge. [more info](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/merging-a-pull-request)

The responsibilities of the reviewer

1. **Make sure the code is correct, clean and convenient with the project**
   - Temporary codes, inconvenient variable names should not be allowed. Code should work and look like as requested in the task.
2. **Providing rich and constructive feedback**
   - Review messages should be clear, rich and constructive and should be avoided from personal ego.
3. **Resolving conflicts**
   - It may be the most important part of the merge processes. Facing with a conflict is pretty common. In such cases reviewer should be careful to not to damage the _dev_ branch. For detailed tutorial please [visit](https://www.atlassian.com/git/tutorials/using-branches/merge-conflicts)
4. **Being clear about request changes and comments**
   - Request changes and comments should be separated locally and globally. For instance, a comment about a single line should not be in the main review message, it should be written on the line comment. The reviewer should be clear about the requested changes and the comments.
5. **Decide whether the new packages(if any) are necessary or not**

### **Example merge process**

1. **Switch to the feature branch**
   - `git checkout 'feature-branch'`
2. **Pull the master branch and test locally to see the PR is correct and convenient with requested.**

   - `git pull origin master`

3. **If everything is fine go to repo and merge the PR.**
4. **If there is a conflict;** Conflicts have to be resolved before merge process. IDEs make resolving process easier by visualizing them. Example: [VS Code Merge Conflicts](https://code.visualstudio.com/docs/sourcecontrol/overview#_merge-conflicts). Once conflict is resolved, it should be pushed to the remote feature branch.
5. **Switch to master branch on local repository**
   - `git checkout master`
6. **Update local master with remote master**
   - `git pull origin master`
7. **Merge feature branch into local master.**
   - `git merge 'feature-branch'`
8. **Once conflicts are resolved and task is done go to GitHub repo and merge the PR**

# Guide for Dockerization on Ubuntu 20.04

## Docker Installation

### Install Docker Engine

1. Update the apt package index and install packages to allow apt to use a repository over HTTPS:

   ```bash
   sudo apt-get update

   sudo apt-get install \
       apt-transport-https \
       ca-certificates \
       curl \
       gnupg \
       lsb-release
   ```

2. Add Docker’s official GPG key:

   ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
   ```

3. Use the following command to set up the stable repository.

   ```bash
   echo \
     "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   ```

4. Update the apt package index, and install the latest version of Docker Engine and containerd, or go to the next step to install a specific version:

   ```bash
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

5. Verify that Docker Engine is installed correctly by running the hello-world image.

   ```bash
   sudo docker run hello-world
   ```

   This command downloads a test image and runs it in a container. When the container runs, it prints an informational message and exits.

I will build the images on local machine and use docker compose for server deployment. The logic is that I will build the images on my local machine and push them to the docker hub. Then I will pull the images from the docker hub and deploy them on the server. I will mention the steps for docker compose at the end of the section.

## Dockerization

### Vue App

I started to containerize the project with the Vue app. First of all, I created a Dockerfile in the root directory of the project on my local machine. I used my PC to build the images. Then I added the following lines to the Dockerfile.

```Dockerfile
# build stage
FROM node:18.15.0-alpine as build-stage
WORKDIR /app
COPY package.json yarn.lock /code/
RUN yarn install
COPY . .
RUN yarn build

# production stage
FROM nginx:stable-alpine as production-stage
COPY --from=build-stage /app/dist /usr/share/nginx/html
```

What do we do in the Dockerfile?

First of all, we create a build stage. In this stage, lts node version is pulled from repo as buld-stage then we install the dependencies and build the Vue app. Then we create a production stage. In this stage, we copy the build files from the build stage to the production stage. Finally, we run the nginx server. You can find the Dockerfile in the root directory of the project. The reason behind Dockerfile is written step by step is each instruction in the Dockerfile creates a new layer in the image. Each layer is cached separately by Docker, so if a layer has not changed since the last build, Docker can reuse it instead of rebuilding it. This is why we use multi-stage builds. We can use the build stage to build the app and then copy the build files to the production stage. This way we can reduce the size of the image.

After Dockerfile I take the image of the Vue app and push it to the Docker Hub. You can find the image [here](https://hub.docker.com/repository/docker/ardabzlk/micro-blog-vue/general).

Next I pulled the image from the Docker Hub to the server. I used the following command to pull the image.

```bash
docker pull ardabzlk/micro-blog-vue:{tag}
```

Then I created a container from the image. I used the following command to create a container.

```bash
docker run -d --network mongo-network -p 8000:80 ardabzlk/micro-blog-flask:{tag}
```

By doing that, micro-blog-vue app started to run on the server port 8080. -d tag allows us to run the container in the background. -p tag allows us to map the container port to the server port. --name tag allows us to give a name to the container.

### Flask App

Containerization of the Flask app is pretty similar to the Vue app. I created a Dockerfile in the root directory of the project on my local machine. I used my PC to take the images. Then I added the following lines to the Dockerfile.

```Dockerfile
FROM python:3.9.6-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn Flask

# Copy the rest of the application code to the container
COPY . .

# Set the environment variables
ENV PORT=80

# Expose the port that the application will run on
EXPOSE 80

# Start Gunicorn
CMD gunicorn app:app \
    --bind=0.0.0.0:$PORT
```

What do we do in the Dockerfile?

First of all, we create a build stage. In this stage, lts python version is pulled from repo as buld-stage then we install the dependencies and build the Flask app. Then we create a production stage. In this stage, we copy the build files from the build stage to the production stage. Finally, we run the gunicorn server. You can find the Dockerfile in the root directory of the project. gunicorn implemented to run application on port 80 and we expose the port 80. Basically Dockerfile is the place that we tell to docker what would we do to run the app on server. Thus it follows the steps and runs the app.

After Dockerfile I take the image of the Flask app and push it to the Docker Hub. You can find the image [here](https://hub.docker.com/repository/docker/ardabzlk/micro-blog-flask/general).

Next I pulled the image from the Docker Hub to the server. I used the following command to pull the image.

```bash
docker pull ardabzlk/micro-blog-flask:{tag}
```

Then I created a container from the image. I used the following command to create a container.

```bash
docker run -d -p 8000:80 --name micro-blog-flask ardabzlk/micro-blog-flask:{tag}
```

By doing that, micro-blog-flask app started to run on the server port 8000. -d tag allows us to run the container in the background. -p tag allows us to map the container port to the server port. --name tag allows us to give a name to the container.

### MongoDB

I used the official MongoDB image from Docker Hub. I used the following command to pull the image.

```bash
docker pull mongo
```

Tricky part is to connect the MongoDB container from outside of container. I used the following command to create a container. I used the --network host tag to connect the container from outside of container. It is also a common practice to use the same network for both containers.

```bash
docker network create mongo-network
```

Thus flask app and mongo db container are in the same network which is "mongo-network". The connection string for mongo db became `mongodb://mongo:27017/`.

### Docker Compose

I used the Docker Compose to run the containers. I created a docker-compose.yml file in the root directory of the project.
Verifying the docker-compose.yml file is a good practice. I used the following command to verify the docker-compose.yml file.

```bash
docker compose version
```

I used the following lines to create the docker-compose.yml file at the root directory of the project.

```yml
version: "3.9"

services:
  vue:
    image: ardabzlk/micro-blog-vue:v.0.2
    ports:
      - "8080:80"
    restart: always
    networks:
      - app_network

  flask:
    image: ardabzlk/micro-blog-flask:v.0.5
    ports:
      - "8000:80"
    restart: always
    networks:
      - app_network
      - mongo-network

  mongo:
    image: mongo:latest
    restart: always
    networks:
      - mongo-network

networks:
  app_network:
    driver: bridge
  mongo-network:
    driver: bridge
    external: true
```

What do we do in the docker-compose.yml file?
We declared the services that we want to run. It allows us to manage containers from one source. I used image tag to pull the images from Docker Hub. However build tag can be used to build the images from Dockerfile as well. Port tag for the mapping the container port to the server port. Restart tag allows us to restart the container if it crashes. Networks tag allows us to connect the containers to the same network. I used the following command to run the containers. It can clearly be seen that we did basically the same thing that we did in the Dockerfile section.

next thing all we have to do is to run the containers. I used the following command to run the containers.

```bash
docker compose up -d
```

### Blockers, issues and solutions

I faced some issues while containerizing the project. I will explain the issues and solutions.

#### Issue 1

The first mistake that I did during containerization was I was trying to take the images from the server. I was trying to take the images from the server because I thought that I can use the same Dockerfile for both local and server. I was wrong. I should have used my PC to take the images. Because the Dockerfile is the place that we tell to docker what would we do to run the app on server. Thus it follows the steps and runs the app. If I take the image from the server, it stucks on the building step because server is not as powerful as my PC. Luckily I asked for help from my team-leader and he helped me to solve the issue before wasting too much time.

Solution: I should have used my PC to take the images and use Dockerhub to push the images from local to server.

#### Issue 2

The second issue was the connection string for mongo db. I was trying to connect the mongo db container from outside of container.

Solution: I used the --network host tag to connect the container from outside of container.

### Conclusion

In this section, I explained how I containerized the micro-blog project. I explained the Dockerfile and the commands that I used to containerize the project. I also explained the issues that I faced during the containerization. I hope this article will help you to understand the containerization process. If you have any questions or suggestions, you can reach me from [here](https://www.linkedin.com/in/ardabzlk/).
