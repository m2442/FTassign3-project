
from django.urls import path, include
from .views import  MemberViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('Member', MemberViewSet, basename='member')
urlpatterns = [


    path('viewset/', include(router.urls)),
    path('viewset/<int:pk>/', include(router.urls)),

  ]
