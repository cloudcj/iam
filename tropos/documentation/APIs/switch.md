# Switch APIs

----------------------------------------READ OPERATION--------------------------------------------

# Read operation for reading all switches

## 1. Switch - READ

**Endpoint:** `{{BASE_URL}}/switches/`

### Description

Fetches a list of switches.

### Request

```
GET {{BASE_URL}}/switches/
```

### Response

```json
"results": [
        {
            "switch_name": "CAX01-2F1-RACK7-H9850H-NFVL-01",
            "device": {
                "id": 1,
                "type": "switch",
                "serial_number": "210235A4AM524CL00059",
                "model": "S9850-32H",
                "rack": 7,
                "rack_unit_allocations": 1,
                "starting_position": 1,
                "ipv4_address": "10.51.54.3",
                "weight": 10,
                "power": 385.0,
                "status": "active",
                "interface_count": 48,
                "description": "This is switch 1"
            }
        },
]
```

# Read operation for reading one switch

## 1. Switch - READ

**Endpoint:** `{{BASE_URL}}/switches/1`

### Description

Fetches a list of switches.

### Request

```
GET {{BASE_URL}}/switches/1
```

### Response

```json
{
  "switch_name": "CAX01-2F1-RACK7-H9850H-NFVL-01",
  "device": {
    "id": 1,
    "type": "switch",
    "serial_number": "210235A4AM524CL00059",
    "model": "S9850-32H",
    "rack": 7,
    "rack_unit_allocations": 1,
    "starting_position": 1,
    "ipv4_address": "10.51.54.3",
    "weight": 10,
    "power": 385.0,
    "status": "active",
    "interface_count": 48,
    "description": "This is switch 1"
  }
}
```

----------------------------------------CREATE OPERATION--------------------------------------------

## 2. Switch - Create

**Endpoint:** `{{BASE_URL}}/switches/`

### Description

Creates a switch device.

### Request

```
POST {{BASE_URL}}/switches/
```

### Request Body

```json
{
  "rack_id": 1,
  "network_area": "Main Data Hall",
  "switch_name": "Core-SW11",
  "serial_number": "SW12345678",
  "ipv4_address": "8.8.8.8",
  "rack_unit_allocations": 1,
  "rack_unit_starting_position": 34,
  "model": "Cisco Catalyst 9300",
  "generation": "Gen3",
  "description": "Main core switch for App Zone 1",
  "weight": 15,
  "power": 250,
  "interface_count": 24,
  "fan_units": [
    {
      "fan_count": 2,
      "fan_speed": 1500,
      "is_internal": true,
      "wattage_max_output": 45.0,
      "wattage_average": 35.0,
      "description": "Front intake fans"
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
