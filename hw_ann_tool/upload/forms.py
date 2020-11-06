from django import forms

LANGUAGE_CHOICES = (
	# ("en-us", "English"),
	("hi", "Hindi"),
	("te", "Telugu"),
	)

class ImUpForm(forms.Form):

	hwform = forms.ImageField(label='Upload your file', widget=forms.FileInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Choose an image file'
            }
        ))
	# para_id = forms.CharField(max_length=100,
	# 						  initial='an',
	# 						  required=False,
	# 						 widget=forms.HiddenInput())

class DetailsForm(forms.Form):

	lang = forms.ChoiceField(choices=LANGUAGE_CHOICES,
		                             label='Your choice of language',
		                             required=True,
		                             widget=forms.Select(attrs={'class':'form-control'}),
		                             )
	email = forms.EmailField(label='Email id')