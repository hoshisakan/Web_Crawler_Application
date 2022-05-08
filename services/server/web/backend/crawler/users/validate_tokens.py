from itsdangerous.url_safe import URLSafeSerializer
from itsdangerous import TimedJSONWebSignatureSerializer
from django.conf import settings

class GenerateSerializerToken():
    def __init__(self, salt='', expires_in=60):
        self.__salt = salt
        self.__expires_in = expires_in
        self.generate_serializer()

    def generate_serializer(self):
        self.__outside_serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, expires_in=self.__expires_in, salt=self.__salt)
        self.__inside_serializer = URLSafeSerializer(settings.SECRET_KEY, salt=self.__salt)

    def encrypt_payload(self, inside_payload_data):
        return self.__outside_serializer.dumps(self.__inside_serializer.dumps(inside_payload_data)).decode('utf-8')

    def descrypt_payload(self, encrypt_token):
        return self.__inside_serializer.loads(self.__outside_serializer.loads(encrypt_token))

class GenerateProtectAuthToken():
    def __init__(self, salt=''):
        self.__salt = salt
        self.generate_serializer()

    def generate_serializer(self):
        self.__protect_token_serializer = URLSafeSerializer(settings.SECRET_KEY, salt=self.__salt)

    def encrypt_payload(self, ori_access, ori_refresh):
        return self.__protect_token_serializer.dumps(ori_access), self.__protect_token_serializer.dumps(ori_refresh)
        
    def descrypt_payload(self, encrypt_token):
        return self.__protect_token_serializer.loads(encrypt_token)

    def encrypt_payload_only_access_token(self, ori_access):
        return self.__protect_token_serializer.dumps(ori_access)