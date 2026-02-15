# permissions/policies/iam.py
from .schema import Policy


IAM_POLICIES = {
    "iam.user.operator": Policy(
        code="iam.user.operator",
        label="User – Read, Create & Update",
        system="iam",
        resource="user",
        permissions=(
            "iam.user.read",
            "iam.user.create",
            "iam.user.update",
        ),
    ),

    "iam.user.admin": Policy(
        code="iam.user.admin",
        label="User – Full Access",
        system="iam",
        resource="user",
        permissions=(
            "iam.user.read",
            "iam.user.create",
            "iam.user.update",
            "iam.user.delete",
        ),
    ),
}
