from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from porsche.core.restframework import (
    PorscheModelSerializer,
    PorschePasswordField,
    PorschePhoneField,
    PorscheUniqueTogetherValidator,
)
from porsche.models import Role, User


class RoleListSerializer(PorscheModelSerializer):
    class Meta:
        model = Role
        fields = ("uid", "name")


class RoleRetrieveSerializer(PorscheModelSerializer):
    class Meta:
        model = Role
        fields = ("uid", "name")


user_validators = [
    PorscheUniqueTogetherValidator(
        queryset=User.objects.all(),
        fields=["username"],
    ),
    PorscheUniqueTogetherValidator(
        queryset=User.objects.all(),
        fields=["email"],
    ),
    PorscheUniqueTogetherValidator(
        queryset=User.objects.all(),
        fields=["phone"],
    ),
]


class UserListSerializer(PorscheModelSerializer):
    role = RoleRetrieveSerializer()

    class Meta:
        model = User
        fields = ("uid", "username", "phone", "email", "avatar", "role")


class UserRetrieveSerializer(PorscheModelSerializer):
    class Meta:
        model = User
        fields = ("uid", "username", "phone", "email", "avatar", "role_id")


class UserCreateSerializer(PorscheModelSerializer):
    password = PorschePasswordField(required=True, write_only=True)
    phone = PorschePhoneField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "password", "phone", "email", "role")
        validators = user_validators

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)


class UserUpdateSerializer(PorscheModelSerializer):
    username = serializers.CharField(max_length=150)
    phone = PorschePhoneField()
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("username", "phone", "email", "role")
        validators = user_validators
