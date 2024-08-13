from rest_framework import serializers
from ecommerce.models import Permission, Role, Person


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "code", "name"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        queryset=Permission.objects.all(), many=True
    )

    class Meta:
        model = Role
        fields = ["id", "name", "permissions"]


class PersonSerializer(serializers.ModelSerializer):
    roles = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), many=True)

    class Meta:
        model = Person
        fields = ["id", "name", "email", "roles"]
