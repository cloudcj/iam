#### QUERY CHECKING ######

## 1️⃣ Verify permissions exist

This confirms permissions is solid.

    SELECT code, description
    FROM iam_permission
    ORDER BY code;

You should see things like:

    inventory.az.read
    inventory.az.create
    iam.user.read
    ...


## 2️⃣ Verify roles exist

This confirms step 2 (roles).

    SELECT code, name
    FROM iam_role
    ORDER BY code;

Expected example:

    iam.admin        | IAM – Admin
    inventory.admin  | Inventory – Admin
    inventory.viewer | Inventory – Viewer
    pleco.admin      | PLECO – Admin


## 3️⃣ Verify role → permission mapping (MOST IMPORTANT)

This confirms flattened access, which is what runtime uses.

    SELECT
        r.code  AS role_code,
        p.code  AS permission_code
    FROM iam_role_permission rp
    JOIN iam_role r ON r.id = rp.role_id
    JOIN iam_permission p ON p.id = rp.permission_id
    ORDER BY r.code, p.code;

Example expected result:

    iam.admin → iam.user.read
    iam.admin → iam.user.create
    iam.admin → iam.user.update
    iam.admin → iam.user.delete

    inventory.viewer → inventory.az.read
    inventory.viewer → inventory.device.read


## 4️⃣ Verify departments exist

This confirms step 4 (deparatments)

    SELECT code, name
    FROM iam_department
    ORDER BY code;

Expected:

    CLOUD_PLATFORM   | Cloud Platform
    CLOUD_SOLUTIONS  | Cloud Solutions
    CLOUD_MONITORING | Cloud Monitoring

## 5️⃣ Verify department → allowed roles

This confirms governance rules are enforced correctly.

    SELECT
        d.code AS department,
        r.code AS allowed_role
    FROM iam_department_allowed_role dar
    JOIN iam_department d ON d.id = dar.department_id
    JOIN iam_role r ON r.id = dar.role_id
    ORDER BY d.code, r.code;

Expected:

    CLOUD_PLATFORM  → iam.admin
    CLOUD_PLATFORM  → inventory.admin
    CLOUD_PLATFORM  → pleco.admin

    CLOUD_SOLUTIONS → inventory.viewer
    CLOUD_SOLUTIONS → pleco.viewer

## 6️⃣ (Optional but powerful) End-to-end access check query

This simulates user.has_permission() in SQL.

Replace values:

- 'USER_UUID_HERE'
- 'inventory.az.read'

    SELECT EXISTS (
        SELECT 1
        FROM iam_user u
        JOIN iam_user_role ur ON ur.user_id = u.id
        JOIN iam_role r ON r.id = ur.role_id
        JOIN iam_role_permission rp ON rp.role_id = r.id
        JOIN iam_permission p ON p.id = rp.permission_id
        WHERE u.id = 'USER_UUID_HERE'
        AND p.code = 'inventory.az.read'
    ) AS has_permission;

Result:

    true

or

    false

👉 This query is exactly what your future user.has_permission() will do.