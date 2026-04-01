appliances_data = [
  
    #-------------------- POD 1 - RACK 9 -----------------------
    {
        "type": "appliance",
        "appliance_type": "Router",
        "name": "CAX01-2F-1-RACK9-MSR3640-OB-Router-01",
        "serial_number": "210235A2YL524AP000ML",
        "model": "MSR3640-X1",
        "rack_number": "9",
        "pod_name": "Pod 1",
        "rack_alloc": 2,
        "starting_position": 31,
        "description": "TL - Router - Role: Out-of-Band Router",
        "interface_count": 14,
        "fan_count": 2,
        "ipv4_address": "10.51.53.60",
        "power": 701,
        "weight": 11.2, 
        "is_chassis": False,
            "appliance_chassis": [],
        "has_components_units": False,
            "memory_units": [],
            "processors": [],
            "storage_units": [],

    },
    
    #-------------------- POD 2 - RACK 9 -----------------------
    {
        "type": "appliance",
        "appliance_type": "Router",
        "name": "CAX01-2F-2-RACK24-MSR3640-OB-Router-01",
        "serial_number": "210235A4AM524CL00034",
        "model": "MSR3640-X1",
        "rack_number": "24",
        "pod_name": "Pod 2",
        "rack_alloc": 2,
        "starting_position": 27,
        "description": "PROD - Router -  Role: Out-of-Band Router",
        "interface_count": 14,
        "fan_count": 2,
        "ipv4_address": "10.50.53.60",
        "power": 688,
        "weight": 11.2, # To be verified
        "is_chassis": False,
            "appliance_chassis": [],
        "has_components_units": False,
            "memory_units": [],
            "processors": [],
            "storage_units": [],
    },
    
    #-------------------- POD 1 - RACK 11 -----------------------
    {
        "type": "appliance",
        "appliance_type": "Firewall",
        "name": "CAX01-2F-1-RACK11-7121F-WAN-FW-02",
        "serial_number": "F7CF1ATB22000023",
        "model": "FG-7121F",
        "rack_number": "11",
        "pod_name": "Pod 2",
        "rack_alloc": 16,
        "starting_position": 15,
        "description": "PROD - Firewall - Perimeter Firewall",
        "interface_count": 32, # To be verified
        "fan_count": 6,
        "ipv4_address": "10.50.53.53",
        "power": 9754,
        "weight": 203.1, 
        "is_chassis": True,
        #     "appliance_chassis": [
#             {"module_name": "Analyzer-Module-1", "serial_number": "AN-CH1", "slot_position": 1},
#             {"module_name": "Analyzer-Module-2", "serial_number": "AN-CH2", "slot_position": 2}
#         ]
        "has_components_units": False,
            "memory_units": [],
            "processors": [],
            "storage_units": [],
    },
    
    #-------------------- POD 1 - RACK 25 -----------------------
    {
        "type": "appliance",
        "appliance_type": "Manager",
        "name": "CAX01-2F-1-RACK25-HD2700-ADSM-02",
        "serial_number": "25-08-P-0114",
        "model": "ADS-M01",
        "rack_number": "25",
        "pod_name": "Pod 1",
        "rack_alloc": 2,
        "starting_position":29,
        "description": "PROD - Manager - Anti-DDoS Management ",
        "interface_count": 8, 
        "fan_count": 2,
        "ipv4_address": "10.50.53.56",
        "power": 350,
        "weight": 16.6, 
        "is_chassis": False,
            "appliance_chassis": [],
        "has_components_units": False,
            "memory_units": [],
            "processors": [],
            "storage_units": [],
    },
    
    #-------------------- POD 1 - RACK 25 -----------------------
    {
        "type": "appliance",
        "appliance_type": "Anti DDoS",
        "name": "CAX01-2F-1-RACK25-20000-DDOS-02",
        "serial_number": "25-08-P-0117",
        "model": "ADSNX5",
        "rack_number": "25",
        "pod_name": "Pod 1",
        "rack_alloc": 6,
        "starting_position": 21,
        "description": "PROD - Anti DDoS - Anti DDoS ",
        "interface_count": 8, 
        "fan_count": 2,
        "ipv4_address": "10.50.53.52",
        "power": 8000,
        "weight": 12, 
        "is_chassis": False,
            "appliance_chassis": [],
        "has_components_units": False,
            "memory_units": [],
            "processors": [],
            "storage_units": [],
    },
    
    #-------------------- POD 2 - RACK 25 -----------------------
    {
        "type": "appliance",
        "appliance_type": "Manager",
        "name": "CAX01-2F-2-RACK24-200G-FRTMNGR-02",
        "serial_number": "FMG2HGTA22000077",
        "model": "FM200G",
        "rack_number": "25",
        "pod_name": "Pod 2",
        "rack_alloc": 1,
        "starting_position": 36,
        "description": "PROD - Manager - Role: FortiManager ",
        "interface_count": 4,
        "fan_count": 4,
        "ipv4_address": "10.50.52.18",
        "power": 99,
        "weight": 10.2, # To be verified
        "is_chassis": False,
            "appliance_chassis": [],
        "has_components_units": False,
            "memory_units": [],
            "processors": [],
            "storage_units": [],
    },
    
    #-------------------- POD 2 - RACK 25 -----------------------
    {
        "type": "appliance",
        "appliance_type": "Firewall",
        "name": "CAX01-2F-2-RACK24-400F-FRTGT-02",
        "serial_number": "FG4H0FT923913541",
        "model": "FG400F",
        "rack_number": "25",
        "pod_name": "Pod 2",
        "rack_alloc": 1,
        "starting_position": 32,
        "description": "PROD - Firewall - Perimeter Firewall",
        "interface_count": 34,
        "fan_count": 2,
        "ipv4_address": "",# To be verified
        "power": 180,
        "weight": 6.4, # To be verified
        "is_chassis": False,
            "appliance_chassis": [],
        "has_components_units": False,
            "memory_units": [],
            "processors": [],
            "storage_units": [],
    },
    
    #-------------------- POD 2 - RACK 25 -----------------------
    {
        "type": "appliance",
        "appliance_type": "Analyzer",
        "name": "CAX01-2F-2-RACK24-3700G-FRTNLYZR-02",
        "serial_number": "FL3K7GT324000033",
        "model": "FAZ-3700G",
        "rack_number": "25",
        "pod_name": "Pod 2",
        "rack_alloc": 4,
        "starting_position": 25,
        "description": "PROD - Analyzer - FortiAnalyzer",
        "interface_count": 4,
        "fan_count": 4,
        "ipv4_address": "10.50.52.21",
        "power": 2000,
        "weight": 53.5,
        "is_chassis": False,
            "appliance_chassis": [],
        "has_components_units": True,
        #     "memory_units": [
        #         {"ram_capacity": 16, "quantity": 4}
        #     ],
        #     "processors": [
        #         {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        #     ],
        #     "storage_units": [
        #         {"storage_type": "SSD",
        #         "storage_capacity": 1024,
        #         "storage_count": 2,
        #         "capacity_unit": "GB",
        #         "storage_interface": {"name": "SATA"},
        #         "form_factor": {"name": "2.5"}
        #     }
        # ],
    },

]
