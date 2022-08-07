from django.http import HttpResponse
from django.shortcuts import render
from blog.models import Friend_Request, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.


def friendsHome(request):
    user_fr = Friend_Request.user_friend_requests(request.user)
    user_friends = request.user.profile.friend.all()
    context = {'user_fr': user_fr, 'friends': user_friends}
    return render(request, 'friend/friends_home.html', context)


@login_required(login_url='login')
def viewRequests(request):
    user_fr = Friend_Request.user_friend_requests(request.user)
    context = {'user_fr': user_fr}
    return render(request, 'friend/friend_requests.html', context)


@login_required(login_url='login')
def sendRequest(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('friend request sent')
    else:
        return HttpResponse('friend request was already sent')


@login_required(login_url='login')
def acceptRequest(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.profile.friend.add(friend_request.from_user)
        friend_request.from_user.profile.friend.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    else:
        return HttpResponse('friend request not accepted')


@login_required(login_url='login')
def rejectRequest(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    friend_request.delete()
    return HttpResponse('friend request rejected')
