from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


class EmailVerificationTokenGenerator(PasswordResetTokenGenerator):
    def make_token(self, user):
        """
        Creates a custom user verification token
        """
        token = super().make_token(user)
        data = f"{user.email}:{token}"
        return urlsafe_base64_encode(force_bytes(data))

    @staticmethod
    def decode_token(token):
        try:
            # Decode the token
            decoded_data = force_str(urlsafe_base64_decode(token))
            email, decoded_token = decoded_data.split(":", 1)
            return {
                "email": email,
                "token": decoded_token
            }
        except (DjangoUnicodeDecodeError, ValueError):
            raise InvalidTokenError("The token could not be decoded properly or is in an invalid format.")

    def _make_hash_value(self, user, timestamp):
        """
        Customised method to use date joined instead of last_login
        """
        # Truncate microseconds so that tokens are consistent even if the
        # database doesn't support microseconds.
        joined_timestamp = (
            ""
            if user.date_joined is None
            else user.date_joined.replace(microsecond=0, tzinfo=None)
        )
        email_field = user.get_email_field_name()
        email = getattr(user, email_field, "") or ""
        return f"{user.pk}{user.password}{joined_timestamp}{timestamp}{email}"


class InvalidTokenError(Exception):
    """
    Custom exception to raise when an invalid token is used.
    """
    pass
