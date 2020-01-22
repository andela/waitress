from datetime import date


CURRENT_DATE = date.today().strftime("%Y-%m-%e")

# FETCH_MEAL_RECORDS = 'SELECT * FROM app_slackuser;'
FETCH_MEAL_RECORDS = f"""
SELECT
    to_char(app_mealservice.date, 'DD-MM-YYYY'),
    app_mealservice.date_modified,
    app_mealservice.user_id,
    app_slackuser.firstname,
    app_slackuser.lastname,
    app_slackuser.user_type,
    app_mealservice.breakfast,
    app_mealservice.lunch
FROM
    app_mealservice
LEFT JOIN
    app_slackuser
ON
    app_mealservice.user_id = app_slackuser.id
WHERE
    date < '{CURRENT_DATE}'
ORDER BY
    app_mealservice.date
DESC;
"""

DELETE_MEAL_RECORDS = f"""
DELETE FROM
    app_mealservice
WHERE
    date < '{CURRENT_DATE}';
"""

FETCH_PANTRY_RECORDS = f"""
SELECT
    app_pantry.date,
    app_slackuser.id,
    app_slackuser.firstname,
    app_slackuser.lastname,
    app_slackuser.user_type
FROM
    app_pantry
LEFT JOIN
    app_slackuser
ON
    app_pantry.user_id=app_slackuser.id
WHERE
    date <= '{CURRENT_DATE}'
ORDER BY
    app_pantry.date
DESC;
"""

DELETE_PANTRY_RECORDS = f"""
DELETE FROM
    app_pantry
WHERE
    date < '{CURRENT_DATE}';
"""
