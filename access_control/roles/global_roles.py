# permissions/policies/global.py
from .schema import Role


# permissions/roles/global.py
GLOBAL_ROLES = {
    "global.readonly": Role(
        code="global.readonly",
        label="Global Viewer",
        policies=("global.viewer",),
    )
}
