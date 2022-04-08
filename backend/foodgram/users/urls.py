from django.urls import path, include

from users.views import SubscriptionsApiView, SubscribeApiView

urlpatterns = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('users/subscriptions/', SubscriptionsApiView.as_view(), name='subscriptions'),
    path('users/<int:following_id>/subscribe/', SubscribeApiView.as_view(), name='subscribe'),
]
