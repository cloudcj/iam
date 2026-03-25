from .schema import Department

_DEPARTMENTS = [
    Department(
        code="GLOBAL",
        name="Global",
        allowed_systems=("tropos","ghidora"),
    ),
    Department(
        code="CLOUD_PLATFORM",
        name="Cloud Platform",
        allowed_systems=("tropos",),
    ),
    Department(
        code="CLOUD_SOLUTIONS",
        name="Cloud Solutions",
        allowed_systems=("tropos",),
    ),
    Department(
        code="CLOUD_MONITORING",
        name="Cloud Monitoring",
        allowed_systems=("ghidora",),
    ),
]

DEPARTMENTS = {d.code: d for d in _DEPARTMENTS}


##########################################################

# DEPARTMENTS = {
#     "GLOBAL": Department(
#         code="GLOBAL",
#         name="Global",
#         allowed_systems=("iam", "inventory"),  # add systems as you expand
#     ),

#     "CLOUD_PLATFORM": Department(
#         code="CLOUD_PLATFORM",
#         name="Cloud Platform",
#         allowed_systems=("iam", "inventory"),

#     ),

#     "CLOUD_SOLUTIONS": Department(
#         code="CLOUD_SOLUTIONS",
#         name="Cloud Solutions",
#         allowed_systems=("inventory",),
#     ),

#     "CLOUD_MONITORING": Department(
#         code="CLOUD_MONITORING",
#         name="Cloud Monitoring",
#         allowed_systems=("inventory",),
#     ),
# }

##########################################################

# DEPARTMENTS = {
#     "CLOUD_PLATFORM": Department(
#         name="CLOUD_PLATFORM",
#         label="Cloud Platform",
#         allowed_roles=(
#             "iam.admin",
#             "inventory.admin",
#             "inventory.viewer"
#             # "pleco.admin",
#         ),
#     ),

#     "CLOUD_SOLUTIONS": Department(
#         name="CLOUD_SOLUTIONS",
#         label="Cloud Solutions",
#         allowed_roles=(
#             "inventory.viewer",
#         ),
#     ),

#     "CLOUD_MONITORING": Department(
#         name="CLOUD_MONITORING",
#         label="Cloud Monitoring",
#         allowed_roles=(
#             "inventory.admin",
#         ),
#     ),
# }


# "GLOBAL": Department(
#     name="GLOBAL",
#     label="Global",
#     allowed_roles=(
#         "iam.admin",
#         "inventory.admin",
#         "inventory.viewer",
#         "monitoring.admin",
#         ...
#     )
# )
