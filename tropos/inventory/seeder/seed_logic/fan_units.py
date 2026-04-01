import random
from inventory.assets.models import Device, FanUnit

def run():
    devices = Device.objects.all()
    if not devices.exists():
        print("⚠️ No devices found. Please seed devices first.")
        return

    print("🚀 Seeding Fan Units...")

    fan_map = {
        "firewall": {"fan_count": 6, "is_internal": False},
        "core": {"fan_count": 2, "is_internal": True},
        "analyzer": {"fan_count": 5, "is_internal": True},
        "manager": {"fan_count": 2, "is_internal": True},
        "router": {"fan_count": 2, "is_internal": False},
        "anti-ddos": {"fan_count": 1, "is_internal": False},
        "server": {"fan_count": 6, "is_internal": True},
        "switch": {"fan_count": 2, "is_internal": True},
    }

    total_seeded = 0
    skipped = 0

    for device in devices:
        # ✅ safely handle devices without appliance
        appliance = getattr(device, "appliance", None)
        if appliance is None:
            skipped += 1
            continue

        appliance_name = getattr(appliance, "name", "")
        if not appliance_name:
            skipped += 1
            continue

        appliance_name = appliance_name.lower()
        fan_data = fan_map.get(appliance_name)

        if not fan_data:
            skipped += 1
            continue

        # Create the fan unit entry
        FanUnit.objects.create(
            device=device,
            fan_count=fan_data["fan_count"],
            fan_speed=random.choice([2800, 3200, 3600, 4000]),
            is_internal=fan_data["is_internal"],
            wattage_max_output=random.choice([30, 45, 60]),
            wattage_average=random.uniform(20, 50),
            description=f"{'Internal' if fan_data['is_internal'] else 'External'} fan unit for {appliance_name.capitalize()}",
        )

        print(
            f"✅ Seeded {appliance_name.capitalize()} "
            f"({device}) with {fan_data['fan_count']} "
            f"{'internal' if fan_data['is_internal'] else 'external'} fan(s)."
        )
        total_seeded += 1

    print(f"\n🎉 Fan seeding complete! Total fans seeded: {total_seeded}")
    print(f"⏭️ Skipped {skipped} devices without appliances.")
