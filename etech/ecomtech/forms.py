from django import forms
class NewsletterForm(forms.Form):
  newsletter_email=forms.CharField(widget=forms.EmailInput(attrs={'class':'input'}))
class LoginForm(forms.Form):
  cust_email=forms.CharField(widget=forms.EmailInput(attrs={'class':'input','placeholder':'Enter Your Email Address'}))
  cust_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'input','placeholder':'Enter Your Password'}),max_length=16,min_length=8)
class SignupForm(forms.Form):
  cust_fname=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter Your First Name'}))
  cust_lname=forms.CharField(widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter Your Last Name'}))
  cust_email=forms.CharField(widget=forms.EmailInput(attrs={'class':'input','placeholder':'Enter Your Email Address'}))
  cust_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'input','placeholder':'Enter Your Password'}),max_length=16,min_length=8)
  confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'input','placeholder':'Confirm Your Password'}),max_length=16,min_length=8)
  cust_phone= forms.CharField(max_length=20,widget=forms.TextInput(attrs={'class':'input','placeholder':'Enter You Phone Number'}))
  def clean(self):
    cleaned_data = super(SignupForm, self).clean()
    password = cleaned_data.get("cust_password")
    confirm_password = cleaned_data.get("confirm_password")

    if password != confirm_password:
      raise forms.ValidationError(
                "password and confirm_password does not match"
            )