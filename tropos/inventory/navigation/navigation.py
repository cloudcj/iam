# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from .registry import NAVIGATION
# from inventory.iam.auth.iam_client import batch_check_permissions

# class NavigationView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):

#         # 1️⃣ Collect all leaf permissions
#         permission_codes = [
#             item["permission"]
#             for section in NAVIGATION
#             for item in section["items"]
#         ]

#         # 2️⃣ Batch check with IAM
#         allowed_permissions = set(
#             batch_check_permissions(request, permission_codes)
#         )

#         # 3️⃣ Filter sections
#         filtered_sections = []

#         for section in NAVIGATION:
#             allowed_items = [
#                 {
#                     "path": item["path"],
#                     "label": item["label"],
#                 }
#                 for item in section["items"]
#                 if item["permission"] in allowed_permissions
#             ]

#             # 4️⃣ Keep section only if it has allowed items
#             if allowed_items:
#                 filtered_sections.append(
#                     {
#                         "title": section["title"],
#                         "items": allowed_items,
#                     }
#                 )

#         return Response(
#             {
#                 "system": "inventory",
#                 "sections": filtered_sections,
#             }
#         )


# # class NavigationView(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def get(self, request):

# #         # Collect all leaf permissions
# #         permission_codes = [
# #             item["permission"]
# #             for section in NAVIGATION
# #             for item in section["items"]
# #         ]

# #         # Batch check with IAM
# #         allowed_permissions = batch_check_permissions(
# #             request,
# #             permission_codes,
# #         )

# #         # Filter routes
# #         allowed_routes = [
# #             {
# #                 "path": route["path"],
# #                 "label": route["label"],
# #             }
# #             for route in NAVIGATION
# #             if route["permission"] in allowed_permissions
# #         ]

# #         return Response(
# #             {
# #                 "system": "inventory",
# #                 "label": "Inventory",
# #                 "routes": allowed_routes,
# #             }
# #         )
