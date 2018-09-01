from django import forms

class UserForm(forms.Form):
    img_folder = forms.FileField()
