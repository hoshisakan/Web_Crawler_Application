from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, \
                                                TokenVerifySerializer
from six import text_type
from module.date import DateTimeTools as DT
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken, UntypedToken
from django.contrib.auth.models import User
from .views_func import UserViewsFunc
from rest_framework_simplejwt.backends import TokenBackend
from crawler.config import SERVER_CONFIG

SUPERUSER_LIFETIME = SERVER_CONFIG.JWT_TOKEN_SETTING['SUPERUSER_LIFETIME']
RESEST_NORMALUSER_LIFETIME = SERVER_CONFIG.JWT_TOKEN_SETTING['RESEST_NORMALUSER_LIFETIME']


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser', 'date_joined', 'last_login']

class TokenVerifyObtainSerializer(TokenVerifySerializer):
    token = serializers.CharField()

    def validate(self, attrs):
        UntypedToken(attrs['token'])

        return {}

class RefreshTokenObtainSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()
    access = serializers.ReadOnlyField()
    viewset_func = UserViewsFunc(User)

    def validate(self, attrs):
        decrypt_token = TokenBackend(algorithm='HS256').decode(attrs['refresh'],verify=False)
        username, user_id = decrypt_token['user'], decrypt_token['user_id']
        refresh = RefreshToken(attrs['refresh'])
        data = {'access': str(refresh.access_token)}
        data['exp'] = DT.format_datetime_str((DT.get_current_datetime() + refresh.access_token.lifetime))
        if self.viewset_func.checkUserIsSuperuser(user_id=user_id, username=username):
            new_token = refresh.access_token
            new_token.set_exp(lifetime=SUPERUSER_LIFETIME)
            data = {'access': str(new_token)}
            data['exp'] = DT.format_datetime_str((DT.get_current_datetime() + SUPERUSER_LIFETIME))
        else:
            data = {'access': str(refresh.access_token)}
            data['exp'] = DT.format_datetime_str((DT.get_current_datetime() + refresh.access_token.lifetime))
        if api_settings.ROTATE_REFRESH_TOKENS:
            if api_settings.BLACKLIST_AFTER_ROTATION:
                try:
                    # Attempt to blacklist the given refresh token
                    refresh.blacklist()
                except AttributeError:
                    # If blacklist app not installed, `blacklist` method will
                    # not be present
                    pass
            refresh.set_jti()
            refresh.set_exp()
            data['refresh'] = str(refresh)
        return data

class LoginTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user'] = user.username
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = text_type(refresh)
        if self.user.is_superuser:
            new_token = refresh.access_token
            new_token.set_exp(lifetime=SUPERUSER_LIFETIME)
            data['access'] = text_type(new_token)
            data['exp'] = DT.format_datetime_str(DT.get_current_datetime() + SUPERUSER_LIFETIME)
        else:
            data['access'] = text_type(refresh.access_token)
            # data['exp'] = DT.format_datetime_str(DT.get_current_datetime() + refresh.access_token.lifetime)
            data['exp'] = str(DT.get_current_datetime() + RESEST_NORMALUSER_LIFETIME)
            print(f'User token expire time is: {refresh.access_token.lifetime}')
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data

class UserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']

class UserPasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['password']

class IdUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']

class TokenObtainPairWithoutPasswordSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    def validate(self, attrs):
        attrs.update({'password': ''})
        return super(TokenObtainPairSerializer, self).validate(attrs)

class ResetPasswordTokenSerializer(TokenObtainPairSerializer):
    viewset_func = UserViewsFunc(User)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].required = False

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        queryset = cls.viewset_func.filterUserByUsernameEmail(username=user.username, email=user.email)
        serializer = UserPasswordSerializer(queryset, many=True)
        token['hash_password'] = serializer.data[0]['password']
        return token

    def validate(self, attrs):
        attrs.update({'password': ''})
        data = super(ResetPasswordTokenSerializer, self).validate(attrs)
        refresh = self.get_token(self.user)
        if self.user.is_superuser:
            new_token = refresh.access_token
            new_token.set_exp(lifetime=SUPERUSER_LIFETIME)
            data['access'] = text_type(new_token)
            data['exp'] = str(DT.get_current_datetime() + SUPERUSER_LIFETIME)
        else:
            new_token = refresh.access_token
            new_token.set_exp(lifetime=RESEST_NORMALUSER_LIFETIME)
            data['access'] = text_type(new_token)
            data['exp'] = str(DT.get_current_datetime() + RESEST_NORMALUSER_LIFETIME)
        del data['refresh']
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        return data