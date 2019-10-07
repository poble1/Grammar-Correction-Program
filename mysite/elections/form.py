from django import forms
from .models import Post


class FormPost(forms.ModelForm):
	class Meta:
		model = Post
		fields = '__all__'


class PostForm(forms.Form):
	text = forms.CharField(widget=forms.Textarea, label='')
