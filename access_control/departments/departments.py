from .schema import Department


DEPARTMENTS = {
    "CLOUD_PLATFORM": Department(
        name="CLOUD_PLATFORM",
        label="Cloud Platform",
        allowed_roles=(
            "iam.admin",
            "inventory.admin",
            "inventory.viewer"
            # "pleco.admin",
        ),
    ),

    "CLOUD_SOLUTIONS": Department(
        name="CLOUD_SOLUTIONS",
        label="Cloud Solutions",
        allowed_roles=(
            "inventory.viewer",
        ),
    ),

    "CLOUD_MONITORING": Department(
        name="CLOUD_MONITORING",
        label="Cloud Monitoring",
        allowed_roles=(
            "inventory.admin",
        ),
    ),
}

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
