# infrastructure/services/rack_service.py
from rest_framework.exceptions import ValidationError
from django.db import transaction
from inventory.infrastructure.models import RackPosition


class RackService:

    @staticmethod
    def _format_occupied_positions(occupied_positions):
        """
        Helper to generate a descriptive message for occupied rack positions.
        """
        if len(occupied_positions) == 1:
            return f"Rack position {occupied_positions[0]} is already occupied"
        return f"Rack positions {min(occupied_positions)}-{max(occupied_positions)} are already occupied"

    @staticmethod
    def validate_positions(rack, start, alloc, exclude_device=None):
        """
        Ensure requested rack positions exist and are unoccupied.
        Raises ValidationError with descriptive messages.
        """
        end = start + alloc - 1

        # ---------------------- Check rack capacity ----------------------
        if hasattr(rack, "max_units") and end > rack.max_units:
            raise ValidationError({
                "rack_positions": [f"Requested positions {start}-{end} exceed rack capacity (max {rack.max_units})"]
            })

        # ---------------------- Check positions exist ----------------------
        positions = RackPosition.objects.filter(
            rack=rack,
            position_number__range=(start, end)
        )
        if positions.count() != alloc:
            raise ValidationError({
                "rack_positions": [f"Rack positions {start}-{end} do not exist"]
            })

        # ---------------------- Check occupancy ----------------------
        if exclude_device:
            positions = positions.exclude(device=exclude_device)

        occupied_positions = list(
            positions.filter(device__isnull=False)
                    .values_list('position_number', flat=True)
        )
        if occupied_positions:
            raise ValidationError({
                "rack_positions": [RackService._format_occupied_positions(occupied_positions)]
            })

    @staticmethod
    @transaction.atomic
    def assign_device_to_positions(rack, start, alloc, device):
        """
        Assign a device to the specified rack positions.
        Ensures positions are valid and unoccupied.
        """
        # Validate before assigning
        RackService.validate_positions(rack, start, alloc)

        # Assign device
        end = start + alloc - 1
        positions = RackPosition.objects.filter(
            rack=rack,
            position_number__range=(start, end)
        )
        positions.update(device=device)

    @staticmethod
    @transaction.atomic
    def release_device_from_positions(rack, start, alloc, device):
        """
        Free rack positions previously assigned to a device.
        """
        end = start + alloc - 1
        RackPosition.objects.filter(
            rack=rack,
            position_number__range=(start, end),
            device=device
        ).update(device=None)




# from rest_framework.exceptions import ValidationError
# from inventory.infrastructure.models import RackPosition


# class RackService:

#     @staticmethod
#     def validate_positions(rack, start, alloc, exclude_device=None):
#         """
#         Ensure requested rack positions exist and are unoccupied.
#         Raises ValidationError with descriptive messages.
#         """
#         end = start + alloc - 1

#         # ---------------------- Check rack capacity ----------------------
#         if hasattr(rack, "max_units") and end > rack.max_units:
#             raise ValidationError({
#                 "rack_positions": [f"Requested positions {start}-{end} exceed rack capacity (max {rack.max_units})"]
#             })

#         # ---------------------- Check positions exist ----------------------
#         positions = RackPosition.objects.filter(
#             rack=rack,
#             position_number__range=(start, end)
#         )
#         if positions.count() != alloc:
#             raise ValidationError({
#                 "rack_positions": [f"Rack positions {start}-{end} do not exist"]
#             })

#         # # ---------------------- Check occupancy ----------------------
#         # if exclude_device:
#         #     positions = positions.exclude(device=exclude_device)

#         # if positions.filter(device__isnull=False).exists():
#         #     raise ValidationError({
#         #         "rack_positions": [f"Rack positions {start}-{end} are already occupied"]
#         #     })

#        # ---------------------- Check occupancy ----------------------
#         if exclude_device:
#             positions = positions.exclude(device=exclude_device)

#         occupied_positions = list(
#             positions.filter(device__isnull=False)
#                     .values_list('position_number', flat=True)
#         )

#         if occupied_positions:
#             if len(occupied_positions) == 1:
#                 # Only one position is occupied → single message
#                 pos = occupied_positions[0]
#                 raise ValidationError({
#                     "rack_positions": [f"Rack position {pos} is already occupied"]
#                 })
#             else:
#                 # Multiple occupied → combined range message
#                 start_pos = min(occupied_positions)
#                 end_pos = max(occupied_positions)
#                 raise ValidationError({
#                     "rack_positions": [
#                         f"Rack positions {start_pos}-{end_pos} are already occupied"
#                     ]
#                 })


#     @staticmethod
#     def allocate_positions(rack, start, alloc, device):
#         """
#         Assign a device to the specified rack positions.
#         """
#         end = start + alloc - 1
#         positions = RackPosition.objects.filter(
#             rack=rack,
#             position_number__range=(start, end)
#         )
#         if positions.count() != alloc:
#             raise ValidationError({
#                 "rack_positions": [f"Cannot allocate positions {start}-{end}, some positions are missing"]
#             })
#         positions.update(device=device)

#     @staticmethod
#     def free_positions(rack, start, alloc, device):
#         """
#         Free rack positions previously assigned to a device.
#         """
#         end = start + alloc - 1
#         RackPosition.objects.filter(
#             rack=rack,
#             position_number__range=(start, end),
#             device=device
#         ).update(device=None)



