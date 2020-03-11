from django.db import models
# from django.core.validators import MaxLengthValidator
# from django.core.validators import MinValueValidator
# Create your models here.

class RecordData(models.Model):

	equipmentID 	= models.CharField(max_length=20, null=False, blank=False)
	equipmentDesc 	= models.TextField(blank= True, null=True)
	building 		= models.CharField(max_length=350, blank= True, null=True)
	elevation 		= models.DecimalField(max_digits=6,decimal_places=3,blank= True, null=True)
	roomID 			= models.CharField(max_length=20, blank= True, null=True)
	notes 			= models.CharField(max_length=200, blank= True, null=True)


	# 'equipmentID'
	# 'equipmentDesc'
	# 'building'
	# 'elevation'
	# 'roomID'
	# 'notes'
