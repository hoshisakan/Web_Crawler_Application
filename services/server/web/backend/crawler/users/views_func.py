from django.db.models import Q


class UserViewsFunc():
    def __init__(self, obj):
        self.__obj = obj

    def filterUserInfo(self, username):
        return self.__obj.objects.filter(username=username)

    def checkUserIsExists(self, username):
        return self.__obj.objects.filter(username=username).exists()
    
    def checkEmailIsExists(self, email):
        return self.__obj.objects.filter(email=email).exists()
    
    def checkRespectivelyUserEmailIsExists(self, username, email):
        return self.__obj.objects.filter(username=username).exists(), self.__obj.objects.filter(Q(email=email)).exists()
    
    def checkUserEmailIsExists(self, user, email):
        return self.__obj.objects.filter(Q(username=user) & Q(email=email)).exists()

    def obtainUsernameById(self, pk):
        return self.__obj.objects.filter(id=pk)

    def filterUserByEmail(self, email):
        return self.__obj.objects.filter(email=email)
    
    def obtainUsernameById(self, user_id):
        return self.__obj.objects.filter(id=user_id)

    def filterUserByUsernameEmail(self, username, email):
        return self.__obj.objects.filter(Q(username=username) & Q(email=email))
    
    def checkHashPasswordExistsById(self, user_id, hash_password):
        return self.__obj.objects.filter(Q(id=user_id) & Q(password=hash_password)).exists()
    
    def changePasswordByUserId(self, user_id, hash_new_password):
        return self.__obj.objects.filter(id=user_id).update(password=hash_new_password)

    def checkUserIdExists(self, user_id):
        return self.__obj.objects.filter(id=user_id).exists()

    def changeAccountActivateStatus(self, user_id, activate_status):
        return self.__obj.objects.filter(id=user_id).update(is_active=activate_status)

    def checkAccountActivateStatus(self, user_id):
        return self.__obj.objects.filter(Q(id=user_id) & Q(is_active=True))
    
    def obtainUsername(self, validate_item):
        if self.checkUserIsExists(username=validate_item) is False:
            return self.filterUserByEmail(email=validate_item)
        return self.filterUserInfo(username=validate_item)

    def checkUserIsSuperuser(self, user_id, username):
        return self.__obj.objects.filter((Q(username=username) & Q(id=user_id)) & Q(is_superuser=True)).exists()

    def checkUserOrEmailIsDuplicate(self, username, email):
        return {
            "is_username_registered": self.checkUserIsExists(username=username),
            "is_email_registered": self.checkEmailIsExists(email=email)
        }