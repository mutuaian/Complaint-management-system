from django import forms
from django.contrib.auth.models import User
from .models import Admin, Complainants, Category, Subcategory, Complaints, ComplaintRemark
class RegisterForm(forms.ModelForm):
    username = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
        	'class': 'form-control',
        	'placeholder': 'Username'
        	 }
        ))
    # first_name = forms.CharField(max_length=150, widget=forms.TextInput(
    #     attrs={
	   #      'class': 'form-control', 
	   #      'placeholder': 'first name'
	   #      }
    #     ))
    # last_name = forms.CharField(max_length=150, widget=forms.TextInput(
    #     attrs={
    #     	'class': 'form-control',
    #     	'placeholder': 'last name'
    #     	}
    #     ))
    email = forms.CharField(max_length=150, widget=forms.TextInput(
        attrs={
        	'class': 'form-control', 
        	'type': 'email', 
        	'placeholder': 'email address'
        	}
        ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
        	'class': 'form-control',
        	'placeholder': 'password'
        	}
        ))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.ModelForm):
	username = forms.CharField(max_length = 50, widget = forms.TextInput(
			attrs ={
				'placeholder': 'UserId',
				'class':'form-control',
				'autofocus':'True'
			}
		))
	password = forms.CharField(widget = forms.PasswordInput(
			attrs = {
				'class':'form-control',
				'placeholder':'Password',
				'autofocus':'True'
			}
		))
	class Meta:
		model = User
		fields = ['username','password']

	def validate_username(self):
		pass

class Forgotpass(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput(
        attrs = {
            'class':'form-control',
            'placeholder':'Password',
            'autofocus':'True'
            }
        ))
    confirm_password = forms.CharField(widget = forms.PasswordInput(
            attrs = {
                'class':'form-control',
                'placeholder':'Password',
                'autofocus':'True'
            }
        ))
    class Meta:
        model = User
        fields = ['password','confirm_password']