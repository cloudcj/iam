# Server APIs

----------------------------------------READ OPERATION--------------------------------------------

# Read operation for reading all servers

## 1. Switch - READ

**Endpoint:** `{{BASE_URL}}/servers/`

### Description

Fetches a list of servers.

### Request

```
GET {{BASE_URL}}/servers/
```

### Response

```json
"results": [
        {
            "server_name": "clb-1-eip-1-product-clb-tgw3weip-rip-1-1",
            "classification": "Network",
            "device": {
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
            }
        },
        {
            "server_name": "vpc-1-nfv-host-1-nfv-vm-host-1-1",
            "classification": "Network",
            "device": {
                "id": 6,
                "type": "server",
                "serial_number": "HDM210235A2T8H252000089",
                "model": "R4900 G5",
                "rack": 7,
                "rack_unit_allocations": 2,
                "starting_position": 7,
                "ipv4_address": "10.51.12.195",
                "weight": 42,
                "power": 780.0,
                "status": "active",
                "interface_count": 4,
                "description": "Primary database server"
            }
        }
    ]
```

# Read operation for reading one server

## 1. Switch - READ

**Endpoint:** `{{BASE_URL}}/servers/1`

### Description

Fetches a list of switches.

### Request

```
GET {{BASE_URL}}/servers/1
```

### Response

```json
{
  "server_name": "vpc-1-nfv-host-1-nfv-vm-host-1-1",
  "classification": "Network",
  "device": {
    "id": 6,
    "type": "server",
    "serial_number": "HDM210235A2T8H252000089",
    "model": "R4900 G5",
    "rack": 7,
    "rack_unit_allocations": 2,
    "starting_position": 7,
    "ipv4_address": "10.51.12.195",
    "weight": 42,
    "power": 780.0,
    "status": "active",
    "interface_count": 4,
    "description": "Primary database server"
  },
  "memory_units": [
    {
      "id": 2,
      "ram_capacity": 32,
      "quantity": 12
    }
  ],
  "processor_units": [
    {
      "id": 3,
      "processor_codename": {
        "id": 1,
        "name": "Ice Lake"
      },
      "processor_tier": {
        "id": 2,
        "name": "Xeon Gold"
      },
      "processor_model": {
        "id": 1,
        "name": "5318Y"
      }
    },
    {
      "id": 4,
      "processor_codename": {
        "id": 1,
        "name": "Ice Lake"
      },
      "processor_tier": {
        "id": 2,
        "name": "Xeon Gold"
      },
      "processor_model": {
        "id": 1,
        "name": "5318Y"
      }
    }
  ],
  "storage_units": [
    {
      "id": 2,
      "storage_type": "SSD",
      "storage_interface": 1,
      "form_factor": 1,
      "storage_capacity": 480,
      "storage_count": 1,
      "capacity_unit": "GB"
    }
  ]
}
```

----------------------------------------CREATE OPERATION--------------------------------------------

## 2. Server - Create

**Endpoint:** `{{BASE_URL}}/servers/`

### Description

Creates a server device.

### Request

```
POST {{BASE_URL}}/servers/
```

### Request Body

```json
{
  "classification": "Application",
  "server_name": "sample",
  "serial_number": "SRV123456789",
  "rack_unit_allocations": 2,
  "rack_unit_starting_position": 32,
  "ipv4_address": "8.8.8.8",
  "description": "Main application server",
  "rack_id": 10,
  "weight": 15,
  "power": 250,
  "interface_count": 4,

  "memory_units": [{ "ram_capacity": 32, "quantity": 2 }],

  "processor_units": [
    { "processor_codename": 1, "processor_tier": 2, "processor_model": 1 }
  ],

  "storage_units": [
    {
      "storage_type": "SSD",
      "storage_interface": 2,
      "form_factor": 1,
      "storage_capacity": 1024,
      "storage_count": 2,
      "capacity_unit": "GB"
    }
  ],

  "power_supply_units": [
    {
      "max_output": 750,
      "heat_dissipation": 50.5,
      "average_output": 500.0,
      "wattage_percentage": 85.5,
      "power_type": "AC",
      "connector_type": "24-pin ATX",
      "description": "Main PSU for server"
    }
  ],

  "fan_units": [
    {
      "fan_count": 2,
      "fan_speed": 1500,
      "is_internal": true,
      "wattage_max_output": 45.0,
      "wattage_average": 35.0,
      "description": "Front intake fans"
    }
  ]
}
```

### Response

```json
{
  "message": "Switch created successfully."
}
```

----------------------------------------UPDATE OPERATION--------------------------------------------

## 3. Dialysis Machine Update

**Endpoint:** `{{BASE_URL}}/switches/5/`

### Description

Update the switch device.

### Request

```
PATCH {{BASE_URL}}/switches/5/
```

### Request Body

```json
{
  "switch_name": "Edge Switch updated sjdkdjsdf - Full Updated",
  "model": "Cisco Catalyst 9300",
  "device": {
    "serial_number": "SW123456-UPDATED",
    "rack_unit_allocations": 3,
    "starting_position": 12,
    "interface_count": 48,
    "rack": 2,
    "weight": 16,
    "power": 260,
    "description": "Updated core switch in Rack 2"
  },
  "power_supply_units": [
    {
      "max_output": 500,
      "description": "PSU 1"
    },
    {
      "max_output": 500,
      "description": "PSU 2"
    }
  ],
  "fan_units": [
    {
      "fan_count": 2,
      "fan_speed": 4000,
      "description": "Fan Unit 1"
    }
  ],
  "interface_count": 48
}
```

### Response

```json
{
  "switch_name": "switch name"
}
```

----------------------------------------DELETE OPERATION--------------------------------------------

## 4. Device - Delete

**EndPoint:** `{{BASE_URL}}/switches/1/`

### Description

Delete a dialysis machine record.

### Request

```
DELETE {{BASE_URL}}/switches/1/
```

### Response

```json
{
  "message": "Switch successfully deleted."
}
```

# (END)
