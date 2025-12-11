from django.db import models # module containing all Django models' base class
from django.contrib.auth.models import User # to associate a user account in the application

# database structure
class TODOO(models.Model):
    srno=models.AutoField(auto_created=True,primary_key=True) #a column that automatically increments with each new record
    title= models.CharField(max_length=25) #Stores a small-to-medium length string of characters
    date = models.DateTimeField(auto_now_add=True)#used to record when the record was created
    status = models.BooleanField(default=False,blank=True,)#for tracking the completion status of a task
    user = models.ForeignKey( User, on_delete=models.CASCADE)#Many-to-One relationship between the TODOO table and the User table
