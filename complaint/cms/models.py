from django.db import models

# Create your models here.

class Admin(models.Model):
	admin_id = models.CharField(max_length=50, primary_key=True)
	admin_username = models.CharField(max_length=200)

class Complainants(models.Model):
	complainant_id = models.CharField(max_length = 50, primary_key = True)
	complainant_name = models.CharField(max_length=200)
	complainant_email = models.EmailField(max_length=300)
	complainant_contact = models.CharField(max_length=20)
	complainantReg_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '(%s)'%(self.complainant_id)

class Category(models.Model):
	category_id = models.AutoField(primary_key = True)
	category_name = models.CharField(max_length=200)
	category_description = models.CharField(max_length=1000)

class Subcategory(models.Model):
	subcategory_id = models.AutoField(primary_key = True)
	category_id = models.ForeignKey(Category, on_delete = models.CASCADE)
	subcategory_name = models.CharField(max_length=100)

	def __str__(self):
		return '(%s)'%(self.subcategory_name)


class Complaints(models.Model):
	complaint_id = models.AutoField(max_length=50, primary_key=True)
	complainant_id = models.ForeignKey(Complainants, on_delete = models.CASCADE)
	category_id = models.ForeignKey(Category, on_delete = models.CASCADE)
	subcategory_id = models.ForeignKey(Subcategory, on_delete = models.CASCADE)
	complaint_type = models.CharField(max_length=100)
	complaint_title = models.CharField(max_length = 100)
	complaint_details = models.CharField(max_length=1000)
	complaint_file = models.FileField(upload_to = 'files/', null = True, blank = True)
	status = models.CharField(max_length=100, null = True, blank = True)
	reg_date = models.DateTimeField(auto_now=True)

	
class ComplaintRemark(models.Model):
	complaint_id = models.ForeignKey(Complaints, on_delete = models.CASCADE)
	remark = models.CharField(max_length=700)
	remark_date = models.DateTimeField(auto_now=True)

