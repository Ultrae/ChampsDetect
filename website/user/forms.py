from django import forms

class UserForm(forms.Form):
    img_folder = forms.FileField()
    select_list = ["Seau de raisin"]
    select = forms.ChoiceField(choices=select_list)
