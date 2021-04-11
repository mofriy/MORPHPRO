from django.db import models
from django.utils import timezone
# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=256)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=256)

    user_created_at = models.DateTimeField()
    user_updated_at = models.DateTimeField()


    @classmethod
    def create_user(cls,data_dict):
        user = cls()
        user.name=data_dict['name']
        user.email=data_dict['email']
        user.password=data_dict['password']
        user.user_created_at=timezone.now()
        user.user_updated_at=timezone.now()
        return user

class MorphRequest(models.Model):

    author = models.ForeignKey('User',on_delete=models.CASCADE)

    protein_a_name = models.CharField(max_length=512)
    protein_b_name = models.CharField(max_length=512)

    protein_a = models.TextField()
    protein_b = models.TextField()

    morping_count = models.IntegerField()

    morph_request_created_at = models.DateTimeField()



    #TODO:
    #def are_equal_length(self):


#TODO:
class Pdb(models.Model):

    # def __init__(self,text):
    #     self.pdb_hash = hasher
    #     #TODO:
    #     #idk what's it for

    pdb_hash = models.CharField(max_length=256)

    pdb = models.TextField()