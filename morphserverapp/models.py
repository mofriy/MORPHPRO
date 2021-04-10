from django.db import models
#import django_sha2.hashers as hasher

# Create your models here.

class User(models.Model):

    name = models.CharField(max_length=256)

    email = models.EmailField(unique=True)

    password = models.CharField(max_length=256)

    remember_me = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    user_created_at = models.DateTimeField()
    user_updated_at = models.DateTimeField()

    reset_password_token = models.CharField(max_length=256)


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