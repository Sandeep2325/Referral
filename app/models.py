from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin,BaseUserManager
from django.utils.translation import gettext_lazy as _
import random
import string
from django.db.models.signals import post_save
from django.dispatch import receiver
class UserManager(BaseUserManager):
    def create_superuser(self, email,password=None,**extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        user = self.model(
            email=self.normalize_email(email)
        )
class User(AbstractUser,PermissionsMixin):
    username = models.CharField(
        max_length=50, blank=False, null=True,verbose_name="user name")
    email = models.EmailField(_('email address'), unique=True)
    phone_no = models.CharField(max_length=13, null=True, unique=True,verbose_name="Mobile number")
    photo=models.ImageField(upload_to='profile',verbose_name="Profile photo", null=True, blank=True)
    is_verified=models.BooleanField(default=False)
    referid=models.CharField(max_length=30,null=True,blank=True,verbose_name="Refer ID")
    referredid=models.CharField(max_length=30,null=True,blank=True,verbose_name="Referred ID")
    online_status=models.BooleanField(default=False)
    referral_code=models.CharField(max_length=10, null=True, blank=True)
    USERNAME_FIELD="email"
    REQUIRED_FIELDS = ["username"]
    # objects = UserManager()
    def __str__(self):
        return "{}".format(str(self.email))

@receiver(post_save, sender=User)
def create_referral_code(sender, instance, created, **kwargs):
    if created:
        code = ReferralCode.generate_unique_code()
        ReferralCode.objects.create(code=code, user=instance)
class ReferralCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_code_owner')
    referred_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_users')

    def __str__(self):
        return self.code

    @staticmethod
    def generate_unique_code():
        length = 10
        code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        while ReferralCode.objects.filter(code=code).exists():
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        return code