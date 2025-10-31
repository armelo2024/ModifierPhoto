from django import forms

class UploadForm(forms.Form):
    image = forms.ImageField()
    bg_color = forms.CharField(max_length=7, initial="#FFFFFF")
    is_transparent = forms.BooleanField(required=False)
