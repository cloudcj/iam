processor_data = {
    "brands": [
        {"name": "Intel"},
    ],

    "processor_codenames": [
        {"name": "Ice Lake", "brand_name": "Intel"},
        {"name": "Emerald Rapids", "brand_name": "Intel"},
    ],

    "processor_tiers": [
        {"name": "Xeon Silver", "brand_name": "Intel"},
        {"name": "Xeon Gold","brand_name": "Intel"},
        {"name": "Xeon Platinum","brand_name": "Intel"},
    ],

    "processor_models": [
        # Ice Lake Models
        {"name": "5318Y", "codename_name": "Ice Lake", "tier_name": "Xeon Gold"},
        {"name": "4310",  "codename_name": "Ice Lake", "tier_name": "Xeon Silver"},
        {"name": "4510",  "codename_name": "Ice Lake", "tier_name": "Xeon Silver"},

        # Emerald Rapids Models
        {"name": "6530",  "codename_name": "Emerald Rapids", "tier_name": "Xeon Gold"},
        {"name": "8558",  "codename_name": "Emerald Rapids", "tier_name": "Xeon Platinum"},
    ]
}


# Appliance Types
appliance_types = [
    "Anti DDoS",
    "Firewall",
    "Analyzer",
    "Manager",
    "Core",
    "Router",
]
# storage interfaces
storage_interfaces = [
    "SATA",
    "NVME",
]

# storage form factors
storage_form_factors = [
    "2.5",
    "3.5",
    "M.2",
]

# Transceiver Types
transceiver_types = ["SFP", "SFP+", "SFP28", "QSFP+", "QSFP28"]

# Network Areas
network_areas = [
    "NFV",
    "LA",
    "SECUIRTY-PROD",
    "ADS-SEC",
    "SWITCHES",
    "LC",
]

# Network Area Orders
network_area_orders = [
    "NFV-TL",
    "SWITCHES-TL",
    "SWITCHES-PROD",
    "LA-02-TL",
    "LA-01-TL",
    "LA-07-PROD",
    "LA-06-PROD",
    "LA-05-PROD",
    "LA-04-PROD",
    "LA-03-PROD",
    "LA-02-PROD",
    "LA-01-PROD",
    "LC-PROD",
    "NFVW-02-PROD",
    "NFVW-01-PROD",
    "NFVL-02-PROD",
    "NFVL-01-PROD",
]
