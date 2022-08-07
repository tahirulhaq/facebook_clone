from venv import create
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from blog.models import Friend_Request
from .models import Comment, Post, Reply
from .forms import PostForm
from django.template.loader import render_to_string


# Create your views here.


def viewPost(request):
    return HttpResponse('view post here')


def createPost(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        post = Post.objects.create(
            author=request.user,
            content=content
        )
    # context = {'form': form}
    # return render(request, 'post/post_form.html', {context})
    return redirect('home')


def updatePost(request, pk):
    post = Post.objects.get(id=pk)
    # form = PostForm(instance=post)
    # if request.method == 'POST':
    #     form = PostForm(request.POST, instance=post)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('home')

    if request.method == 'POST':
        content = request.POST.get('content')
        post.content = content
        post.save()
    return redirect('home')

    # context = {'form': form}
    # return render(request, 'post/post_form.html',{})


def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('home')
    # return render(request, 'post/delete.html', {})


def deleteComment(request, pk):
    comment = Comment.objects.get(id=pk)

    comment.delete()
    return redirect('home')


def deleteReply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.delete()
    return redirect('home')


def createComment(request, id):
    post = Post.objects.get(id=id)
    if request.method == 'POST':
        comment = Comment.objects.create(
            user=request.user,
            post=post,
            body=request.POST.get('body')
        )
    return redirect('home')


def createReply(request, id):
    comment = Comment.objects.get(id=id)
    if request.method == 'POST':
        reply = Reply.objects.create(
            user=request.user,
            comment=comment,
            description=request.POST.get('description')
        )
    return redirect('home')

# solution for error => request.is_ajax is not a function


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def like_post(request):
    print(request.POST.get('id'))
    print('hello world')
    post = get_object_or_404(Post, id=request.POST.get('id'))

    for likes in post.likes.all():
        print(likes)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        print('removed')
    else:
        post.likes.add(request.user)
        print('added')

    post.save()
    context = {'post': post}
    print(post)
    if is_ajax(request):
        html = render_to_string('post/like_section.html',
                                context, request=request)
        return JsonResponse({'form': html})
