from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.core.signing import SignatureExpired
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from apps.users.models import User
from apps.users.password_validators import apply_password_validators


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        try:
            self.user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(_("Email does not exist."))
        return email


class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField()
    token = serializers.CharField()

    def validate_token(self, token):
        try:
            decoded_token = urlsafe_base64_decode(token)
            user_id, user_token = signing.loads(decoded_token.decode())
            self.user = user = User.objects.get(pk=user_id)
            if not (default_token_generator.check_token(user, user_token)):
                raise serializers.ValidationError(_("Invalid token."))
        except (
            signing.BadSignature,
            DjangoUnicodeDecodeError,
            SignatureExpired,
            UnicodeDecodeError,
        ):
            raise serializers.ValidationError(_("Invalid token."))
        return token

    def validate_new_password(self, new_password):
        apply_password_validators(new_password)
        return new_password

    def save(self):
        self.user.set_password(self.data["new_password"])
        self.user.save()