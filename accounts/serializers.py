from rest_framework import serializers
from accounts.models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Users
        fields = ['id', 'name', 'email', 'is_admin']