# Waitress

[![Travis build badge](https://travis-ci.org/waitress-andela/waitress.svg?branch=master)](https://travis-ci.org/waitress-andela/waitress) [![Coverage Status](https://coveralls.io/repos/waitress-andela/waitress/badge.svg?branch=master&service=github)](https://coveralls.io/github/waitress-andela/waitress?branch=master)
_The meal tracking app of Andela Lagos_

## Waitress API

This repository houses the API endpoints for the waitress project

### Available Endpoints

It can be found [here](https://waitressandela.herokuapp.com/docs)

### Contribution

Calling all developers ![call](markdown_imgs/call.png)

All forms of contribution is welcome. Thank you for helping to make this project great!!!

Please view this [documentation](https://docs.google.com/a/andela.co/document/d/1xiDfPL-JTebwav6jdW30SzwwnDNZmajJVZhpU6h4kxg/edit?usp=sharing) over here, prepared just for you

## Setup

1. Install Xcode command line tool `xcode-select --install`
2. Install [homebrew](http://brew.sh/)

## Installation

Before you start please ensure you have Python and PostgreSQL installed

### Python Setup

1. Install Python from [here](http://www.python.org/download/) or run the command `brew install python`
2. Install Pipenv with the command

    ```bash
    pip install pipenv
    ```

3. Create a vritual environment with the command

    ```bash
    pipenv shell
    ```

### Database Setup

1. Install [postgresql](http://postgresapp.com/) (Mac OS X)

Copy the following into your `~/.bash_profile` or `~/.zshrc` if you use zsh

```bash
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin
```

### App setup

* Clone the repository

```bash
git clone git@github.com:waitress-andela/waitress.git
```

* Pip install all requirements for the app

_Before installing dependencies make sure your virtual env is activated, if not run `pipenv shell` to activate_

```bash
pipenv install
```

* Create a copy of the `.env.example` file and rename to `.env`.

* Add the different variables as they are needed to get the project running.

* Migrate the models to your database

```bash
python manage.py makemigrations
python manage.py migrate
```

* Startup the server

```bash
python manage.py runserver
```

* Navigate to the api [doc](http://localhost:8000/docs/) built with swagger

And you are all setup :)

## Testing

To test the application and see the coverage

1. Run coverage `coverage run manage.py test` to know how much of the app is covered by automated testing.
2. View the report of the coverage on your terminal `coverage report`.
3. Produce the html of coverage result `coverage html`.
