from django import forms

class ImUpForm(forms.Form):

	hwform = forms.ImageField(label='Upload an image ', widget=forms.FileInput(
            attrs={
                'style': 'border-color: blue;',
                'placeholder': 'Choose an image file'
            }
        ))
