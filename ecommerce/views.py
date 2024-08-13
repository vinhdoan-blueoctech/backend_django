from rest_framework import generics
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
        permission = Permission.objects.get(id=request.data["permission_id"])
        role.permissions.add(permission)
        role.save()
        return Response({"status": "permission added"})

    @action(detail=True, methods=["post"])
    def remove_permission(self, request, pk=None):
        role = self.get_object()
        permission = Permission.objects.get(id=request.data["permission_id"])
        role.permissions.remove(permission)
        role.save()
        return Response({"status": "permission removed"})


class PersonDetail(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    @action(detail=True, methods=["post"])
    def add_role(self, request, pk=None):
        person = self.get_object()
        role = Role.objects.get(id=request.data["role_id"])
        person.roles.add(role)
        person.save()
        return Response({"status": "role added"})

    @action(detail=True, methods=["post"])
    def remove_role(self, request, pk=None):
        person = self.get_object()
        role = Role.objects.get(id=request.data["role_id"])
        person.roles.remove(role)
        person.save()
        return Response({"status": "role removed"})
