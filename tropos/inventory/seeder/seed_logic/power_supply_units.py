from inventory.assets.models import PowerSupplyUnit, Device
from django.db import transaction

# PSU count mapping based on appliance or role name
PSU_COUNTS = {
    "firewall": 8,
    "core": 4,
    "analyzer": 2,
    "manager": 1,
    "router": 2,
    "anti-ddos": 2,
    "server": 2,
    "switch": 2,
}

# PSU data defaults
PSU_DATA_TEMPLATE = {
    "heat_dissipation": 35.5,
    "max_output": 750,
    "average_output": 650,
    "wattage_percentage": 85.0,
    "power_type": "AC",
    "connector_type": "C14",
    "description": "High-efficiency redundant PSU",
}


@transaction.atomic
def run():
    print("🚀 Seeding Power Supply Units...")

    devices = Device.objects.all()
    if not devices.exists():
        raise ValueError("❌ No devices found. Please seed devices first.")

    created_count = 0

    for device in devices:
        # Dynamically get device name from related model (appliance, server, or switch)
        device_name = (
            getattr(getattr(device, "appliance", None), "name", None)
            or getattr(getattr(device, "server", None), "name", None)
            or getattr(getattr(device, "switch", None), "name", None)
            or "Unnamed Device"
        ).lower()

        # Determine PSU count (default to 1 if not mapped)
        psu_count = PSU_COUNTS.get(device_name, 1)

        # Avoid duplicate PSU creation
        if PowerSupplyUnit.objects.filter(device=device).exists():
            continue

        for _ in range(psu_count):
            PowerSupplyUnit.objects.create(
                device=device,
                heat_dissipation=PSU_DATA_TEMPLATE["heat_dissipation"],
                max_output=PSU_DATA_TEMPLATE["max_output"],
                average_output=PSU_DATA_TEMPLATE["average_output"],
                wattage_percentage=PSU_DATA_TEMPLATE["wattage_percentage"],
                power_type=PSU_DATA_TEMPLATE["power_type"],
                connector_type=PSU_DATA_TEMPLATE["connector_type"],
                description=PSU_DATA_TEMPLATE["description"],
            )
            created_count += 1
            print(f"✅ Created PSU for {device_name}")

    print(f"🎉 Successfully seeded {created_count} Power Supply Units.")


def revert():
    deleted_count, _ = PowerSupplyUnit.objects.all().delete()
    print(f"🧹 Deleted {deleted_count} Power Supply Units.")
