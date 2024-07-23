from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_logged_in)
def send_login_email(sender, request, user, **kwargs):
    subject = 'Login Notification'
    message = f'Hi {user.cust_fname} {user.cust_lname},\n\nYou have successfully logged in.'
    recipient_list = [user.email]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
