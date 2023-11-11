import re
from django.utils.http import (
    urlsafe_base64_encode, 
    urlsafe_base64_decode,
    base36_to_int,
    int_to_base36
)
from django.utils.crypto import (
    constant_time_compare, 
    salted_hmac
)
from django.core.mail import (
    BadHeaderError, 
    EmailMultiAlternatives,
    send_mail,
)
from django.contrib.auth.tokens import (
    default_token_generator,
)
import hashlib
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from cryptography.fernet import Fernet
from django.conf import settings
from datetime import datetime
import random
import array


fernet = Fernet(settings.FERNET_KEY.encode())


class CustomTokenGenerator:
    """
    Strategy object used to generate and check tokens for source.
    """

    key_salt = "CustomTokenGenerator"
    algorithm = None
    _secret = None
    _secret_fallbacks = None

    def __init__(self):
        self.algorithm = self.algorithm or "sha256"

    def _get_secret(self):
        return self._secret or settings.SECRET_KEY

    def _set_secret(self, secret):
        self._secret = secret

    secret = property(_get_secret, _set_secret)

    def _get_fallbacks(self):
        if self._secret_fallbacks is None:
            return settings.SECRET_KEY_FALLBACKS
        return self._secret_fallbacks

    def _set_fallbacks(self, fallbacks):
        self._secret_fallbacks = fallbacks

    secret_fallbacks = property(_get_fallbacks, _set_fallbacks)

    def make_token(self, src):
        """
        Return a token that can be used once to do for given source.
        """
        return self._make_token_with_timestamp(
            src,
            self._num_seconds(self._now()),
            self.secret,
        )

    def check_token(self, src, token):
        """
        Check that a password reset token is correct for a given user.
        """
        if not (src and token):
            return False
        # Parse the token
        try:
            ts_b36, _ = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        for secret in [self.secret, *self.secret_fallbacks]:
            if constant_time_compare(
                self._make_token_with_timestamp(src, ts, secret),
                token,
            ):
                break
        else:
            return False

        # Check the timestamp is within limit.
        if (self._num_seconds(self._now()) - ts) > settings.PASSWORD_RESET_TIMEOUT:
            return False

        return True

    def _make_token_with_timestamp(self, src, timestamp, secret):
        # timestamp is number of seconds since 2001-1-1. Converted to base 36,
        # this gives us a 6 digit string until about 2069.
        ts_b36 = int_to_base36(timestamp)
        hash_string = salted_hmac(
            self.key_salt,
            self._make_hash_value(src, timestamp),
            secret=secret,
            algorithm=self.algorithm,
        ).hexdigest()[
            ::2
        ]  # Limit to shorten the URL.
        return "%s-%s" % (ts_b36, hash_string)

    def _make_hash_value(self, src, timestamp):
        hash_object = hashlib.sha256(src.encode())
        hashed_string = hash_object.hexdigest()
        
        return f"{hashed_string}{timestamp}"

    def _num_seconds(self, dt):
        return int((dt - datetime(2001, 1, 1)).total_seconds())

    def _now(self):
        # Used for mocking in tests
        return datetime.now()

custom_token_generator = CustomTokenGenerator()


def gen_strong_password():    
    # maximum length of password needed
    # this can be changed to suit your password length
    MAX_LEN = 12
    
    # declare arrays of the character that we need in out password
    # Represented as chars to enable easy string concatenation
    DIGITS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'] 
    LOCASE_CHARACTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                        'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                        'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                        'z']
    
    UPCASE_CHARACTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                        'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                        'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                        'Z']
    
    SYMBOLS = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
            '*', '(', ')', '<', '!', '&']
    
    # combines all the character arrays above to form one array
    COMBINED_LIST = DIGITS + UPCASE_CHARACTERS + LOCASE_CHARACTERS + SYMBOLS
    
    # randomly select at least one character from each character set above
    rand_digit = random.choice(DIGITS)
    rand_upper = random.choice(UPCASE_CHARACTERS)
    rand_lower = random.choice(LOCASE_CHARACTERS)
    rand_symbol = random.choice(SYMBOLS)
    
    # combine the character randomly selected above
    # at this stage, the password contains only 4 characters but
    # we want a 12-character password
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
    
    # now that we are sure we have at least one character from each
    # set of characters, we fill the rest of
    # the password length by selecting randomly from the combined
    # list of character above.
    for x in range(MAX_LEN - 4):
        temp_pass = temp_pass + random.choice(COMBINED_LIST)
    
        # convert temporary password into array and shuffle to
        # prevent it from having a consistent pattern
        # where the beginning of the password is predictable
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)
    
    # traverse the temporary password array and append the chars
    # to form the password
    password = ""
    for x in temp_pass_list:
            password = password + x
            
    return password


def is_strong_password(password):
    # Check if the password meets the strength requirements.
    # You can customize the requirements as needed (e.g., minimum length, special characters, etc.).
    # For this example, we'll require at least 6 characters, one uppercase letter, one lowercase letter,
    # one digit, and one special character.
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%=:?./|~>*()<!&])[A-Za-z\d@#$%=:?./|~>*()<!&]{6,}$'
    return re.match(pattern, password)


def send_verification_mail(request, user, email_template, subject):
    email_template_name = email_template
    info = {
        "email": user.email,
        'domain': request.headers['Host'],
        'site_name': 'Study-Stash',
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "user": user.__str__(),
        'token': default_token_generator.make_token(user),
        'protocol': 'http',
    }
    content = render_to_string(email_template_name, info)
    try:
        message = EmailMultiAlternatives(
            subject=subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email]
        )
        message.attach_alternative(content, "text/html")
        message.send(fail_silently=False)
        # send_mail(subject=subject, message=content, from_email=None, recipient_list=[user.email], fail_silently=False)
        return True
    except BadHeaderError as err:
        print("Error in send_activate_request: ", err)
        return False
    

def send_subscribe_confirmation_mail(request, user, email_template, subject, email=None):
    email_template_name = email_template
    if not email:
        return False
    info = {
        "email": email,
        'domain': request.headers['Host'],
        'site_name': 'Study-Stash',
        "uid": fernet.encrypt(email.encode()).decode('utf-8'),
        "user": user.__str__(),
        'token': custom_token_generator.make_token(email),
        'protocol': 'http',
    }
    content = render_to_string(email_template_name, info)
    try:
        message = EmailMultiAlternatives(
            subject=subject,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        message.attach_alternative(content, "text/html")
        message.send(fail_silently=False)
        # send_mail(subject=subject, message=content, from_email=None, recipient_list=[user.email], fail_silently=False)
        return True
    except BadHeaderError as err:
        print("Error in send_activate_request: ", err)
        return False
    

def send_general_mail(user, email_template, subject, from_email=None, recipient_list=None, info=None):
    email_template_name = email_template
    if not info:
        content = render_to_string(email_template_name)
    else:
        content = render_to_string(email_template_name, info)
    if not recipient_list:
        recipient_list=[user.email]
    try:
        message = EmailMultiAlternatives(
            subject=subject,
            from_email=from_email,
            to=recipient_list
        )
        message.attach_alternative(content, "text/html")
        message.send(fail_silently=False)
        return True
    except BadHeaderError as err:
        print("Error in send_activate_request: ", err)
        return False
