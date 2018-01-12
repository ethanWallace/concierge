from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate 
from django.contrib.auth.forms import AuthenticationForm
from two_factor.forms import AuthenticationTokenForm, TOTPDeviceForm
from two_factor.utils import totp_digits, default_device
from emailvalidator.validator import is_email_valid
from .models import User, EventLog
from django_otp.forms import OTPTokenForm
from django.forms import Form
from django.conf import settings
import requests

class EmailField(forms.EmailField):
    def clean(self, value):
        super(EmailField, self).clean(value)
        if not is_email_valid(value):
            raise forms.ValidationError(
                _("Your email address is not allowed.")
            )
        try:
            User.objects.get(email=value, is_active=True)
            raise forms.ValidationError("This e-mail is already registered.")
        except User.DoesNotExist:
            return value


class RegisterForm(forms.Form):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'captcha_mismatch': 'captcha_mismatch',
    }

    name = forms.CharField(required=True, max_length=100)
    email = EmailField(required=True)
    password1 = forms.CharField(strip=False, widget=forms.PasswordInput)
    password2 = forms.CharField(strip=False, widget=forms.PasswordInput)
    accepted_terms = forms.BooleanField(required=True)
    receives_newsletter = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields["g-recaptcha-response"] = forms.CharField()

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        password_validation.validate_password(self.cleaned_data.get('password2'))
        return password2

    def clean(self):
        super(RegisterForm, self).clean()
        if not verify_captcha_response(self.cleaned_data.get('g-recaptcha-response')):
            raise forms.ValidationError(
                self.error_messages['captcha_mismatch'],
                code='captcha_mismatch',
            )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'email', 'avatar')


class PleioAuthenticationForm(AuthenticationForm):
    error_messages = {
        'captcha_mismatch': 'captcha_mismatch',
        'invalid_login': 'invalid_login',
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        super(PleioAuthenticationForm, self).__init__(*args, **kwargs)

        if EventLog.reCAPTCHA_needed(request):
            self.fields['g-recaptcha-response'] = forms.CharField()

    def clean(self):
        if self.fields.get('g-recaptcha-response'):
            g_recaptcha_response = self.cleaned_data.get('g-recaptcha-response')

            if not self.verify_captcha_response(g_recaptcha_response):
                raise forms.ValidationError(
                    self.error_messages['captcha_mismatch'],
                    code='captcha_mismatch',
                )

        super(PleioAuthenticationForm, self).clean()

    def verify_captcha_response(self, response):
        try:
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': response
            }
        except AttributeError:
            return True

        if not response:
            return False
        
        try:
            result = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data).json()
            return result['success']

        except:
            return False

class PleioAuthenticationTokenForm(OTPTokenForm):
    otp_token = forms.IntegerField(label=_("Token"), widget=forms.TextInput)
    otp_device = forms.ChoiceField(choices=[], required=False)

    def clean(self):
        self.clean_otp(self.user)
        return self.cleaned_data

    def clean_otp(self, user):
        if user is None:
            return

        device = default_device(user)
        token = self.cleaned_data.get('otp_token')

        user.otp_device = None

        try:
            if self.cleaned_data.get('otp_challenge'):
                self._handle_challenge(device)
            elif token:
                user.otp_device = self._verify_token(user, token, device)
            else:
                raise forms.ValidationError(_('Please enter your OTP token.'), code='required')
        finally:
            if user.otp_device is None:
                self._update_form(user)


class PleioBackupTokenForm(OTPTokenForm):
    otp_token = forms.CharField(label=_("Token"))
    otp_device = forms.ChoiceField(choices=[], required=False)


class PleioTOTPDeviceForm(TOTPDeviceForm):
    token = forms.IntegerField(label=_("Token"), widget=forms.TextInput)


class ChangePasswordForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    error_messages = {
        'invalid_password': _("The password is invalid."),
        'password_mismatch': _("The two password fields didn't match."),
    }

    old_password = forms.CharField(strip=False, widget=forms.PasswordInput)
    new_password1 = forms.CharField(strip=False, widget=forms.PasswordInput)
    new_password2 = forms.CharField(strip=False, widget=forms.PasswordInput)

    def clean_old_password(self):
        old_password = self.cleaned_data.get("old_password")
        user = authenticate(username=self.user.email, password=old_password)
        
        if user is None:
            raise forms.ValidationError(
                self.error_messages['invalid_password'],
                code='invalid_password',
            )

        return old_password

    def clean_new_password2(self):
        new_password1 = self.cleaned_data.get("new_password1")
        new_password2 = self.cleaned_data.get("new_password2")

        if new_password1 and new_password2 and new_password1 != new_password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )

        password_validation.validate_password(self.cleaned_data.get('new_password2'))
        return new_password2
