from django.forms import Form, CharField, PasswordInput, TextInput


class LoginForm(Form):
    username = CharField(
        max_length=20,
        error_messages={"required": "Please enter your username"},
        widget=TextInput(
            attrs={"class": "input form-control", "placeholder": "enter your username"}
        ),
    )
    password = CharField(
        max_length=20,
        error_messages={"required": "Password is required"},
        widget=PasswordInput(
            attrs={"class": "input form-control", "placeholder": "enter your password"}
        ),
    )
