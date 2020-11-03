from django import forms

LANGUAGE_CHOICES = (
	("en-us", "English"),
	("hi", "Hindi"),
	("te", "Telugu"),
	)

class ImUpForm(forms.Form):

	hwform = forms.ImageField(label='Upload an image ', widget=forms.FileInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Choose an image file'
            }
        ))

class DetailsForm(forms.Form):

	lang = forms.MultipleChoiceField(choices=LANGUAGE_CHOICES, label='Choose language', required=True)
	email = forms.EmailField(label='Email id', required=True)