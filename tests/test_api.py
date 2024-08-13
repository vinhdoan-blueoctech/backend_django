import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ecommerce.models import Permission, Role, Person
from django.contrib.auth.models import User


@pytest.fixture(scope="function")
def setup_data():
    # Setup test data
    client = APIClient()

    permission1 = Permission.objects.create(code="perm_1", name="Permission 1")
    permission2 = Permission.objects.create(code="perm_2", name="Permission 2")

    role1 = Role.objects.create(name="Role 1")
    role2 = Role.objects.create(name="Role 2")

    person1 = Person.objects.create(name="Person 1", email="person1@example.com")
    person2 = Person.objects.create(name="Person 2", email="person2@example.com")

    return {
        "client": client,
        "permission1": permission1,
        "permission2": permission2,
        "role1": role1,
        "role2": role2,
        "person1": person1,
        "person2": person2,
    }


@pytest.mark.django_db
def test_create_permission(setup_data):
    client = setup_data["client"]
    url = reverse("permission-list")
    data = {"code": "perm_3", "name": "Permission 3"}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Permission.objects.filter(code="perm_3").exists()


@pytest.mark.django_db
def test_retrieve_permission(setup_data):
    client = setup_data["client"]
    permission1 = setup_data["permission1"]
    url = reverse("permission-detail", kwargs={"pk": permission1.id})
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["code"] == permission1.code


@pytest.mark.django_db
def test_update_permission(setup_data):
    client = setup_data["client"]
    permission1 = setup_data["permission1"]
    url = reverse("permission-detail", kwargs={"pk": permission1.id})
    data = {"name": "Permission 1 Updated"}
    response = client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    permission1.refresh_from_db()


@pytest.mark.django_db
def test_delete_permission(setup_data):
    client = setup_data["client"]
    permission1 = setup_data["permission1"]
    url = reverse("permission-detail", kwargs={"pk": permission1.id})
    response = client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Permission.objects.filter(id=permission1.id).exists()


# CRUD Tests for Role
@pytest.mark.django_db
def test_create_role(setup_data):
    client = setup_data["client"]
    url = reverse("role-list")
    data = {"name": "Role 1 Updated", "permissions": []}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_retrieve_role(setup_data):
    client = setup_data["client"]
    role1 = setup_data["role1"]
    url = reverse("role-detail", kwargs={"pk": role1.id})
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == role1.name


@pytest.mark.django_db
def test_update_role(setup_data):
    client = setup_data["client"]
    role1 = setup_data["role1"]
    url = reverse("role-detail", kwargs={"pk": role1.id})
    data = {"name": "Role 1 Updated"}
    response = client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    role1.refresh_from_db()
    assert role1.name == "Role 1 Updated"


@pytest.mark.django_db
def test_delete_role(setup_data):
    client = setup_data["client"]
    role1 = setup_data["role1"]
    url = reverse("role-detail", kwargs={"pk": role1.id})
    response = client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Role.objects.filter(id=role1.id).exists()


# CRUD Tests for Person
@pytest.mark.django_db
def test_create_person(setup_data):
    client = setup_data["client"]
    url = reverse("person-list")
    data = {"name": "Person 3", "email": "person3@example.com", "roles": []}
    response = client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert Person.objects.filter(email="person3@example.com").exists()


@pytest.mark.django_db
def test_retrieve_person(setup_data):
    client = setup_data["client"]
    person1 = setup_data["person1"]
    url = reverse("person-detail", kwargs={"pk": person1.id})
    response = client.get(url, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == person1.name


@pytest.mark.django_db
def test_update_person(setup_data):
    client = setup_data["client"]
    person1 = setup_data["person1"]
    url = reverse("person-detail", kwargs={"pk": person1.id})
    data = {"name": "Person 1 Updated", "email": "person1_updated@example.com"}
    response = client.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    person1.refresh_from_db()
    assert person1.name == "Person 1 Updated"


@pytest.mark.django_db
def test_delete_person(setup_data):
    client = setup_data["client"]
    person1 = setup_data["person1"]
    url = reverse("person-detail", kwargs={"pk": person1.id})
    response = client.delete(url, format="json")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Person.objects.filter(id=person1.id).exists()


# Add/Remove permission
@pytest.mark.django_db
def test_add_permission_to_role(setup_data):
    client = setup_data["client"]
    role1 = setup_data["role1"]
    permission1 = setup_data["permission1"]
    url = reverse("role-detail", kwargs={"pk": role1.id}) + "add_permission/"
    response = client.post(url, {"permission_id": permission1.id}, format="json")
    assert response.status_code == status.HTTP_200_OK
    role1.refresh_from_db()
    assert permission1 in role1.permissions.all()


@pytest.mark.django_db
def test_remove_permission_from_role(setup_data):
    client = setup_data["client"]
    role1 = setup_data["role1"]
    permission1 = setup_data["permission1"]
    role1.permissions.add(permission1)
    url = reverse("role-detail", kwargs={"pk": role1.id}) + "remove_permission/"
    response = client.post(url, {"permission_id": permission1.id}, format="json")
    assert response.status_code == status.HTTP_200_OK
    role1.refresh_from_db()
    assert permission1 not in role1.permissions.all()


# Add/ Remove Role
@pytest.mark.django_db
def test_add_role_to_person(setup_data):
    client = setup_data["client"]
    person1 = setup_data["person1"]
    role1 = setup_data["role1"]
    url = reverse("person-detail", kwargs={"pk": person1.id}) + "add_role/"
    response = client.post(url, {"role_id": role1.id}, format="json")
    assert response.status_code == status.HTTP_200_OK
    person1.refresh_from_db()
    assert role1 in person1.roles.all()


@pytest.mark.django_db
def test_remove_role_from_person(setup_data):
    client = setup_data["client"]
    person1 = setup_data["person1"]
    role1 = setup_data["role1"]
    person1.roles.add(role1)
    url = reverse("person-detail", kwargs={"pk": person1.id}) + "remove_role/"
    response = client.post(url, {"role_id": role1.id}, format="json")
    assert response.status_code == status.HTTP_200_OK
    person1.refresh_from_db()
    assert role1 not in person1.roles.all()
