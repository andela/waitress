# Waitress

[![Travis build badge](https://travis-ci.org/waitress-andela/waitress.svg?branch=master)](https://travis-ci.org/waitress-andela/waitress) [![Coverage Status](https://coveralls.io/repos/waitress-andela/waitress/badge.svg?branch=master&service=github)](https://coveralls.io/github/waitress-andela/waitress?branch=master)
_The meal tracking app of Andela Lagos_

## Waitress API

This repository houses the API endpoints for the waitress project.
This project makes use of Python3.5 and above.
For production it makes use of Python 3.7.6

### Available Endpoints

It can be found [here](https://waitressandela.herokuapp.com/docs)

## Installation

Before you start please ensure you have Python and PostgreSQL installed

### Python Setup

1. Install Python3 from [here](http://www.python.org/download/) or run the command `brew install python3`
2. Install Pipenv with the command

    ```bash
    pip install pipenv
    ```

3. Create a virtual environment with the command

    ```bash
    pipenv shell
    ```

### Database Setup

1. Install [postgresql](http://postgresapp.com/) (Mac OS X)

Copy the following into your `~/.bash_profile` or `~/.zshrc` if you use zsh and you think your postgres isn't properly configured

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
pipenv run python manage.py makemigrations
pipenv run python manage.py migrate
```

* Startup the server

```bash
pipenv run python manage.py runserver
```

* Navigate to the api [doc](http://localhost:8000/docs/) built with swagger

And you are all setup :)

## Backups

The backup process is automated and is schedule to run on the 1st of every month. The backup process involves fetching the meals data for the waitress and pantry Django apps from the database, write them to a CSV file and upload the file to google drive. It uses slack to handle notifications to the waitress team. Scheduling is handle by the Heroku Scheduler.

The backup process uses some environment variables like `ENABLE_BACKUP_DELETE_ACTION` to give the user more control.

`ENABLE_BACKUP_DELETE_ACTION`: is a boolean value used to enable/disable the delete operation on the database, especially when testing/developing locally.

To run the backup script, just execute:

```sh
make run-backup
```

## Testing

To test the application and see the coverage

1. Run coverage `make test` to know how much of the app is covered by automated testing.
2. View the report of the coverage on your terminal `coverage report`.
3. Produce the html of coverage result `coverage html`.
