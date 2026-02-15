from .schema import Role


IAM_ROLES = {
    "iam.viewer": Role(
        code="iam.viewer",
        label="IAM – Viewer",
        policies=("iam.user.operator",),
    ),

    "iam.admin": Role(
        code="iam.admin",
        label="IAM – Admin",
        policies=("iam.user.admin",),
    ),
}


