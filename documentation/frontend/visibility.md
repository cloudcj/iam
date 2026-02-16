## Bootstrap Endpoint

    GET /api/v1/me

Purpose

Returns user context + systems + permission snapshot.

Response Example

    {
        "id": "uuid",
        "username": "alice",
        "email": "alice@example.com",

        "department": {
            "code": "CLOUD_PLATFORM",
            "label": "Cloud Platform"
        },

        "systems": [
            { "code": "inventory", "label": "Inventory" },
            { "code": "iam", "label": "IAM" }
        ],

        "permissions": {
            "inventory": [
                "region.read",
                "az.read"
            ],
            "iam": [
                "user.read"
            ]
        }
    }

## Navigation per menu endpoint

    GET /<system>/navigation

    example:

    GET /inventory/navigation

Purpose

Returns filtered navigation tree for Inventory system.

Response Example

    {
        "system": "inventory",
        "sections": [
            {
            "title": "Infrastructure",
            "items": [
                {
                    "label": "Regions",
                    "path": "/inventory/regions"
                },
                {
                    "label": "AZ",
                    "path": "/inventory/az"
                }
            ]
            }
        ]
    }
