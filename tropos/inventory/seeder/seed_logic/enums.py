from inventory.enums.models import (
    ProcessorBrand,
    ProcessorModel,
    ProcessorCodename,
    ProcessorTier,
    StorageFormFactor,
    StorageInterface,
    ApplianceType,
    NetworkArea,
    NetworkAreaOrder,
    TransceiverType,  # added
)

from ..seed_data import processor_data, appliance_types, storage_form_factors, storage_interfaces, transceiver_types, network_areas,network_area_orders

# ----------------------
# Seeder Data
# ----------------------

# processor_data = {
#     "brands": [
#         {"name": "Intel"},
#     ],

#     "processor_codenames": [
#         {"name": "Icelake", "brand_name": "Intel"},
#         {"name": "Emerald Rapids", "brand_name": "Intel"},
#     ],

#     "processor_tiers": [
#         {"name": "Xeon Silver", "brand_name": "Intel"},
#         {"name": "Xeon Gold", "brand_name": "Intel"},
#         {"name": "Xeon Platinum", "brand_name": "Intel"},
#     ],

#     "processor_models": [
#         # Icelake Models
#         {"name": "5318Y", "codename_name": "Icelake", "tier_name": "Xeon Gold", "brand_name": "Intel"},
#         {"name": "4310",  "codename_name": "Icelake", "tier_name": "Xeon Silver", "brand_name": "Intel"},
#         {"name": "4510",  "codename_name": "Icelake", "tier_name": "Xeon Silver", "brand_name": "Intel"},

#         # Emerald Rapids Models
#         {"name": "6530",  "codename_name": "Emerald Rapids", "tier_name": "Xeon Gold", "brand_name": "Intel"},
#         {"name": "8558",  "codename_name": "Emerald Rapids", "tier_name": "Xeon Platinum", "brand_name": "Intel"},
#     ]
# }


def run():

    # ---------------------------
    # Seed Processor Data
    # ---------------------------
    # for brand_name, generation, codename, model, cores, threads in processor_data:
    #     brand, _ = ProcessorBrand.objects.get_or_create(name=brand_name)

    #     family, _ = ProcessorFamily.objects.get_or_create(
    #         brand=brand,
    #         generation=generation,
    #         codename=codename,
    #     )

    #     ProcessorType.objects.get_or_create(
    #         family=family,
    #         model=model,
    #         defaults={"cores": cores, "threads": threads},
    #     )

    #     print(f"✅ Seeded Processor: {brand_name} {model} ({generation}, {codename})")

    # ---------------------------
    # Seed Processor Data (New Structure)
    # ---------------------------

 
    # 1. Seed Brands
    brands = {}
    for brand_data in processor_data["brands"]:
        brand, _ = ProcessorBrand.objects.get_or_create(name=brand_data["name"])
        brands[brand.name] = brand

    # 2. Seed Codenames
    codenames = {}
    for codename_data in processor_data["processor_codenames"]:
        brand = brands[codename_data["brand_name"]]
        codename, _ = ProcessorCodename.objects.get_or_create(name=codename_data["name"], brand=brand)
        codenames[codename.name] = codename

    # 3. Seed Tiers
    tiers = {}
    for tier_data in processor_data["processor_tiers"]:
        brand = brands[tier_data["brand_name"]]  # get brand instance
        tier, _ = ProcessorTier.objects.get_or_create(name=tier_data["name"], brand=brand)
        tiers[tier.name] = tier

    # 4. Seed Processor Models
    for model_data in processor_data["processor_models"]:
        codename = codenames[model_data["codename_name"]]
        tier = tiers[model_data["tier_name"]]
        model, _ = ProcessorModel.objects.get_or_create(
            name=model_data["name"],
            codename=codename,
            tier=tier
        )
        print(f"✅ Seeded: {codename.brand.name} / {codename.name} / {tier.name} / {model.name}")



    # for brand_name, codename_name, tier_name, model_name in processor_data:

    #     # 1. Brand
    #     brand, _ = ProcessorBrand.objects.get_or_create(name=brand_name)

    #     # 2. Codename
    #     codename, _ = ProcessorCodename.objects.get_or_create(
    #         name=codename_name,
    #         brand=brand
    #     )

    #     # 3. Tier
    #     tier, _ = ProcessorTier.objects.get_or_create(
    #         name=tier_name,
    #         brand=brand
    #     )

    #     # 4. Model
    #     ProcessorModel.objects.get_or_create(
    #         name=model_name,
    #         codename=codename,
    #         tier=tier,
    #         brand=brand
    #     )

    #     print(f"✅ Seeded: {brand_name} / {codename_name} / {tier_name} / {model_name}")


    # ---------------------------
    # Seed Storage Types
    # ---------------------------
    # for st in storage_types:
    #     StorageType.objects.get_or_create(name=st)
    #     print(f"✅ Seeded Storage Type: {st}")

    # ---------------------------
    # Seed Appliance Types
    # ---------------------------
    for at in appliance_types:
        ApplianceType.objects.get_or_create(name=at)
        print(f"✅ Seeded Appliance Type: {at}")

    # ---------------------------
    # Seed Transceiver Types
    # ---------------------------
    for tt in transceiver_types:
        TransceiverType.objects.get_or_create(name=tt)
        print(f"✅ Seeded Transceiver Type: {tt}")

    # ---------------------------
    # Seed Network Areas
    # ---------------------------
    area_objects = {}
    for area_name in network_areas:
        area, _ = NetworkArea.objects.get_or_create(name=area_name)
        area_objects[area_name] = area
        print(f"✅ Seeded Network Area: {area_name}")

    # ---------------------------
    # Seed Network Area Orders
    # ---------------------------
    for order_name in network_area_orders:
        prefix = order_name.split("-")[0]

        # Try closest match if prefix not exact
        if prefix not in area_objects:
            for area_name in area_objects.keys():
                if prefix.startswith(area_name):
                    prefix = area_name
                    break

        if prefix not in area_objects:
            print(f"⚠ Skipped Network Area Order (no matching area): {order_name}")
            continue

        NetworkAreaOrder.objects.get_or_create(
            area=area_objects[prefix],
            name=order_name,
        )

        print(f"  ↳ Seeded Area Order: {order_name} → {prefix}")


        # ---------------------------
        # Seed Storage Interfaces
        # ---------------------------
        for si in storage_interfaces:
            StorageInterface.objects.get_or_create(name=si)
            print(f"✅ Seeded Storage Interface: {si}")

        # ---------------------------
        # Seed Storage Form Factors
        # ---------------------------
        for ff in storage_form_factors:
            StorageFormFactor.objects.get_or_create(name=ff)
            print(f"✅ Seeded Storage Form Factor: {ff}")

    print("🎉 Enums seeding complete!")




def revert():
    print("🧹 Reverting enums...")

    # ---------------------------
    # Remove Network Area Orders
    # ---------------------------
    NetworkAreaOrder.objects.filter(name__in=network_area_orders).delete()

    # ---------------------------
    # Remove Network Areas
    # ---------------------------
    NetworkArea.objects.filter(name__in=network_areas).delete()

    # ---------------------------
    # Remove Processor Models
    # ---------------------------
    for model_data in processor_data["processor_models"]:
        ProcessorModel.objects.filter(
            name=model_data["name"],
            codename__id=model_data["codename_id"],
            tier__id=model_data["tier_id"],
            brand__id=model_data["brand_id"]
        ).delete()

    # ---------------------------
    # Remove Processor Tiers
    # ---------------------------
    for tier_data in processor_data["processor_tiers"]:
        ProcessorTier.objects.filter(
            name=tier_data["name"],
            brand__id=tier_data["brand_id"]
        ).delete()

    # ---------------------------
    # Remove Processor Codenames
    # ---------------------------
    for codename_data in processor_data["processor_codenames"]:
        ProcessorCodename.objects.filter(
            name=codename_data["name"],
            brand__id=codename_data["brand_id"]
        ).delete()

    # ---------------------------
    # Remove Processor Brands
    # ---------------------------
    for brand_data in processor_data["brands"]:
        ProcessorBrand.objects.filter(
            name=brand_data["name"]
        ).delete()

    print("✅ Reverted all processor enums successfully.")















# def revert():
#     print("🧹 Reverting enums...")

#     # ---------------------------
#     # Remove Network Area Orders
#     # ---------------------------
#     NetworkAreaOrder.objects.filter(name__in=network_area_orders).delete()

#     # ---------------------------
#     # Remove Network Areas
#     # ---------------------------
#     NetworkArea.objects.filter(name__in=network_areas).delete()

#     # ---------------------------
#     # Remove Processor Types
#     # ---------------------------
#     for brand_name, generation, codename, model, cores, threads in processors_data:
#         try:
#             brand = ProcessorBrand.objects.get(name=brand_name)
#             family = ProcessorFamily.objects.get(
#                 brand=brand,
#                 generation=generation,
#                 codename=codename,
#             )
#         except (ProcessorBrand.DoesNotExist, ProcessorFamily.DoesNotExist):
#             continue

#         ProcessorType.objects.filter(family=family, model=model).delete()

#     # ---------------------------
#     # Remove Processor Families & Brands
#     # ---------------------------
#     for brand_name, generation, codename, *_ in processors_data:
#         ProcessorFamily.objects.filter(
#             brand__name=brand_name,
#             generation=generation,
#             codename=codename,
#         ).delete()

#         ProcessorBrand.objects.filter(name=brand_name).delete()

#     # ---------------------------
#     # Remove Storage Types
#     # ---------------------------
#     # StorageType.objects.filter(name__in=storage_types).delete()
    
#     # ---------------------------
#     # Remove Storage Interfaces
#     # ---------------------------
#     StorageInterface.objects.filter(name__in=storage_interfaces).delete()

#     # ---------------------------
#     # Remove Storage Form Factors
#     # ---------------------------
#     StorageFormFactor.objects.filter(name__in=storage_form_factors).delete()


#     # ---------------------------
#     # Remove Appliance Types
#     # ---------------------------
#     ApplianceType.objects.filter(name__in=appliance_types).delete()

#     # ---------------------------
#     # Remove Transceiver Types
#     # ---------------------------
#     TransceiverType.objects.filter(name__in=transceiver_types).delete()

#     print("✅ Enums reverted successfully!")
