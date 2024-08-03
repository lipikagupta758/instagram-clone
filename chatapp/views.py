from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

def inbox(request):
    user= request.user
    messages= Message.get_message(user= user)      #fetch the user's messages, grouped by recipient, including the last message date and unread count    
    
    return render(request, 'chatapp/inbox.html', {'messages': messages})
    
def directs(request, username):
    user= request.user
    messages= Message.get_message(user=user)
    active_direct= username   #active_directs represent the username of the user with whom the most recent conversation is active
    directs= Message.objects.filter(user= user, reciepient__username= active_direct)    #store the list of messages exchanged between the logged-in user and the active direct user

    directs.update(is_read= True)

    for message in messages:
        if message['user'].username== active_direct:
            message['unread']= 0

    return render(request, 'chatapp/directs.html', {'directs': directs, 'active_direct': active_direct, 'messages': messages})
