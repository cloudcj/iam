regions_data = [{"name": "Luzon"}]

az_data = [
    {"name": "NCR-AZ1", "location": "Caloocan", "region": "Luzon"},
    {"name": "CLZ-AZ2", "location": "Angeles", "region": "Luzon"},
]

buildings_data = [
    {"name": "J3 Data Center", "az": "NCR-AZ1"},
    {"name": "Angeles Data Center", "az": "CLZ-AZ2"},
]

floors_data = [
    {"number": 1, "building": "J3 Data Center"},
    {"number": 2, "building": "J3 Data Center"},
    {"number": 3, "building": "J3 Data Center"},
]

rooms_data = [
    {"number": "201", "floor": 2, "building_id": 1},
    {"number": "202", "floor": 2, "building_id": 1},
]

pods_data = [
    {"name": "Pod 1", "room": "202"},
    {"name": "Pod 2", "room": "202"},
    {"name": "Pod 3", "room": "202"},
]

racks_data = [
    #--- POD 1 ---
    {"number": "1", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "2", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "3", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "4", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "5", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "6", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "7", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "8", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "9", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "10", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "11", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "12", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "13", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "14", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "15", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "16", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "17", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "18", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "19", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "20", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "21", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "22", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "23", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "24", "ru_count": 42, "weight": 300, "pod": "Pod 1"},
    {"number": "25", "ru_count": 42, "weight": 300, "pod": "Pod 1"},

    #--- POD 2 ---
    {"number": "1", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "2", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "3", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "4", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "5", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "6", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "7", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "8", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "9", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "10", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "11", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "12", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "13", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "14", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "15", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "16", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "17", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "18", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "19", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "20", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "21", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "22", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "23", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "24", "ru_count": 42, "weight": 300, "pod": "Pod 2"},
    {"number": "25", "ru_count": 42, "weight": 300, "pod": "Pod 2"},

    #--- POD 3 ---
    {"number": "1", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "2", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "3", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "4", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "5", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "6", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "7", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "8", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "9", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "10", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "11", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "12", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "13", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "14", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "15", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "16", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "17", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "18", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "19", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "20", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "21", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "22", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "23", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "24", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
    {"number": "25", "ru_count": 42, "weight": 300, "pod": "Pod 3"},
]

network_areas = [
    "NFV", "LA", "SECURITY-PROD", "ADS-SEC", "SWITCHES", "LC"
]

network_area_orders = [
    "NFV-TL", "SWITCHES-TL", "SWITCHES-PROD",
    "LA-02-TL", "LA-01-TL", "LA-07-PROD", "LA-06-PROD",
    "LA-05-PROD", "LA-04-PROD", "LA-03-PROD", "LA-02-PROD",
    "LA-01-PROD", "LC-PROD", "NFVW-02-PROD", "NFVW-01-PROD",
    "NFVL-02-PROD", "NFVL-01-PROD"
]
