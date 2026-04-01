# # myapp/seeders/device_seeder.py
# from inventory.assets.models import Device, Switch, Interface
# devices_data = [
#     ("switch", "1", "Pod 1"),  # (type, rack_number, pod_name)
# ]


# def run(apps):
#     Pod = apps.get_model("infrastructure", "Pod")
#     Rack = apps.get_model("infrastructure", "Rack")
#     RackPosition = apps.get_model("infrastructure", "RackPosition")
#     Device = apps.get_model("assets", "Device")
#     Switch = apps.get_model("assets", "Switch")  # holds rack_alloc & rack_start

#     for device_type, rack_number, pod_name in devices_data:
#         try:
#             pod = Pod.objects.get(name=pod_name)
#             rack = Rack.objects.get(number=str(rack_number), pod=pod)
#         except (Pod.DoesNotExist, Rack.DoesNotExist):
#             continue

#         # Get the switch for this rack + device type
#         switch = Switch.objects.filter(
#             device__rack=rack, device__type=device_type
#         ).first()
#         if not switch:
#             continue

#         ru_count = switch.rack_unit_allocations
#         top_pos = switch.rack_unit_starting_position

#         rack_positions = RackPosition.objects.filter(
#             rack=rack,
#             position_number__lte=top_pos,
#             position_number__gt=top_pos - ru_count,
#         ).order_by("-position_number")

#         # Validate availability
#         if rack_positions.count() != ru_count or rack_positions.filter(device__isnull=False).exists():
#             continue

#         # Create/fetch Device
#         device, _ = Device.objects.get_or_create(
#             rack=rack,
#             type=device_type,
#         )

#         # Assign rack positions in bulk
#         rack_positions.update(device=device, status="occupied")


# def unrun(apps):
#     """Undo the seeded devices and free rack positions."""
#     RackPosition = apps.get_model("infrastructure", "RackPosition")
#     Device = apps.get_model("assets", "Device")

#     devices_to_remove = Device.objects.filter(type="switch")
#     for device in devices_to_remove:
#         RackPosition.objects.filter(device=device).update(device=None, status="unoccupied")
#         device.delete()


# myapp/seeders/device_seeder.py
from inventory.infrastructure.models import Pod, Rack
from inventory.assets.models import Device

devices_data = [
    ("switch", "Pod 1", "2"),
    ("switch", "Pod 1", "2"),
    ("appliance", "Pod 1", "2"),
    ("appliance", "Pod 1", "2"),
    ("server", "Pod 1", "2"),
    ("server", "Pod 1", "2")
]

def run():
    for device_type, pod_name, rack_number in devices_data:
        try:
            pod = Pod.objects.get(name=pod_name)
            rack = Rack.objects.get(number=str(rack_number), pod=pod)
        except (Pod.DoesNotExist, Rack.DoesNotExist):
            continue

        # Just create or reuse Device tied to Rack
        Device.objects.get_or_create(
            rack=rack,
            type=device_type,
        )


def revert():
    for device_type, pod_name, rack_number in devices_data:
        try:
            pod = Pod.objects.get(name=pod_name)
            rack = Rack.objects.get(number=str(rack_number), pod=pod)
        except (Pod.DoesNotExist, Rack.DoesNotExist):
            continue

        Device.objects.filter(rack=rack, type=device_type).delete()
