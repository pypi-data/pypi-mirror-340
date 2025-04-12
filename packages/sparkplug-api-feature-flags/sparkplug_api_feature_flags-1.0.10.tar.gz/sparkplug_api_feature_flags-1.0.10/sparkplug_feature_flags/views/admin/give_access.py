from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from sparkplug_core.permissions import IsAdmin
from sparkplug_core.utils import get_validated_dataclass

from ...models import FeatureFlag
from ...queries import flag_access_list
from ...serializers import (
    FlagAccessSerializer,
    UserUuidData,
    UserUuidSerializer,
)


class GiveAccessView(APIView):
    permission_classes = (IsAdmin,)

    def patch(self, request: Request, uuid: str) -> Response:
        instance = get_object_or_404(FeatureFlag, uuid=uuid)
        validated_data: UserUuidData = get_validated_dataclass(
            UserUuidSerializer,
            input_data=request.data,
        )
        instance.users.add(validated_data.user)

        qs = flag_access_list(request.user, uuid)
        return Response(
            data=FlagAccessSerializer(qs, many=True).data,
            status=status.HTTP_200_OK,
        )
