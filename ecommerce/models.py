from django.db import models

# Create your models here.


class Permission(models.Model):
    code = models.CharField(max_length=7, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=100)
    permissions = models.ManyToManyField(Permission, related_name="roles")

    def __str__(self):
        return self.name

    def get_permissions(self):
        return Permission.objects.filter(roles=self).distinct()


class Person(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    roles = models.ManyToManyField(Role, related_name="persons")

    def __str__(self):
        return self.name

    def get_permissions(self):
        return Permission.objects.filter(roles__persons=self).distinct()
