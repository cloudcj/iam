# permissions/policies/iam.py
from .schema import Policy
from ..helpers import all_permissions_for_service, read_permissions_for_service
from ..systems.ghidora import GHIDORA_SERVICE

_POLICIES = [
    # --------------------------------------------------
    # System-wide (used by platform roles)
    # --------------------------------------------------
    Policy(
        code="ghidora.full",
        name="Ghidora – Full Access",
        system="iam",
        resource="*",
        permissions=all_permissions_for_service(GHIDORA_SERVICE),
        visible_in_ui=False,
    ),
    Policy(
        code="ghidora.read_only",
        name="GHIDORA – Read Only",
        system="ghidora",
        resource="*",
        permissions=read_permissions_for_service(GHIDORA_SERVICE),
        visible_in_ui=False,
    ),

    # --------------------------------------------------
    # User resource (used by dept roles)
    # --------------------------------------------------
    # Policy(
    #     code="iam.user.read_only",
    #     name="IAM Users – Read Only",
    #     system="iam",
    #     resource="user",
    #     permissions=("iam.user.read",),
    # ),
    # Policy(
    #     code="iam.user.manage",
    #     name="IAM Users – Manage",
    #     system="iam",
    #     resource="user",
    #     permissions=(
    #         "iam.user.read",
    #         "iam.user.create",
    #         "iam.user.update",
    #         "iam.user.delete",
    #         "iam.user.update_role",
    #         "iam.user.update_policy",
    #         "iam.user.assign_policy",
    #         "iam.user.remove_policy",
    #         # no update_dept — dept.admin cannot move users between departments
    #     ),
    # ),
]

GHIDORA_POLICIES = {p.code: p for p in _POLICIES}