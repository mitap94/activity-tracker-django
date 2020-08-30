from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user import views

app_name = 'user'

router = DefaultRouter()
router.register('users', views.UserViewSet)


# All users
# /api/user/create - create a new user
# /api/user/token - retrieve an auth token

# Authenticated users
# /api/user/me - manage current user

# Admins only
# /api/user/users - list all users
# /api/user/users/<id> - view detail for a specific user

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('google_token/', views.GoogleLogin.as_view(), name='google_token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('', include(router.urls)),
]
