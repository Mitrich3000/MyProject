from django.contrib.auth.models import User
from django.forms import Textarea

from .models import Post, Blog
from django import forms


class PostForm(forms.ModelForm):
    title = forms.CharField(label="Заголовок", widget=forms.TextInput(attrs={'size': 100}), )
    content = forms.Textarea()

    class Meta:
        model = Post
        fields = ('title', 'content')
        widgets = {
            'content': Textarea(attrs={'cols': 100, 'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        blog = kwargs.pop('blog', None)
        super(PostForm, self).__init__(*args, **kwargs)


class Blog1Form(forms.ModelForm):
    title = forms.CharField(label="Заголовок")

    class Meta:
        model = Blog
        fields = ('title',)


class UserForm(forms.ModelForm):
    subscribed = forms.ModelMultipleChoiceField(queryset=Blog.objects.all(), label='Доступные блоги',
                                           widget=forms.CheckboxSelectMultiple, required=False)

    # display only available blogs
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['subscribed'].queryset = Blog.objects.filter(subscribed=user)

    class Meta:
        model = User
        fields = ('subscribed',)
