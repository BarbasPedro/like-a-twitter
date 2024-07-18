from django import forms

from twitter.models import Post


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("content", "photo")
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 3,
                'cols': 40,
            }),
        }
