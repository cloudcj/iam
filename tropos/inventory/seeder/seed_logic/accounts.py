from django.contrib.auth.models import Group, Permission
from django.contrib.auth.hashers import make_password
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db import transaction

# Fetch Abstracted User Model
User = get_user_model()

@transaction.atomic
def run():
    # Clear old data (optional, for re-running seeds)
    # Group.objects.filter(name__in=['Root', 'Admin', 'Member']).delete()
    # User.objects.filter(username__in=['root_user', 'admin_user', 'member_user']).delete()

    # Create Groups
    root_group, _ = Group.objects.get_or_create(name='Root')
    admin_group, _ = Group.objects.get_or_create(name='Admin')
    member_group, _ = Group.objects.get_or_create(name='Member')
    # root_group = Group.objects.create(name='Root')
    # admin_group = Group.objects.create(name='Admin')
    # member_group = Group.objects.create(name='Member')

    # All permissions
    all_perms = Permission.objects.all()

    # Get all permissions as a set
    # all_perms = set(Permission.objects.all())

    # Get restricted permissions for auth app models (User, Group, Permission)
    restricted_models = ContentType.objects.filter(
        app_label='auth',
        model__in=['user', 'group', 'permission']
    )

     # Root: all permissions
    root_group.permissions.set(all_perms)

    # Admin: all except restricted
    admin_group.permissions.set(
        Permission.objects.exclude(content_type__in=restricted_models)
    )

    # Member: admin perms without delete
    member_group.permissions.set(
        Permission.objects.exclude(content_type__in=restricted_models)
                  .exclude(codename__startswith='delete_')
    )




    # restricted_perms = set(Permission.objects.filter(content_type__in=restricted_models))

    # # Admin = all perms - restricted
    # admin_perms = all_perms - restricted_perms

    # # Staff = admin perms without delete perms
    # no_delete_perms = {perm for perm in admin_perms if not perm.codename.startswith('delete_')}

    # Assign permissions
    # root_group.permissions.set(Permission.objects.all())
    # admin_group.permissions.set(Permission.objects.filter(id__in=[p.id for p in admin_perms]))
    # member_group.permissions.set(Permission.objects.filter(id__in=[p.id for p in no_delete_perms]))

    # Create users with first_name and last_name
    root_user,_ = User.objects.get_or_create(
        username='root_user',
        email='root@example.com',
        first_name='Root',
        last_name='Beer',
        password=make_password('rootpass123'),
        is_superuser=True,
        is_staff=True
    )
    admin_user,_ = User.objects.get_or_create(
        username='admin_user',
        email='admin@example.com',
        first_name='Admin',
        last_name='Stration',
        password=make_password('adminpass123'),
        is_staff=False
    )
    member_user,_ = User.objects.get_or_create(
        username='member_user',
        email='member@example.com',
        first_name='Member',
        last_name='Me',
        password=make_password('memberpass123'),
        is_staff=False
    )

    # Assign groups - user belongs exactly to the intended group.
    root_user.groups.set([root_group])
    admin_user.groups.set([admin_group])
    member_user.groups.set([member_group])

    # Assign groups -  Keep old roles, just add one more
    # root_user.groups.add(root_group)
    # admin_user.groups.add(admin_group)
    # member_user.groups.add(member_group)

def revert():
    Group.objects.filter(name__in=['Root', 'Admin', 'Member']).delete()
    User.objects.filter(username__in=['root_user', 'admin_user', 'member_user']).delete()

