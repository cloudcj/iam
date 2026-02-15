3️⃣ The correct seeding order (this matters)

Always seed top → bottom, never the other way around.

✅ Correct order

1️⃣ Permissions
2️⃣ Roles
3️⃣ Role → Permission links
4️⃣ Departments
5️⃣ Department → Allowed Roles
6️⃣ Users (optional / later)
7️⃣ User → Roles / Department

If you break this order, FK errors or silent bugs happen.

