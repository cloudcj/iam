from rest_framework import generics
from ..serializers import UserRoleSerializer
from django.contrib.auth.models import Group

class UserRoleListView(generics.ListAPIView):
  queryset = Group.objects.all().order_by("id")
  serializer_class = UserRoleSerializer
