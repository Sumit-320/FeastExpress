from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.

class Manager(BaseUserManager): # to manage the custom user
    def create_user(self,username,f_name,l_name,email,password=None):
        if not username:
            raise ValueError("User shall have a valid username!!")
        if not email:
            raise ValueError("User shall have a valid email-ID!!")
        
        user = self.model(
            username=username,
            f_name=f_name,
            l_name=l_name,
            email= self.normalize_email(email), # to handle case sensitivity in user input of email ID
        )
        user.set_password(password)
        user.save(using = self._db) #default db in settings.py (postgres one--> feastDB)
        return user

    def create_superuser(self,username,f_name,l_name,email,contact,password=None):
        user = self.create_user(
            username=username,
            f_name=f_name,
            l_name=l_name,
            password = password,
            email = self.normalize_email(email),
        )
        # after creating normal user, we assign them addtitional properties(necessary for superuser)

        user.is_admin = True
        user.is_superadmin =  True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user

# abstract base user-> gives full control over its user
class User(AbstractBaseUser): # custom user --> not the django default
    # two types of user -> Seller and Customer
    Seller = 1
    Buyer = 2
    
    Choice = (
        (Seller,'Vendor'),
        (Buyer,'Customer'),
    )
    username= models.CharField(max_length=25,unique=True)
    f_name= models.CharField(max_length=50)
    l_name= models.CharField(max_length=50)
    email= models.EmailField(max_length=50,unique=True)
    contact= models.CharField(max_length=12,blank=True)
    type= models.IntegerField(choices=Choice,blank=True,null=True) # 1 for vendor and 2 for customer
    date_of_register = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    date_of_create = models.DateTimeField(auto_now_add=True)
    date_of_update = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'  #  primary identifier for the user
    REQUIRED_FIELDS = ['username','f_name','l_name'] # necessary fields for user to register
    objects=Manager() 
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perms(self,app_label):
        return True
    def get_type(self):
        if self.type==1:
            user_type='Vendor'
        elif self.type==2:
            user_type='Customer'
        return user_type    

    

# upon creation of user, profile will not be created automatically!!

class Profile2(models.Model):  # for customer
    user = models.OneToOneField(User, on_delete=models.CASCADE,blank=True,null=True)
    profile_pic= models.ImageField(upload_to='users/profile_pics',blank=True,null=True) 
    bg_pic= models.ImageField(upload_to='users/bg_pics',blank=True,null=True) 
    address = models.CharField(max_length=150,blank=True,null =True)
    country = models.CharField(max_length=20,blank=True,null =True)
    state = models.CharField(max_length=20,blank=True,null =True)
    city = models.CharField(max_length=20,blank=True,null =True)
    pin = models.CharField(max_length=6,blank=True,null =True)
    latitude = models.CharField(max_length=20,blank=True,null =True)
    longitude = models.CharField(max_length=20,blank=True,null =True)
    create_time = models.DateTimeField(auto_now_add=True)
    modified_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email
   