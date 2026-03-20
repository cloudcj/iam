# from apps.common.constants.role_codes import RoleCodes

# HIDDEN_FROM_IAM_ADMIN = {
#     RoleCodes.IAM_ADMIN,
#     RoleCodes.GLOBAL_READONLY,
# }


from apps.common.constants.role_codes import RoleCodes

HIDDEN_FROM_IAM_ADMIN = {
    RoleCodes.PLATFORM_ADMIN,
    RoleCodes.PLATFORM_VIEWER,
    RoleCodes.DEPT_ADMIN,
    RoleCodes.DEPT_VIEWER,
}
