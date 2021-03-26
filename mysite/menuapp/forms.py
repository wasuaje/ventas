
from django import forms
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from models import *
from django.forms import ModelForm,Textarea,TextInput,HiddenInput
from django.forms.extras.widgets import SelectDateWidget

class GenericSearchForm(forms.Form):
    buscar = forms.CharField(required=False)  

class ManageMenuItems(ModelForm):
    class Meta:
        model = MenuItem
        fields = '__all__' 

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)    


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','first_name','last_name')        

    def save(self,commit = True):   
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']        

        if commit:
            user.save()

        return user


class MyLoginForm(AuthenticationForm):
    username = forms.CharField(required = True)
    password = forms.CharField(required = True,widget=forms.PasswordInput)
   

    class Meta:
        model = User
        fields = ('username',  'password')   