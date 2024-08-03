from .models import Profile
from django import forms

class EditProfileForm(forms.ModelForm):
    image= forms.ImageField(required=True)
    first_name= forms.CharField(widget= forms.TextInput(attrs= {'class': 'input'}), required=True)
    bio= forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'cols': 40}))
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'image', 'location', 'bio', 'url')
