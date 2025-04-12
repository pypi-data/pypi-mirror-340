from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from sparkplug_core.permissions import IsAdmin

from ...models import FeatureFlag
from ...serializers import FeatureFlagSerializer


class DetailView(APIView):
    permission_classes = (IsAdmin,)

    def get(self, request: Request, uuid: str) -> Response:
        instance = get_object_or_404(FeatureFlag, uuid=uuid)
        return Response(
            data=FeatureFlagSerializer(instance).data,
            status=status.HTTP_200_OK,
        )
