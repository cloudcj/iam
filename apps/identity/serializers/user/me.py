from rest_framework import serializers
from apps.identity.models import User

class MeSerializer(serializers.ModelSerializer): 
    department = serializers.SerializerMethodField() 
    roles = serializers.SerializerMethodField() 
    
    def get_department(self, obj): 
        link = obj.user_department.first() 
        return link.department.code if link else None 
    
    def get_roles(self, obj): 
        
        return [ur.role.code for ur in obj.user_roles.all()] 
    
    class Meta: 
        model = User 
        fields = [ 
            "id", 
            "username", 
            "email", 
            "is_active", 
            "department", 
            "roles", ] 
        read_only_fields = fields