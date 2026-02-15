from .schema import System, Resource, Action


INVENTORY_SERVICE = System(
    name="inventory",
    label="Inventory",
    resources={
        "region": Resource(
            name="region",
            label="Regions",
            actions={
                "read": Action("read", "inventory.region.read"),
                "create": Action("create", "inventory.region.create"),
                "update": Action("update", "inventory.region.update"),
                "delete": Action("delete", "inventory.region.delete"),
            },
        ),
        "az": Resource(
            name="az",
            label="Availability Zones",
            actions={
                "read": Action("read", "inventory.az.read"),
                "create": Action("create", "inventory.az.create"),
                "update": Action("update", "inventory.az.update"),
                "delete": Action("delete", "inventory.az.delete"),
            },
        ),
        "device": Resource(
            name="device",
            label="Devices",
            actions={
                "read": Action("read", "inventory.device.read"),
                "create": Action("create", "inventory.device.create"),
                "update": Action("update", "inventory.device.update"),
                "delete": Action("delete", "inventory.device.delete"),
            },
        ),
    },
)
