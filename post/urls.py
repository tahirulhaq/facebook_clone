from django.urls import path
from . import views
urlpatterns = [
    path('post/<slug>/', views.viewPost, name='viewPost'),

    # create objects
    path('create-post/', views.createPost, name='create-post'),
    path('create-comment/<id>', views.createComment, name='create-comment'),
    path('create-reply/<id>', views.createReply, name='create-reply'),

    # update objects
    path('update-post/<str:pk>', views.updatePost, name='update-post'),


    # delete objects
    path('delete-post/<str:pk>', views.deletePost, name='delete-post'),
    path('delete-comment/<str:pk>', views.deleteComment, name='delete-comment'),
    path('delete-reply/<str:pk>', views.deleteReply, name='delete-reply'),

    # like section
    path('like/', views.like_post, name='like_post')
]
