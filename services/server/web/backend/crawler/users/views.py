from loguru import logger
from rest_framework.exceptions import ValidationError
from .serializers import LoginTokenObtainSerializer, RefreshTokenObtainSerializer, \
                        IdUsernameSerializer, UsernameSerializer, UserIdSerializer, \
                        TokenVerifyObtainSerializer
from rest_framework import authentication, viewsets, status
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.decorators import action
from .exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import UserInfoSerializer
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .views_func import UserViewsFunc
from django.shortcuts import get_object_or_404
from .tasks import chain_tasks_send_email
from django.contrib.auth.hashers import make_password
from itsdangerous.exc import BadSignature, SignatureExpired
from .validate_tokens import GenerateSerializerToken, GenerateProtectAuthToken
from django.core.cache import cache
from module.date import DateTimeTools as DT
from django.conf import settings
from module.handle_exception import HandleException
from module.log_generate import Loggings

logger = Loggings()

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer
    parsers_classes = (JSONParser,)
    viewset_func = UserViewsFunc(User)

    def get_permissions(self):
        if self.action in ('list', 'destroy'):
            permission_classes = [IsAdminUser]
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]

    def list(self, request):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.serializer_class(queryset, many=True)
            res_msg = {
                "info": serializer.data
            }
            return Response(res_msg, status=status.HTTP_200_OK)
        except Exception as e:
            res_msg = {
                "error": e.args[0],
                "message": "register user failed."
            }
            return Response(res_msg, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        try:
            data = request.data
            email = data.get('email', None)
            username = data.get('username', None)
            password = data.get('password', None)

            if username is None or email is None or password is None:
                raise Exception("username and email and password doesn't empty")

            duplicate_check = self.viewset_func.checkUserOrEmailIsDuplicate(
                username=username,
                email=email)

            if any(list(duplicate_check.values())):
                raise Exception(duplicate_check)

            # create user, but set activate equal False, until email validated
            add_user = User(username=username)
            add_user.email = email
            add_user.set_password(password)
            add_user.is_active = False
            add_user.save()
            # generate token for user validate email exists
            queryset = self.viewset_func.filterUserByUsernameEmail(username=username, email=email)
            self.serializer_class = UserIdSerializer
            serializer = self.serializer_class(queryset, many=True)
            serializer_items = GenerateSerializerToken(salt='activate account', expires_in=300)
            serializer_items.generate_serializer()
            token = serializer_items.encrypt_payload(serializer.data)
            link = f"{settings.SERVER_BASE_URL}/session/confirm-account?token={token}"
            # send register account activate email
            task_id = chain_tasks_send_email(
                subject='[Crawler Website] Activate Register Account',
                username=username,
                template='register_user.html',
                link=link,
                to=[email]
            )
            return Response({
                "message": "The activation email has been send to your mailbox, Please go to the mailbox to activate your account",
                "is_registered": True,
                "task_id": task_id}, status=status.HTTP_201_CREATED)
        except Exception as e:
            res_msg = {
                "error": e.args[0],
                "is_registered": False
            }
            return Response(res_msg, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            queryset = self.viewset_func.obtainUsernameById(pk)
            instance = get_object_or_404(queryset)
            self.perform_destroy(instance)
            return Response({'message': 'delete user successfully.', 'is_removed': True}, status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({
                'error': e.args[0],
                'is_removed': False
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='reissue-activate')
    def reissue_register_activate(self, request):
        try:
            data = request.data
            email = data.get('email', None)
            username = data.get('username', None)
            queryset = self.viewset_func.filterUserByUsernameEmail(username=username, email=email)
            self.serializer_class = UserIdSerializer
            serializer = self.serializer_class(queryset, many=True)
            serializer_items = GenerateSerializerToken(salt='activate account', expires_in=300)
            serializer_items.generate_serializer()
            token = serializer_items.encrypt_payload(serializer.data)
            link = f"{settings.SERVER_BASE_URL}/session/confirm-account?token={token}"
            task_id = chain_tasks_send_email(
                subject='[Crawler Website] Activate Register Account',
                username=username,
                template='register_user.html',
                link=link,
                to=[email]
            )
            return Response({
                "message": "reissue account validate email has been send to your mailbox",
                "is_reissue": True,
                "task_id": task_id}, status=status.HTTP_200_OK)
        except Exception as e:
            res_msg = {
                "error": e.args[0],
                "is_reissue": False
            }
            return Response(res_msg, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='reset-password')
    def reset_password(self, request):
        try:
            data = request.data
            token = data.get('token', None)
            new_password = data.get('new_password', None)
            if token is None:
                raise Exception("Validate failed,Token can't be empty")
            serializer_items = GenerateSerializerToken(salt='reset password', expires_in=300)
            serializer_items.generate_serializer()
            user_id = serializer_items.descrypt_payload(token)['id']
            hash_password = serializer_items.descrypt_payload(token)['hash_password']
            if self.viewset_func.checkUserIdExists(user_id=user_id) is False:
                raise Exception("The user doesn't exists")
            if self.viewset_func.checkHashPasswordExistsById(user_id, hash_password) is False:
                raise Exception('Oh, No.The Token has been invaild.')
            hash_new_password = make_password(password=new_password, salt=None)
            reset_result = self.viewset_func.changePasswordByUserId(user_id, hash_new_password)
            if reset_result != 1:
                raise Exception("Reset password failed")
            return Response({'message': 'Change Password Successful.', 'is_password_changed': True}, status=status.HTTP_200_OK)
        except BadSignature as bad_signature:
            return Response({'error': 'Invalid Reset Token' , 'is_password_changed':False, 'detail': bad_signature.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except SignatureExpired as signature_expired:
            return Response({'error': 'Token Expired', 'is_password_changed':False, 'detail': signature_expired.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error('message: {}'.format(e))
            return Response({'error': e.args[0], 'is_password_changed':False}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='sign-in')
    def login_validate(self, request):
        data = request.data
        try:
            username = data.get('username', None)
            if username is None:
                raise Exception("{'username': ['The field is required.']}")
            queryset = self.viewset_func.obtainUsername(data.get('username', None))
            serializer_ = UsernameSerializer(queryset, many=True)
            username = serializer_.data[0]['username']
            check_logged_in = cache.get(username, False)
            serializer = LoginTokenObtainSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            if check_logged_in is False:
                original_token = serializer.validated_data
                generate_protect_auth = GenerateProtectAuthToken('auth token')
                access_token, refresh_token = generate_protect_auth.encrypt_payload(original_token['access'], original_token['refresh'])
                generate_token = {
                    "refresh": refresh_token,
                    "access": access_token,
                    "exp": original_token['exp']
                }
                cache.set(username, generate_token, timeout=None)
            else:
                generate_token = check_logged_in
            return Response(generate_token, status=status.HTTP_200_OK)
        except TokenError as tr:
            raise InvalidToken(tr.args[0])
        except Exception as e:
            return Response({
                "error": e.args[0],
                "detail": "user login failed."
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False)
    def logout(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh', None)
            if refresh_token is not None:
                protect_auth = GenerateProtectAuthToken(salt='auth token')
                raw_refresh_token = protect_auth.descrypt_payload(refresh_token)
                valid_data = TokenBackend(algorithm='HS256').decode(raw_refresh_token, verify=False)
                username = valid_data['user']
            else:
                raise Exception("Refresh token can't be empty, will force logout account")
            revoke_token = RefreshToken(raw_refresh_token)
            revoke_token.blacklist()
            cache.delete(username)
            return Response({"message": "Success Logout", "allow_logout": True})
        except Exception as e:
            cache.delete(username)
            return Response({'error': e.args[0], "allow_logout": True}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='token-refresh')
    def token_refresh(self, request):
        try:
            self.serializer_class = RefreshTokenObtainSerializer
            data = request.data['refresh']
            protect_auth = GenerateProtectAuthToken(salt='auth token')
            raw_refresh_token = {
                'refresh': protect_auth.descrypt_payload(data)
            }
            serializer = self.get_serializer(data=raw_refresh_token)
            serializer.is_valid(raise_exception=True)
            original_access_token = serializer.validated_data
            encrypt_access_token = protect_auth.encrypt_payload_only_access_token(original_access_token['access'])
            generate_token = {
                "access": encrypt_access_token,
                "exp": original_access_token['exp']
            }
            return Response(generate_token, status=status.HTTP_200_OK)
        except TokenError as tr:
            logger.error({"error": tr.args[0]})
            raise InvalidToken(tr.args[0])
        except Exception as e:
            logger.error({"error": e.args[0]})
            return Response({"error": e.args[0]}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(methods=['POST'], detail=False, url_path='token-expire-check')
    def token_refresh(self, request):
        try:
            access_token = request.data.get('token', None)
            if access_token is None:
                raise Exception("Token can't be empty")

            protect_auth = GenerateProtectAuthToken(salt='auth token')
            # logger.info(f'protect_auth: {protect_auth}')
            raw_access_token = protect_auth.descrypt_payload(access_token)
            # logger.info(f'raw_access_token: {raw_access_token}')
            decrypt_token = TokenBackend(algorithm='HS256').decode(raw_access_token, verify=False)
            username = decrypt_token['user']
            expires_in_timestamp = decrypt_token['exp']
            logger.info(f'expires_in_timestamp: {expires_in_timestamp}')
            expires_in_datetime = DT.convert_timestamp_to_datetime(expires_in_timestamp)
            logger.info(f'expires_in_datetime: {expires_in_datetime}')
            now_datetime = DT.get_current_datetime()
            logger.info(f'now_datetime: {now_datetime}')
            token_time_left = int((expires_in_datetime - now_datetime).total_seconds())

            if cache.get(username, False) is False:
                raise Exception("Invalid token or expired or will expire")
            self.serializer_class = TokenVerifyObtainSerializer
            serializer = self.get_serializer(data={"token": raw_access_token})
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            validated_data['message'] = "Token is valid"
            validated_data['is_valid'] = True
            validated_data['token_time_left'] = token_time_left
            return Response(validated_data, status=status.HTTP_200_OK)
        except Exception as e:
            err_msg = {
                "error": HandleException.show_exp_detail_message(e),
                "is_invalid": False,
            }
            logger.error(err_msg)
            return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['POST'], detail=False, url_path='token-expire-check')
    # def token_expire_check(self, request):
    #     try:
    #         access_token = request.data.get('token', None)
    #         if access_token is None:
    #             raise Exception("Token can't be empty")
    #         protect_auth = GenerateProtectAuthToken(salt='auth token')
    #         raw_access_token = protect_auth.descrypt_payload(access_token)

    #         decrypt_token = TokenBackend(algorithm='HS256').decode(raw_access_token, verify=False)
    #         username = decrypt_token['user']
    #         expires_in_timestamp = decrypt_token['exp']
    #         expires_in_datetime = DT.convert_timestamp_to_datetime(expires_in_timestamp)
    #         now_datetime = DT.get_current_datetime()
    #         token_time_left = int((expires_in_datetime - now_datetime).total_seconds())

    #         if cache.get(username, False) is False:
    #             raise Exception("Invalid token or expired or will expire")
    #         self.serializer_class = TokenVerifyObtainSerializer
    #         serializer = self.get_serializer(data={"token": raw_access_token})
    #         serializer.is_valid(raise_exception=True)
    #         validated_data = serializer.validated_data
    #         validated_data['message'] = "Token is valid"
    #         validated_data['is_valid'] = True
    #         validated_data['token_time_left'] = token_time_left
    #         return Response(validated_data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         err_msg = {
    #             "error": e.args[0],
    #             "is_invalid": False,
    #             "token_time_left": token_time_left
    #         }
    #         logger.error(err_msg)
    #         return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['GET'], detail=False, url_path='profile')
    def obtain_user_profile(self, request, *args, **kwargs):
        try:
            token = request.headers.get('Authorization').split(' ')[1]
            protect_auth = GenerateProtectAuthToken(salt='auth token')
            raw_access_token = protect_auth.descrypt_payload(token)
            valid_data = TokenBackend(algorithm='HS256').decode(raw_access_token,verify=False)
            del valid_data['user_id']
            return Response({'info': valid_data}, status=status.HTTP_200_OK)
        except ValidationError as v:
            err_msg = {
                "error": f"validation error: {v}"
            }
        except Exception as e:
            err_msg = {
                "error": f"{e.args[0]}",
            }
            return Response(err_msg, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='validate-account')
    def validate_register_activate(self, request):
        try:
            user_id = None
            data = request.data
            token = data.get('token', None)
            if token is None:
                raise Exception("Validate failed,Token can't be empty")
            serializer_items = GenerateSerializerToken(salt='activate account', expires_in=300)
            serializer_items.generate_serializer()
            user_id = serializer_items.descrypt_payload(token)[0]['id']
            if self.viewset_func.checkUserIdExists(user_id=user_id) is False:
                raise Exception("The user doesn't exists")
            if self.viewset_func.checkAccountActivateStatus(user_id=user_id):
                raise Exception("The account has been activated")
            activate_result = self.viewset_func.changeAccountActivateStatus(user_id=user_id, activate_status=True)
            logger.info(f"{user_id} of {activate_result}")
            if activate_result != 1:
                logger.info(f"{user_id} of {activate_result} ,The account activate failed")
                raise Exception(f"{user_id} of {activate_result} ,The account activate failed")
            return Response({'message': 'Test Successful!', 'is_account_validated': True}, status=status.HTTP_200_OK)
        except BadSignature as bad_signature:
            logger.error(bad_signature.args[0])
            return Response({'error': 'Invalid Acticate Token' , 'is_account_validated':False, 'detail': bad_signature.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except SignatureExpired as signature_expired:
            logger.error(signature_expired.args[0])
            return Response({'error': 'Token Expired', 'is_account_validated':False, 'detail': signature_expired.args[0]}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(e.args[0])
            return Response({'error': e.args[0], 'is_account_validated':False}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=False, url_path='forget-password')
    def apply_reset_password(self, request, *args, **kwargs):
        try:
            data = request.data
            email = data.get('email', None)
            if email is None:
                raise Exception("email is required.")
            if not self.viewset_func.checkEmailIsExists(email=email):
                raise Exception('The username with email not match.')
            else:
                queryset = self.viewset_func.filterUserByEmail(email=email)
                self.serializer_class = IdUsernameSerializer
                serializer = self.get_serializer(queryset, many=True)
                username = serializer.data[0]['username']
                encrypt_payload = {
                    'id': serializer.data[0]['id'],
                    'hash_password': serializer.data[0]['password']
                }
                serializer_items = GenerateSerializerToken(salt='reset password', expires_in=300)
                serializer_items.generate_serializer()
                token = serializer_items.encrypt_payload(encrypt_payload)
                link = f"{settings.SERVER_BASE_URL}/session/reset-password?token={token}"
                task_id = chain_tasks_send_email(
                    subject='[Crawler Website] Reset Password Request',
                    username=username,
                    template='register_user.html',
                    link=link,
                    to=[email]
                )
            return Response({'message': 'Reset Password Apply Success.','apply_reset_success': True, 'task_id': task_id}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': e.args[0], 'apply_reset_success': False}, status=status.HTTP_400_BAD_REQUEST)