import os

environment = os.getenv("ENV", "development")

if environment == "staging":
    from settings.staging import *
elif os.getenv("TRAVIS_CI") or environment == "testing":
    from settings.testing import *
elif environment == "production":
    from settings.production import *
else:
    from settings.development import *
