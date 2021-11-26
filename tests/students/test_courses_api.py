import pytest
from rest_framework.reverse import reverse

from students.models import Course


@pytest.mark.django_db
def test_get_course(api_client, course_factory):
    course_factory(_quantity=1)
    course_1 = Course.objects.first()
    url = reverse("courses-detail", args=(course_1.id, ))
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.data["id"] == course_1.id
    assert response.data["name"] == course_1.name


@pytest.mark.django_db
def test_get_list_courses(api_client, course_factory):
    url = reverse("courses-list")
    course_factory(_quantity=5)
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 5


@pytest.mark.django_db
def test_get_course_filter_id(api_client, course_factory):
    course_factory(_quantity=5)
    course_1 = Course.objects.first()
    url = reverse("courses-list")+f'?id={course_1.id}'
    response = api_client.get(url)
    assert response.status_code == 200
    for item in response.data:
        assert item["id"] == course_1.id


@pytest.mark.django_db
def test_get_course_filter_id(api_client, course_factory):
    course_factory(_quantity=5)
    course_1 = Course.objects.first()
    url = reverse("courses-list")+f'?name={course_1.name}'
    response = api_client.get(url)
    assert response.status_code == 200
    for item in response.data:
        assert item["name"] == course_1.name


@pytest.mark.django_db
def test_create_courses(api_client):
    url = reverse("courses-list")
    data_new = {
        "name": "Super course",
        "students": []
    }
    response = api_client.post(url, data_new)
    assert response.status_code == 201
    assert response.data["name"] == data_new["name"]


@pytest.mark.django_db
def test_update_courses(api_client, course_factory):
    course_factory(_quantity=5)
    course_1 = Course.objects.first()
    url = reverse("courses-detail", args=(course_1.id, ))
    data_update = {
        "name": "Super course"
    }
    response = api_client.patch(url, data_update)
    assert response.status_code == 200
    assert response.data["name"] == data_update["name"]


@pytest.mark.django_db
def test_delete_courses(api_client, course_factory):
    course_factory(_quantity=5)
    course_1 = Course.objects.first()
    url = reverse("courses-detail", args=(course_1.id, ))
    response = api_client.delete(url)
    assert response.status_code == 204
    assert response.data is None
