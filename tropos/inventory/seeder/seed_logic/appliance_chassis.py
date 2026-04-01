# assets/management/commands/seeds/appliance_chasis.py
import random
from inventory.assets.models import ApplianceChasis, Device, Interface

# --------------------------
# Chassis module configuration
# --------------------------
CHASSIS_MODULES_PER_APPLIANCE = 4  # default number of modules per appliance
INTERFACES_PER_MODULE = 2          # default number of interfaces per module
CHASSIS_TYPES = ["Firewall", "Anti-DDoS"]  # Only these appliance types get chassis modules

# --------------------------
# Seeder Run
# --------------------------
def run():
    print("🚀 Seeding appliance chassis modules...")

    # Filter only devices linked to appliances that are chasis type
    for appliance_device in Device.objects.filter(appliance__appliance_type__name__in=CHASSIS_TYPES):
        appliance_name = appliance_device.appliance.appliance_type.name
        print(f"🔹 Seeding modules for appliance '{appliance_name}' device ID {appliance_device.id}...")

        for slot_position in range(1, CHASSIS_MODULES_PER_APPLIANCE + 1):
            module_name = f"Module-{slot_position}"
            serial_number = f"{appliance_name[:3].upper()}-MOD-{slot_position}-{random.randint(1000,9999)}"

            # Create chassis module
            module, created = ApplianceChasis.objects.get_or_create(
                device=appliance_device,
                slot_position=slot_position,
                defaults={
                    "module_name": module_name,
                    "serial_number": serial_number,
                    "is_occupied": True,
                    "description": f"{module_name} for {appliance_name}",
                }
            )

            # Create interfaces for this module
            for i in range(1, INTERFACES_PER_MODULE + 1):
                Interface.objects.get_or_create(
                    device=appliance_device,
                    interface_number=i,
                    defaults={
                        "to_location": "",
                        "cable_type": "copper",
                        "port_type": "RJ45",
                        "description": f"Interface {i} for {module_name}",
                    },
                )

            print(f"✅ Created {module_name} with {INTERFACES_PER_MODULE} interfaces for '{appliance_name}' (Device ID {appliance_device.id})")

    print("🎉 Appliance chassis seeding complete!")


# --------------------------
# Seeder Revert
# --------------------------
def revert():
    print("🧹 Reverting appliance chassis modules...")
    for module in ApplianceChasis.objects.all():
        # Delete interfaces for the device
        Interface.objects.filter(device=module.device).delete()
        module.delete()
    print("✅ Appliance chassis modules reverted successfully.")
