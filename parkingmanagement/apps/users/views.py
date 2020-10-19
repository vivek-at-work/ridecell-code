from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from users.serializers import SignUpSerializer, UserSerializer

USER = get_user_model()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read Only Model view set for user listing and sign up
    """
    queryset = USER.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(
        detail=False,
        serializer_class=SignUpSerializer,
        permission_classes=[permissions.AllowAny],
        methods=['post'],
    )
    def signup(self, request):
        """
        Custom action for user sign up using contact number and password
        """
        serializer = self.serializer_class(
            data=request.data, context={'request': request},
        )
        if serializer.is_valid(raise_exception=True):
            user = USER.objects.create_user(
                serializer.validated_data['contact_number'],
                serializer.validated_data['password'],
            )
            return Response(
                UserSerializer(user, context={'request': request}).data,
                status=status.HTTP_201_CREATED,
            )
