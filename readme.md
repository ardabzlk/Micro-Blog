# My Playground For Micro-Blog Project

<br>

## Instructions: Starting to work on the project

### Repository 

git: git clone https://github.com/ardabzlk/Micro-Blog-Playground.git

There are one working directory.

* server (backend / Flask)

<br>

### Server-side

To work in server-side put `cd server` to terminal

To access virtual environment write `env\Scripts\activate.bat` to terminal

Install packages:

~~~bash
```
pip install -r requirements.txt
```
~~~

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
"DB_URI":"mongodb+srv://{example_user_name}:{example_password}@cluster0.ldccoab.mongodb.net/{example_db}?retryWrites=true&w=majority",

"MONGODB_SETTINGS": {
  "db": "example_db",
  "host": "example_host"
 }
}
```

<br>

### Client-side

# micro-blog

## Project setup

```
yarn install
```

### Compiles and hot-reloads for development

```
yarn serve
```

### Compiles and minifies for production

```
yarn build
```

### Lints and fixes files

```
yarn lint
```

### Customize configuration

See [Configuration Reference](https://cli.vuejs.org/config/).

## TechStack

* Backend: Flask
* Frontent: Vue2.js