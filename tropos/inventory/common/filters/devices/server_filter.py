from inventory.assets.models import Server
from ..base_filter import BaseFilter

class ServerFilter(BaseFilter):
    class Meta:
        model = Server
        fields = []  # we define fields manually via class methods below

# Filter
ServerFilter.add_exact_field("status","type")                     
ServerFilter.add_number_list_field("device__id", "device_id","device__rack_id", "rack_id")   

# Search
ServerFilter.search_fields = ["device__id","device__name","classification","module_name", "device__rack__number", "device__type", "device__status"]

# ServerFilter.add_search_field("server_name","name","status","type")        # search bar
# ServerFilter.add_exact_field("status")                     # buttons
# ServerFilter.add_exact_field("type")                       # buttons/dropdowns
# ServerFilter.add_number_field("device__id", "device_id")   # dropdowns
# ServerFilter.add_number_field("device__rack_id", "rack_id")# dropdowns
