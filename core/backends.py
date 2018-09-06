import requests
import json
from .models import User, SiteConfiguration
from django.core.files.base import ContentFile
from urllib.request import urlopen
from django.core.mail.backends.smtp import EmailBackend

class ElggBackend:

    def authenticate(self, request, username=None, password=None):

        #load site configuration
        site_config = SiteConfiguration.objects.get()
        config_data = site_config.get_values()

        if not config_data['elgg_url']:
            return None

        elgg_url = config_data['elgg_url']

        # Check if user exists (case-insensitive)
        try:
            user = User.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            # Verify username/password combination
            valid_user_request = requests.post(elgg_url + "/services/api/rest/json/", data={'method': 'pleio.verifyuser', 'user': username, 'password': password})
            valid_user_json = json.loads(valid_user_request.text)
            valid_user_result = valid_user_json["result"] if 'result' in valid_user_json else []
            valid_user = valid_user_result["valid"] if 'valid' in valid_user_result else False
            name = valid_user_result["name"] if 'name' in valid_user_result else username
            admin = valid_user_result["admin"] if 'admin' in valid_user_result else False

            # If valid, create new user with Elgg attributes
            if valid_user is True:
                user = User.objects.create_user(
                    name=name,
                    email=username,
                    password=password,
                    accepted_terms=True,
                    receives_newsletter=True
                )
                user.is_active = True
                user.is_admin = admin
                user.save()
                return user
            else:
                return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class SiteConfigEmailBackend(EmailBackend):
    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=None, use_ssl=None, timeout=None,
                 ssl_keyfile=None, ssl_certfile=None,
                 **kwargs):

        configuration = SiteConfiguration.objects.get()

        super(SiteConfigEmailBackend, self).__init__(
             host = configuration.email_host if host is None else host,
             port = configuration.email_port if port is None else port,
             username = configuration.email_user if username is None else username,
             password = configuration.email_password if password is None else password,
             use_tls = configuration.email_use_tls if use_tls is None else use_tls,
             fail_silently = configuration.email_fail_silently if fail_silently is None else fail_silently,
             use_ssl = configuration.email_use_ssl if use_ssl is None else use_ssl,
             timeout = configuration.email_timeout if timeout is None else timeout,
             ssl_keyfile = ssl_keyfile,
             ssl_certfile = ssl_certfile,
             **kwargs)


__all__ = ['SiteConfigEmailBackend']
