from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from six import text_type

USER = get_user_model()

class EmailVerification:

    def send_conformation_email(self, request, user):
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = AppTokenGenerator()
        token.make_token(user)
        domain = get_current_site(request).domain
        link = reverse('users:activate', kwargs={'uid': uidb64, 'token': token})
        activate_url = 'http://'+domain+link
        email_subject = 'Activate Your Email'
        email_body = 'Hi ' + user.username + ' Please use this to verify your account.'+activate_url
        email = EmailMessage(
            email_subject,
            email_body,
            'noreply@myblogpost.com',
            [user.email],
        )
        email.send(fail_silently=True)

    def get_user_id(self, uid):
        return force_text((urlsafe_base64_decode(uid)))


class AppTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return (text_type(user.is_active)+text_type(user.pk)+text_type(timestamp))