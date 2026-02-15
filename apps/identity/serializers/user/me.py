# from rest_framework import serializers
# from apps.identity.models import User

# class MeSerializer(serializers.ModelSerializer): 
#     department = serializers.SerializerMethodField() 
#     roles = serializers.SerializerMethodField() 
    
#     def get_department(self, obj): 
#         link = obj.user_department.first() 
#         return link.department.code if link else None 
    
#     def get_roles(self, obj): 
        
#         return [ur.role.code for ur in obj.user_roles.all()] 
    
#     class Meta: 
#         model = User 
#         fields = [ 
#             "id", 
#             "username", 
#             "email", 
#             "is_active", 
#             "department", 
#             "roles", ] 
#         read_only_fields = fields

# apps/identity/serializers/me.py

from rest_framework import serializers

class MeSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_blank=True, allow_null=True)

    department = serializers.SerializerMethodField()

    def get_department(self, obj):
        return {
            "code": obj.department.code,
            "label": obj.department.name,
        }
