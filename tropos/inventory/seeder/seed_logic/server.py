# myapp/seeders/server_seeder.py
from django.db import transaction

from inventory.infrastructure.models import Pod, Rack

from inventory.infrastructure.models import Pod, Rack
from inventory.assets.models import Device, Server

from ..seed_data import servers_data
from .seed_helpers.rack_allocation_helper import allocate_rack_positions
from .seed_helpers.compute_units_helpers import create_memory_unit,create_processor_unit,create_storage_unit



# -----------------------------
# Main Seeder
# -----------------------------
@transaction.atomic
def run():

    # Preload everything (DB performance optimization)
    pods = {p.name: p for p in Pod.objects.all()}
    racks = {(r.pod.pk, r.number): r for r in Rack.objects.select_related("pod")}

    for data in servers_data:

        pod_name = data["pod_name"]
        rack_number = str(data["rack_number"])

        # --- Get Pod ---
        pod = pods.get(pod_name)
        if not pod:
            raise ValueError(f"❌ Pod '{pod_name}' not found")

        # --- Get Rack ---
        rack = racks.get((pod.pk, rack_number))
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
            # device_label=data["server_name"],
        )

        # --- Create Server ---
        server = Server.objects.create(
            device=device,
            # server_name=data["server_name"],
            classification=data["classification"],
            module_name=data["module_name"],
        )

        # --- Memory Units ---
        for mem in data.get("memory_units", []):
            create_memory_unit(device, mem)

        # --- Processor Units ---
        for proc in data.get("processors", []):
            create_processor_unit(device, proc)

        # --- Storage Units ---
        for sto in data.get("storage_units", []):
            create_storage_unit(device, sto)

       
        print(f"✅ Seeded {data['name']} with all components.")


# def run():
#     for server_data in servers_data:

#         pod_name = server_data["pod_name"]
#         rack_number = server_data["rack_number"]
#         rack_alloc = server_data["rack_alloc"]
#         starting_position = server_data["starting_position"]
#         device_type = server_data["device_type"]
#         server_name = server_data["server_name"]
#         module_name = server_data["module_name"]
#         model= server_data["model"]
#         classification = server_data["classification"]
#         serial_number = server_data.get("serial_number")
#         ipv4_address = server_data["ipv4_address"]
#         memories = server_data.get("memory_units", [])
#         processors = server_data.get("processors", [])
#         storages = server_data.get("storage_units", [])
#         interface_count = server_data.get("interface_count", 4)
#         power = server_data.get("power")
#         weight = server_data.get("weight")
#         description = server_data.get("description", "")

#         # --- Fetch Pod & Rack ---
#         try:
#             pod = Pod.objects.get(name=pod_name)
#             rack = Rack.objects.get(number=str(rack_number), pod=pod)
#         except (Pod.DoesNotExist, Rack.DoesNotExist):
#             raise ValueError(f"❌ {pod_name} or Rack {rack_number} not found")

#         # --- Create Device ---
#         device = Device.objects.create(
#             rack=rack,
#             type=device_type,
#             serial_number=serial_number,
#             model=model,
#             rack_unit_allocations=rack_alloc,
#             starting_position=starting_position,
#             ipv4_address = ipv4_address,
#             description=description,
#             interface_count=interface_count,
#             power=power,
#             weight=weight,
#         )

#         # --- Allocate Rack Positions ---
#         rack_positions = RackPosition.objects.filter(
#             rack=rack,
#             position_number__lte=starting_position,
#             position_number__gt=starting_position - rack_alloc,
#         ).order_by("-position_number")

#         if rack_positions.count() != rack_alloc:
#             raise ValueError(
#                 f"❌ Cannot seed {server_name}: requested {rack_alloc}U starting at {rack_start}, "
#                 f"but found only {rack_positions.count()} slots."
#             )

#         occupied = rack_positions.filter(device__isnull=False)
#         if occupied.exists():
#             conflict_positions = list(occupied.values_list("position_number", flat=True))
#             raise ValueError(
#                 f"❌ Cannot seed {server_name}: rack positions {conflict_positions} already occupied."
#             )

#         rack_positions.update(device=device, is_occupied=True)

#         # --- Create Server ---
#         server = Server.objects.create(
#             device=device,
#             server_name=server_name,
#             classification=classification,
#             module_name=module_name
#         )

#         # # --- Create Interfaces ---
#         # for i in range(1, interface_count + 1):
#         #     Interface.objects.create(
#         #         device=device,
#         #         interface_number=i,
#         #         cable_type="fiber",
#         #         port_type="fiber",
#         #         description=f"Interface {i} for {server_name}",
#         #     )

#         # --- Memory Units ---
#         for mem in memories:
#             MemoryUnit.objects.create(
#                 device=device,
#                 ram_capacity=mem["ram_capacity"],
#                 quantity=mem["quantity"]

#             )

#         # --- Processor Units ---
#         # for proc in processors:
#         #     brand, _ = ProcessorBrand.objects.get_or_create(name=proc["brand_description"])
#         #     family, _ = ProcessorFamily.objects.get_or_create(
#         #         brand=brand,
#         #         generation=proc["generation"],
#         #         codename=proc.get("codename") or proc["generation"]
#         #     )
#         #     processor_type, _ = ProcessorType.objects.get_or_create(
#         #         family=family,
#         #         model=proc["model"],
#         #         defaults={"cores": proc.get("cores", 0), "threads": proc.get("threads", 0)},
#         #     )
#         #     ProcessorUnit.objects.create(
#         #         device=device,
#         #         processor_type=processor_type,
#         #         description=proc.get("description", "")
#         #     )

#         # --- Processor Units ---

#         for proc in processors:
#             # 1. Get or create Brand (for codename)
#             brand, _ = ProcessorBrand.objects.get_or_create(name=proc["brand_name"])

#             # 2. Get or create Codename
#             codename, _ = ProcessorCodename.objects.get_or_create(
#                 name=proc["codename"],
#                 brand=brand
#             )

#             # 3. Get or create Tier (generic, no brand)
#             tier, _ = ProcessorTier.objects.get_or_create(
#                 name=proc["tier"]
#             )

#             # 4. Get or create Model (brand removed)
#             model, _ = ProcessorModel.objects.get_or_create(
#                 name=proc["model"],
#                 codename=codename,
#                 tier=tier
#             )

#             # 5. Create ProcessorUnit
#             ProcessorUnit.objects.create(
#                 device=device,
#                 processor_codename=codename,
#                 processor_tier=tier,
#                 processor_model=model
#             )

#         # for proc in processors:
#         #     # 1. Brand
#         #     brand, _ = ProcessorBrand.objects.get_or_create(name=proc["brand_name"])

#         #     # 2. Codename
#         #     codename, _ = ProcessorCodename.objects.get_or_create(
#         #         name=proc["codename"],
#         #         brand=brand
#         #     )

#         #     # 3. Tier
#         #     tier, _ = ProcessorTier.objects.get_or_create(
#         #         name=proc["tier"],  # e.g., Xeon Gold / Silver / Platinum
#         #         brand=brand
#         #     )

#         #     # 4. Model
#         #     model, _ = ProcessorModel.objects.get_or_create(
#         #         name=proc["model"],
#         #         codename=codename,
#         #         tier=tier,
#         #     )

#         #     # 5. Create ProcessorUnit
#         #     ProcessorUnit.objects.create(
#         #         device=device,
#         #         processor_codename=codename,
#         #         processor_tier=tier,
#         #         processor_model=model,
#         #     )


#         # --- Storage Units ---
#         for sto in storages:
#             interface = None
#             form_factor = None
#             if isinstance(sto.get("storage_interface"), dict):
#                 interface = StorageInterface.objects.filter(name=sto["storage_interface"]["name"]).first()
#             if isinstance(sto.get("form_factor"), dict):
#                 form_factor = StorageFormFactor.objects.filter(name=sto["form_factor"]["name"]).first()

#             StorageUnit.objects.create(
#                 device=device,
#                 storage_type=sto["storage_type"],
#                 storage_capacity=sto["storage_capacity"],
#                 storage_count=sto.get("storage_count", 1),
#                 capacity_unit=sto.get("capacity_unit", "GB"),
#                 storage_interface=interface,
#                 form_factor=form_factor,
#             )

#         # --- Add Internal Fans ---
#         for i in range(4):
#             FanUnit.objects.create(
#                 device=device,
#                 fan_count=1,
#                 fan_speed=random.randint(2500, 4000),
#                 is_internal=True,
#                 wattage_max_output=random.randint(20, 50),
#                 wattage_average=random.uniform(15.0, 40.0),
#                 description=f"Internal fan #{i+1} for {server_name}",
#             )

#         print(f"✅ Seeded {server_name} with all components.")


# def revert():
#     """Reverse seeding: remove server, device, fans, free rack positions."""
#     for server_data in servers_data:
#         server_name = server_data["server_name"]
#         pod_name = server_data["pod_name"]
#         rack_number = server_data["rack_number"]

#         try:
#             pod = Pod.objects.get(name=pod_name)
#             rack = Rack.objects.get(number=str(rack_number), pod=pod)
#         except (Pod.DoesNotExist, Rack.DoesNotExist):
#             continue

#         try:
#             server = Server.objects.get(server_name=server_name, device__rack=rack)
#             device = server.device

#             FanUnit.objects.filter(device=device).delete()
#             RackPosition.objects.filter(device=device).update(device=None, is_occupied=False)
#             server.delete()
#             device.delete()

#             print(f"🗑️ Removed {server_name} and its components from Rack {rack.number}")
#         except Server.DoesNotExist:
#             continue
