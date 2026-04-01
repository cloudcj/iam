from inventory.assets.models import Switch
from ..base_filter import BaseFilter

class SwitchFilter(BaseFilter):
    class Meta:
        model = Switch
        fields = []  # we define fields manually via class methods below

# Add fields
# SwitchFilter.add_search_field("server_name", "name")        # search bar

# Filter
SwitchFilter.add_exact_field("status","type")                     # buttons
SwitchFilter.add_number_list_field("device__id", "device_id","device__rack_id", "rack_id")  

# Search
SwitchFilter.search_fields = ["device__id", "device__name", "device__rack__number", "device__type", "device__status"]


# SwitchFilter.add_exact_field("status")                     # buttons
# SwitchFilter.add_exact_field("type")                       # buttons/dropdowns
# SwitchFilter.add_number_field("device__id", "device_id")   # dropdowns
# SwitchFilter.add_number_field("device__rack_id", "rack_id")# dropdowns