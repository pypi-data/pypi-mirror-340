from unittest.mock import patch

from apps.users.factories import UserFactory
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from sparkplug_feature_flags.views.admin import SearchView


class TestSearchView(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = UserFactory(is_staff=True)

    @patch("sparkplug_feature_flags.queries.feature_flag_search")
    def test_search_view(self, mock_feature_flag_search):
        mock_feature_flag_search.return_value = []

        request = self.factory.get(
            "/api/feature-flags/search/?term=test&page=1"
        )
        force_authenticate(request, user=self.user)
        response = SearchView.as_view()(request)
        assert response.status_code == 200
        assert "results" in response.data
        assert "count" in response.data
