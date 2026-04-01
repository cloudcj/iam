# myapp/seeders/interface_seeder.py
import random
from inventory.assets.models import Device, Interface
from inventory.enums.models import TransceiverType

def run():
    # Fetch all transceiver types for lookup
    transceiver_types = list(TransceiverType.objects.all())

    for device in Device.objects.all():
        if device.type == "switch":
            interfaces_count = 48
            cable_type = "copper"
            port_type_name = "RJ45"
            transceiver_type = None
        elif device.type == "server":
            interfaces_count = 4
            cable_type = "fiber"
            port_type_name = "fiber"
            transceiver_type = None  # random per interface
        elif device.type == "appliance":
            interfaces_count = 2
            # Here you can decide if some appliances are fiber or copper
            # For this example, let's randomly assign copper or fiber per appliance
            cable_type = random.choice(["copper", "fiber"])
            port_type_name = "RJ45" if cable_type == "copper" else "fiber"
            transceiver_type = None
        else:
            interfaces_count = 0
            cable_type = port_type_name = ""
            transceiver_type = None

        for i in range(1, interfaces_count + 1):
            interface, created = Interface.objects.get_or_create(
                device=device,
                interface_number=i,
                defaults={
                    "to_location": "",
                    "cable_type": cable_type,
                    "port_type": port_type_name,
                    "description": f"Interface {i} for {device.type.capitalize()}",
                },
            )

         # --- Update interface_count for every device instance ---
        device.interface_count = interfaces_count
        device.save()

        # For fiber interfaces, pick a random TransceiverType
        if cable_type == "fiber" and transceiver_types:
            random_transceiver = random.choice(transceiver_types)
            interface.transceiver_units.get_or_create(
                transceiver_type=random_transceiver
            )
       
def unrun():
    """Delete all interfaces and associated transceiver units."""
    for interface in Interface.objects.all():
        interface.transceiver_units.all().delete()
    Interface.objects.all().delete()
