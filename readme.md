# Micro-Blog

Micro-Blog provides an environment to users which allows read, write and share their opinion.

### Table of Contents

- [Micro-Blog](#Micro-Blog)
  - [Repository](#Repository)
- [Server](#Server)
  - [Run](#Run)
  - [Folder Structure](#Folder-Structure)
  - [API References](#API-References)
    - [Authentication](#Authentication)
      - [Register user](#Register-user)
      - [Login user](#Login-user)
    - [User Listing](#User-Listing)
      - [Get all users](#Get-all-users)
      - [Get user by id](#Get-user-by-id)
      - [Get user posts by user id](#Get-user-posts-by-user-id)
    - [Blog Post Endpoints](#Blog-Post-Endpoints)
      - [Get all posts](#Get-all-posts)
      - [Post new blog-post](#Post-new-blog-post)
      - [Get blog-post by id](#Get-post-by-id)
      - [Update blog-post by id](#Update-post-by-id)
      - [Delete blog-post by id](#Delete-post-by-id)
      - [Get all categories](#Get-all-categories)
    - [Comment Endpoints](#Comment-Endpoints)
      - [Get all comments](#Get-all-comments)
      - [Post new comment](#Post-new-comment)
      - [Get comment by id](#Get-comment-by-id)
      - [Update comment by id](#Update-comment-by-id)
      - [Delete comment by id](#Delete-comment-by-id)
    - [Vote endpoints](#Vote-Endpoints)
      - [Post vote](#Post-new-vote)
- [Client](#Client)
  - [Recommended System Environment](#Recommended-System-Environment)
  - [Project Setup](#Project-Setup)
  - [Folder Structure](#Folder-Structure)
  - [Project Plan](#Project-Plan)
    - [Pages](#Pages)
- [Appendix](#Appendix)
  - [Status Codes](#Status-Codes)
- [Guide for pull requests](#Guide-for-pull-requests)
  - [Creating Pull Requests](#Creating-Pull-Requests)
  - [Reviewing Pull Requests](#Reviewing-and-Merging-the-Pull-Requests)

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

Project needs a environment files before run. They have to be created under `client/` directory. The name of the files should be ``".env.production"`` and ``".env.development"``. They should contain the following code:

``` .env
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
