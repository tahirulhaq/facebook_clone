from asyncio.windows_events import NULL
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from blog.models import Friend_Request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from post.models import Post, Comment, Reply
# Create your views here.

# 1 Home Page


@login_required(login_url='login')
def home(request):
    user = request.user
    posts = Post.objects.all()
    comments = Comment.objects.all()
    replies = Reply.objects.all()

    context = {'user': user, 'posts': posts,
               'comments': comments, 'replies': replies}
    return render(request, 'blog/home.html', context)

# 2 ViewProfile


@login_required(login_url='login')
def viewProfile(request, username):

    user = User.objects.get(username=username)
    is_private = user.profile.is_private

# posts
    posts = Post.objects.all().filter(author=user)

# is blocked or not
    if user.profile.blocked_user.filter(username=request.user.username).exists():
        is_blocked_by_user = True
    else:
        is_blocked_by_user = False

    if request.user.profile.blocked_user.filter(username=user.username).exists():
        is_blocked_by_you = True
    else:
        is_blocked_by_you = False

# friend requests and friends
    friends = user.profile.friend.all()
    friend_requests = Friend_Request.all_friend_requests()

    fr_sent = False
    for fr in friend_requests:
        if request.user == fr.from_user and user == fr.to_user:
            fr_sent = True

    context = {'user': user, 'posts': posts, 'friends': friends, 'fr_sent': fr_sent,
               'is_blocked_by_user': is_blocked_by_user, 'is_blocked_by_you': is_blocked_by_you, 'is_private': is_private}
    return render(request, 'blog/profile.html', context)

# 3 LoginUSer


def loginUser(request):
    context = {}
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            print('user does not exist')
        if user.is_active == False:
            context = {'message': 'Account is not Active'}
            return render(request, 'blog/login.html', context)

        user = authenticate(request, username=user.username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            context = {'user': user,
                       'message': 'Email OR password does not exist'}

    return render(request, 'blog/login.html', context)

# 4 logout user


def logoutUser(request):
    logout(request)
    return redirect('home')

# 5 registerUser


def createBirth(request):
    year = request.POST.get('birthday_year')
    month = request.POST.get('birthday_month')
    day = request.POST.get('birthday_day')
    birth = year + '-' + month + '-' + day
    return birth


def registerUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':

        # post variables
        username = request.POST.get('first_name').replace(" ", "").lower()
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email_no').lower()
        password = request.POST.get('password1')
        gender = request.POST.get('gender')
        birth_date = createBirth(request)

        # user object create
        user = User.objects.create_user(username, email, password)
        user.is_active = False
        user.first_name = first_name
        user.last_name = last_name
        user.profile.gender = gender
        user.profile.birth_date = birth_date
        user.save()
        current_site = get_current_site(request)
        mail_subject = 'Activation link has been sent to your email id'
        message = render_to_string('blog/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = email
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        try:
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration <a href="/">Go to Login</a>')
        except:
            user.delete()
            context = {'message': 'an error occured while sending email'}

    else:
        context = {'message': 'An error occured during registration'}
        return render(request, 'blog/login_register.html', context)

# Block User


def blockUser(request, id):
    user = User.objects.get(id=id)
    request.user.profile.blocked_user.add(user)
    request.user.profile.friend.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# Unblock User


def unblockUser(request, id):
    user = User.objects.get(id=id)
    request.user.profile.blocked_user.remove(user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

# make private or public


def changePrivacy(request, id):
    user = User.objects.get(id=id)
    if user.profile.is_private == True:
        user.profile.is_private = False
        user.save()
    else:
        user.profile.is_private = True
        user.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.<a href="/">Go to Login</a>')
    else:
        return HttpResponse('Activation link is invalid!')


def viewTest(request):
    return render(request, 'blog/test-page.html', {})
