# permissions/policies/iam.py
from .schema import Policy
from ..helpers import all_permissions_for_service, read_permissions_for_service
from ..systems.iam import IAM_SERVICE

_POLICIES = [
    # --------------------------------------------------
    # System-wide (used by platform roles)
    # --------------------------------------------------
    Policy(
        code="iam.full",
        name="IAM – Full Access",
        system="iam",
        resource="*",
        permissions=all_permissions_for_service(IAM_SERVICE),
        visible_in_ui=False,
    ),
    Policy(
        code="iam.read_only",
        name="IAM – Read Only",
        system="iam",
        resource="*",
        permissions=read_permissions_for_service(IAM_SERVICE),
        visible_in_ui=False,
    ),

    # --------------------------------------------------
    # User resource (used by dept roles)
    # --------------------------------------------------
    Policy(
        code="iam.user.read_only",
        name="IAM Users – Read Only",
        system="iam",
        resource="user",
        permissions=("iam.user.read",),
    ),
    Policy(
        code="iam.user.manage",
        name="IAM Users – Manage",
        system="iam",
        resource="user",
        permissions=(
            "iam.user.read",
            "iam.user.create",
            "iam.user.update",
            "iam.user.delete",
            "iam.user.update_role",
            "iam.user.update_policy",
            "iam.user.assign_policy",
            "iam.user.remove_policy",
            # no update_dept — dept.admin cannot move users between departments
        ),
    ),
]

IAM_POLICIES = {p.code: p for p in _POLICIES}













# # permissions/policies/iam.py
# from .schema import Policy

# from .schema import Policy

# _POLICIES = [
    # Policy(
    #     code="iam.user.full",
    #     name="User – Read, Create & Update",
    #     system="iam",
    #     resource="user",
    #     permissions=(
    #         "iam.user.read",
    #         "iam.user.create",
    #         "iam.user.update",
    #     ),
    # ),
#     Policy(
#         code="iam.full",
#         name="User – Read, Create & Update",
#         system="iam",
#         resource="user",
#         permissions=(
#             "iam.user.read",
#             "iam.user.create",
#             "iam.user.update",
#         ),
#     ),
#     Policy(
#         code="iam.user.admin",
#         name="User – Full Access",
#         system="iam",
#         resource="user",
#         permissions=(
#             "iam.user.read",
#             "iam.user.create",
#             "iam.user.update",
#             "iam.user.delete",
#         ),
#     ),
# ]

# IAM_POLICIES = {p.code: p for p in _POLICIES}


# IAM_POLICIES = {
#     "iam.user.operator": Policy(
#         code="iam.user.operator",
#         name="User – Read, Create & Update",
#         system="iam",
#         resource="user",
#         permissions=(
#             "iam.user.read",
#             "iam.user.create",
#             "iam.user.update",
#         ),
#     ),

#     "iam.user.admin": Policy(
#         code="iam.user.admin",
#         name="User – Full Access",
#         system="iam",
#         resource="user",
#         permissions=(
#             "iam.user.read",
#             "iam.user.create",
#             "iam.user.update",
#             "iam.user.delete",
#         ),
#     ),
# }
