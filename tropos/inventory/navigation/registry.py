# NAVIGATION = [
#     {
#         "path": "/inventory/devices",
#         "label": "Devices",
#         "permission": "inventory.device.read",
#     },
#     {
#         "path": "/inventory/az",
#         "label": "Availability Zones",
#         "permission": "inventory.az.read",
#     },
#     {
#         "path": "/inventory/regions",
#         "label": "Regions",
#         "permission": "inventory.region.read",
#     },
#     {
#         "path": "/inventory/sample",
#         "label": "Regions",
#         "permission": "pleco.region.read",
#     },
# ]

NAVIGATION = [
    {
        "title": "Assets",
        "items": [
            {
                "path": "/inventory/switch",
                "label": "Switch",
                "permission": "inventory.switch.read",
            },
            {
                "path": "/inventory/server",
                "label": "Server",
                "permission": "inventory.server.read",
            },
        ],
    },
    {
        "title": "Infrastructure",
        "items": [
            {
                "path": "/inventory/region",
                "label": "Region",
                "permission": "inventory.region.read",
            },
            {
                "path": "/inventory/az",
                "label": "az",
                "permission": "inventory.az.read",
            },
            
        ],
    },
]

