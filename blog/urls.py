from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('viewProfile/<username>/', views.viewProfile, name='viewProfile'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('block-user/<id>', views.blockUser, name='block-user'),
    path('unblock-user/<id>', views.unblockUser, name='unblock-user'),
    path('change-privacy/<id>', views.changePrivacy, name='change-privacy'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('test', views.viewTest, name='test-page'),



]
# path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),
