from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser,BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class CustomUserManager(BaseUserManager):
    def _create(self,username,email,password,**extra_fields):
        if not username:
            raise ValueError('Укажите username')
        email = self.normalize_email(email)
        user = self.model(email=email,username=username,**extra_fields)
        user.set_password(password)
        user.save() # команда save когда заносим инфо в базу данных
        return user 
    
    def create_user(self,username,email,password,**extra_fields): #ПОКА ПОЛЬЗОВАТЕЛЬ НЕ АКТВИРУЕТ АККАУНТ ОН НЕ МОЖЕТ ПРОИЗВОДИТЬ ДЕЙСТВИЯ 
        extra_fields.setdefault('is_active',False)
        extra_fields.setdefault('is_staff',False)
        return self._create(username,email,password,**extra_fields)
    
    def create_superuser(self,username,email,password,**extra_fields):# А ОН МОЖЕТ 
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        return self._create(username,email,password,**extra_fields)





class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=100,unique=True)#при чарфилде всегда нужна максимальная длина
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False) #невозможно выполнять никакие действия без активации
    is_staff = models.BooleanField(default=False)#является ли пользователь модератором 
    activation_code = models.CharField(max_length=10,blank=True) #чтобы активационный код не придумывался пользовтелем сам есть переменная blank пока она не будет заполненна

    REQUIRED_FIELDS = ['email'] #почта в обязательном порядке

    USERNAME_FIELD = 'username'

    objects = CustomUserManager()

    def has_module_perms(self,app_label):
        return self.is_staff # у какого юзера есть права администратора
    
    def has_perm(self,obj=None):
        return self.is_staff # доступность операций к каким либо методам
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
