🧠 Two Completely Different Authentication Moments

There are two authentication moments in your system:

Moment                              Purpose                                     What is used
Login                           Verify username + password              authenticate() → ModelBackend
Every API request                   Verify JWT                                  CustomAuthentication


--------------

Custom User Model (IDENTITY ONLY)
What the User model is for

username
password hash
active / deleted state

What it is NOT for

roles
permissions
business logic