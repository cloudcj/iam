from django.db import transaction
from inventory.infrastructure.models import Pod, Rack, RackPosition
from inventory.assets.models import Device, Switch, FanUnit
import random
from ..seed_data import switches_data   # switch data
from .seed_helpers.rack_allocation_helper import allocate_rack_positions


@transaction.atomic
def run():
    # Preload pods and racks for performance
    pods = {p.name: p for p in Pod.objects.all()}
    racks = {(r.pod_id, r.number): r for r in Rack.objects.all()}

    for data in switches_data:

        pod_name = data["pod_name"]
        rack_number = str(data["rack_number"])

        # --- Fetch Pod ---
        pod = pods.get(pod_name)
        if not pod:
            raise ValueError(f"❌ Pod '{pod_name}' not found")

        # --- Fetch Rack ---
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
            serial_number=data["serial_number"],
            model=data["model"],
            rack_unit_allocations=data["rack_alloc"],
            starting_position=data["starting_position"],
            ipv4_address=data["ipv4_address"],
            description=data.get("description", ""),
            power=data.get("power"),
            weight=data.get("weight"),
        )

        # --- Allocate Rack Positions ---
        allocate_rack_positions(
            rack=rack,
            start=data["starting_position"],
            size=data["rack_alloc"],
            device=device,
            # device_label=data["switch_name"],
        )

        # --- Create Switch role ---
        if device.type == 'switch':
            Switch.objects.create(device=device)


        # --- Create/Update Switch ---
        # Switch.objects.update_or_create(
        #     device=device,
        #     defaults={
        #         "switch_name": data["switch_name"],
        #     }
        # )



# -----------------------------
# Revert function
# -----------------------------

def revert():
    """
    Reverse seeding: delete switches, fans, and free rack slots.
    """
    for data in switches_data:
        try:
            pod = Pod.objects.get(name=data["pod_name"])
            rack = Rack.objects.get(number=str(data["rack_number"]), pod=pod)
        except (Pod.DoesNotExist, Rack.DoesNotExist):
            continue

        try:
            # Find the device first
            device = Device.objects.get(serial_number=data["serial_number"], rack=rack)

            # Delete associated fans
            FanUnit.objects.filter(device=device).delete()

            # Free rack slots
            RackPosition.objects.filter(device=device).update(device=None, is_occupied=False)

            # Delete Switch role if it exists
            if hasattr(device, 'switch'):
                device.switch.delete()

            # Delete the device itself
            device.delete()

            print(f"🗑️ Removed device '{data['name']}' and its fans from Rack {rack.number}")

        except Device.DoesNotExist:
            continue


#     """Reverse seeding: delete switches, fans, and free rack slots."""
#     for data in switches_data:
#         try:
#             pod = Pod.objects.get(name=data["pod_name"])
#             rack = Rack.objects.get(number=str(data["rack_number"]), pod=pod)
#         except (Pod.DoesNotExist, Rack.DoesNotExist):
#             continue

#         try:
#             switch = Switch.objects.get(switch_name=data["switch_name"], device__rack=rack)
#             device = switch.device

#             # Delete associated fans
#             FanUnit.objects.filter(device=device).delete()

#             # Free rack slots
#             RackPosition.objects.filter(device=device).update(device=None, is_occupied=False)

#             # Delete switch and device
#             switch.delete()
#             if device.type == data["device_type"]:
#                 device.delete()

#             print(f"🗑️ Removed {data['switch_name']} and its fans from Rack {rack.number}")
#         except Switch.DoesNotExist:
#             continue



