from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, mixins
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from user.serializers import CreateManageUserSerializer, UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user"""
    serializer_class = CreateManageUserSerializer

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the current user"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    serializer_class = CreateManageUserSerializer

    def get_object(self):
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    """Create an authentication token for a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """View list of users or detail for a single user"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsAdminUser,)

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

