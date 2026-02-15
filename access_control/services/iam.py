from .schema import System, Resource, Action


IAM_SERVICE = System(
    name="iam",
    label="IAM",
    resources={
        "user": Resource(
            name="user",
            label="Users",
            actions={
                "read": Action("read", "iam.user.read"),
                "create": Action("create", "iam.user.create"),
                "update": Action("update", "iam.user.update"),
                "delete": Action("delete", "iam.user.delete"),
                "assign_role": Action(
                    "assign_role",
                    "iam.user.assign_role",
                ),
            },
        ),
    },
)
