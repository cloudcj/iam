# from .schema import System, Resource, Action


# IAM_SERVICE = System(
#     name="iam",
#     label="IAM",
#     resources={
#         "user": Resource(
#             name="user",
#             label="Users",
#             actions={
#                 "read": Action("read", "iam.user.read"),
#                 "create": Action("create", "iam.user.create"),
#                 "update": Action("update", "iam.user.update"),
#                 "delete": Action("delete", "iam.user.delete"),
#                 "assign_role": Action(
#                     "assign_role",
#                     "iam.user.assign_role",
#                 ),
#             },
#         ),
#     },
# )


from .schema import make_system


# IAM_SERVICE = make_system(
#     name="iam",
#     label="IAM",
#     resources={
#         "user": ("Users", [
#             "read",
#             "create",
#             "update",
#             "delete",
#             "update_role",
#             "update_policy",
#             "update_dept",
#         ]),
#     },
# )

from .schema import make_system

IAM_SERVICE = make_system(
    name="iam",
    label="IAM",
    resources={
        "user": ("Users", [
            "read",
            "create",
            "update",
            "delete",
            "update_role",
            "update_policy",
            "update_dept",
            "assign_policy",
            "remove_policy",
        ]),
        "department": ("Departments", [
            "read",
            "update_systems",
        ]),
    },
)



# IAM_SERVICE = make_system(
#     name="iam",
#     label="IAM",
#     resources={
#         "user": ("Users", ["read", "create", "update", "delete", "assign_role"]),
#     },
# )