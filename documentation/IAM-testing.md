python manage.py shell

### for creating user

    from iam.models import User

    user = User.objects.create_user(
        username="cj",
        password="secret123"
    )

    print(user.id, user.username)

    print(user.id, user.username)

### create one role + one permission

    from authz.models import Role, Permission, UserRole
    from iam.models import User

    # Create permission

    perm, \_ = Permission.objects.get_or_create(
    code="iam.test.read"
    )

    # Create role

    role, \_ = Role.objects.get_or_create(
    name="Admin"
    )

    role.permissions.add(perm)

    # Assign role to user

    user = User.objects.get(username="cj")
    UserRole.objects.get_or_create(user=user, role=role)

### negative test

    role.permissions.clear()

### to check if roles are there

    from authz.models import Role

    admin = Role.objects.get(name="Admin")
    print(admin.permissions.values_list("code", flat=True))

### to check “What roles and permissions does this user actually have in IAM?”