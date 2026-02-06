psql -U postgres postgres

DROP DATABASE testing;
CREATE DATABASE testing;


================================================






## Check permissions of a role (MOST IMPORTANT)
### By role name

SELECT
    r.name  AS role,
    p.code  AS permission
FROM iam_role_permissions rp
JOIN iam_role r
    ON r.id = rp.role_id
JOIN iam_permission p
    ON p.id = rp.permission_id
WHERE r.name = 'inventory_admin'
ORDER BY p.code;

### BY role UUID

SELECT
    r.id    AS role_id,
    r.name  AS role,
    p.id    AS permission_id,
    p.code  AS permission
FROM iam_role_permissions rp
JOIN iam_role r
    ON r.id = rp.role_id
JOIN iam_permission p
    ON p.id = rp.permission_id
WHERE r.id = '87af0e6d-1e30-4224-8c82-cd7a69edfa91';



## List all roles with their permissions

SELECT
    r.name AS role,
    ARRAY_AGG(p.code ORDER BY p.code) AS permissions
FROM iam_role r
JOIN iam_role_permissions rp
    ON rp.role_id = r.id
JOIN iam_permission p
    ON p.id = rp.permission_id
GROUP BY r.name
ORDER BY r.name;


## Check what roles a user has

SELECT
    u.username,
    r.name AS role
FROM iam_user_role ur
JOIN iam_user u
    ON u.id = ur.user_id
JOIN iam_role r
    ON r.id = ur.role_id
WHERE u.username = 'alice';




## Department → Allowed Roles validation (ADMIN SIDE)

SELECT
    d.name AS department,
    r.name AS allowed_role
FROM iam_department_allowed_role dar
JOIN iam_department d
    ON d.id = dar.department_id
JOIN iam_role r
    ON r.id = dar.role_id
WHERE d.name = 'Inventory Operations';


## Check effective permissions of a user (REAL access)

SELECT DISTINCT permission
FROM (
    -- permissions via roles
    SELECT p.code AS permission
    FROM iam_user u
    JOIN iam_user_role ur
        ON ur.user_id = u.id
    JOIN iam_role_permissions rp
        ON rp.role_id = ur.role_id
    JOIN iam_permission p
        ON p.id = rp.permission_id
    WHERE u.username = 'cj'

    UNION

    -- direct user permissions
    SELECT p.code
    FROM iam_user u
    JOIN iam_user_user_permissions up
        ON up.user_id = u.id
    JOIN iam_permission p
        ON p.id = up.permission_id
    WHERE u.username = 'cj'
) perms
ORDER BY permission;




============================

from iam.services.users import create_user, assign_department
from iam.services.assignments import assign_role_to_user

# 1. Create user
user = create_user(
    username="moni",
    email="moni@gaia.io",
    password="TempPass123",
)

# 2. Assign department
assign_department(
    user=user,
    department_code="SECURITY",
)

# 3. Assign role (validated)
assign_role_to_user(
    user=user,
    role_name="SecurityAuditor",
)