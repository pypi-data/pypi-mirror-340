from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from sparkplug_core.permissions import IsAdmin
from sparkplug_core.utils import get_paginated_response

from ...queries import feature_flag_list
from ...serializers import FeatureFlagSerializer


class ListView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request: Request) -> Response:
        return get_paginated_response(
            serializer_class=FeatureFlagSerializer,
            queryset=feature_flag_list(),
            request=request,
            view=self,
        )
