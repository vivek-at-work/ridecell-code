from django.contrib import admin
from django.urls import include, path
from parkings.routers import parkings_router
from users.routers import users_router

from parkingmanagement.default_router import DefaultRouter

router = DefaultRouter()
router.extend(users_router)
router.extend(parkings_router)
urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('admin/', admin.site.urls),
]
