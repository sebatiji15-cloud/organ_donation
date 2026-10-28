from django.db import models

class UserRegistrations(models.Model):
    username = models.CharField(max_length=50,unique=True)
    email = models.EmailField()
    blood=models.CharField(max_length=50,null=True)
    phno=models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    rights = models.CharField(max_length=35,default='User')

    def __str__(self):
        return self.username
class HOSPITALRegistrations(models.Model):
    hospitalname = models.CharField(max_length=50)
    username = models.CharField(max_length=50,null=True)
    address= models.CharField(max_length=50)
    emailid=models.EmailField()
    phonenumber = models.CharField(max_length=50)
    password= models.CharField(max_length=50)
    rights = models.CharField(max_length=35,default='New Hospital')
    def __str__(self):
        return self.hospitalname

class Donations(models.Model):
    user= models.CharField(max_length=50)
    name= models.CharField(max_length=50)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=50,null=True)
    bloodgroup = models.CharField(max_length=50)
    organtype= models.CharField(max_length=50)
    age= models.CharField(max_length=35)
    hospital= models.CharField(max_length=35)
    status= models.CharField(max_length=35,default="pending")
    def __str__(self):
        return self.user

class OrganRequest(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=50)
    age = models.CharField(max_length=35)
    bloodgroup = models.CharField(max_length=50)
    organtype = models.CharField(max_length=50)
    gender= models.CharField(max_length=35)
    phonenumber = models.CharField(max_length=35)
    status=models.CharField(max_length=50,default='Pending')
    def __str__(self):
        return self.username


