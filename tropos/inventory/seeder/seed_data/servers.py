# myapp/seeders/seed_data/servers.py

servers_data = [

    #-------------------- POD 1 - RACK 3 -----------------------
    {
        "pod_name": "Pod 1",
        "rack_number": "3",
        "rack_alloc":2,
        "starting_position": 18,
        "type": "server",
        "name": "cosv3-1-cell-1-yottastore-1-06",
        "module_name": "T3-SC71XE-25G",
        "model": "R4900 G6",
        "classification": "Network",
        "serial_number": "HDM210235A4TGH252000014",
        "ipv4_address": "10.51.17.147",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Data Storage Node",
    },

    {
        "pod_name": "Pod 1",
        "rack_number": "3",
        "rack_alloc":2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-lavadbcell-1-06",
        "module_name": "T3-SC71XE-25G",
        "model": "R4900 G6",
        "classification": "Network",
        "serial_number": "HDM210235A4TEH252000003",
        "ipv4_address": "10.51.17.144",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Index Storage Node",
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "3",
        "rack_alloc":2,
        "starting_position": 12,
        "type": "server",
        "name": "cfs-1-cell-1-cfs-nasagent-1-02",
        "module_name": "T3-CS50XE-25G",
        "model": "R4900 G5",
        "classification": "Network",
        "serial_number": "HDM210235A2T8H252000005",
        "ipv4_address": "10.51.17.141",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "CFS NAS Head",
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "3",
        "rack_alloc":2,
        "starting_position": 9,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-1-02",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Network",
        "serial_number": "HDM210235A2T5H252000238",
        "ipv4_address": "10.51.17.138",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "Storage Pool HDD",
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "3",
        "rack_alloc":2,
        "starting_position": 6,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-06",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Network",
        "serial_number": "HDM210235A2T8H252000065",
        "ipv4_address": "10.51.17.135",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)",
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "3",
        "rack_alloc":2,
        "starting_position": 3,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-master-1-02",
        "module_name": "T3-SW59XE-25G",
        "model": "R4900 G5",
        "classification": "Network",
        "serial_number": "HDM210235A2T5H252000010",
        "ipv4_address": "10.51.17.132",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Master Node)",
    },

    #-------------------- POD 1 - RACK 4 -----------------------
    {
        "pod_name": "Pod 1",
        "rack_number": "4",
        "rack_alloc":2,
        "starting_position": 18,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-02",
        "module_name": "T3-CS81XE-25G",
        "model": "R4900 G6",
        "classification": "Network",
        "serial_number": "HDM210235A4TEH252000042",
        "ipv4_address": "10.51.17.148",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "CVM Node",
    },

    {
        "pod_name": "Pod 1",
        "rack_number": "4",
        "rack_alloc":2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-yottastore-1-02",
        "module_name": "T3-SW81XE-25G",
        "model": "R4900 G6",
        "classification": "Network",
        "serial_number": "HDM210235A4TGH252000016",
        "ipv4_address": "10.51.17.145",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Data Storage Node",
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "4",
        "rack_alloc":2,
        "starting_position": 12,
        "type": "server",
        "name": "cosv3-1-cell-1-lavadbcell-1-02",
        "module_name": "T3-SH71XE-25G",
        "model": "R4900 G5",
        "classification": "Network",
        "serial_number": "HDM210235A4TEH252000006",
        "ipv4_address": "10.51.17.142",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Index Storage Node",
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "4",
        "rack_alloc":2,
        "starting_position": 9,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-1-04",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Network",
        "serial_number": "HDM210235A2T5H252000224",
        "ipv4_address": "10.51.17.139",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "Storage Pool HDD",
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "4",
        "rack_alloc":2,
        "starting_position": 6,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-08",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Network",
        "serial_number": "HDM210235A2T8H252000076",
        "ipv4_address": "10.51.17.136",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)",
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "4",
        "rack_alloc":2,
        "starting_position": 3,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-02",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Network",
        "serial_number": "HDM210235A2T8H252000062",
        "ipv4_address": "10.51.17.133",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],     
        "storage_units": [
            {
                "storage_type": "SSD",                # TextChoices in StorageUnit
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
                "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12},
        ],  
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Master Node)",
    },


    #-------------------- POD 1 - RACK 5 -----------------------
    
    {
        "pod_name": "Pod 1",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 18,
        "type": "server",
        "name": "inta-1-core-1-inta-core-ip-1-01",
        "module_name": "T3-SW81XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TGH252000021",
        "ipv4_address": "10.51.17.149",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "NTA analysis platform hardware server"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-yottastore-1-04",
        "module_name": "T3-SW81XE-25G",
        "model": "R4900 G6",
        "classification": "Storage",
        "serial_number": "HDM210235A4TGH252000010",
        "ipv4_address": "10.51.17.146",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Data Storage Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 12,
        "type": "server",
        "name": "cosv3-1-cell-1-lavadbcell-1-04",
        "module_name": "T3-SH71XE-25G",
        "model": "R4900 G6",
        "classification": "Storage",
        "serial_number": "HDM210235A4TEH252000014",
        "ipv4_address": "10.51.17.143",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Index Storage Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 9,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-1-06",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T5H252000241",
        "ipv4_address": "10.51.17.140",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "Storage Pool HDD"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-09",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000066",
        "ipv4_address": "10.51.17.137",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 3,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-03",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000075",
        "ipv4_address": "10.51.17.134",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)"
    },


    #-------------------- POD 1 - RACK 7 -----------------------
    
    {
        "pod_name": "Pod 1",
        "rack_number": "7",
        "rack_alloc": 2,
        "starting_position": 21,
        "type": "server",
        "name": "nips-1-nipsprobe-1-nips-probe-group-1-1",
        "module_name": "T3-NS82XE-10G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000022",
        "ipv4_address": "10.51.1.163",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "NIPS probe node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "7",
        "rack_alloc": 2,
        "starting_position": 18,
        "type": "server",
        "name": "inta-1-core-1-inta-probe-ip-1-1",
        "module_name": "T3-NS82XE-10G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000026",
        "ipv4_address": "10.51.1.164",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "NTA traffic probe hardware server"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "7",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "vpc-1-nfv-host-1-nfv-vm-host-1-1",
        "module_name": "T3-NS51XE-100G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000089",
        "ipv4_address": "10.51.12.195",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "EIPGateway"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "7",
        "rack_alloc": 2,
        "starting_position": 3,
        "type": "server",
        "name": "clb-1-eip-1-product-clb-tgw3weip-rip-1-1",
        "module_name": "T3-NS51XE-100G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000083",
        "ipv4_address": "10.51.0.3",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "EIPGateway"
    },


    #-------------------- POD 1 - RACK 8 -----------------------
    
    {
        "pod_name": "Pod 1",
        "rack_number": "8",
        "rack_alloc": 2,
        "starting_position": 12,
        "type": "server",
        "name": "nips-1-nipsprobe-1-nips-probe-group-1-2",
        "module_name": "T3-NS82XE-10G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000024",
        "ipv4_address": "10.51.1.165",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "NIPS probe node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "8",
        "rack_alloc": 2,
        "starting_position": 9,
        "type": "server",
        "name": "inta-1-core-1-inta-probe-ip-1-2",
        "module_name": "T3-NS82XE-10G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000027",
        "ipv4_address": "10.51.1.166",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "NTA traffic probe hardware server"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "8",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "vpc-1-nfv-host-1-nfv-vm-host-1-2",
        "module_name": "T3-NS51XE-100G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000080",
        "ipv4_address": "10.51.12.196",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "EIPGateway"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "8",
        "rack_alloc": 2,
        "starting_position": 3,
        "type": "server",
        "name": "clb-1-eip-1-product-clb-tgw3weip-rip-1-2",
        "module_name": "T3-NS51XE-100G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000086",
        "ipv4_address": "10.51.0.4",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "EIPGateway"
    },


    #-------------------- POD 1 - RACK 9 -----------------------
    #-------------------- POD 1 - RACK 25 -----------------------
    {
        "pod_name": "Pod 1",
        "rack_number": "10",
        "rack_alloc": 1,
        "starting_position": 28,
        "type": "server",
        "name": "CAX01-2F-1-RACK10-G5-AAA-02",
        "module_name": "R4900 G5",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2RAH251000150",
        "ipv4_address": "10.51.53.4",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "Authentication, Authorization, and Accounting"
    },
   
    #-------------------- POD 1 - RACK 15 -----------------------

    {
        "pod_name": "Pod 1",
        "rack_number": "15",
        "rack_alloc": 2,
        "starting_position": 18,
        "type": "server",
        "name": "cosv3-1-cell-1-yottastore-1-05",
        "module_name": "T3-SW81XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TGH252000019",
        "ipv4_address": "10.51.17.19",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Data Storage Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "15",
        "rack_alloc": 2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-lavadbcell-1-04",
        "module_name": "T3-SH71XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000011",
        "ipv4_address": "10.51.17.16",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Index Storage Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "15",
        "rack_alloc": 2,
        "starting_position": 12,
        "type": "server",
        "name": "cfs-1-cell-1-cfs-nasagent-1-01",
        "module_name": "T3-CS50XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000084",
        "ipv4_address": "10.51.17.13",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "CFS NAS Head"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "15",
        "rack_alloc": 2,
        "starting_position": 9,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-1-01",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T5H252000234",
        "ipv4_address": "10.51.17.10",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "Storage pool HDD"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "15",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-04",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000061",
        "ipv4_address": "10.51.17.7",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "15",
        "rack_alloc": 2,
        "starting_position": 3,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-master-1-01",
        "module_name": "T3-SW59XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T5H252000009",
        "ipv4_address": "10.51.17.4",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Master Node)"
    },

    #-------------------- POD 1 - RACK 16 -----------------------

    {
        "pod_name": "Pod 1",
        "rack_number": "16",
        "rack_alloc": 2,
        "starting_position": 18,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-01",
        "module_name": "T3-CS81XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000060",
        "ipv4_address": "10.51.17.20",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "16",
        "rack_alloc": 2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-yottastore-1-01",
        "module_name": "T3-SW81XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TGH252000007",
        "ipv4_address": "10.51.17.17",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Data Storage Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "16",
        "rack_alloc": 2,
        "starting_position": 12,
        "type": "server",
        "name": "cosv3-1-cell-1-lavadbcell-1-03",
        "module_name": "T3-SH71XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000005",
        "ipv4_address": "10.51.17.14",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Index Storage Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "16",
        "rack_alloc": 2,
        "starting_position": 9,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-1-03",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T5H252000212",
        "ipv4_address": "10.51.17.11",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "Storage pool HDD"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "16",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-05",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000074",
        "ipv4_address": "10.51.17.8",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "16",
        "rack_alloc": 2,
        "starting_position": 3,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-master-1-03",
        "module_name": "T3-SW59XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T5H252000011",
        "ipv4_address": "10.51.17.5",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Master Node)"
    },


    #-------------------- POD 1 - RACK 17 -----------------------
    {
        "pod_name": "Pod 1",
        "rack_number": "17",
        "rack_alloc": 2,
        "starting_position": 18,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-03",
        "module_name": "T3-CS81XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000052",
        "ipv4_address": "10.51.17.21",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "17",
        "rack_alloc": 2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-yottastore-1-03",
        "module_name": "T3-SW81XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TGH252000015",
        "ipv4_address": "10.51.17.18",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Data Storage Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "17",
        "rack_alloc": 2,
        "starting_position": 12,
        "type": "server",
        "name": "cosv3-1-cell-1-lavadbcell-1-03",
        "module_name": "T3-SH71XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000007",
        "ipv4_address": "10.51.17.15",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "COS Index Storage Node"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "17",
        "rack_alloc": 2,
        "starting_position": 9,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-1-05",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T5H252000221",
        "ipv4_address": "10.51.17.12",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "Storage pool HDD"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "17",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-07",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000071",
        "ipv4_address": "10.51.17.9",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)"
    },
    {
        "pod_name": "Pod 1",
        "rack_number": "17",
        "rack_alloc": 2,
        "starting_position": 3,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-01",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000077",
        "ipv4_address": "10.51.17.6",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "SSD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 780.0,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)"
    },

    #-------------------- POD 2 - RACK  -----------------------


    {
        "pod_name": "Pod 2",
        "rack_number": "4",
        "rack_alloc": 2,
        "starting_position": 27,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-67",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000058",
        "ipv4_address": "10.50.17.220",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "4",
        "rack_alloc": 2,
        "starting_position": 24,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-46",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000095",
        "ipv4_address": "10.50.17.217",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "4",
        "rack_alloc": 2,
        "starting_position": 21,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-25",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000087",
        "ipv4_address": "10.50.17.214",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "4",
        "rack_alloc": 2,
        "starting_position": 18,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-04",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000046",
        "ipv4_address": "10.50.17.211",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "4",
        "rack_alloc": 2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-lavadbcell-1-03",
        "module_name": "T3-SH71XE-25G",
        "model": "R4900 G6",
        "classification": "Storage",
        "serial_number": "HDM210235A4TEH252000010",
        "ipv4_address": "10.50.17.208",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 8}
        ],
        "power": 610,
        "weight": 39.5,
        "description": "COS Index Storage Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "4",
        "rack_alloc": 2,
        "starting_position": 12,
        "type": "server",
        "name": "cbs-1-cell-2-cbs-depot-ec-cell-3-06",
        "module_name": "T3-SH54XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T8H252000040",
        "ipv4_address": "10.50.17.205",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
             {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
        "description": "Storage pool SSD"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "4",
        "rack_alloc": 2,
        "starting_position": 9,
        "type": "server",
        "name": "cbs-1-cell-2-cbs-depot-ec-cell-1-06",
        "module_name": "T3-SH54XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T8H252000039",
        "ipv4_address": "10.50.17.202",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
             {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
        "description": "Storage pool SSD"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "4",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-1-11",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T5H252000230",
        "ipv4_address": "10.50.17.199",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,
        "description": "Storage pool HDD"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "4",
        "rack_alloc": 2,
        "starting_position": 3,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-04",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000070",
        "ipv4_address": "10.50.17.196",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
            {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 4,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 8}
        ],
        "power": 580,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 27,
        "type": "server",
        "name": "inta-1-core-1-inta-core-ip-1-02",
        "module_name": "T3-SW81XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TGH252000024",
        "ipv4_address": "10.50.17.221",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 1127,
        "weight": 39.5,
        "description": "NTA analysis platform hardware server"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 24,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-51",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000048",
        "ipv4_address": "10.50.17.218",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 21,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-30",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000061",
        "ipv4_address": "10.50.17.215",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 18,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-09",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000049",
        "ipv4_address": "10.50.17.212",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-yottastore-1-02",
        "module_name": "T3-SC71XE-25G",
        "model": "R4900 G6",
        "classification": "Storage",
        "serial_number": "HDM210235A4TGH252000005",
        "ipv4_address": "10.50.17.209",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 756,
        "weight": 39.5,
        "description": "COS Data Storage Node"
    },

    {
        "pod_name": "Pod 2",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 12,
        "type": "server",
        "name": "cbs-1-cell-2-cbs-depot-ec-cell-3-07",
        "module_name": "T3-SH54XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T8H252000041",
        "ipv4_address": "10.50.17.206",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
        "description": "Storage pool SSD"
    },
    
    {
        "pod_name": "Pod 2",
        "rack_number": "9",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-2-09",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T5H252000231",
        "ipv4_address": "10.50.17.137",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,
        "description": "Storage pool HDD"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 3,
        "type": "server",
        "name": "tcs-core-1-base-1-tcs-global-node-1-11",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000068",
        "ipv4_address": "10.50.17.197",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
            {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 4,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 8}
        ],
        "power": 580,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "6",
        "rack_alloc": 2,
        "starting_position": 27,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-57",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000067",
        "ipv4_address": "10.50.17.219",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "6",
        "rack_alloc": 2,
        "starting_position": 24,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-36",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000044",
        "ipv4_address": "10.50.17.216",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "6",
        "rack_alloc": 2,
        "starting_position": 21,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-15",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000062",
        "ipv4_address": "10.50.17.213",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "8",
        "rack_alloc": 2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-lavadbcell-1-04",
        "module_name": "T3-SH71XE-25G",
        "model": "R4900 G6",
        "classification": "Storage",
        "serial_number": "HDM210235A4TEH252000008",
        "ipv4_address": "10.50.17.145",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 8}
        ],
        "power": 610,
        "weight": 39.5,
        "description": "COS Index Storage Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "6",
        "rack_alloc": 2,
        "starting_position": 9,
        "type": "server",
        "name": "cbs-1-cell-2-cbs-depot-ec-cell-2-03",
        "module_name": "T3-SH54XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T8H252000043",
        "ipv4_address": "10.50.17.204",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
        "description": "Storage pool SSD"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 9,
        "type": "server",
        "name": "cbs-1-cell-2-cbs-depot-ec-cell-1-11",
        "module_name": "T3-SH54XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T8H252000044",
        "ipv4_address": "10.50.17.203",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
        "description": "Storage pool SSD"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "15",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-1-06",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T5H252000232",
        "ipv4_address": "10.50.18.7",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,
        "description": "Storage pool HDD"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "6",
        "rack_alloc": 2,
        "starting_position": 3,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-1-1",
        "module_name": "T3-CI58XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T5H252000240",
        "ipv4_address": "10.50.17.198",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,
        "description": "TCS Platform Cluster (Worker Node)"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "5",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-2-4",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A2T5H252000222",
        "ipv4_address": "10.50.17.200",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "6",
        "rack_alloc": 2,
        "starting_position": 15,
        "type": "server",
        "name": "cosv3-1-cell-1-yottastore-1-08",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TGH252000006",
        "ipv4_address": "10.50.17.210",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 8}
        ],
        "power": 610,
        "weight": 39.5,
        "description": "COS Data Storage Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "6",
        "rack_alloc": 2,
        "starting_position": 12,
        "type": "server",
        "name": "cfs-1-cell-1-cfs-nasagent-1-1",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A2T8H252000003",
        "ipv4_address": "10.50.17.207",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
        "description": "CFS NAS Head"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "6",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-2-08",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T5H252000220",
        "ipv4_address": "10.50.17.201",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,

        "description": "Storage pool HDD"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "21",
        "rack_alloc": 2,
        "starting_position": 12,
        "type": "server",
        "name": "cbs-1-cell-2-cbs-depot-ec-cell-3-09",
        "module_name": "T3-SH54XE-25G",
        "model": "R4900 G5",
        "classification": "Storage",
        "serial_number": "HDM210235A2T8H252000046",
        "ipv4_address": "10.50.17.15",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
        "description": "Storage pool SSD"
    },
    # {
    #     "pod_name": "Pod 2",
    #     "rack_number": "24",
    #     "rack_alloc": 1,
    #     "starting_position": 5,
    #     "type": "server",
    #     "name": "Prod-jumpserver",
    #     "module_name": "",
    #     "model": "ProLiant DL380 Gen10",
    #     "classification": "",
    #     "serial_number": "SGH132THC0",
    #     "ipv4_address": "10.60.0.2",
    #     "processors": [
    #         {"brand_name": "", "codename": "", "tier": "", "model": ""},
    #         {"brand_name": "", "codename": "", "tier": "", "model": ""}
    #     ],
    #     "storage_units": [
	#     {
    #             "storage_type": "",
    #             "storage_capacity": ,
    #             "storage_count": ,
    #             "capacity_unit": "",
    #             "storage_interface": {"name": ""},
    #             "form_factor": {"name": ""}
    #         }
    #     ],
    #     "memory_units": [
    #         {"ram_capacity": , "quantity": }
    #     ],
    #     "power": 580,
    #     "weight": ,
    #     "description": "Proxmox Virtualization"
    # },
    # {
    #     "pod_name": "Pod 2",
    #     "rack_number": "24",
    #     "rack_alloc": 2,
    #     "starting_position": 6,
    #     "type": "server",
    #     "name": "Proxmox Server 01",
    #     "module_name": "",
    #     "model": "ProLiant DL380 Gen10",
    #     "classification": "",
    #     "serial_number": "SGH132THC0",
    #     "ipv4_address": "10.60.0.2",
    #     "processors": [
    #         {"brand_name": "", "codename": "", "tier": "", "model": ""},
    #         {"brand_name": "", "codename": "", "tier": "", "model": ""}
    #     ],
    #     "storage_units": [
	#     {
    #             "storage_type": "",
    #             "storage_capacity": ,
    #             "storage_count": ,
    #             "capacity_unit": "",
    #             "storage_interface": {"name": ""},
    #             "form_factor": {"name": ""}
    #         }
    #     ],
    #     "memory_units": [
    #         {"ram_capacity": , "quantity": }
    #     ],
    #     "power": 580,
    #     "weight": ,
    #     "description": "Proxmox Virtualization"
    # },
    # {
    #     "pod_name": "Pod 2",
    #     "rack_number": "24",
    #     "rack_alloc": 2,
    #     "starting_position": 9,
    #     "type": "server",
    #     "name": "Proxmox Server 02",
    #     "module_name": "",
    #     "model": "ProLiant DL380 Gen10",
    #     "classification": "",
    #     "serial_number": "SGH132THC4",
    #     "ipv4_address": "10.60.0.3",
    #     "processors": [
    #         {"brand_name": "", "codename": "", "tier": "", "model": ""},
    #         {"brand_name": "", "codename": "", "tier": "", "model": ""}
    #     ],
    #     "storage_units": [
	#     {
    #             "storage_type": "",
    #             "storage_capacity": ,
    #             "storage_count": ,
    #             "capacity_unit": "",
    #             "storage_interface": {"name": ""},
    #             "form_factor": {"name": ""}
    #         }
    #     ],
    #     "memory_units": [
    #         {"ram_capacity": , "quantity": }
    #     ],
    #     "power": 580,
    #     "weight": ,
    #     "description": "Proxmox Virtualization"
    # },
    # {
    #     "pod_name": "Pod 2",
    #     "rack_number": "7",
    #     "rack_alloc": 2,
    #     "starting_position": 6,
    #     "type": "server",
    #     "name": "cbs-1-cell-1-cbs-depot-cell-1-14",
    #     "module_name": "T3-SW50XE-25G",
    #     "model": "R4900 G5",
    #     "classification": "Storage",
    #     "serial_number": "HDM210235A2T5H252000233",
    #     "ipv4_address": "10.50.18.201",
    #     "processors": [
    #         {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
    #         {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
    #     ],
    #     "storage_units": [
    #         {
    #             "storage_type": "HDD",
    #             "storage_capacity": 16,
    #             "storage_count": 10,
    #             "capacity_unit": "TB",
    #             "storage_interface": {"name": "SATA"},
    #             "form_factor": {"name": "3.5"}
    #         },
	#     {
    #             "storage_type": "HDD",
    #             "storage_capacity": 480,
    #             "storage_count": 1,
    #             "capacity_unit": "GB",
    #             "storage_interface": {"name": "SATA"},
    #             "form_factor": {"name": "2.5"}
    #         },
	#     {
    #             "storage_type": "SSD",
    #             "storage_capacity": 6.4,
    #             "storage_count": 2,
    #             "capacity_unit": "TB",
    #             "storage_interface": {"name": "NVME"},
    #             "form_factor": {"name": "M.2"}
    #         }
    #     ],
    #     "memory_units": [
    #         {"ram_capacity": 32, "quantity": 12}
    #     ],
    #     "power": 937,
    #     "weight": 42.10,
    #     "description": "Storage pool HDD"
    # },
    {
        "pod_name": "Pod 2",
        "rack_number": "21",
        "rack_alloc": 2,
        "starting_position": 6,
        "type": "server",
        "name": "cbs-1-cell-1-cbs-depot-cell-2-03",
        "module_name": "T3-SW50XE-25G",
        "model": "R4900 G5",
        "classification": "Compute",
        "serial_number": "HDM210235A2T5H252000225",
        "ipv4_address": "10.50.17.9",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,
        "description": "Storage Pool HDD"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "9",
        "rack_alloc": 2,
        "starting_position": 21,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-31",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000065",
        "ipv4_address": "10.50.19.223",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "20",
        "rack_alloc": 2,
        "starting_position": 21,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-20",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000066",
        "ipv4_address": "10.50.17.23",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "7",
        "rack_alloc": 2,
        "starting_position": 27,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-63",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000043",
        "ipv4_address": "10.50.17.156",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
{
        "pod_name": "Pod 2",
        "rack_number": "7",
        "rack_alloc": 2,
        "starting_position": 24,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-42",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000081",
        "ipv4_address": "10.50.17.153",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "7",
        "rack_alloc": 2,
        "starting_position": 21,
        "type": "server",
        "name": "cvm-1-host-1-cvm-overlay-machine-21",
        "module_name": "T3-CM82XE-25G",
        "model": "R4900 G6",
        "classification": "Compute",
        "serial_number": "HDM210235A4TEH252000038",
        "ipv4_address": "10.50.17.150",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
        "description": "CVM Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "7",
        "rack_alloc": 2,
        "starting_position": 18,
        "type": "server",
        "name": "cosv3-1-cell-1-yottastore-1-14",
        "module_name": "T3-SC71XE-25G",
        "model": "R4900 G6",
        "classification": "Storage",
        "serial_number": "HDM210235A4TGH252000001",
        "ipv4_address": "10.50.17.147",
        "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 8}
        ],
        "power": 610,
        "weight": 39.5,
        "description": "COS Data Storage Node"
    },
    {
        "pod_name": "Pod 2",
        "rack_number": "7",
        "rack_alloc": 2,
        "starting_position": 15,
        "type": "server",
        "name": "clb-1-clbwan7-1-stgw-outer-ip1-2",
        "module_name": "T3-CS50XE-25G",
        "model": "R4900 G5",
        "classification": "Network",
        "serial_number": "HDM210235A2T8H252000004",
        "ipv4_address":"0.0.0.0",
        "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
        "description": "External network layer 7 load balancing gateway"
    },
{
    "pod_name": "Pod 2",
    "rack_number": "7",
    "rack_alloc": 2,
    "starting_position": 9,
    "type": "server",
    "name": "cbs-1-cell-2-cbs-depot-ec-cell-1-07",
    "module_name": "T3-SH54XE-25G",
    "model": "R4900 G5",
    "classification": "Storage",
    "serial_number": "HDM210235A2T8H252000056",
    "ipv4_address": "10.50.17.138",
    "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
    "description": "Storage pool SSD"
},
{
    "pod_name": "Pod 2",
    "rack_number": "7",
    "rack_alloc": 2,
    "starting_position": 6,
    "type": "server",
    "name": "cbs-1-cell-1-cbs-depot-cell-1-12",
    "module_name": "T3-SW50XE-25G",
    "model": "R4900 G5",
    "classification": "Storage",
    "serial_number": "HDM210235A2T5H252000216",
    "ipv4_address": "10.50.17.135",
    "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,
    	"description": "Storage pool HDD"
},
{
    "pod_name": "Pod 2",
    "rack_number": "7",
    "rack_alloc": 2,
    "starting_position": 3,
    "type": "server",
    "name": "tcs-core-1-base-1-tcs-global-node-1-5",
    "module_name": "T3-CI58XE-25G",
    "model": "R4900 G5",
    "classification": "Compute",
    "serial_number": "HDM210235A2T8H252000060",
    "ipv4_address": "10.50.17.132",
    "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
    "description": "TCS platform cluster (Worker node)"
},
{
    "pod_name": "Pod 2",
    "rack_number": "8",
    "rack_alloc": 2,
    "starting_position": 28,
    "type": "server",
    "name": "inta-1-core-1-inta-core-ip-1-03",
    "module_name": "T3-SW81XE-25G",
    "model": "R4900 G6",
    "classification": "Compute",
    "serial_number": "HDM210235A4TGH252000023",
    "ipv4_address": "10.50.17.157",
    "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,
    "description": "NTA analysis platform hardware server"
},
# {
#     "pod_name": "Pod 2",
#     "rack_number": "8",
#     "rack_alloc": 2,
#     "starting_position": 24,
#     "type": "server",
#     "name": "cvm-1-host-1-cvm-overlay-machine-47",
#     "module_name": "T3-CM82XE-25G",
#     "model": "R4900 G6",
#     "classification": "",
#     "serial_number": "HDM210235A4TEH252000055",
#     "ipv4_address": "10.50.17.154",
#     "processors": [
#         { "brand_name": "", "codename": "", "tier": "", "model": "" },
#         { "brand_name": "", "codename": "", "tier": "", "model": "" }
#     ],
#     "storage_units": [],
#     "memory_units": [],
#     "power": 1193,
#     "weight": null,
#     "description": "CVM Node"
# },
{
    "pod_name": "Pod 2",
    "rack_number": "8",
    "rack_alloc": 2,
    "starting_position": 21,
    "type": "server",
    "name": "cvm-1-host-1-cvm-overlay-machine-26",
    "module_name": "T3-CM82XE-25G",
    "model": "R4900 G6",
    "classification": "Compute",
    "serial_number": "HDM210235A4TEH252000051",
    "ipv4_address": "10.50.17.151",
    "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
    "description": "CVM Node"
},
{
    "pod_name": "Pod 2",
    "rack_number": "8",
    "rack_alloc": 2,
    "starting_position": 18,
    "type": "server",
    "name": "cvm-1-host-1-cvm-overlay-machine-05",
    "module_name": "T3-CM82XE-25G",
    "model": "R4900 G6",
    "classification": "Compute",
    "serial_number": "HDM210235A4TEH252000053",
    "ipv4_address": "10.50.17.148",
    "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
    "description": "CVM Node"
},
# {
#     "pod_name": "Pod 2",
#     "rack_number": "8",
#     "rack_alloc": 2,
#     "starting_position": 15,
#     "type": "server",
#     "name": "cosv3-1-cell-1-lavadbcell-1-04",
#     "module_name": "T3-SH71XE-25G",
#     "model": "R4900 G6",
#     "classification": "Storage",
#     "serial_number": "HDM210235A4TEH252000008",
#     "ipv4_address": "10.50.17.145",
#     "processors": [
#             {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"},
#             {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Silver", "model": "4510"}
#         ],
#         "storage_units": [
#             {
#                 "storage_type": "HDD",
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},
#                 "form_factor": {"name": "2.5"}
#             },
# 	    {
#                 "storage_type": "SSD",
#                 "storage_capacity": 3.84,
#                 "storage_count": 2,
#                 "capacity_unit": "TB",
#                 "storage_interface": {"name": "NVME"},
#                 "form_factor": {"name": "M.2"}
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 8}
#         ],
#         "power": 610,
#         "weight": 39.5,

#     "description": "COS Index Storage Node"
# },
{
    "pod_name": "Pod 2",
    "rack_number": "8",
    "rack_alloc": 2,
    "starting_position": 12,
    "type": "server",
    "name": "cbs-1-cell-2-cbs-depot-ec-cell-3-11",
    "module_name": "T3-SH54XE-25G",
    "model": "R4900 G5",
    "classification": "Storage",
    "serial_number": "HDM210235A2T8H252000034",
    "ipv4_address": "10.50.17.142",
    "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
    "description": "Storage pool SSD"
},
{
    "pod_name": "Pod 2",
    "rack_number": "8",
    "rack_alloc": 2,
    "starting_position": 9,
    "type": "server",
    "name": "cbs-1-cell-2-cbs-depot-ec-cell-1-12",
    "module_name": "T3-SH54XE-25G",
    "model": "R4900 G5",
    "classification": "Storage",
    "serial_number": "HDM210235A2T8H252000048",
    "ipv4_address": "10.50.17.139",
    "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
    "description": "Storage pool SSD"
},
{
    "pod_name": "Pod 2",
    "rack_number": "8",
    "rack_alloc": 2,
    "starting_position": 6,
    "type": "server",
    "name": "cbs-1-cell-1-cbs-depot-cell-2-05",
    "module_name": "T3-SW50XE-25G",
    "model": "R4900 G5",
    "classification": "Storage",
    "serial_number": "HDM210235A2T5H252000228",
    "ipv4_address": "10.50.17.136",
    "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 16,
                "storage_count": 10,
                "capacity_unit": "TB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            },
	    {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 6.4,
                "storage_count": 2,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 12}
        ],
        "power": 937,
        "weight": 42.10,
    "description": "Storage pool HDD"
},
{
    "pod_name": "Pod 2",
    "rack_number": "8",
    "rack_alloc": 2,
    "starting_position": 3,
    "type": "server",
    "name": "tcs-core-1-base-1-tcs-global-node-1-12",
    "module_name": "T3-CI58XE-25G",
    "model": "R4900 G5",
    "classification": "Platform",
    "serial_number": "HDM210235A2T8H252000059",
    "ipv4_address": "10.50.17.133",
    "processors": [
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
            {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "2.5"}
            },
	    {
                "storage_type": "SSD",
                "storage_capacity": 3.84,
                "storage_count": 12,
                "capacity_unit": "TB",
                "storage_interface": {"name": "NVME"},
                "form_factor": {"name": "M.2"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 32, "quantity": 4}
        ],
        "power": 655,
        "weight": 42.10,
    "description": "TCS Platform Cluster (Worker Node)"
},
{
    "pod_name": "Pod 2",
    "rack_number": "9",
    "rack_alloc": 2,
    "starting_position": 24,
    "type": "server",
    "name": "cvm-1-host-1-cvm-overlay-machine-52",
    "module_name": "T3-CM82XE-25G",
    "model": "R4900 G6",
    "classification": "Compute",
    "serial_number": "HDM210235A4TEH252000036",
    "ipv4_address": "10.50.17.155",
    "processors": [
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"},
            {"brand_name": "Intel", "codename": "Emerald Rapids", "tier": "Xeon Platinum", "model": "8558"}
        ],
        "storage_units": [
            {
                "storage_type": "HDD",
                "storage_capacity": 480,
                "storage_count": 1,
                "capacity_unit": "GB",
                "storage_interface": {"name": "SATA"},
                "form_factor": {"name": "3.5"}
            }
        ],
        "memory_units": [
            {"ram_capacity": 64, "quantity": 24}
        ],
        "power": 1193,
        "weight": 39.5,
    "description": "CVM Node"
},


   

]






    

#     #-------------------- NFV-TL RACK 7 -----------------------
#     {
#         "pod_name": "Pod 1",
#         "rack_number": "3",
#         "rack_alloc":2,
#         "starting_position": 41,
#         "type": "server",
#         "name": "clb-1-eip-1-product-clb-tgw3weip-rip-1-1",
#         "module_name": "T3-NS51XE-100G",
#         "model": "R4900 G5",
#         "classification": "Network",
#         "serial_number": "HDM210235A2T8H252000083",
#         "ipv4_address": "10.51.0.3",
#         "processors": [
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
#         ],     
#         "storage_units": [
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 12},
#         ],  
#         "power": 780.0,
#         "weight": 42.10,
#         "description": "",
#     },

#     #-------------------- NFV-TL RACK 7 -----------------------
#     {
#         "pod_name": "Pod 1",
#         "rack_number": "7",
#         "rack_alloc":2,
#         "starting_position": 1,
#         "type": "server",
#         "name": "clb-1-eip-1-product-clb-tgw3weip-rip-1-1",
#         "module_name": "T3-NS51XE-100G",
#         "model": "R4900 G5",
#         "classification": "Network",
#         "serial_number": "HDM210235A2T8H252000083",
#         "ipv4_address": "10.51.0.3",
#         "processors": [
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
#         ],     
#         "storage_units": [
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 12},
#         ],  
#         "power": 780.0,
#         "weight": 42.10,
#         "description": "",
#     },
#     {
#         "pod_name": "Pod 1",
#         "rack_number": "7",
#         "rack_alloc":2,
#         "starting_position": 2,
#         "type": "server",
#         "name": "vpc-1-nfv-host-1-nfv-vm-host-1-1",
#         "module_name": "T3-NS51XE-100G",
#         "model": "R4900 G5",
#         "classification": "Network",
#         "serial_number": "HDM210235A2T8H252000089",
#         "ipv4_address": "10.51.12.195",
#         "processors": [
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
#         ],     
#         "storage_units": [
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 12},
#         ],  
#         "power": 780.0,
#         "weight": 42.10,
#         "description": "",
#     },
#     {
#         "pod_name": "Pod 1",
#         "rack_number": "7",
#         "rack_alloc":2,
#         "starting_position": 3,
#         "type": "server",
#         "name": "inta-1-core-1-inta-probe-ip-1-1",
#         "module_name": "T3-NS82XE-10G",
#         "model": "R4900 G6",
#         "classification": "Security",
#         "serial_number": "HDM210235A4TEH252000026",
#         "ipv4_address": "10.51.1.164",
#         "processors": [
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
#         ],     
#         "storage_units": [
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 8000,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "3.5"},        # must match StorageFormFactor.name
#             },
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 4},
#         ],  
#         "power": 780.0,
#         "weight": 42.10,
#         "description": "",
#     },
#     {
#         "pod_name": "Pod 1",
#         "rack_number": "7",
#         "rack_alloc":2,
#         "starting_position": 3,
#         "type": "server",
#         "name": "nips-1-nipsprobe-1-nips-probe-group-1-1",
#         "module_name": "T3-NS82XE-10G",
#         "model": "R4900 G6",
#         "classification": "Security",
#         "serial_number": "HDM210235A4TEH252000022",
#         "ipv4_address": "10.51.1.163",
#         "processors": [
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"},
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "4310"}
#         ],     
#         "storage_units": [
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 8000,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "3.5"},        # must match StorageFormFactor.name
#             },
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 4},
#         ],  
#         "power": 780.0,
#         "weight": 42.10,
#         "description": "",
#     },

#     #-------------------- NFV-TL RACK 8 -----------------------
#     {
#         "pod_name": "Pod 1",
#         "rack_number": "8",
#         "rack_alloc":2,
#         "starting_position": 1,
#         "type": "server",
#         "name": "clb-1-eip-1-product-clb-tgw3weip-rip-1-2",
#         "module_name": "T3-NS51XE-100G",
#         "model": "R4900 G5",
#         "classification": "Network",
#         "serial_number": "HDM210235A2T8H252000086",
#         "ipv4_address": "10.51.0.4",
#         "processors": [
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
#         ],     
#         "storage_units": [
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 12},
#         ],  
#         "power": 780.0,
#         "weight": 42.10,
#         "description": "",
#     },
#     {
#         "pod_name": "Pod 1",
#         "rack_number": "8",
#         "rack_alloc":2,
#         "starting_position": 2,
#         "type": "server",
#         "name": "vpc-1-nfv-host-1-nfv-vm-host-1-2",
#         "module_name": "T3-NS51XE-100G",
#         "model": "R4900 G5",
#         "classification": "Unknown",
#         "serial_number": "HDM210235A2T8H252000080",
#         "ipv4_address": "10.51.12.196",
#         "processors": [
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"},
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Gold", "model": "5318Y"}
#         ],     
#         "storage_units": [
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 12},
#         ],  
#         "power": 780.0,
#         "weight": 42.10,
#         "description": "",
#     },
#     {
#         "pod_name": "Pod 1",
#         "rack_number": "8",
#         "rack_alloc":2,
#         "starting_position": 3,
#         "type": "server",
#         "name": "inta-1-core-1-inta-probe-ip-1-2",
#         "module_name": "T3-NS82XE-10G",
#         "model": "R4900 G6",
#         "classification": "Security",
#         "serial_number": "HDM210235A4TEH252000027",
#         "ipv4_address": "10.51.1.166",
#         "processors": [
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "5318Y"},
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "5318Y"}
#         ],     
#         "storage_units": [
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 8000,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "3.5"},        # must match StorageFormFactor.name
#             },
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 4},
#         ],  
#         "power": 780.0,
#         "weight": 42.10,
#         "description": "",
#     },
#     {
#         "pod_name": "Pod 1",
#         "rack_number": "8",
#         "rack_alloc":2,
#         "starting_position": 4,
#         "type": "server",
#         "name": "nips-1-nipsprobe-1-nips-probe-group-1-2",
#         "module_name": "T3-NS82XE-10G",
#         "model": "R4900 G6",
#         "classification": "Security",
#         "serial_number": "HDM210235A4TEH252000024",
#         "ipv4_address": "10.51.1.166",
#         "processors": [
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "5318Y"},
#             {"brand_name": "Intel", "codename": "Ice Lake", "tier": "Xeon Silver", "model": "5318Y"}
#         ],     
#         "storage_units": [
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 8000,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "3.5"},        # must match StorageFormFactor.name
#             },
#             {
#                 "storage_type": "SSD",                # TextChoices in StorageUnit
#                 "storage_capacity": 480,
#                 "storage_count": 1,
#                 "capacity_unit": "GB",
#                 "storage_interface": {"name": "SATA"},  # must match StorageInterface.name
#                 "form_factor": {"name": "2.5"},        # must match StorageFormFactor.name
#             }
#         ],
#         "memory_units": [
#             {"ram_capacity": 32, "quantity": 4},
#         ],  
#         "power": 780.0,
#         "weight": 42.10,
#         "description": "",
#     },
# 
