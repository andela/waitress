from django.forms import CharField, Form, PasswordInput, TextInput


class LoginForm(Form):
    username = CharField(
        max_length=20,
        error_messages={"required": "Please enter your username"},
        widget=TextInput(
            attrs={
                "class": "input form-control mb-2",
                "placeholder": "Enter your username",
                "autofocus": "autofocus",
            }
        ),
    )
    password = CharField(
        max_length=20,
        error_messages={"required": "Password is required"},
        widget=PasswordInput(
            attrs={"class": "input form-control", "placeholder": "Enter your password"}
        ),
    )
