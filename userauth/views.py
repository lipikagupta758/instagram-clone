from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from post.models import Post, Follow, Stream
from .models import Profile
from .forms import EditProfileForm
from django.core.paginator import Paginator
from django.urls import resolve
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction

# Create your views here.

def userProfile(request, username):
    user= get_object_or_404(User, username= username)
    profile= Profile.objects.get(user= user)
    url_name= resolve(request.path).url_name
    if url_name== 'profile':
        posts= Post.objects.filter(user= user).order_by('-posted')
    else:
        posts= profile.favourite.all()

    # Track number of posts and followers, following
    post_count= Post.objects.filter(user= user).count()
    following_count= Follow.objects.filter(follower= user). count()
    followers_count= Follow.objects.filter(following= user). count()

    # Follow status
    follow_status= Follow.objects.filter(follower= request.user , following= user).exists()
    
    # pagination
    paginator= Paginator(posts, 3)
    page_number= request.GET.get('page')
    posts_paginator= paginator.get_page(page_number)

    context={
        'post_paginator': posts_paginator,
        'posts': posts,
        'profile': profile,
        'url_name': url_name,
        'post_count': post_count,
        'following_count': following_count,
        'followers_count': followers_count,
        'follow_status': follow_status
    }
    return render(request, 'profile.html', context)

def follow(request, username):
    user= request.user
    following= get_object_or_404(User, username= username)
    try:
        followed= Follow.objects.filter(follower= user , following= following).exists()

        if not followed:
            followed= Follow.objects.create(follower= user, following= following)
            posts= Post.objects.filter(user= following)[:5]       #5 posts which are already posted by the user, are added in stream of follower
            with transaction.atomic():
                for post in posts:
                    stream= Stream(post=post, user= user, date= post.posted, following= following)
                    stream.save()
        else:
            followed= Follow.objects.filter(follower= user, following= following).delete()
            Stream.objects.filter(user= user, following= following).all().delete()
 
        return HttpResponseRedirect(reverse('profile', args= [username]))
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse('profile', args= [username]))
    
def editProfile(request, username):
    user= request.user
    profile= get_object_or_404(Profile, user= user)
    if request.method== 'POST':
        form= EditProfileForm(request.POST, request.FILES, instance= profile)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('profile', args= [username]))
    else:
        form= EditProfileForm(instance= profile)
    return render(request, 'editprofile.html', {'form': form})
