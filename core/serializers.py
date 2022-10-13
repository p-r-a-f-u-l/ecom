from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', "id", "email"]
        # fields = tuple(User.REQUIRED_FIELDS) + (
        # settings.USER_ID_FIELD,
        # settings.LOGIN_FIELD,
        # )
        # read_only_fields = (settings.LOGIN_FIELD,)
#
    # def update(self, instance, validated_data):
        # email_field = get_user_email_field_name(User)
        # if settings.SEND_ACTIVATION_EMAIL and email_field in validated_data:
        # instance_email = get_user_email(instance)
        # if instance_email != validated_data[email_field]:
        # instance.is_active = False
        # validated_data['first_name'] = User.objects.filter(email=instance_email).first()
        # instance.save(update_fields=["is_active"])
        # return super().update(instance, validated_data)


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password'])

        return user


class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetEmailPassword(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
