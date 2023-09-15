from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm

from .models import User,Review

class NewsletterForm(forms.Form):
  newsletter_email=forms.CharField(widget=forms.EmailInput(attrs={'class':'input'}))

class ReviewForm(forms.Form):
  review_email=forms.CharField(widget=forms.EmailInput(attrs={'class':'input','placeholder':'Your Email'}))
  review_content=forms.CharField(widget=forms.Textarea(attrs={'class':'input','placeholder':'Your Review'}))
  review_by=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Your Name'}))
  
  #  class Meta:
  #     model=Review
  #     fields=('review_email','review_content', 'review_by','review_ratings','review_for')
  #     widgets = {
  #                   'review_email': forms.EmailInput(attrs={'class': 'input','placeholder':'Your Email'}),
  #                   'review_content': forms.Textarea(attrs={'class': 'input','placeholder':'Your Review'}),
  #                   'review_by': forms.TextInput(attrs={'class': 'input','placeholder':'Your Name'}),
  #               }
class SignupForm(UserCreationForm):
  password1= forms.CharField(label='Enter Your Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Enter Your Password'}))
  password2=forms.CharField(label='Confirm Your Password',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Your Password'}))
  class Meta:
    model= User
    fields=('cust_fname','cust_lname', 'email', 'password1','password2')
    labels={'cust_lname':'Enter Your Last Name', 'cust_fname':'Enter Your First Name', 'cust_email':'Enter Your Email Address' }
    widgets = {
            'cust_lname': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Last Name'}),
            'cust_fname': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your First Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control','placeholder':'Enter Your Email Address'}),
        }
  def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('password2')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
class ProfileForm(UserChangeForm):
  class Meta:
        model = User
        fields = ('cust_image','cust_fname','cust_lname','cust_phone','cust_address')
        exclude =['password']
        labels={'cust_image':'Pick Your Image','cust_fname':'Enter Your First Name','cust_lname':'Enter Your Last Name','cust_phone':'Enter Your Phone Number','cust_address':'Enter Your Address'}    
        widgets = {
                    'cust_lname': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Last Name'}),
                    'cust_fname': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your First Name'}),
                    'cust_phone': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Phone Number'}),
                    'cust_image': forms.FileInput(attrs={'class': 'form-image'}),
                    'cust_address': forms.Textarea(attrs={'class': 'form-control','placeholder':'Enter Your Address'})
                }
  # class Meta:
  #     model=User
  #     fields=['cust_image','cust_fname','cust_lname','cust_phone','cust_address']
  #     labels={'cust_image':'Pick Your Image','cust_fname':'Enter Your First Name','cust_lname':'Enter Your Last Name','cust_phone':'Enter Your Phone Number','cust_address':'Enter Your Address'}
  #     widgets = {
  #           'cust_lname': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Last Name'}),
  #           'cust_fname': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your First Name'}),
  #           'cust_phone': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter Your Phone Number'}),
  #           'cust_image': forms.FileInput(attrs={'class': ' custom-file-input'}),
  #           'cust_address': forms.Textarea(attrs={'class': 'form-control','placeholder':'Enter Your Address'})
  #       }