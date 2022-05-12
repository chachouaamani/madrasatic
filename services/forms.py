from django import forms
from users.models import Users

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = Users
        fields= ['first_name','last_name','image']