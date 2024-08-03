from django import forms
from post.models import Post, Comment

class CreatePostForm(forms.ModelForm):
    picture= forms.ImageField(required= True)
    caption= forms.CharField(widget= forms.TextInput(attrs= {'class': 'input', 'placeholder': 'Caption'}), required= True)
    tags= forms.CharField(widget= forms.TextInput(attrs= {'class': 'input', 'placeholder': 'Tags- Seperate Tag with commas'}), required= True)

    class Meta:
        model= Post
        fields= ['picture', 'caption', 'tags'] 

class CommentForm(forms.ModelForm):
    body= forms.CharField(widget= forms.TextInput(attrs= {'class': 'input', 'placeholder': 'Add a Comment...'}), required= True)
    class Meta:
        model= Comment
        fields= ['body']