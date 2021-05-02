from django import forms
from blog.models import Comment, Post
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ShareByEmailForm(forms.Form):
    to_email = forms.EmailField(required=True)
    # username = forms.CharField(max_length=20, required=True)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        
# class SignUpForm(forms.ModelForm):
#     password=forms.CharField(widget=forms.PasswordInput())
#     confirm_password=forms.CharField(widget=forms.PasswordInput())
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']
        
#     def clean(self):
#         pass1 = self.cleaned_data['password']
#         pass2 = self.cleaned_data['confirm_password']
        
#         if pass1 != pass2:
#             raise forms.ValidationError("Password doesn't match")
        
class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'tags', 'status']
        # fields = '__all__'
        
        
        
class SignUpForm(UserCreationForm):
    email = forms.EmailField(label = "Email")

    class Meta:
        model = User
        fields = ('username', )
        
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user