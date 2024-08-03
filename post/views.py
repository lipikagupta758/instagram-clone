from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from post.models import Tag, Stream, Follow, Post, Likes, Comment
from post.forms import CreatePostForm, CommentForm
from django.urls import reverse, resolve
from userauth.models import Profile
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

# view to display posts on home page  

def index(request):
    user= request.user 
    profile= Profile.objects.get(user= user)
    posts= Stream.objects.filter(user=user)    #posts of following 
    posts_user= Post.objects.filter(user= user)    #posts of self

    group_ids= []
    for post in posts:
        group_ids.append(post.post_id)  
    for post in posts_user:
        group_ids.append(post.id)  

    post_items= Post.objects.filter(id__in= group_ids).all().order_by('-posted')     #using -posted, posts will be ordered based on their posted date. Recent post will come firsr, then old posts 
    
    # context= {
    #     'post_items': post_items
    # }
     
    return render(request, 'index.html', {'post_items': post_items, 'profile': profile})  

# view to create a new post
def createPost(request):
    user= request.user
    tags_objs= []

    if request.method== "POST":
        form= CreatePostForm(request.POST, request.FILES)
        if form.is_valid():
            picture= form.cleaned_data.get('picture')
            caption= form.cleaned_data.get('caption')
            tags_input= form.cleaned_data.get('tags')
            tags_list= list(tags_input.split(','))  # house, icecream, etc. 

            for tag in tags_list:
                t, created= Tag.objects.get_or_create(title= tag)
                tags_objs.append(t)

            # Create Post object
            try:
                post_obj = Post.objects.create( picture=picture, caption=caption, user= user)
                post_obj.tags.set(tags_objs)
                post_obj.save()

                return redirect('index')
            except Exception as e:
                logger.error(f'Error creating post: {e}')      
    else:
        form= CreatePostForm()

    return render(request, 'createpost.html', {'form': form} )

# view for viewing a post seperately
def postDetail(request, post_id):
    post= get_object_or_404(Post, id= post_id)
    user_has_liked= Likes.objects.filter(user= request.user, post= post)
    # displaying all comments on a post
    comments= Comment.objects.filter(post= post).all().order_by('-date')

    # add comment
    if request.method== "POST":
        form= CommentForm(request.POST)
        if form.is_valid():
            comment= form.save(commit=False)
            comment.post= post
            comment.user= request.user
            comment.save()
            return redirect('post-details', post_id)
    else:
        form= CommentForm()
    return render(request, 'postdetail.html', {'post': post, 'form': form, 'comments': comments, 'user_has_liked': user_has_liked})

# view for liking and disliking a post
def like(request, post_id):
    user= request.user
    post= Post.objects.get(id= post_id)
    current_likes= post.likes
    liked= Likes.objects.filter(user= user, post= post).count()
    if not liked:
        liked= Likes.objects.create(user= user, post=post)
        current_likes= current_likes + 1
    else:
        liked= Likes.objects.filter(user= user, post=post).delete()
        current_likes= current_likes - 1
    
    post.likes= current_likes
    post.save()
    url_name= resolve(request.path).url_name
    if url_name== 'post-details':
        return redirect('post-details', post_id)
    else:
        return redirect('index')
    # return HttpResponseRedirect(reverse('post-details', args=[post_id]))

# view for adding posts to favourites
def favourite(request, post_id):
    user= request.user
    post= Post.objects.get(id= post_id)
    profile= Profile.objects.get(user= user)
    if profile.favourite.filter(id= post_id).exists():
        profile.favourite.remove(post)
    else:
        profile.favourite.add(post)
    return redirect('index')
    # return HttpResponseRedirect(reverse('post-details', args=[post_id]))