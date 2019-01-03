from django import forms

class ImSearchForm(forms.Form):

	#name = forms.ModelChoiceField(label='Choose a collection',
	#							 queryset=Collections.objects.all(),
	#							 initial=Collections.objects.filter(id = 0))
	query = forms.ImageField(label='Upload an image ')


class TxtSearchForm(forms.Form):

	query = forms.CharField(label='Enter your query')

	