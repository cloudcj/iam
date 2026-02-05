from seeder.constants.role_constants import RoleCodes


# Roles that bypass department scoping
GLOBAL_ROLES = {
    RoleCodes.SUPER_ADMIN,
    RoleCodes.GLOBAL_VIEWER
}
