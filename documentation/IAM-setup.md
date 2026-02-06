# creating the django-project

## creating venv

    uv init
    uv venv
    .venv/Scripts/activate

## configure settings.py

### settings structure

        iam/
    ├── config/
    │   ├── __init__.py
    │   ├── settings/
    │   │   ├── base.py  # The Foundation
    │   │   ├── dev.py   # Local Developer Mode
    │   │   ├── prod.py  # Internet-Facing Security Mode
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── iam/
    ├── authz/
    ├── tokens/
    └── manage.py


    iam/
    ├── auth/
    │   ├── tokens/
    │   │   ├── service.py      # issue / revoke tokens
    │   │   └── cookies.py
    │   ├── views/
    │   │   ├── login.py
    │   │   ├── refresh.py
    │   │   └── logout.py
    │   └── csrf.py
    │
    ├── identity/
    │   ├── models/
    │   │   ├── user.py
    │   │   ├── role.py
    │   │   ├── permission.py
    │   │   └── department.py
    │   ├── services/
    │   │   └── permission_resolver.py
    │   └── admin.py
    │
    ├── settings.py
    └── urls.py


### Steps in using the modified settings.py:

#### 1.) install python-dotenv

    uv add python-dotenv

#### 2.) create .env

    DJANGO_SETTINGS_MODULE=config.settings.dev

#### 3.) Load .env in Django entrypoints

    # manage.py

    from dotenv import load_dotenv
    load_dotenv()
    -----------------------------------
    # Place it before:

    execute_from_command_line(sys.argv)
    -----------------------------------
    # config/wsgi.py & config/asgi.py

    from dotenv import load_dotenv
    load_dotenv()

    Note: (Do NOT skip)
    DJANGO_SETTINGS_MODULE=config.settings.dev
    SECRET_KEY=dev-secret

#### Where do you get SECRET_KEY?

    # Generate it using Django. Run this once:

    python - <<EOF
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    EOF

    ------------------------------------------

    # Example output:
    django-insecure-^7y4!%w1@k#...x$2

# Adding dependecies

### Dependencies for the project

    # CMD

    uv add django django-cors-headers django-environ django-filter django-redis djangorestframework djangorestframework-simplejwt gunicorn psycopg2-binary uvicorn


    # Linux
    uv add \
    django \
    django-cors-headers \
    django-environ \
    django-filter \
    django-redis \
    djangorestframework \
    djangorestframework-simplejwt \
    gunicorn \
    psycopg2-binary \
    uvicorn
