from django.db import models

# Create your models here.
class Students(models.Model):
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    gmail=models.CharField(max_length=100,unique=True)

# -------Django requires max_length for CharField.
# This creates a Django model name movies_review.
# It tells Django: “Create a table called employees in the database.”
class movies_review(models.Model): #models.Model is a built-in Django class that gives your class all the features of a database table.
    movie=models.CharField(max_length=100)   #CharField = used for short text.
    collections=models.IntegerField()   #(don’t use commas) IntegerField does NOT support max_length.
    r_date=models.CharField(max_length=100)
    ratings=models.FloatField(default=0)


# IntegerField does NOT support max_length.
# max_length works only for CharField.


# CharField
# EmailField
# TextField
# PasswordField
# .DateField()--Stores date only (YYYY-MM-DD format).
                # Used for joining date, DOB, etc.


class employees(models.Model):      
    name=models.CharField(max_length=200)
    emp_id=models.IntegerField()
    date=models.DateField()
    location=models.CharField(max_length=100)
    
class basic_users_login(models.Model):
    username = models.CharField(max_length=100)
    email = models.CharField(max_length=40,unique=True)
    password = models.CharField(max_length=100)
