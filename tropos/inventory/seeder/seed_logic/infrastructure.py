from inventory.infrastructure.models import (
    Region,
    AvailabilityZone,
    Building,
    Floor,
    Room,
    Pod,
    Rack,
    RackPosition,
    PowerDeliveryUnit,
)
from inventory.enums.models import NetworkArea, NetworkAreaOrder
from inventory.infrastructure.models import Environment

from ..seed_data import regions_data,az_data,buildings_data,floors_data,rooms_data,pods_data,racks_data,network_area_orders,network_areas

# ------------------------------
# Seeder function
# ------------------------------
def run():
    # ---------- REGIONS ----------
    Region.objects.bulk_create(
        [Region(name=r["name"]) for r in regions_data],
        ignore_conflicts=True
    )
    regions = {r.name: r for r in Region.objects.all()}

    # ---------- AVAILABILITY ZONES ----------
    AvailabilityZone.objects.bulk_create(
        [
            AvailabilityZone(
                name=az["name"],
                location=az["location"],
                region=regions[az["region"]]
            )
            for az in az_data
        ],
        ignore_conflicts=True
    )
    azs = {az.name: az for az in AvailabilityZone.objects.all()}

    # ---------- BUILDINGS ----------
    Building.objects.bulk_create(
        [
            Building(name=b["name"], availability_zone=azs[b["az"]])
            for b in buildings_data
        ],
        ignore_conflicts=True
    )
    buildings = {b.name: b for b in Building.objects.all()}

    # ---------- FLOORS ----------
    Floor.objects.bulk_create(
        [
            Floor(number=f["number"], building=buildings[f["building"]])
            for f in floors_data
        ],
        ignore_conflicts=True
    )
    floors = {(f.number, f.building.pk): f for f in Floor.objects.select_related("building")}

    # ---------- ROOMS ----------
    Room.objects.bulk_create(
        [
            # Room(number=r["number"], floor=floors[(r["floor"], r["building"])],building=floors[(r["floor"], r["building"])].building)
            # for r in rooms_data
            Room(
            number=r["number"],
            floor=floors[(r["floor"], r["building_id"])])
            # building_id=r["building_id"])
        for r in rooms_data
        ],
        ignore_conflicts=True
    )
    rooms = {r.number: r for r in Room.objects.all()}

    # ---------- PODS ----------
    Pod.objects.bulk_create(
        [
            Pod(name=p["name"], room=rooms[p["room"]])
            for p in pods_data
        ],
    )
    pods = {p.name: p for p in Pod.objects.all()}

    # ---------- NETWORK AREAS & ORDERS ----------
    area_objects = {a: NetworkArea.objects.get_or_create(name=a)[0] for a in network_areas}
    order_objects = {}
    for order_name in network_area_orders:
        prefix = order_name.split("-")[0]
        area = area_objects.get(prefix, list(area_objects.values())[0])
        order_objects[order_name] = NetworkAreaOrder.objects.get_or_create(area=area, name=order_name)[0]

    # ---------- RACKS ----------
    rack_instances = []
    for r in racks_data:
        pod = pods.get(r["pod"])
        if not pod:
            continue

        area_name = network_areas[0]
        order_name = next(
            (o for o in network_area_orders if o.startswith(area_name)),
            network_area_orders[0]
        )

        rack_instances.append(
            Rack(
                number=r["number"],
                pod=pod,
                weight=r["weight"],
                environment=Environment.TEST_LAB,
                network_area=area_objects[area_name],
                network_area_order=order_objects[order_name],
            )
        )
    Rack.objects.bulk_create(rack_instances)
    racks = {r.number: r for r in Rack.objects.all()}

    # ---------- RACK POSITIONS & PDUs ----------

    # map racks uniquely
    racks = {(r.pod.pk, r.number): r for r in Rack.objects.all()}
    
    rack_positions = []
    pdus = []
    for r in racks_data:
        pod = pods[r["pod"]]
        rack = racks.get((pod.pk, r["number"]))
        if not rack:
            continue
        rack_positions.extend([RackPosition(rack=rack, position_number=i + 1) for i in range(r["ru_count"])])
        pdus.extend([
            PowerDeliveryUnit(rack=rack, position="left"),
            PowerDeliveryUnit(rack=rack, position="right"),
        ])
    RackPosition.objects.bulk_create(rack_positions, ignore_conflicts=True)
    PowerDeliveryUnit.objects.bulk_create(pdus, ignore_conflicts=True)


# ------------------------------
# Revert function
# ------------------------------
def revert():
    # Delete in reverse dependency order
    PowerDeliveryUnit.objects.all().delete()
    RackPosition.objects.all().delete()
    Rack.objects.all().delete()
    Pod.objects.all().delete()
    Room.objects.all().delete()
    Floor.objects.all().delete()
    Building.objects.all().delete()
    AvailabilityZone.objects.all().delete()
    Region.objects.all().delete()
    NetworkAreaOrder.objects.all().delete()
    NetworkArea.objects.all().delete()








# from inventory.infrastructure.models import (
#     Region,
#     AvailabilityZone,
#     Building,
#     Floor,
#     Room,
#     Pod,
#     Rack,
#     RackPosition,
#     PowerDeliveryUnit,
# )
# from inventory.enums.models import NetworkArea, NetworkAreaOrder
# from inventory.infrastructure.models import Environment

# # ------------------------------
# # Data definitions
# # ------------------------------
# region_data = ['Luzon']

# az_data = [
#     ('NCR-AZ1', 'Caloocan', 'Luzon'),
#     ('CLZ-AZ2', 'Angeles', 'Luzon'),
# ]

# buildings_data = [
#     ('J3 Data Center', 'NCR-AZ1'),
#     ('Angeles Data Center', 'CLZ-AZ2'),
# ]

# floors_data = [
#     (1, 'J3 Data Center'),
#     (2, 'J3 Data Center'),
#     (3, 'J3 Data Center'),
# ]

# rooms_data = [
#     ('101', 1, 'J3 Data Center'),
#     ('102', 1, 'J3 Data Center'),
# ]

# pods_data = [
#     ('Pod 1', '102'),
#     ('Pod 2', '102'),
#     ('Pod 3', '102'),
# ]

# racks_data = [
#     ('1', 42, 300, 'Pod 1'),
#     ('2', 42, 300, 'Pod 2'),
#     ('3', 42, 300, 'Pod 3'),
# ]

# network_areas = [
#     "NFV",
#     "LA",
#     "SECURITY-PROD",
#     "ADS-SEC",
#     "SWITCHES",
#     "LC",
# ]

# network_area_orders = [
#     "NFV-TL",
#     "SWITCHES-TL",
#     "SWITCHES-PROD",
#     "LA-02-TL",
#     "LA-01-TL",
#     "LA-07-PROD",
#     "LA-06-PROD",
#     "LA-05-PROD",
#     "LA-04-PROD",
#     "LA-03-PROD",
#     "LA-02-PROD",
#     "LA-01-PROD",
#     "LC-PROD",
#     "NFVW-02-PROD",
#     "NFVW-01-PROD",
#     "NFVL-02-PROD",
#     "NFVL-01-PROD",
# ]

# # ------------------------------
# # Seeder function
# # ------------------------------
# def run():
#     # ---------- REGIONS ----------
#     Region.objects.bulk_create([Region(name=r) for r in region_data], ignore_conflicts=True)
#     regions = {r.name: r for r in Region.objects.all()}

#     # ---------- AVAILABILITY ZONES ----------
#     AvailabilityZone.objects.bulk_create(
#         [AvailabilityZone(name=az_name, location=location, region=regions[region_name])
#          for az_name, location, region_name in az_data],
#         ignore_conflicts=True
#     )
#     azs = {az.name: az for az in AvailabilityZone.objects.all()}

#     # ---------- BUILDINGS ----------
#     Building.objects.bulk_create(
#         [Building(name=b_name, availability_zone=azs[az_name])
#          for b_name, az_name in buildings_data],
#         ignore_conflicts=True
#     )
#     buildings = {b.name: b for b in Building.objects.all()}

#     # ---------- FLOORS ----------
#     Floor.objects.bulk_create(
#         [Floor(number=num, building=buildings[b_name])
#          for num, b_name in floors_data],
#         ignore_conflicts=True
#     )
#     floors = {(f.number, f.building.name): f for f in Floor.objects.select_related("building")}

#     # ---------- ROOMS ----------
#     Room.objects.bulk_create(
#         [Room(number=r_num, floor=floors[(f_num, b_name)])
#          for r_num, f_num, b_name in rooms_data],
#         ignore_conflicts=True
#     )
#     rooms = {r.number: r for r in Room.objects.all()}

#     # ---------- PODS ----------
#     Pod.objects.bulk_create(
#         [Pod(name=p_name, room=rooms[r_num])
#          for p_name, r_num in pods_data],
#         ignore_conflicts=True
#     )
#     pods = {p.name: p for p in Pod.objects.all()}

#     # ---------- NETWORK AREAS & ORDERS ----------
#     area_objects = {a: NetworkArea.objects.get_or_create(name=a)[0] for a in network_areas}
#     order_objects = {}
#     for order_name in network_area_orders:
#         prefix = order_name.split("-")[0]
#         area = area_objects.get(prefix, list(area_objects.values())[0])
#         order_objects[order_name] = NetworkAreaOrder.objects.get_or_create(area=area, name=order_name)[0]

#     # ---------- RACKS ----------
#     rack_instances = []
#     for rack_number, ru_count, weight, pod_name in racks_data:
#         pod = pods.get(pod_name)
#         if not pod:
#             continue
#         # Network area assignment (same for all racks)
#         area_name = network_areas[0]
#         order_name = next(
#             (o for o in network_area_orders if o.startswith(area_name)),
#             network_area_orders[0]
#         )
#         rack_instances.append(
#             Rack(
#                 number=rack_number,
#                 pod=pod,
#                 weight=weight,
#                 environment=Environment.TEST_LAB,
#                 network_area=area_objects[area_name],
#                 network_area_order=order_objects[order_name],
#             )
#         )
#     Rack.objects.bulk_create(rack_instances, ignore_conflicts=True)
#     racks = {r.number: r for r in Rack.objects.all()}

#     # ---------- RACK POSITIONS & PDUs ----------
#     rack_positions = []
#     pdus = []
#     for rack_number, ru_count, _, pod_name in racks_data:
#         rack = racks.get(rack_number)
#         if not rack:
#             continue
#         rack_positions.extend([RackPosition(rack=rack, position_number=i+1) for i in range(ru_count)])
#         pdus.extend([
#             PowerDeliveryUnit(rack=rack, position="left"),
#             PowerDeliveryUnit(rack=rack, position="right"),
#         ])
#     RackPosition.objects.bulk_create(rack_positions, ignore_conflicts=True)
#     PowerDeliveryUnit.objects.bulk_create(pdus, ignore_conflicts=True)


# # ------------------------------
# # Revert function
# # ------------------------------
# def revert():
#     Region.objects.all().delete()
#     AvailabilityZone.objects.all().delete()
#     Building.objects.all().delete()
#     Floor.objects.all().delete()
#     Room.objects.all().delete()
#     Pod.objects.all().delete()
#     Rack.objects.all().delete()
#     RackPosition.objects.all().delete()
#     PowerDeliveryUnit.objects.all().delete()
#     NetworkAreaOrder.objects.all().delete()
#     NetworkArea.objects.all().delete()




# from inventory.infrastructure.models import (
#   Area, 
#   Building, 
#   Floor, 
#   Room, 
#   Pod, 
#   Rack, 
#   RackPosition, 
#   PowerDeliveryUnit
#   )

# # Default data
# default_areas = ['Caloocan', 'Angeles']

# buildings_data = [
#     ('J3 Data Center', 'Caloocan'),
#     ('Angeles Data Center', 'Angeles'),
# ]

# floors_data = [
#     (1, 'J3 Data Center'),
#     (2, 'J3 Data Center'),
#     (3, 'J3 Data Center'),
#     (1, 'Angeles Data Center'),
#     (2, 'Angeles Data Center'),
#     (3, 'Angeles Data Center'),
# ]

# rooms_data = [
#     ('101', 1, 'J3 Data Center'),
#     ('102', 1, 'J3 Data Center'),
#     ('201', 2, 'Angeles Data Center'),
#     ('202', 2, 'Angeles Data Center'),
# ]

# pods_data = [
#     ('Pod 1', '101'),
#     ('Pod 2', '201'),
#     ('Pod 3', '201'),
# ]

# racks_data = [
#     ('1', 42, 300, 'Pod 1'),
#     ('2', 42, 300, 'Pod 2'),
#     ('3', 42, 300, 'Pod 3'),
# ]

# def run():
#   # --- AREAS ---
#   Area.objects.bulk_create([Area(location=loc) for loc in default_areas], ignore_conflicts=True)
#   areas = {a.location: a for a in Area.objects.all()}

#   # --- BUILDINGS ---
#   Building.objects.bulk_create(
#       [Building(name=building_name, area=areas[area_location])
#         for building_name, area_location in buildings_data if area_location in areas],
#       ignore_conflicts=True
#   )
#   buildings = {b.name: b for b in Building.objects.all()}

#   # --- FLOORS ---
#   Floor.objects.bulk_create(
#       [Floor(number=floor_number, building=buildings[building_name])
#         for floor_number, building_name in floors_data if building_name in buildings],
#       ignore_conflicts=True
#   )
#   floors = {(f.number, f.building.name): f for f in Floor.objects.select_related("building")}

#   # --- ROOMS ---
#   Room.objects.bulk_create(
#       [Room(number=room_number, floor=floors[(floor_number, building_name)])
#         for room_number, floor_number, building_name in rooms_data
#         if (floor_number, building_name) in floors],
#       ignore_conflicts=True
#   )
#   rooms = {r.number: r for r in Room.objects.all()}

#   # --- PODS ---
#   Pod.objects.bulk_create(
#       [Pod(name=pod_name, room=rooms[room_number])
#         for pod_name, room_number in pods_data if room_number in rooms],
#       ignore_conflicts=True
#   )
#   pods = {p.name: p for p in Pod.objects.all()}

#   # --- RACKS ---
#   Rack.objects.bulk_create(
#       [Rack(number=rack_number, pod=pods[pod_name], weight=weight)
#         for rack_number, ru_count, weight, pod_name in racks_data if pod_name in pods],
#       ignore_conflicts=True
#   )
#   racks = {r.number: r for r in Rack.objects.all()}

#   # --- RACK POSITIONS + PDUs ---
#   rack_positions = []
#   pdus = []
#   for rack_number, ru_count, weight, pod_name in racks_data:
#       rack = racks.get(rack_number)
#       if not rack:
#           continue
#       rack_positions.extend([RackPosition(rack=rack, position_number=i+1) for i in range(ru_count)])
#       pdus.extend([
#           PowerDeliveryUnit(rack=rack, position="left"),
#           PowerDeliveryUnit(rack=rack, position="right"),
#       ])

#   RackPosition.objects.bulk_create(rack_positions, ignore_conflicts=True)
#   PowerDeliveryUnit.objects.bulk_create(pdus, ignore_conflicts=True)

# def revert():
#   # Delete in correct order (respect FKs)
#   PowerDeliveryUnit.objects.all().delete()
#   RackPosition.objects.all().delete()
#   Rack.objects.all().delete()
#   Pod.objects.all().delete()
#   Room.objects.all().delete()
#   Floor.objects.all().delete()
#   Building.objects.all().delete()
#   Area.objects.all().delete()