# Waitress [![Travis build badge](https://travis-ci.org/andela-osule/waitress.svg?branch=master)](https://travis-ci.org/andela-osule/waitress) [![Coverage Status](https://coveralls.io/repos/andela-osule/waitress/badge.svg?branch=master&service=github)](https://coveralls.io/github/andela-osule/waitress?branch=master)

_A meals tracking app for keeping updated list of served persons._

[Waitress](http://waitressandela.herokuapp.com/) tracks persons who have had meals.

__AVAILABLE ENDPOINTS__

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
- `POST "/users/update-users" --name="Guest 1"`
    ```javascript
    {
      "status": "Guest user was created successfully.",
      "id": 149
    }
    ```

- `GET "/users/remove-old-friends"`
  ```javascript
  {
      "status": "Users deleted",
      "users": ["Peter Parker", "Ben Bruce"]
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
- `POST "/users/{id}/retrieve-secure/" --passphrase="cdfd"`
  ```javascript
  {
      "id": 5,
      "firstname": "A...",
      "lastname": "J...",
      "photo": "https://avatars.slack-edge.com/...jpg",
      "is_tapped": false,
      "slack_id": "U-SLACK"
  }
  ```
- `GET "/reports/"`
  ```javascript
  // Gets the meal record for the day.
  {
      breakfast: {num_served: X},
      lunch: {num_served: Y},
      date: date_today
  }
  ```
- `GET "/reports?from=yyyy-mm-dd&to=yyyy-mm-dd"` get report.
  `GET "/reports?from=yyyy-mm&to=yyyy-mm-dd"` get reports from month in the year until set date.
  `GET "/reports?from=yyyy-mm-dd"` get reports from date until today.

  *If the to query parameter is missing, reports is crammed until the present date.*

  ```javascript
  [
    {
      breakfast:
      lunch:
      date:
    },
    {
      ...
    }
  ]
  ```

__CHANGE LOG__
* Added 2 new endpoints [February 4, 2016]
