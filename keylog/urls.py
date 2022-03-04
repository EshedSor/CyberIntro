from django.urls import path, include
from rest_framework import routers
from keylog import views
from django.conf.urls.static import static
from django.conf import settings
router = routers.SimpleRouter()
router.register('sendData',views.streamViewSet)
urlpatterns = [
    path('',include(router.urls)),
]