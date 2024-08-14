import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from ecommerce.models import Permission, Role, Person


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
def test_add_invalid_permission_to_role(setup_data):
    client = setup_data["client"]
    role1 = setup_data["role1"]
    invalid_permission_id = 9999

    url = reverse("role-detail", kwargs={"pk": role1.id}) + "add_permission/"
    response = client.post(url, {"permission_id": invalid_permission_id}, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_remove_non_associated_permission_from_role(setup_data):
    client = setup_data["client"]
    role1 = setup_data["role1"]
    permission2 = setup_data["permission2"]

    url = reverse("role-detail", kwargs={"pk": role1.id}) + "remove_permission/"
    response = client.post(url, {"permission_id": permission2.id}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "The role does not have this permission."


@pytest.mark.django_db
def test_remove_invalid_permission_from_role(setup_data):
    client = setup_data["client"]
    role1 = setup_data["role1"]
    invalid_permission_id = 9999

    url = reverse("role-detail", kwargs={"pk": role1.id}) + "remove_permission/"
    response = client.post(url, {"permission_id": invalid_permission_id}, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_add_invalid_role_to_person(setup_data):
    client = setup_data["client"]
    person1 = setup_data["person1"]
    invalid_role_id = 9999

    url = reverse("person-detail", kwargs={"pk": person1.id}) + "add_role/"
    response = client.post(url, {"role_id": invalid_role_id}, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_remove_non_associated_role_from_person(setup_data):
    client = setup_data["client"]
    person1 = setup_data["person1"]
    role2 = setup_data["role2"]

    url = reverse("person-detail", kwargs={"pk": person1.id}) + "remove_role/"
    response = client.post(url, {"role_id": role2.id}, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "The person does not have this role."


@pytest.mark.django_db
def test_remove_invalid_role_from_person(setup_data):
    client = setup_data["client"]
    person1 = setup_data["person1"]
    invalid_role_id = 9999

    url = reverse("person-detail", kwargs={"pk": person1.id}) + "remove_role/"
    response = client.post(url, {"role_id": invalid_role_id}, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
