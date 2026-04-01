from inventory.assets.models import Device
from ..base_filter import BaseFilter

class DeviceFilter(BaseFilter):
  class Meta:
    model = Device
    fields = []

# Filter
# Exact match filters
DeviceFilter.add_string_list_field("rack__number")
DeviceFilter.add_exact_field('status','type')
DeviceFilter.add_number_list_field('id','number_of_interfaces',"starting_position","interface_count")
DeviceFilter.add_search_list_field("serial_number","model",'ipv4_address',)

# Number filters (IDs, foreign keys)
DeviceFilter.add_number_field('rack')

# Search
DeviceFilter.search_fields = ["id", "name", "rack__number", "type", "status", "serial_number","ipv4_address"]





# DeviceFilter.add_exact_field(field_name='type')
# DeviceFilter.add_exact_field(field_name='status')
# DeviceFilter.add_number_list_field(field_name='id')
# DeviceFilter.add_number_list_field(field_name='number_of_interfaces', param_name='active_interfaces')
# DeviceFilter.add_number_list_field(field_name='fan_units', param_name='fan_count')


# Exact match filters

# DeviceFilter.add_search_list_field(field_name="ipv4_address")
# DeviceFilter.add_search_list_field(field_name="name")
# DeviceFilter.add_search_list_field(field_name="serial_number")
# DeviceFilter.add_search_list_field(field_name="model")

# DeviceFilter.add_string_list_field(field_name='rack__number', param_name='rack_number')

# DeviceFilter.add_number_field(field_name="rack_unit_allocations")
# DeviceFilter.add_number_field(field_name="starting_position")
# DeviceFilter.add_number_field(field_name="weight")
# DeviceFilter.add_number_field("power")
# DeviceFilter.add_number_list_field(field_name='interface_count')
# DeviceFilter.add_number_list_field(field_name='id')

# DeviceFilter.add_exact_field(field_name='type')
# DeviceFilter.add_exact_field(field_name="status")

# # Number filters (IDs, foreign keys)
# DeviceFilter.add_number_field(field_name='rack', param_name='rack_id')

# # Partial search fields (for ?search= query)
# DeviceFilter.search_fields = ["id", "name", "serial_number", "rack__number", "ipv4_address"]