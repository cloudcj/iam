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
    # Dasboard resource (used by dept roles)
    # --------------------------------------------------
    Policy(
        code="iam.dashboard.read_only",
        name="IAM Dashboard – Read Only",
        system="iam",
        resource="dashboard",
        permissions=("iam.dashboard.read",),
    ),
    Policy(
        code="iam.dashboard.full",
        name="IAM Dashboard – Manage",
        system="iam",
        resource="dashboard",
        permissions=(
            "iam.dashboard.read",
            "iam.dashboard.create",
            "iam.dashboard.update",
            "iam.dashboard.delete",
        ),
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
        code="iam.user.full",
        name="IAM Users – Manage",
        system="iam",
        resource="user",
        permissions=(
            "iam.user.read",
            "iam.user.create",
            "iam.user.update",
            "iam.user.delete",
            # "iam.user.update_role",
            # "iam.user.update_policy",
            # "iam.user.assign_policy",
            # "iam.user.remove_policy",
            "iam.user.reset_password",
            # no update_dept — dept.admin cannot move users between departments
        ),
    ),

    # --------------------------------------------------
    # Department resource (used by dept roles)
    # --------------------------------------------------
    Policy(
        code="iam.department.read_only",
        name="IAM Departments – Read Only",
        system="iam",
        resource="department",
        permissions=("iam.department.read",),
    ),
    Policy(
        code="iam.department.full",
        name="IAM Departments – Manage",
        system="iam",
        resource="department",
        permissions=(
            "iam.department.read",
            "iam.department.create",
            "iam.department.update",
            "iam.department.delete",
        ),
    ),
    # --------------------------------------------------
    # Approval resource (used by dept roles)
    # --------------------------------------------------
    # Policy(
    #     code="iam.approval.read_only",
    #     name="IAM Approval – Read Only",
    #     system="iam",
    #     resource="approval",
    #     permissions=("iam.approval.read",),
    # ),
    # Policy(
    #     code="iam.approval.full",
    #     name="IAM Approval – Manage",
    #     system="iam",
    #     resource="approval",
    #     permissions=(
    #         "iam.approval.read",
    #         "iam.approval.update",
    #     ),
    # ),
    # --------------------------------------------------
    # Audit log resource (used by dept roles)
    # --------------------------------------------------
    Policy(
        code="iam.audit.read_only",
        name="IAM Audit Logs – Read Only",
        system="iam",
        resource="audit",
        permissions=("iam.audit.read",),
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
