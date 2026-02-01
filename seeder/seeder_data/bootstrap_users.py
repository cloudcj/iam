# import os
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from authz.models import Role, UserRole

# User = get_user_model()


# def seed_superadmin():
#     """
#     Create a bootstrap SuperAdmin account if it does not exist.
#     This is the ONLY user that may be created automatically in production.
#     """

#     username = os.getenv("IAM_SUPERADMIN_USERNAME", "superadmin")
#     password = os.getenv("IAM_SUPERADMIN_PASSWORD")

#     if not password:
#         print("⚠️ IAM_SUPERADMIN_PASSWORD not set — skipping superadmin seed")
#         return

#     user, created = User.objects.get_or_create(
#         username=username,
#         defaults={
#             "is_staff": True,
#             "is_active": True,
#         },
#     )

#     if created:
#         user.set_password(password)
#         user.save()
#         print(f"✅ SuperAdmin user '{username}' created")
#     else:
#         print(f"ℹ️ SuperAdmin user '{username}' already exists")

#     # Assign SuperAdmin role
#     try:
#         role = Role.objects.get(name="SuperAdmin")
#     except Role.DoesNotExist:
#         print("❌ SuperAdmin role does not exist. Run RBAC seeder first.")
#         return

#     UserRole.objects.get_or_create(user=user, role=role)
#     print("✅ SuperAdmin role assigned")


# def seed_admin():
#     """
#     Optional bootstrap Admin account (non-IAM admin).
#     Should normally be used only in dev/staging.
#     """

#     if os.getenv("IAM_BOOTSTRAP_ADMIN") != "true":
#         return

#     username = os.getenv("IAM_ADMIN_USERNAME", "admin")
#     password = os.getenv("IAM_ADMIN_PASSWORD")

#     if not password:
#         print("⚠️ IAM_ADMIN_PASSWORD not set — skipping admin seed")
#         return

#     user, created = User.objects.get_or_create(
#         username=username,
#         defaults={
#             "is_staff": True,
#             "is_active": True,
#         },
#     )

#     if created:
#         user.set_password(password)
#         user.save()
#         print(f"✅ Admin user '{username}' created")
#     else:
#         print(f"ℹ️ Admin user '{username}' already exists")

#     role = Role.objects.get(name="Admin")
#     UserRole.objects.get_or_create(user=user, role=role)
#     print("✅ Admin role assigned")


# def seed_member():
#     """
#     Optional demo member account.
#     NEVER enable in production.
#     """

#     if os.getenv("ENV") != "local":
#         return

#     username = "member"
#     password = "member123"

#     user, created = User.objects.get_or_create(
#         username=username,
#         defaults={
#             "is_active": True,
#         },
#     )

#     if created:
#         user.set_password(password)
#         user.save()
#         print("✅ Demo Member user created")

#     role = Role.objects.get(name="Member")
#     UserRole.objects.get_or_create(user=user, role=role)
#     print("✅ Member role assigned")


# def seed_accounts():
#     """
#     Entry point for accounts seeding.
#     """
#     seed_superadmin()
#     seed_admin()
#     seed_member()

#     print("🎉 Account seeding complete")




# # # --------------------
# # # Super Admin
# # # --------------------
# # def seed_super_admin():
# #     user, created = User.objects.get_or_create(
# #         username=SUPER_ADMIN["username"],
# #         defaults={
# #             "email": SUPER_ADMIN["email"],
# #             "is_staff": True,
# #             "is_superuser": True,
# #         },
# #     )

# #     if created:
# #         user.set_password(SUPER_ADMIN["password"])
# #         user.save()

# #     department = Department.objects.get(code=SUPER_ADMIN["department"])
# #     role = Role.objects.get(name=SUPER_ADMIN["role"])

# #     UserDepartment.objects.get_or_create(
# #         user=user,
# #         department=department,
# #     )

# #     UserRole.objects.get_or_create(
# #         user=user,
# #         role=role,
# #     )