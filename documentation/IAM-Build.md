# accounts model: create custom user model

# create managers.py

    - create UserManager because ActiveBaseUser doesnt have default manager
    - Create ActiveUserManager to query active users

# Modify settings

    AUTH_USER_MODEL = "iam.User"
