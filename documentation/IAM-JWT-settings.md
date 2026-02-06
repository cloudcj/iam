from pathlib import Path

BASE_DIR = Path(**file**).resolve().parent.parent

# JWT settings

JWT_PRIVATE_KEY_PATH = BASE_DIR / "keys" / "private.pem"
JWT_PUBLIC_KEY_PATH = BASE_DIR / "keys" / "public.pem"

JWT_ALGORITHM = "RS256"
JWT_ISSUER = "gaia-iam"
JWT_ACCESS_TOKEN_MINUTES = 15

## Decode JWT to check it

- Copy the access_token and decode it using: https://jwt.io

  ## Expected payload:

  {

  "iss": "gaia-iam",
  "sub": "84249033-d316-46c1-9c71-2a59b90c99dc",
  "username": "cj",
  "type": "user",
  "roles": ["Admin"],
  "permissions": ["iam.test.read"],
  "iat": 1700000000,
  "exp": 1700000900
  }

## Fixing JWT_PRIVATE_KEY_PATH

    AttributeError: 'Settings' object has no attribute 'JWT_PRIVATE_KEY_PATH' [20/Jan/2026 12:28:54] "POST /api/auth/login/ HTTP/1.1" 500 108303

    ## steps:

    ## 1.) install cryptography

        uv add cryptography

    ## 2. create a file called: generat_keys.py. then add this:

    from cryptography.hazmat.primitives.asymmetric import rsa
    from cryptography.hazmat.primitives import serialization
    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent
    KEYS_DIR = BASE_DIR / "keys"
    KEYS_DIR.mkdir(exist_ok=True)

    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    (KEYS_DIR / "private.pem").write_bytes(private_pem)
    (KEYS_DIR / "public.pem").write_bytes(public_pem)

    print("✅ RSA keys generated in /keys")

    ## 3.) after running it, you should now have:

        IAM/
        ├── keys/
        │   ├── private.pem
        │   └── public.pem

    ## 4.) add jwt settings to settings/base.py

    from pathlib import Path

    BASE_DIR = Path(__file__).resolve().parent.parent

    # JWT settings
    JWT_PRIVATE_KEY_PATH = BASE_DIR / "keys" / "private.pem"
    JWT_PUBLIC_KEY_PATH = BASE_DIR / "keys" / "public.pem"

    JWT_ALGORITHM = "RS256"
    JWT_ISSUER = "gaia-iam"
    JWT_ACCESS_TOKEN_MINUTES = 15
