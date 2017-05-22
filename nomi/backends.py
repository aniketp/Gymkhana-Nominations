from django.contrib.auth.models import User
from imaplib import IMAP4


class MyCustomBackend:

    # Create an authentication method
    # This is called by the standard Django login procedure
    def authenticate(self, username=None, password=None):
        try:
            # Check if this user is valid on the mail server
            c = IMAP4('newmailhost.cc.iitk.ac.in')
            c.login(username, password)
        except:
            return None

        user, created = User.objects.get_or_create(username=username)

        return user

    # Required for your backend to work properly - unchanged in most scenarios
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None