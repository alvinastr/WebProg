from django import forms
from content.models import ContentPost


class CreateContentPostForm(forms.ModelForm):

	class Meta:
		model = ContentPost
		fields = ['title', 'body', 'image']

class UpdateContentPostForm(forms.ModelForm):

	class Meta:
		model = ContentPost
		fields = ['title', 'body', 'image']

	def save(self, commit=True):
		content_post = self.instance
		content_post.title = self.cleaned_data['title']
		content_post.body = self.cleaned_data['body']

		if self.cleaned_data['image']:
			content_post.image = self.cleaned_data['image']

		if commit:
			content_post.save()
		return content_post