from .tropos import TROPOS_ROLES
from .iam import IAM_ROLES
from .global_roles import GLOBAL_ROLES
from .ghidora import GHIDORA_ROLES

ROLES_REGISTRY = {
    **TROPOS_ROLES,
    **IAM_ROLES,
    **GHIDORA_ROLES,
    **GLOBAL_ROLES

}
