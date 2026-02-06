# Identity & User Management

## All identity-related operations are handled under:

    /api/identity/


## Create User

    POST /api/identity/users/

Creates a new user account.


## List Users

    GET /api/identity/users/list/

Returns a list of users.

## Update User Basic Info

    PUT /api/identity/users/{user_id}/basic/

Updates basic user details (e.g., name, email).

## Update User Roles

    PUT /api/identity/users/{user_id}/roles/

Assigns or updates user roles.

## Update User Department

    PUT /api/identity/users/{user_id}/department/

Assigns a user to a department.

## Delete User

    DELETE /api/identity/users/{user_id}/delete/

Deletes a user account.