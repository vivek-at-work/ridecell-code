from rest_framework.routers import DefaultRouter
from users.views import UserViewSet

users_router = DefaultRouter()
users_router.register(r'users', UserViewSet)
