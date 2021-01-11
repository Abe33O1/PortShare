from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'tags',
        ]
    def __init(self, *args, **kwargs):
        user = kwargs.pop('user',None)
        super(PostForm, self).__init__(*args, **kwargs)
