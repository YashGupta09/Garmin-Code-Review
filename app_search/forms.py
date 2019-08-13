from django import forms

class SearchForm(forms.Form):
	fileName = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'id': 'search',
			'name': 'fname',
			'placeholder': 'File Name . .'
		}))
	content = forms.CharField(required=False, widget=forms.TextInput(attrs={
			'id': 'search1',
			'name': 'content',
			'placeholder': 'Arguments . . '
		}))