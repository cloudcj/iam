# from apps.common.constants.role_codes import RoleCodes

# HIDDEN_FROM_IAM_ADMIN = {
#     RoleCodes.IAM_ADMIN,
#     RoleCodes.GLOBAL_READONLY,
# }


from apps.common.constants.role_codes import RoleCodes

HIDDEN_FROM_PLATFORM_ADMIN = {
    RoleCodes.PLATFORM_ADMIN,
    RoleCodes.PLATFORM_VIEWER,
}

HIDDEN_FROM_DEPARTMENT_ADMIN = {
    RoleCodes.PLATFORM_ADMIN,
    RoleCodes.PLATFORM_VIEWER,
    RoleCodes.DEPT_ADMIN,
    RoleCodes.DEPT_VIEWER,
}

# Roles that are not tied to any system — exempt from allowed_systems check
MANAGEMENT_ROLES = {
    RoleCodes.PLATFORM_ADMIN,
    RoleCodes.PLATFORM_VIEWER,
    RoleCodes.DEPT_ADMIN,
    RoleCodes.DEPT_VIEWER,
}