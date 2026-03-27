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
        system="ghidora",
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
    # Dashboard resource
    # --------------------------------------------------
    Policy(
        code="ghidora.dashboard.read_only",
        name="Dashboard – Read Only",
        system="ghidora",
        resource="dashboard",
        permissions=(
            "ghidora.dashboard.read",
        ),
    ),
    Policy(
        code="ghidora.dashboard.full",
        name="Dashboard – Full access",
        system="ghidora",
        resource="dashboard",
        permissions=(
            "ghidora.dashboard.read",
            "ghidora.dashboard.create",
            "ghidora.dashboard.update",
            "ghidora.dashboard.delete",
        ),
    ),

    # --------------------------------------------------
    # Approval resource
    # --------------------------------------------------
    Policy(
        code="ghidora.approval.read_only",
        name="Approval – Read Only",
        system="ghidora",
        resource="approval",
        permissions=(
            "ghidora.approval.read",
        ),
    ),
    Policy(
        code="ghidora.approval.full",
        name="Approval – Full access",
        system="ghidora",
        resource="approval",
        permissions=(
            "ghidora.approval.read",
            "ghidora.approval.update",
        ),
    ),
]

GHIDORA_POLICIES = {p.code: p for p in _POLICIES}