import random
from django.db import transaction
from inventory.infrastructure.models import Pod, Rack
from inventory.assets.models import Device, Appliance, MemoryUnit, ProcessorUnit, StorageUnit, Interface, ApplianceChassis
from inventory.enums.models import ApplianceType, StorageInterface, StorageFormFactor, ProcessorBrand, ProcessorCodename, ProcessorTier, ProcessorModel
from ..seed_data import appliances_data
from .seed_helpers.compute_units_helpers import create_processor_unit,create_memory_unit,create_storage_unit
from .seed_helpers.rack_allocation_helper import allocate_rack_positions



@transaction.atomic
def run():
    print("🚀 Seeding appliances...")

    # Preload everything (DB performance optimization)
    pods = {p.name: p for p in Pod.objects.all()}
    racks = {(r.pod_id, r.number): r for r in Rack.objects.all()}

    for data in appliances_data:

        pod_name = data["pod_name"]
        rack_number = str(data["rack_number"])

        # --- Get Pod ---
        pod = pods.get(pod_name)
        if not pod:
            raise ValueError(f"❌ Pod '{pod_name}' not found")

        # --- Get Rack ---
        rack = racks.get((pod.id, rack_number))
        if not rack:
            raise ValueError(
                f"❌ Rack '{rack_number}' not found inside Pod '{pod_name}'"
            )
        # --- Create Device ---
        device = Device.objects.create(
            rack=rack,
            type=data["type"],
            name=data["name"],
            serial_number=data.get("serial_number"),
            model=data["model"],
            rack_unit_allocations=data["rack_alloc"],
            starting_position=data["starting_position"],
            ipv4_address=data["ipv4_address"],
            description=data.get("description", ""),
            interface_count=data.get("interface_count", 4),
            power=data.get("power"),
            weight=data.get("weight"),
        )

        # --- Allocate Rack Positions ---
        allocate_rack_positions(
            rack=rack,
            start=data["starting_position"],
            size=data["rack_alloc"],
            device=device,
            # device_label=data["appliance_name"],
        )

        # Create Appliance
        appliance_type_obj, _ = ApplianceType.objects.get_or_create(name=data["appliance_type"])
        appliance_obj = Appliance.objects.create(
            device=device,
            appliance_type=appliance_type_obj,
            # appliance_name=data["appliance_name"],
            is_chassis=data.get("is_chassis", False),
            has_components_units=data.get("has_components_units", False),  # mark this appliance

        )

        # # Seed Memory Units
        # MemoryUnit.objects.bulk_create([
        #     MemoryUnit(device=device, **mu) for mu in appliance.get("memory_units", [])
        # ])

        # # Seed Processor Units with get_or_create
        # for cpu in appliance.get("processors", []):
        #     brand_obj, _ = ProcessorBrand.objects.get_or_create(name=cpu["brand"])
        #     codename_obj, _ = ProcessorCodename.objects.get_or_create(name=cpu["codename"], brand=brand_obj)
        #     tier_obj, _ = ProcessorTier.objects.get_or_create(name=cpu["tier"], brand=brand_obj)
        #     model_obj, _ = ProcessorModel.objects.get_or_create(name=cpu["model"], codename=codename_obj, tier=tier_obj)
        #     ProcessorUnit.objects.create(
        #         device=device,
        #         processor_codename=codename_obj,
        #         processor_tier=tier_obj,
        #         processor_model=model_obj,
        #     )

        # # Seed Storage Units
        # StorageUnit.objects.bulk_create([
        #     StorageUnit(
        #         device=device,
        #         storage_type=su["storage_type"],
        #         storage_capacity=su["storage_capacity"],
        #         storage_count=su["storage_count"],
        #         capacity_unit=su["capacity_unit"],
        #         storage_interface=StorageInterface.objects.get(name=su["storage_interface"]["name"]),
        #         form_factor=StorageFormFactor.objects.get(name=su["form_factor"]["name"]),
        #     ) for su in appliance.get("storage_units", [])
        # ])

        # --- Memory Units ---
        for mem in data.get("memory_units", []):
            create_memory_unit(device, mem)

        # --- Processor Units ---
        for proc in data.get("processors", []):
            create_processor_unit(device, proc)

        # --- Storage Units ---
        for sto in data.get("storage_units", []):
            create_storage_unit(device, sto)


        # Seed Interfaces
        Interface.objects.bulk_create([
            Interface(
                device=device,
                interface_number=i,
                port_type="RJ45",
                cable_type="copper",
                description=f"Interface {i} for {data['name']}",
            ) for i in range(1, data.get("interface_count", 2) + 1)
        ])

        # Seed Chassis Modules
        if data.get("is_chassis", False):
            ApplianceChassis.objects.bulk_create([
                ApplianceChassis(
                    device=device,
                    module_name=f"Module-{slot_position}",
                    serial_number=f"{data['name'][:3].upper()}-MOD-{slot_position}-{random.randint(1000,9999)}",
                    slot_position=slot_position,
                    is_occupied=True,
                    is_chassis=True,
                ) for slot_position in range(1, 5)
            ])

        print(f"✅ Seeded Appliance: {data['name']}")

    print("🎉 Seeding complete!")








# import random
# from inventory.enums.models import (
#     ApplianceType, StorageInterface, StorageFormFactor, ProcessorBrand, ProcessorCodename, ProcessorTier, ProcessorModel
# )
# from inventory.infrastructure.models import Pod, Rack
# from inventory.assets.models import (
#     Device, Appliance, MemoryUnit, ProcessorUnit, StorageUnit, Interface, ApplianceChassis
# )

# appliances_data = [
#     {
#         "appliance_type": "Analyzer",
#         "appliance_name": "Analyzer-01",
#         "serial_number": "SNAN001",
#         "rack_alloc": 4,
#         "rack_start": 15,
#         "description": "Network Analyzer Appliance",
#         "pod_name": "Pod 1",
#         "rack_number": "1",
#         "interface_count": 4,
#         "fan_count": 2,
#         "memory_units": [
#             {"ram_capacity": 16, "quantity": 4},
#             {"ram_capacity": 16, "quantity": 4},
#         ],
#         "processors": [
#             {"brand": "Intel", "codename": "Xeon", "tier": "Silver", "model": "4210"},
#         ],
#         "storage_units": [
#             {
#                 "storage_type": "SSD",
#                 "storage_capacity": 1024,
#                 "storage_count": 2,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},
#                 "form_factor": {"name": "2.5"},
#             }
#         ],
#         "is_chassis": True,
#     },
#     {
#         "appliance_type": "Anti DDoS",
#         "appliance_name": "AntiDDoS-01",
#         "serial_number": "SNADD001",
#         "rack_alloc": 4,
#         "rack_start": 5,
#         "description": "Anti-DDoS Appliance",
#         "pod_name": "Pod 1",
#         "rack_number": "1",
#         "interface_count": 2,
#         "fan_count": 6,
#         "processors": [],
#         "memory_units": [],
#         "storage_units": [],
#         "is_chassis": True,
#     },
# ]

# def run():
#     print("🚀 Seeding appliances...")

#     for appliance in appliances_data:
#         pod = Pod.objects.get(name=appliance["pod_name"])
#         rack = Rack.objects.get(number=str(appliance["rack_number"]), pod=pod)

#         # Create Device
#         device = Device.objects.create(
#             rack=rack,
#             type="appliance",
#             rack_unit_allocations=appliance["rack_alloc"],
#             starting_position=appliance["rack_start"],
#             description=appliance.get("description", ""),
#             interface_count=appliance.get("interface_count", 2),
#             fan_count=appliance.get("fan_count", 2),
#             serial_number=appliance.get("serial_number"),
#         )

#         # Get or create ApplianceType
#         appliance_type_obj, _ = ApplianceType.objects.get_or_create(name=appliance["appliance_type"])

#         # Create Appliance
#         appliance_obj = Appliance.objects.create(
#             device=device,
#             appliance_type=appliance_type_obj,
#             appliance_name=appliance["appliance_name"],
#             is_chassis=appliance.get("is_chassis", False),
#         )

#         # Memory Units
#         for mu in appliance.get("memory_units", []):
#             MemoryUnit.objects.create(device=device, **mu)

#         # Processor Units
#         for cpu in appliance.get("processors", []):
#             brand_obj, _ = ProcessorBrand.objects.get_or_create(name=cpu["brand"])
#             ProcessorUnit.objects.create(
#                 device=device,
#                 processor_codename=ProcessorCodename.objects.get(name=cpu["codename"], brand=brand_obj),
#                 processor_tier=ProcessorTier.objects.get(name=cpu["tier"], brand=brand_obj),
#                 processor_model=ProcessorModel.objects.get(name=cpu["model"]),
#             )

#         # Storage Units
#         for su in appliance.get("storage_units", []):
#             StorageUnit.objects.create(
#                 device=device,
#                 storage_type=su["storage_type"],
#                 storage_capacity=su["storage_capacity"],
#                 storage_count=su["storage_count"],
#                 capacity_unit=su["capacity_unit"],
#                 storage_interface=StorageInterface.objects.get(name=su["storage_interface"]["name"]),
#                 form_factor=StorageFormFactor.objects.get(name=su["form_factor"]["name"]),
#             )

#         # Interfaces
#         for i in range(1, appliance.get("interface_count", 2) + 1):
#             Interface.objects.create(
#                 device=device,
#                 interface_number=i,
#                 port_type="RJ45",
#                 cable_type="copper",
#                 description=f"Interface {i} for {appliance['appliance_name']}",
#             )

#         # Chassis Modules
#         if appliance.get("is_chassis", False):
#             for slot_position in range(1, 5):
#                 ApplianceChassis.objects.create(
#                     device=device,
#                     module_name=f"Module-{slot_position}",
#                     serial_number=f"{appliance['appliance_name'][:3].upper()}-MOD-{slot_position}-{random.randint(1000,9999)}",
#                     slot_position=slot_position,
#                     is_occupied=True,
#                     is_chassis=True,
#                 )

#         print(f"✅ Seeded Appliance: {appliance['appliance_name']}")

#     print("🎉 Seeding complete!")



# import random
# from inventory.enums.models import ApplianceType, StorageType, ProcessorBrand, ProcessorCodename, ProcessorModel, ProcessorTier, CapacityUnit, StorageFormFactor, StorageInterface
# from inventory.infrastructure.models import Pod, Rack, RackPosition
# from inventory.assets.models import (
#     Device,
#     Appliance,
#     FanUnit,
#     StorageUnit,
#     MemoryUnit,
#     ProcessorUnit,
#     Interface,
#     ApplianceChassis,  # ✅ corrected import name
# )
# from inventory.enums.models import StorageType  # ✅ added for TB/GB enum

# # --------------------------
# # Define appliances to seed
# # --------------------------
# appliances_data = [
#     ("appliance", "Firewall", "SN-FW-12345", 4, 24, "Firewall appliance", "Pod 1", "1"),
#     ("appliance", "Core", "SN-CORE-12345", 4, 19, "Core appliance", "Pod 1", "1"),
#     ("appliance", "Analyzer", "SN-AN-22222", 4, 15, "Analyzer appliance", "Pod 1", "1"),
#     ("appliance", "Manager", "SN-MGR-11111", 4, 29, "Manager appliance", "Pod 1", "1"),
#     # ("appliance", "Router", "SN-RT-55555", 4, 5, "Router appliance", "Pod 1", "1"),
#     ("appliance", "Anti-DDoS", "SN-ADDos-55555", 4, 5, "Anti-DDos appliance", "Pod 1", "1"),
# ]

# # --------------------------
# # Fan configuration rules
# # --------------------------
# FAN_RULES = {
#     "Anti-DDoS": {"fan_count": 6, "is_internal": False},
#     "Firewall": {"fan_count": 6, "is_internal": False},
#     "Core": {"fan_count": 4, "is_internal": True},
#     "Analyzer": {"fan_count": 2, "is_internal": True},
#     "Manager": {"fan_count": 2, "is_internal": True},
#     "Router": {"fan_count": 2, "is_internal": False},
#     "Server": {"fan_count": 6, "is_internal": True},
# }

# # --------------------------
# # Appliances considered chassis-type
# # --------------------------
# CHASSIS_TYPES = ["Firewall", "Anti-DDoS"]

# # --------------------------
# # Seeder Run
# # --------------------------
# def run():
#     print("🚀 Seeding appliances...")

#     for (
#         device_type,
#         appliance_type_name,
#         serial_number,
#         rack_alloc,
#         rack_start,
#         description,
#         pod_name,
#         rack_number,
#     ) in appliances_data:

#         # --- Ensure ApplianceType exists ---
#         appliance_type, _ = ApplianceType.objects.get_or_create(name=appliance_type_name)

#         # --- Validate Pod and Rack ---
#         try:
#             pod = Pod.objects.get(name=pod_name)
#             rack = Rack.objects.get(number=str(rack_number), pod=pod)
#         except (Pod.DoesNotExist, Rack.DoesNotExist):
#             raise ValueError(f"❌ Pod '{pod_name}' or Rack '{rack_number}' not found. Seed infrastructure first!")

#         # --- Create Device ---
#         device = Device.objects.create(rack=rack, type=device_type)

#         # --- Allocate Rack Positions ---
#         rack_positions = RackPosition.objects.filter(
#             rack=rack,
#             position_number__lte=rack_start,
#             position_number__gt=rack_start - rack_alloc,
#         ).order_by("-position_number")

#         if rack_positions.count() != rack_alloc:
#             raise ValueError(
#                 f"❌ Cannot seed {appliance_type_name}: requested {rack_alloc}U starting at {rack_start}, "
#                 f"but found only {rack_positions.count()} slots."
#             )
#         if rack_positions.filter(device__isnull=False).exists():
#             conflict_positions = list(
#                 rack_positions.filter(device__isnull=False).values_list("position_number", flat=True)
#             )
#             raise ValueError(
#                 f"❌ Cannot seed {appliance_type_name}: rack positions {conflict_positions} already occupied."
#             )
#         rack_positions.update(device=device, is_occupied=True)

#         # --- Determine if chassis ---
#         is_chassis = appliance_type_name in CHASSIS_TYPES

#         # --- Create Appliance ---
#         appliance, _ = Appliance.objects.update_or_create(
#             device=device,
#             defaults={
#                 "appliance_type": appliance_type,
#                 "serial_number": serial_number,
#                 "rack_unit_allocations": rack_alloc,
#                 "rack_unit_starting_position": rack_start,
#                 "description": description,
#                 "is_chassis": is_chassis,  # ✅ new field
#             },
#         )

#         # 🌀 --- Add Fans ---
#         fan_rule = FAN_RULES.get(appliance_type_name, {"fan_count": 1, "is_internal": True})
#         for i in range(fan_rule["fan_count"]):
#             FanUnit.objects.create(
#                 device=device,
#                 fan_count=1,
#                 fan_speed=random.randint(2500, 4000),
#                 is_internal=fan_rule["is_internal"],
#                 wattage_max_output=random.randint(8, 20),
#                 wattage_average=random.uniform(5.0, 15.0),
#                 description=f"{'Internal' if fan_rule['is_internal'] else 'External'} fan #{i+1} for {appliance_type_name}",
#             )

#         # 🧠 --- Add Storage Units ---
#         # storage_types = list(StorageType.objects.all())
#         # if not storage_types:
#         #     raise ValueError("❌ No StorageType entries found. Please seed enums first.")
#         # for i in range(2):
#         #     StorageUnit.objects.create(
#         #         device=device,
#         #         storage_capacity=random.choice([256, 512, 1024, 2048]),
#         #         storage_count=random.randint(1, 4),
#         #         storage_unit=random.choice([Type.TB, Type.GB]),  # ✅ valid enum usage
#         #         storage_type=random.choice(storage_types),
#         #     )

#         storage_choices = list(StorageType.values)  # ["HDD", "SSD"]

#         for i in range(2):
#             StorageUnit.objects.create(
#                 device=device,
#                 storage_capacity=random.choice([256, 512, 1024, 2048]),
#                 storage_count=random.randint(1, 4),
#                 capacity_unit =random.choice([CapacityUnit.TB, CapacityUnit.GB]),
#                 storage_type=random.choice(storage_choices),
#                 storage_interface=StorageInterface.objects.get(name="SATA"),   # must exist
#                 form_factor=StorageFormFactor.objects.get(name="2.5"),          # must exist
#             )

#         # 🧠 --- Add Memory Units ---
#         for i in range(2):
#             MemoryUnit.objects.create(
#                 device=device,
#                 brand_description=f"{appliance_type_name}-Memory-{i+1}"[:50],
#                 ram_capacity=random.choice([8, 16, 32, 64]),
#             )

#         # ⚙️ --- Add Processor Units ---
#         processor_types = list(ProcessorType.objects.all())
#         if not processor_types:
#             raise ValueError("❌ No ProcessorType entries found. Please seed enums first.")
#         for i in range(2):
#             ProcessorUnit.objects.create(
#                 device=device,
#                 description=f"{appliance_type_name}-CPU-{i+1}"[:50],
#                 processor_type=random.choice(processor_types),
#             )

#         # 🌐 --- Add Interfaces ---
#         interfaces_count = 4 if appliance_type_name == "Analyzer" else 2
#         for i in range(1, interfaces_count + 1):
#             Interface.objects.create(
#                 device=device,
#                 interface_number=i,
#                 to_location="",
#                 cable_type="copper",
#                 port_type="RJ45",
#                 description=f"Interface {i} for {appliance_type_name}",
#             )

#         # 🧩 --- Add Chassis Modules if applicable ---
#         if is_chassis:
#             CHASSIS_MODULES_PER_APPLIANCE = 4
#             INTERFACES_PER_MODULE = 2

#             for slot_position in range(1, CHASSIS_MODULES_PER_APPLIANCE + 1):
#                 module_name = f"Module-{slot_position}"
#                 serial_number_mod = f"{appliance_type_name[:3].upper()}-MOD-{slot_position}-{random.randint(1000,9999)}"

#                 module, _ = ApplianceChassis.objects.get_or_create(
#                     device=device,
#                     slot_position=slot_position,
#                     defaults={
#                         "module_name": module_name,
#                         "serial_number": serial_number_mod,
#                         "is_occupied": True,
#                         "is_chassis": True,  # ✅ consistent flag
#                     },
#                 )

#                 # Add interfaces for each module
#                 for i in range(1, INTERFACES_PER_MODULE + 1):
#                     Interface.objects.get_or_create(
#                         device=device,
#                         interface_number=i,
#                         defaults={
#                             "to_location": "",
#                             "cable_type": "copper",
#                             "port_type": "RJ45",
#                             "description": f"Interface {i} for {module_name}",
#                         },
#                     )

#         print(f"✅ Seeded {appliance_type_name} ({serial_number}) with all units and chassis modules if applicable.")

#     print("🎉 Appliance seeding complete!")


# # --------------------------
# # Seeder Revert
# # --------------------------
# def revert():
#     print("🧹 Reverting appliances...")
#     for (
#         device_type,
#         appliance_type_name,
#         serial_number,
#         rack_alloc,
#         rack_start,
#         description,
#         pod_name,
#         rack_number,
#     ) in appliances_data:
#         try:
#             pod = Pod.objects.get(name=pod_name)
#             rack = Rack.objects.get(number=str(rack_number), pod=pod)
#         except (Pod.DoesNotExist, Rack.DoesNotExist):
#             continue

#         try:
#             appliance = Appliance.objects.get(serial_number=serial_number, device__rack=rack)
#             device = appliance.device

#             # Delete associated units
#             FanUnit.objects.filter(device=device).delete()
#             StorageUnit.objects.filter(device=device).delete()
#             MemoryUnit.objects.filter(device=device).delete()
#             ProcessorUnit.objects.filter(device=device).delete()
#             Interface.objects.filter(device=device).delete()
#             ApplianceChassis.objects.filter(device=device).delete()  # ✅ corrected model name

#             # Free rack slots
#             RackPosition.objects.filter(device=device).update(device=None, is_occupied=False)
#             appliance.delete()
#             if device.type == device_type:
#                 device.delete()

#             print(f"🗑️ Removed {appliance_type_name} and all associated units from Rack {rack.number}")
#         except Appliance.DoesNotExist:
#             continue

#     print("✅ Appliance data reverted successfully.")
