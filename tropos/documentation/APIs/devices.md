# Device API

These APIs are accessible to most of the users.

----------------------------------------READ OPERATION--------------------------------------------

## 1. Devices - Read

**Endpoint:** `{{base_url}}/devices`

### Description

Fetches list of devices

### Request

```
GET {{base_url}}/devices
```

### Response

```json
"results": [

        # For Appliance
        {
            "id": 12,
            "type": "appliance",
            "serial_number": "SNRT001",
            "model": null,
            "rack": 26,
            "rack_unit_allocations": 2,
            "starting_position": 25,
            "ipv4_address": "192.168.1.15",
            "weight": 20,
            "power": 220.0,
            "status": "active",
            "interface_count": 2,
            "description": "Router Appliance"
        },
        {
            "id": 11,
            "type": "appliance",
            "serial_number": "SNCR001",
            "model": null,
            "rack": 26,
            "rack_unit_allocations": 3,
            "starting_position": 20,
            "ipv4_address": "192.168.1.14",
            "weight": 22,
            "power": 300.0,
            "status": "active",
            "interface_count": 2,
            "description": "Core Appliance"
        },
        {
            "id": 10,
            "type": "appliance",
            "serial_number": "SNMG001",
            "model": null,
            "rack": 26,
            "rack_unit_allocations": 2,
            "starting_position": 13,
            "ipv4_address": "192.168.1.13",
            "weight": 15,
            "power": 200.0,
            "status": "active",
            "interface_count": 2,
            "description": "Manager Appliance"
        },
        {
            "id": 9,
            "type": "appliance",
            "serial_number": "SNFW001",
            "model": null,
            "rack": 26,
            "rack_unit_allocations": 2,
            "starting_position": 9,
            "ipv4_address": "192.168.1.12",
            "weight": 18,
            "power": 250.0,
            "status": "active",
            "interface_count": 2,
            "description": "Firewall Appliance"
        },
        {
            "id": 8,
            "type": "appliance",
            "serial_number": "SNADD001",
            "model": null,
            "rack": 26,
            "rack_unit_allocations": 4,
            "starting_position": 30,
            "ipv4_address": "192.168.1.11",
            "weight": 20,
            "power": 400.0,
            "status": "active",
            "interface_count": 2,
            "description": "Anti-DDoS Appliance"
        },
        {
            "id": 7,
            "type": "appliance",
            "serial_number": "SNAN001",
            "model": null,
            "rack": 26,
            "rack_unit_allocations": 4,
            "starting_position": 4,
            "ipv4_address": "192.168.1.10",
            "weight": 25,
            "power": 350.5,
            "status": "active",
            "interface_count": 2,
            "description": "Network Analyzer Appliance"
        },

        # For Server
        {
            "id": 5,
            "type": "server",
            "serial_number": "HDM210235A2T8H252000083",
            "model": "R4900 G5",
            "rack": 7,
            "rack_unit_allocations": 2,
            "starting_position": 5,
            "ipv4_address": "10.51.0.3",
            "weight": 42,
            "power": 780.0,
            "status": "active",
            "interface_count": 4,
            "description": "Primary database server"
        },

        # For Switch
        {
            "id": 4,
            "type": "switch",
            "serial_number": "210235A2GM524CP0009L",
            "model": "S5850-54QS",
            "rack": 7,
            "rack_unit_allocations": 1,
            "starting_position": 4,
            "ipv4_address": "10.51.53.131",
            "weight": 6,
            "power": 213.0,
            "status": "active",
            "interface_count": 48,
            "description": "This is switch 1"
        },
    ]
```

## Note: There is no create endpoint for Device; creation is handled through the specific device types.
