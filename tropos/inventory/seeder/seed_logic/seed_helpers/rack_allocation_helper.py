# infra/seed_helpers.py

from inventory.infrastructure.models import RackPosition
from ...seed_data.servers import servers_data

def allocate_rack_positions(rack, start, size, device):
    """
    Validate and allocate rack positions for any device.
    Ensures:
        - Required number of rack slots exist
        - None of the slots are occupied
        - Assigns the device to the slots in bulk
    """

    # #For Ascending
    slots = list(
        RackPosition.objects.filter(
            rack=rack,
            position_number__gte=start,
            position_number__lt=start + size,
        ).order_by("position_number")  # ascending
    )


    # #For Descending
    # slots = list(
    #     RackPosition.objects.filter(
    #         rack=rack,
    #         position_number__lte=start,
    #         position_number__gt=start - size,
    #     ).order_by("position_number")
    # )

    # Validate slot count
    if len(slots) != size:
        raise ValueError(
            f"❌ Cannot seed {device.name}: "
            f"Insufficient rack space: the device requires {size}U, but only {len(slots)} are available."
        )

    # Check occupancy (Python-side, no extra DB)

    # occupied = [s.position_number for s in slots if s.device_id is not None]
    # if occupied:
    #     raise ValueError(
    #         f"❌ Cannot seed {device_label}: "
    #         f"Rack positions {occupied} are already occupied."
    #     )

    # Check occupancy (Python-side, no extra DB)
    # occupied_positions = {
    #     s.position_number
    #     for s in slots
    #     if s.device is not None
    # }

    # device_sn = {
    #     s.device.serial_number
    #     for s in slots
    #     if s.device is not None
    # }

    # if occupied_positions:
    #     positions_str = ",".join(map(str, sorted(occupied_positions)))

    #     if len(device_sn) == 1:
    #         sn_str = next(iter(device_sn))
    #     else:
    #         sn_str = ",".join(sorted(device_sn))

    #     raise ValueError(
    #         f"Rack position(s) {{{positions_str}}} "
    #         f"already occupied by device serial number: "
    #         f"{{{sn_str}}}."
    #     )

    occupied_positions = {
    s.position_number
    for s in slots
    if s.device is not None
    }

    # existing_device_sn = {
    #     s.device.serial_number
    #     for s in slots
    #     if s.device is not None
    # }

    existing_device_name = {
    # getattr(s.device.server, "server_name", s.device.serial_number)
    s.device.name
    for s in slots
    if s.device is not None
}

    if occupied_positions:
        sorted_positions = sorted(occupied_positions)

        # format contiguous positions as range
        if sorted_positions == list(range(sorted_positions[0], sorted_positions[-1] + 1)):
            positions_str = f"{sorted_positions[0]}-{sorted_positions[-1]}"
        else:
            positions_str = ",".join(map(str, sorted_positions))

        existing_sn_str = ",".join(sorted(existing_device_name))

        # 👇 FROM SEEDER JSON
        # placing_sn = servers_data.get("serial_number") or servers_data.get("name") or "Unknown device"
        placing_device_label = device.name 

        raise ValueError(
            f"Device {placing_device_label} cannot seed. "
            f"{rack.pod.name} rack pos {positions_str} "
            f"already occupied by device serial number(s): {existing_device_name}"
        )



    # # Bulk assign device to rack positions
    # RackPosition.objects.filter(pk__in=[s.pk for s in slots]).update(
    #     device=device,
    #     is_occupied=True
    # )

     # Assign device to positions
    for slot in slots:
        slot.device = device
        slot.is_occupied = True  # ensure correct state

    # Bulk update positions for speed
    RackPosition.objects.bulk_update(slots, ["device", "is_occupied"])

    # Update rack occupancy once
    rack.update_occupancy()
