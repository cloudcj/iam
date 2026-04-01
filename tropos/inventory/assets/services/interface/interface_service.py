from django.db import transaction
from inventory.assets.models import Interface

class InterfaceService:

    @staticmethod
    @transaction.atomic
    def create_interfaces(device, count: int):
        existing_count = device.interfaces.count()
        interfaces = [
            Interface(
                device=device,
                interface_number=existing_count + i + 1,
                to_location=None,
                cable_type="",
                port_type="",
                description=f"Auto-generated interface {existing_count + i + 1}"
            )
            for i in range(count)
        ]
        Interface.objects.bulk_create(interfaces)

    @staticmethod
    @transaction.atomic
    def sync_interfaces(device, new_count: int):
        current = device.interfaces.count()
        if current < new_count:
            interfaces = [
                Interface(
                    device=device,
                    interface_number=current + i + 1,
                    to_location=None,
                    cable_type="",
                    port_type="",
                    description=f"Auto-generated interface {current + i + 1}"
                )
                for i in range(new_count - current)
            ]
            Interface.objects.bulk_create(interfaces)
