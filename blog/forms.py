from django import forms
from blog.models import Comment

class ShareByEmailForm(forms.Form):
    to_email = forms.EmailField(required=True)
    # username = forms.CharField(max_length=20, required=True)
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']