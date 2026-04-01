from inventory.assets.models.components import (
    MemoryUnit, ProcessorUnit, StorageUnit
)

from inventory.enums.models import (
    StorageInterface, StorageFormFactor,
    ProcessorBrand, ProcessorCodename, ProcessorTier, ProcessorModel
)

# -----------------------------
# Processoy,Memory & Storage Helpers
# -----------------------------
def create_processor_unit(device, proc):
    brand, _ = ProcessorBrand.objects.get_or_create(name=proc["brand_name"])

    codename, _ = ProcessorCodename.objects.get_or_create(
        name=proc["codename"],
        brand=brand,
    )

    tier, _ = ProcessorTier.objects.get_or_create(name=proc["tier"])

    model, _ = ProcessorModel.objects.get_or_create(
        name=proc["model"],
        codename=codename,
        tier=tier,
    )

    ProcessorUnit.objects.create(
        device=device,
        processor_codename=codename,
        processor_tier=tier,
        processor_model=model,
    )

def create_memory_unit(device, mem):
    MemoryUnit.objects.create(
        device=device,
        ram_capacity=mem["ram_capacity"],
        quantity=mem["quantity"],
    )


def create_storage_unit(device, sto):
    interface = None
    if isinstance(sto.get("storage_interface"), dict):
        interface = StorageInterface.objects.filter(
            name=sto["storage_interface"]["name"]
        ).first()

    form_factor = None
    if isinstance(sto.get("form_factor"), dict):
        form_factor = StorageFormFactor.objects.filter(
            name=sto["form_factor"]["name"]
        ).first()

    StorageUnit.objects.create(
        device=device,
        storage_type=sto["storage_type"],
        storage_capacity=sto["storage_capacity"],
        storage_count=sto.get("storage_count", 1),
        capacity_unit=sto.get("capacity_unit", "GB"),
        storage_interface=interface,
        form_factor=form_factor,
    )
