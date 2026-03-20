from .schema import Policy

# _POLICIES = [
#     Policy(
#         code="global.viewer",
#         name="Global Viewer",
#         system="global",
#         resource="viewer",
#         permissions=(
#             "inventory.az.read",
#             "inventory.device.read",
#         ),
#     ),
# ]

# GLOBAL_POLICIES = {p.code: p for p in _POLICIES}

# GLOBAL_POLICIES = {
#     "global.viewer": Policy(
#         code="global.viewer",
#         name="Global Viewer",
#         system="global",
#         resource="viewer",
#         permissions=(
#             "inventory.az.read",
#             "inventory.device.read",
#             # "pleco.resource.read",
#             # add more read-only permissions as needed
#         ),
#     ),
# }

GLOBAL_POLICIES = {}
