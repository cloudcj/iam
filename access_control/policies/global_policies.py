from .schema import Policy


GLOBAL_POLICIES = {
    "global.viewer": Policy(
        code="global.viewer",
        label="Global Viewer",
        system="global",
        resource="viewer",
        permissions=(
            "inventory.az.read",
            "inventory.device.read",
            # "pleco.resource.read",
            # add more read-only permissions as needed
        ),
    ),
}
