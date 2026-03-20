from .inventory import INVENTORY_ROLES
from .iam import IAM_ROLES
from .global_roles import GLOBAL_ROLES


ROLES_REGISTRY = {
    **INVENTORY_ROLES,
    **IAM_ROLES,
    **GLOBAL_ROLES
}
