class IAMPermissions:
    USER_READ          = "iam.user.read"
    USER_CREATE        = "iam.user.create"
    USER_UPDATE        = "iam.user.update"
    USER_DELETE        = "iam.user.delete"
    USER_UPDATE_ROLE   = "iam.user.update_role"
    USER_UPDATE_POLICY = "iam.user.update_policy"
    # USER_UPDATE_DEPT   = "iam.user.update_dept"
    USER_RESET_PASSWORD = "iam.user.reset_password"

    DEPARTMENT_READ    = "iam.department.read"
    DEPARTMENT_CREATE  = "iam.department.create"
    DEPARTMENT_UPDATE  = "iam.department.update"
    DEPARTMENT_DELETE  = "iam.department.delete"

    AUDIT_READ = "iam.audit.read"
