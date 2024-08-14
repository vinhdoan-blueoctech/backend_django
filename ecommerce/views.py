from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from ecommerce.models import Permission, Role, Person
from ecommerce.serializers import (
    PermissionSerializer,
    RoleSerializer,
    PersonSerializer,
)

# Permission Views
class PermissionList(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


class PermissionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer


# Role Views
class RoleList(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class RoleDetail(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    @action(detail=True, methods=["post"])
    def add_permission(self, request, pk=None):
        role = self.get_object()
        permission_id = request.data.get("permission_id")

        permission = get_object_or_404(Permission, id=permission_id)

        role.permissions.add(permission)
        role.save()
        return Response({"status": "permission added"})

    @action(detail=True, methods=["post"])
    def remove_permission(self, request, pk=None):
        role = self.get_object()
        permission_id = request.data.get("permission_id")

        permission = get_object_or_404(Permission, id=permission_id)
        if not role.permissions.filter(id=permission.id).exists():
            return Response(
                {"error": "The role does not have this permission."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        role.permissions.remove(permission)
        role.save()

        return Response({"status": "Permission removed successfully."})


class PersonDetail(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=True, methods=["post"])
    def add_role(self, request, pk=None):
        person = self.get_object()
        role_id = request.data.get("role_id")

        role = get_object_or_404(Role, id=role_id)

        person.roles.add(role)
        person.save()
        return Response({"status": "role added"})

    @action(detail=True, methods=["post"])
    def remove_role(self, request, pk=None):
        person = self.get_object()
        role_id = request.data.get("role_id")

        role = get_object_or_404(Role, id=role_id)

        if not person.roles.filter(id=role.id).exists():
            return Response(
                {"error": "The person does not have this role."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        person.roles.remove(role)
        person.save()
        return Response({"status": "role removed"})
