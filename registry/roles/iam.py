from .schema import Role

# _ROLES = [
#     Role(
#         code="iam.viewer",
#         name="IAM – Viewer",
#         policies=("iam.user.operator",),
#     ),
#     Role(
#         code="iam.admin",
#         name="IAM – Admin",
#         policies=("iam.user.admin",),
#     ),
# ]

# IAM_ROLES = {r.code: r for r in _ROLES}
###############################################################

from .schema import Role

_ROLES = [
    Role(
        code="dept.viewer",
        name="Department Viewer",
        policies=("iam.user.read_only",),
    ),
    Role(
        code="dept.admin",
        name="Department Admin",
        policies=("iam.user.manage",),
    ),
]

IAM_ROLES = {r.code: r for r in _ROLES}

###############################################################
# IAM_ROLES = {
#     "iam.viewer": Role(
#         code="iam.viewer",
#         name="IAM – Viewer",
#         policies=("iam.user.operator",),
#     ),

#     "iam.admin": Role(
#         code="iam.admin",
#         name="IAM – Admin",
#         policies=("iam.user.admin",),
#     ),
# }


