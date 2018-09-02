from django import forms

class UserForm(forms.Form):
    img_folder = forms.FileField()
    select_list = [(1, "Seau de raisin"), (2, "Parcelle de blé")]
    select = forms.ChoiceField(choices=select_list,
                               initial='',
                               widget=forms.Select())
