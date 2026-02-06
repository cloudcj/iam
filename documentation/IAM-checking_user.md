from iam.services.authz import resolve_user_roles_and_permissions
from iam.models import User

user = User.objects.get(username="alice")
roles, permissions = resolve_user_roles_and_permissions(user)

print("Roles:", roles)
print("Permissions:", permissions)
