# permissions/policies/iam.py
from .schema import Policy

from .schema import Policy

_POLICIES = [
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
    Policy(
        code="iam.full",
        name="User – Read, Create & Update",
        system="iam",
        resource="user",
        permissions=(
            "iam.user.read",
            "iam.user.create",
            "iam.user.update",
        ),
    ),
    Policy(
        code="iam.user.admin",
        name="User – Full Access",
        system="iam",
        resource="user",
        permissions=(
            "iam.user.read",
            "iam.user.create",
            "iam.user.update",
            "iam.user.delete",
        ),
    ),
]

IAM_POLICIES = {p.code: p for p in _POLICIES}


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
