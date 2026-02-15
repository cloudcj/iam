## 1️⃣ Permissions (foundation)

Check permissions exist

    SELECT code, description
    FROM iam_permission
    ORDER BY code;

✅ You should see things like:

    iam.user.read
    inventory.az.read
    inventory.az.update

❌ If a permission referenced by a policy is missing → policy seeding must fail (good).

## 2️⃣ Policies (access intent)

    SELECT code, label, service, resource
    FROM iam_policy
    ORDER BY code;

✅ You should see:

    inventory.az.read_only
    inventory.az.read_update
    inventory.az.full
    iam.user.operator
    iam.user.admin
    global.viewer

## 3️⃣ Policy → Permission mapping (policy meaning)
Inspect what each policy expands to

    SELECT
        p.code AS policy,
        perm.code AS permission
    FROM iam_policy_permission pp
    JOIN iam_policy p ON p.id = pp.policy_id
    JOIN iam_permission perm ON perm.id = pp.permission_id
    ORDER BY p.code, perm.code;

✅ Example expected output:

    inventory.az.read_only  → inventory.az.read
    inventory.az.read_update → inventory.az.read
    inventory.az.read_update → inventory.az.update
    inventory.az.full       → inventory.az.create
    inventory.az.full       → inventory.az.delete

If this is wrong → policy registry or policy-permission seeder is wrong.

## 4️⃣ Roles

Check roles exist

    SELECT code, name
    FROM iam_role
    ORDER BY code;

✅ Example:

    iam.viewer   | IAM – Viewer
    iam.admin    | IAM – Admin
    inventory.viewer
    inventory.admin

## 5️⃣ Role → Policy mapping (intent assignment)

Which roles have which policies

    SELECT
        r.code   AS role,
        p.code   AS policy
    FROM iam_role_policy rp
    JOIN iam_role r ON r.id = rp.role_id
    JOIN iam_policy p ON p.id = rp.policy_id
    ORDER BY r.code, p.code;

✅ Example:

    iam.viewer  → iam.user.operator
    iam.admin   → iam.user.admin
    inventory.admin → inventory.az.full

If a role has no rows here, it has no access intent.

## 6️⃣ Role → Permission mapping (🔥 runtime truth 🔥)

This is the most important table.

What permissions does each role REALLY have?

    SELECT
        r.code   AS role,
        perm.code AS permission
    FROM iam_role_permission rp
    JOIN iam_role r ON r.id = rp.role_id
    JOIN iam_permission perm ON perm.id = rp.permission_id
    ORDER BY r.code, perm.code;

✅ This must reflect policy expansion.

Example:

    iam.admin → iam.user.read
    iam.admin → iam.user.create
    iam.admin → iam.user.update
    iam.admin → iam.user.delete

If this table is empty or wrong:

❌ seed_role_permissions is wrong
❌ runtime auth will FAIL

## 7️⃣ Departments

Check departments

    SELECT code, name
    FROM iam_department
    ORDER BY code;

## 8️⃣ Department → Allowed roles (structural constraint)

    SELECT
        d.code AS department,
        r.code AS allowed_role
    FROM iam_department_allowed_role dar
    JOIN iam_department d ON d.id = dar.department_id
    JOIN iam_role r ON r.id = dar.role_id
    ORDER BY d.code, r.code;

✅ Example:

    CLOUD_PLATFORM → iam.admin
    CLOUD_PLATFORM → inventory.admin

This table is not used at runtime, only for validation.

## 9️⃣ Users & effective access (ultimate test)

Check users

    SELECT id, username, is_superuser
    FROM iam_user;


## Check what permissions a user actually has
Replace 'SuperAdmin' with any username:

    SELECT DISTINCT
        u.username,
        perm.code AS permission
    FROM iam_user u
    JOIN iam_user_role ur ON ur.user_id = u.id
    JOIN iam_role r ON r.id = ur.role_id
    JOIN iam_role_permission rp ON rp.role_id = r.id
    JOIN iam_permission perm ON perm.id = rp.permission_id
    WHERE u.username = 'SuperAdmin'
    ORDER BY perm.code;

✅ This must match what user.has_permission() returns in Django.

## 🔟 One-liner sanity checks (quick)
Any role without permissions? (bad)

    SELECT r.code
    FROM iam_role r
    LEFT JOIN iam_role_permission rp ON rp.role_id = r.id
    WHERE rp.id IS NULL;

Should return 0 rows (unless intentional).

Any policy without permissions? (bad)

    SELECT p.code
    FROM iam_policy p
    LEFT JOIN iam_policy_permission pp ON pp.policy_id = p.id
    WHERE pp.id IS NULL;


# For checking user

## 1️⃣ Check a user’s department

    SELECT
        u.username,
        d.code   AS department_code,
        d.name   AS department_name
    FROM iam_user u
    JOIN department_department d
    ON d.id = u.department_id
    WHERE u.username = 'alice';

## 2️⃣ Check roles assigned to a user

    SELECT
        u.username,
        r.code  AS role_code,
        r.name  AS role_name
    FROM iam_user u
    JOIN iam_user_role ur
    ON ur.user_id = u.id
    JOIN iam_role r
    ON r.id = ur.role_id
    WHERE u.username = 'alice';

## 3️⃣ Check policies granted via roles

    SELECT DISTINCT
        u.username,
        r.code     AS role_code,
        p.code     AS policy_code,
        p.label    AS policy_label
    FROM iam_user u
    JOIN iam_user_role ur
    ON ur.user_id = u.id
    JOIN iam_role r
    ON r.id = ur.role_id
    JOIN iam_role_policy rp
    ON rp.role_id = r.id
    JOIN iam_policy p
    ON p.id = rp.policy_id
    WHERE u.username = 'alice'
    ORDER BY r.code, p.code;

## 4️⃣ Check ALL policies a user effectively has
(roles + direct policies if you add those later)

    SELECT DISTINCT
        u.username,
        p.code   AS policy_code,
        p.label
    FROM iam_user u
    JOIN iam_user_role ur
    ON ur.user_id = u.id
    JOIN iam_role_policy rp
    ON rp.role_id = ur.role_id
    JOIN iam_policy p
    ON p.id = rp.policy_id
    WHERE u.username = 'alice'
    ORDER BY p.code;

## 5️⃣ Check permissions granted by policies

    SELECT DISTINCT
        u.username,
        p.code       AS policy_code,
        perm.code    AS permission_code
    FROM iam_user u
    JOIN iam_user_role ur
    ON ur.user_id = u.id
    JOIN iam_role_policy rp
    ON rp.role_id = ur.role_id
    JOIN iam_policy p
    ON p.id = rp.policy_id
    JOIN iam_policy_permission pp
    ON pp.policy_id = p.id
    JOIN iam_permission perm
    ON perm.id = pp.permission_id
    WHERE u.username = 'alice'
    ORDER BY perm.code;

This should match what user.has_permission() returns.

## 6️⃣ One-shot “what can this user do?”
6️⃣ One-shot “what can this user do?”

    SELECT DISTINCT
        perm.code AS effective_permission
    FROM iam_user u
    JOIN iam_user_role ur
    ON ur.user_id = u.id
    JOIN iam_role_policy rp
    ON rp.role_id = ur.role_id
    JOIN iam_policy_permission pp
    ON pp.policy_id = rp.policy_id
    JOIN iam_permission perm
    ON perm.id = pp.permission_id
    WHERE u.username = 'alice'
    ORDER BY perm.code;

## 7️⃣ Sanity checks (HIGHLY recommended)

Users with NO access (should be ZERO)

    SELECT u.username
    FROM iam_user u
    LEFT JOIN iam_user_role ur ON ur.user_id = u.id
    WHERE ur.id IS NULL;

## Roles with no policies (bad role)

    SELECT r.code
    FROM iam_role r
    LEFT JOIN iam_role_policy rp ON rp.role_id = r.id
    WHERE rp.id IS NULL;

## Policies with no permissions (broken policy)

    SELECT p.code
    FROM iam_policy p
    LEFT JOIN iam_policy_permission pp ON pp.policy_id = p.id
    WHERE pp.id IS NULL;

## to check what permissions does a user have 

    -- Effective permissions for a user (roles + direct policies)
    SELECT DISTINCT perm.code AS effective_permission
    FROM iam_user u

    -- via roles
    LEFT JOIN iam_user_role ur
    ON ur.user_id = u.id
    LEFT JOIN iam_role_policy rp
    ON rp.role_id = ur.role_id
    LEFT JOIN iam_policy_permission rpp
    ON rpp.policy_id = rp.policy_id

    -- via direct user policies
    LEFT JOIN iam_user_policy up
    ON up.user_id = u.id
    LEFT JOIN iam_policy_permission upp
    ON upp.policy_id = up.policy_id

    JOIN iam_permission perm
    ON perm.id = COALESCE(rpp.permission_id, upp.permission_id)

    WHERE u.username = 'bob'
    ORDER BY perm.code;


    I strongly recommend this one for debugging:


        -- Permissions via roles
    SELECT DISTINCT perm.code
    FROM iam_user u
    JOIN iam_user_role ur ON ur.user_id = u.id
    JOIN iam_role_policy rp ON rp.role_id = ur.role_id
    JOIN iam_policy_permission pp ON pp.policy_id = rp.policy_id
    JOIN iam_permission perm ON perm.id = pp.permission_id
    WHERE u.username = 'bob'

    UNION

    -- Permissions via direct user policies
    SELECT DISTINCT perm.code
    FROM iam_user u
    JOIN iam_user_policy up ON up.user_id = u.id
    JOIN iam_policy_permission pp ON pp.policy_id = up.policy_id
    JOIN iam_permission perm ON perm.id = pp.permission_id
    WHERE u.username = 'bob'

    ORDER BY code;

