from django.contrib import admin
from .models import Admin, Complainants, Category, Subcategory, Complaints, ComplaintRemark
# Register your models here.

admin.site.register(Admin)
admin.site.register(Complainants)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Complaints)
admin.site.register(ComplaintRemark)

