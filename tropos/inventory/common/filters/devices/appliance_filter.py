from inventory.assets.models import Appliance
from ..base_filter import BaseFilter

class ApplianceFilter(BaseFilter):
    class Meta:
        model = Appliance
        fields = []  # we define fields manually via class methods below

# Add fields
# ApplianceFilter.add_search_field("server_name", "name")        # search bar
# ApplianceFilter.add_exact_field("status")                     # buttons
# ApplianceFilter.add_exact_field("type")                       # buttons/dropdowns
# ApplianceFilter.add_number_field("device__id", "device_id")   # dropdowns
# ApplianceFilter.add_number_field("device__rack_id", "rack_id")# dropdowns

# Filter
ApplianceFilter.add_number_list_field(("device__id","id"),"device__rack_id", "rack_id")   
ApplianceFilter.add_exact_field("status","type")                    

# Search
ApplianceFilter.search_fields = ["device__id","appliance_type__name", "device__rack__number", "device__type", "device__status"]

# ApplianceFilter.add_number_list_field(("device__id","id"),"device__rack_id", "rack_id")   # syntax when you want a custom params
