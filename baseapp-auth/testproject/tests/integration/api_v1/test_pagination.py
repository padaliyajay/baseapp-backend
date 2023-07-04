from django.test import RequestFactory

import pytest
from rest_framework import viewsets
from rest_framework.settings import api_settings

from apps.api.v1.users.serializers import UserSerializer
from apps.users.models import User

import tests.factories as f
import tests.helpers as h

pytestmark = pytest.mark.django_db


class TestPagination:
    class TestModelViewSet(viewsets.ModelViewSet):
        queryset = User.objects.all()
        permission_classes = []
        serializer_class = UserSerializer

    def test_uses_page_size_query_param(self):
        expected_page_size = 5
        f.UserFactory.create_batch(size=expected_page_size + 1)
        self.factory = RequestFactory()

        request = self.factory.get("", {"page_size": expected_page_size})
        response = self.TestModelViewSet.as_view({"get": "list"})(request)
        h.responseOk(response)
        assert len(response.data["results"]) == expected_page_size

    def test_uses_page_size_setting_by_default(self):
        f.UserFactory.create_batch(size=api_settings.PAGE_SIZE + 1)
        self.factory = RequestFactory()

        request = self.factory.get("")
        response = self.TestModelViewSet.as_view({"get": "list"})(request)
        h.responseOk(response)
        assert len(response.data["results"]) == api_settings.PAGE_SIZE