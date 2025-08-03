from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'messages', views.MessageViewSet, basename='message')
router.register(r'notifications', views.NotificationViewSet, basename='notification')
router.register(r'conversations', views.ConversationViewSet, basename='conversation')

app_name = 'messaging'

urlpatterns = [
    path('', include(router.urls)),
] 