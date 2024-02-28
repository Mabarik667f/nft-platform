from django.urls import path

from .views import UserLoginView, UserProfileView

app_name = 'users'
urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile')
]