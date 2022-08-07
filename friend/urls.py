from django.urls import path
from . import views


urlpatterns = [
    path('friends/', views.friendsHome, name='friends'),
    path('friends/friend-requests', views.viewRequests, name='friend-requests'),
    path('friends/friend-requests/accept-request/<requestID>',
         views.acceptRequest, name='accept-request'),
    path('friends/friend-requests/reject-request/<requestID>',
         views.rejectRequest, name='reject-request'),
    path('friends/friend-requests/send-request/<userID>',
         views.sendRequest, name='send-request'),

]
