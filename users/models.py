from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

GENDER_CHOICES = (
    (0, 'Male'),
    (1, 'Female'),
    (2, 'Not to disclose')
)

class UserManager(BaseUserManager):
    def _create_user(self, email, username, password, gender=2, **extra_fields): #  맨 앞에 "_"표시 : 클래스 내에서만 사용한다는 명시적인 표현
        
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(email=email, username=username, gender=gender, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, username='', password=None, **extra_fields):
        extra_fields.setdefalut('is_staff', False)
        extra_fields.setdefalut('is_superuser', False)
        return self._create_user(email, username, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_supseruser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, 'blogs/like_section.html', password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(verbose_name='email', max_length=255, unique=True)
    
    username = models.CharField(max_length=30)
    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] # 필수로 받고 싶은 필드들 넣기, 기본 소스 코드엔 email 필드가 들어가지만 로그인을 이메일로 이미 하기 때문에.
    
    def __str__(self):
        return "<%d %s>" % (self.pk, self.email)

