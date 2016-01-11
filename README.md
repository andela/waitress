# Meals' Tracking Service [![Travis build badge](https://travis-ci.org/andela-osule/waitress.svg?branch=master)](https://travis-ci.org/andela-osule/waitress) [![Coverage Status](https://coveralls.io/repos/andela-osule/waitress/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-osule/waitress?branch=master)

_A meals tracking app for keeping updated list of served persons._

[Meals tracking app](http://waitressandela.herokuapp.com/) tracks persons who have had meals.

__Available Endpoints__

- `GET "/users"`
    ```javascript
    [
        {
            "id": 1,
            "firstname": "E",
            "lastname": "",
            "photo": "https://avatars.slack-edge.com/...jpg",
            "is_tapped": false
        },
    ]
    ```

- `GET "/users?filter=a"`
    ```javascript
    [
        {
            "id": 5,
            "firstname": "A...",
            "lastname": "J...",
            "photo": "https://avatars.slack-edge.com/...jpg",
            "is_tapped": false
            ""
        },
    ]
    ```

- `GET "/users/update-users"`
    ```javascript
    {
        "status": "Users list not changed"
    }
    ```

- `POST "/users/{id}/tap"` 
    ```javascript
    {
        'status': 'You tapped successfully'
    }
    ```
 
- `POST "/users/nfctap" --slackUserId="ident"`
    ```javascript
    {
        'firstname': 'Test',
        'lastname': 'User',
        'status': 'You tapped successfully'
    }
    ```

- `POST "/users/nfctap" --slackUserId="ident"`
    ```javascript
    {
        'firstname': 'Test',
        'lastname': 'User',
        'status': 'You tapped successfully'
    }
    ```

- `POST "/users/{id}/untap" --passphrase="njdgf"`
    ```javascript
    {
        'status': 'You untapped successfully'
    }
    ```

- `GET "/meal-sessions/"` 
    ```javascript
    {
        "before_midday": false
    }
    ```

- `POST "/meal-sessions/start/" --before_midday=bool --passphrase="cdfjfd"`
    ```javascript
    {
        "status": "Breakfast session started"
    }
    ```

- `POST "/meal-sessions/stop/" --before_midday=bool --passphrase="cdfjfd"`
    ```javascript
    {
        "status": "Breakfast session stopped"
    }
    ```
