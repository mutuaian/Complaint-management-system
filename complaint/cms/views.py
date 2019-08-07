from django.shortcuts import render, redirect, reverse
from django.views import View
from . import forms
from django.http import HttpResponse, JsonResponse
from .models import Admin, Complainants, Category, Subcategory, Complaints, ComplaintRemark
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, update_session_auth_hash, authenticate
import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.conf import settings
from django.core.paginator import Paginator
import json
from django.core import serializers
from .utils import render_to_pdf


class Login(View):
    form_class = forms.LoginForm
    template = "cms/login.html"

    def get(self, request):
    	if request.user.is_authenticated:
        	username = request.user
        	admin = Admin.objects.filter(admin_id=username).exists()
        	complainant = Complainants.objects.filter(complainant_id=username).exists()
        	department = Category.objects.filter(category_name = username).exists()
        	print(department)
        	if admin:
        		return redirect('cms:notprocessedcomplaints')
        	elif complainant:
        		return redirect('cms:dashboard')
        	elif department:
        		return redirect('cms:depnotprocessed')
        	else:
        		pass
    	else:
        	form = self.form_class(None)
        	return render(request, self.template, {'form': form})

    def post(self, request):
    	user_name = request.POST['username']
    	password = request.POST['password']
    	user = authenticate(request, username = user_name, password = password)
    	if user is not None:
    		login(request, user)
    		admin = Admin.objects.filter(admin_id=user_name).exists()
    		complainant = Complainants.objects.filter(complainant_id=user_name).exists()
    		department = Category.objects.filter(category_name = user_name).exists()
    		if admin:
    			return redirect('cms:notprocessedcomplaints')
    		elif complainant:
    			return redirect('cms:dashboard')
    		elif department:
    			return redirect('cms:depnotprocessed')
    		else:
    			pass
    	else:
    		form = self.form_class(None)
    		message = 'Incorrect username/password'
    		context = {
    			'form' : form,
    			'message' : message
			}
    		return render(request, self.template, context)

class Logout(View):
	def get(self, request):
		logout(request)
		return redirect('cms:login')

class Register(View):
	form_class = forms.RegisterForm
	template = 'cms/register.html'

	def get(self, request):
		form = self.form_class(None)
		context = {
			'form' : form,
		}
		return render(request, self.template, context)
	def post(self, request):
		form = self.form_class(request.POST)
		# if form.is_valid():
		username = request.POST['username']
		admin = Admin.objects.filter(admin_id = username).exists()
		department = Category.objects.filter(category_name = username).exists()
		user = Complainants.objects.filter(complainant_id = username).exists()
		if admin or department or user:
			email = request.POST['email']
			password = request.POST['password']
			print(email)
			exist = User.objects.filter(username = username).exists()
			if exist:
				context = {
					'form' : form,
					'message' : "You already have an existing account",
				}
				return render(request, self.template, context)
			else:
				user = User.objects.create_user(username, email, password)
				user.save()
				return redirect('cms:login')
		else:
			context = {
				'message' : "You cannot create an account, Please contact the admin for assistance",
				'form' : form,
			}
			return render(request, self.template, context)

class Index(View):
    template = "cms/index.html"
    
    def get(self, request):
    	return render(request, self.template)

class numbers(UserPassesTestMixin, View):
	template = 'cms/admin/base.html'

	def test_func(self):
		user = request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request):
		i_status = 'in process'
		c_status = 'closed'
		numberofinprocess_complaints = ComplaintDetails.objects.filter(status = i_status).count()
		numberofnotprocessed_complaints = ComplaintDetails.objects.filter(status__isnull = True).count()
		numberofclosed_complaints = ComplaintDetails.objects.filter(status = c_status).count()
		context = {
			'numberofinprocess_complaints' : numberofinprocess_complaints,
			'numberofnotprocessed_complaints' : numberofnotprocessed_complaints,
			'numberofclosed_complaints' : numberofclosed_complaints
			}
		print(context)
		return render(request, self.template, context)

class InProcessComplaints(UserPassesTestMixin, View):
	login_url = settings.LOGIN_URL
	template = 'cms/admin/inprocess-complaints.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request):
		status = 'in process'
		inprocess_complaints = Complaints.objects.filter(status = status)
		context = {
			'inprocess_complaints': inprocess_complaints
			}
		return render(request, self.template, context)


class NotProcessedComplaints(UserPassesTestMixin, View):
	template = 'cms/admin/notprocessed-complaints.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request):
		notprocessed_complaints = Complaints.objects.filter(status__isnull = True)
		context = {
			'notprocessed_complaints': notprocessed_complaints
			}
		return render(request, self.template, context)


class ClosedComplaints(UserPassesTestMixin, View):
	template = 'cms/admin/closed-complaints.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request):
		status = 'closed'
		closed_complaints = Complaints.objects.filter(status = status)
		context = {
			'closed_complaints': closed_complaints
			}
		return render(request, self.template, context)


class ManageUsers(UserPassesTestMixin, View):
	template = 'cms/admin/manage-users.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request):
		complainants = Complainants.objects.all()
		context = {
			'complainants': complainants
			}
		return render(request, self.template, context)


class ManageCategories(UserPassesTestMixin, View):
	template = 'cms/admin/category.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request):
		categories = Category.objects.all()
		context = {
			'categories': categories	
			}
		return render(request, self.template, context)


class NewCategory(UserPassesTestMixin, View):
	template = 'cms/admin/category.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def post(self, request):
		new_cat = request.POST.get('category')
		cat_description = request.POST.get('description')
		Category.objects.create(category_name = new_cat, category_description = cat_description)
		categories = Category.objects.all()
		context = {
			'categories': categories	
			}
		return render(request, self.template, context)


class ManageSubCategories(UserPassesTestMixin, View):
	template = 'cms/admin/subcategory.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request):
		subcategories = Subcategory.objects.all()
		categories = Category.objects.all()
		context = {
			'subcategories': subcategories,
			'categories': categories	
			}
		return render(request, self.template, context)

class NewSubcategory(UserPassesTestMixin, View):
	template = 'cms/admin/subcategory.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def post(self, request):
		print(request.GET)
		print(request.POST)
		cat_id = request.POST.get('category')
		subcat_name = request.POST.get('subcategory')
		Subcategory.objects.create(category_id_id = cat_id,subcategory_name = subcat_name)
		subcategories = Subcategory.objects.all()
		categories = Category.objects.all()
		context = {
			'subcategories': subcategories,
			'categories': categories	
			}
		return render(request, self.template, context)

class ChangePassword(UserPassesTestMixin, View):
	template = 'cms/admin/change-password.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request):
		return render(request, self.template)

class AdminComplaintDetails(UserPassesTestMixin, View):
	template = 'cms/admin/complaint-details.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request, complaint_id):
		cmpl_details = Complaints.objects.filter(complaint_id = complaint_id)
		cmpl_remark =  ComplaintRemark.objects.filter(complaint_id = complaint_id)
		if cmpl_remark:
			for rmrk in cmpl_remark:
				remark = rmrk.remark
				remarkdate = rmrk.remark_date
		else:
			remark = "No remark"
			remarkdate = "No remark"

		context = {
			'cmpl_details' : cmpl_details,
			'complaint_id' : complaint_id,
			'remark' : remark,
			'remarkdate' : remarkdate,
		}
		return render(request, self.template, context)

class EditCategory(UserPassesTestMixin, View):
	template = 'cms/admin/edit-category.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request, category_id):
		category = Category.objects.filter(category_id = category_id)
		context = {
			'category' : category
		}
		return render(request, self.template, context)

	def post(self, request, category_id):
		cat_name = request.POST.get('category')
		cat_description = request.POST.get('description')
		category = Category.objects.filter(category_id = category_id).update(category_name = cat_name, category_description = cat_description)
		message = "Category successfully Edited"
		context = {
			'message' : message
		}
		return render(request, self.template, context)

class EditSubcategory(UserPassesTestMixin, View):
	template = 'cms/admin/edit-subcategory.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request, subcategory_id):
		subcategory = Subcategory.objects.filter(subcategory_id = subcategory_id)
		category = Category.objects.all()
		context = {
			'category' : category,
			'subcategory' : subcategory,
		}
		return render(request, self.template, context)

	def post(self, request, subcategory_id):
		cat_id = request.POST.get('category')
		subcat_name = request.POST.get('subcategory')
		subcategory = Subcategory.objects.filter(subcategory_id = subcategory_id).update(subcategory_name = subcat_name, category_id = cat_id)
		if subcategory:
			message = "Category successfully Edited"
		else:
			message = "Not changed"
	
		context = {
			'message' : message
		}
		return render(request, self.template, context)

class UpdateState(UserPassesTestMixin, View):
	template = 'cms/admin/update-complaint.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request, complaint_id):
		context = {
			'complaint_id' : complaint_id,
		}
		return render(request, self.template, context)


	def post(self, request, complaint_id):
		status = request.POST.get('status')
		remark = request.POST.get('remark')
		print(complaint_id, status, remark)
		comp_status = Complaints.objects.filter(complaint_id = complaint_id).update(status = status)
		remark_exists = ComplaintRemark.objects.filter(complaint_id_id = complaint_id)
		if remark_exists:
			comp_remark = remark_exists.update(remark = remark)
		else:
			comp_remark = ComplaintRemark.objects.create(complaint_id_id = complaint_id, remark = remark)

		if comp_remark:
			message = "status updated successfully"
		else:
			message = "Request not successful, Please try again"
		context = {
			'complaint_id' : complaint_id,
			'message' : message
		}
		return render(request, self.template,context)


class UserDetails(UserPassesTestMixin, View):
	template = 'cms/admin/userdetails.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request, complainant_id):
		print(complainant_id)
		userInfo = Complainants.objects.filter(complainant_id = complainant_id)
		context = {
			'userInfo' : userInfo,
			'complainant_id' : complainant_id
			}
		return render(request, self.template, context)

class AdminReport(UserPassesTestMixin, View):
	template = 'cms/admin/report-pdf.html'

	def test_func(self):
		user = self.request.user
		return Admin.objects.filter(admin_id = user).exists()

	def get(self, request):
		cat_list = {}
		all_complaints = Complaints.objects.all()
		count_all = Complaints.objects.all().count()
		all_categories = Category.objects.all()
		number_of_categories = Category.objects.all().count()

		for category in all_categories:
			category_id = category.category_id
			category_name = category.category_name
			number = Complaints.objects.filter(category_id = category_id).count()
			notprocessed = Complaints.objects.filter(status__isnull = True, category_id = category_id).count()
			inprocess = Complaints.objects.filter(status = 'in process', category_id = category_id).count()
			closed = Complaints.objects.filter(status = 'closed', category_id = category_id).count()
			percentage = round((number/count_all)*100, 1)
			cat_list[str(category)] = {
				'category_name' : category_name,
				'number' : number,
				'percentage' : percentage,
				'inprocess' : inprocess,
				'notprocessed' : notprocessed,
				'closed' : closed,
			}
		context = {
			'cat_list' : cat_list,
		}
		pdf = render_to_pdf(self.template, context)
		return HttpResponse(pdf, content_type='application/pdf')

class DeleteSubcategory(View):
	template = ''

	def get(self,request):
		return render(request, self.template)


# ==================================user views==============================
class Dashboard(UserPassesTestMixin, View):
	template = 'cms/users/dashboard.html'

	def test_func(self):
		user = self.request.user
		return Complainants.objects.filter(complainant_id = user).exists()

	def get(self, request):
		logged = request.user
		user = Complainants.objects.get(complainant_id = logged)
		inprocess = 'in process'
		closed = 'closed'
		number_inprocess = Complaints.objects.filter(complainant_id = user, status = inprocess).count()
		number_closed = Complaints.objects.filter(complainant_id = user, status = closed).count()
		number_notprocessed = Complaints.objects.filter(complainant_id = user, status__isnull = True).count()
		context = {
			'number_inprocess' : number_inprocess,
			'number_closed' : number_closed,
			'number_notprocessed' : number_notprocessed,
			}
		return render(request, self.template, context)

class ComplaintHistory(UserPassesTestMixin, View):
	template = 'cms/users/complaint-history.html'

	def test_func(self):
		user = self.request.user
		return Complainants.objects.filter(complainant_id = user).exists()

	def get(self, request):
		logged= request.user
		user = Complainants.objects.get(complainant_id = logged)
		complainthistory = Complaints.objects.filter(complainant_id = user)
		context = {
			'complainthistory' : complainthistory
			}
		return render(request, self.template, context)

class UserProfile(UserPassesTestMixin, View):
	template = 'cms/users/profile.html'

	def test_func(self):
		user = self.request.user
		return Complainants.objects.filter(complainant_id = user).exists()

	def get(self, request):
		user = request.user
		userInfo = Complainants.objects.filter(complainant_id = user)
		context = {
			'userInfo' : userInfo,
			'user' : user
			}
		return render(request, self.template, context)

	def post(self, request):
		user = request.user
		email = request.POST.get('useremail')
		contact = request.POST.get('contactno')
		update = Complainants.objects.filter(complainant_id = user).update(complainant_email = email, complainant_contact = contact)
		if update:
			message = "yesupdate"
		else:
			message = "noupdate"
		context = {
			'message' : message
			}
		return render(request, self.template, context)

class UserChangePassword(UserPassesTestMixin, View):
	redirect_field_name = 'redirect_to'
	form_class = forms.Forgotpass
	template = 'cms/users/change-password.html'

	def test_func(self):
		user = self.request.user
		return Complainants.objects.filter(complainant_id = user).exists()

	def get(self, request):
		form = self.form_class(None)
		context = {
			'form' : form,
		}
		return render(request, self.template, context)

	def post(self, request):
		user = request.user
		old_password = request.POST['password']
		new_password = request.POST['newpassword']
		confirm_password = request.POST['confirmpassword']
		updated = User.objects.get(username = user).set_password(new_password)
		update_session_auth_hash(request, request.user)
		return HttpResponseRedirect()

class RegisterComplaint(UserPassesTestMixin, View):
	template = 'cms/users/register-complaint.html'

	def test_func(self):
		user = self.request.user
		return Complainants.objects.filter(complainant_id = user).exists()

	def get(self, request):
		categories = Category.objects.all()
		category = request.GET.get('category')
		subcategories = Subcategory.objects.filter(category_id = category)
		print(subcategories)
		context = {
			'categories' : categories,
			'subcategories' : subcategories
		}
		return render(request, self.template, context)

	def post(self, request):
		user = self.request.user
		cat = request.POST.get('category')
		subcat = request.POST.get('subcategory')
		comptype = request.POST.get('complaintype')
		comptitle = request.POST.get('title')
		desc = request.POST.get('complaindetails')
		today_date = datetime.datetime.now()
		# same_complaint = Complaints.objects.filter(complainant_id = user, category_id = cat, reg_date = today_date)
		print(today_date)
		new_complaint = Complaints.objects.create(complainant_id_id = user, category_id_id = cat, subcategory_id_id = subcat, complaint_type = comptype, complaint_title = comptitle, complaint_details = desc)
		if new_complaint:
			message = "Complaint successfully posted"
		context = {
			'message' : message
		}
		return render(request, self.template, context)

class filterSubcategories(UserPassesTestMixin, View):
	template = 'cms/users/register-complaint.html'

	def test_func(self):
		user = self.request.user
		return Complainants.objects.filter(complainant_id = user).exists()

	def get(self, request, category_id):
		
		category = Category.objects.get(category_id = category_id)
		subcategories = Subcategory.objects.all().filter(category_id = category_id)
		json_models = serializers.serialize("json", subcategories)
		return HttpResponse(json_models, content_type="application/javascript")


class ComplaintDetails(UserPassesTestMixin, View):
	template = 'cms/users/complaint-details.html'

	def test_func(self):
		user = self.request.user
		return Complainants.objects.filter(complainant_id = user).exists()

	def get(self, request, complaint_id):
		cmpl_details = Complaints.objects.filter(complaint_id = complaint_id)
		cmpl_remark =  ComplaintRemark.objects.filter(complaint_id = complaint_id)
		if cmpl_remark:
			for rmrk in cmpl_remark:
				remark = rmrk.remark
				remarkdate = rmrk.remark_date
		else:
			remark = "No remark"
			remarkdate = "No remark"

		context = {
			'cmpl_details' : cmpl_details,
			'complaint_id' : complaint_id,
			'remark' : remark,
			'remarkdate' : remarkdate,
		}

		print(context)
		return render(request, self.template, context)

class Userprofile(UserPassesTestMixin, View):
	template = 'cms/admin/user-profile.html'

	def test_func(self):
		user = self.request.user
		return Complainants.objects.filter(complainant_id = user).exists()

	def get(self, request, complainant_id):
		return render(request, self.template)

class UserReport(UserPassesTestMixin, View):
	template = 'cms/users/report-pdf.html'

	def test_func(self):
		user = self.request.user
		return Complainants.objects.filter(complainant_id = user).exists()

	def get(self, request):
		logged = request.user
		user = Complainants.objects.get(complainant_id = logged)
		comp_details = Complaints.objects.filter(complainant_id = user)
		context = {
			'user' : user,
			'comp_details' : comp_details,
			'today' : datetime.datetime.now(),
		}
		pdf = render_to_pdf(self.template, context)
		return HttpResponse(pdf, content_type='application/pdf')

###################department views################

class department(View):
	template = 'cms/department/not-processed.html'
	def get(self, request):
		category_id = 1
		notprocessed_complaints = Complaints.objects.filter(status__isnull = True, category_id = category_id)
		context = {
			'notprocessed_complaints': notprocessed_complaints
			}
		return render(request, self.template, context)


class DepInProcessComplaints(UserPassesTestMixin, View):
	login_url = settings.LOGIN_URL
	template = 'cms/department/inprocess-complaints.html'

	def test_func(self):
		user = self.request.user
		return Category.objects.filter(category_name = user).exists()

	def get(self, request):
		status = 'in process'
		category = request.user
		cat_id = Category.objects.get(category_name = category)
		inprocess_complaints = Complaints.objects.filter(status = status, category_id = cat_id)
		context = {
			'inprocess_complaints': inprocess_complaints
			}
		return render(request, self.template, context)

class DepNotProcessComplaints(UserPassesTestMixin, View):
	login_url = settings.LOGIN_URL
	template = 'cms/department/not-processed.html'

	def test_func(self):
		user = self.request.user
		return Category.objects.filter(category_name = user).exists()

	def get(self, request):
		category = request.user
		cat_id = Category.objects.get(category_name = category)
		print(cat_id)
		notprocessed_complaints = Complaints.objects.filter(status__isnull = True, category_id = cat_id)
		context = {
			'notprocessed_complaints': notprocessed_complaints
			}
		return render(request, self.template, context)

class DepClosedComplaints(UserPassesTestMixin, View):
	login_url = settings.LOGIN_URL
	template = 'cms/department/closed-complaints.html'

	def test_func(self):
		user = self.request.user
		return Category.objects.filter(category_name = user).exists()

	def get(self, request):
		status = 'closed'
		category = request.user
		cat_id = Category.objects.get(category_name = category)
		print(cat_id)
		closed_complaints = Complaints.objects.filter(status = status, category_id = cat_id)
		context = {
			'closed_complaints': closed_complaints
			}
		return render(request, self.template, context)

class DepComplaintDetails(UserPassesTestMixin, View):
	template = 'cms/department/complaint-details.html'

	def test_func(self):
		user = self.request.user
		return Category.objects.filter(category_name = user).exists()

	def get(self, request, complaint_id):
		cmpl_details = Complaints.objects.filter(complaint_id = complaint_id)
		cmpl_remark =  ComplaintRemark.objects.filter(complaint_id = complaint_id)
		if cmpl_remark:
			for rmrk in cmpl_remark:
				remark = rmrk.remark
				remarkdate = rmrk.remark_date
		else:
			remark = "No remark"
			remarkdate = "No remark"

		context = {
			'cmpl_details' : cmpl_details,
			'complaint_id' : complaint_id,
			'remark' : remark,
			'remarkdate' : remarkdate,
		}
		return render(request, self.template, context)

class DepUpdateState(View):
	template = 'cms/department/update-complaint.html'

	def get(self, request, complaint_id):
		context = {
			'complaint_id' : complaint_id,
		}
		return render(request, self.template, context)


	def post(self, request, complaint_id):
		status = request.POST.get('status')
		remark = request.POST.get('remark')
		print(complaint_id, status, remark)
		comp_status = Complaints.objects.filter(complaint_id = complaint_id).update(status = status)
		remark_exists = ComplaintRemark.objects.filter(complaint_id_id = complaint_id)
		if remark_exists:
			comp_remark = remark_exists.update(remark = remark)
		else:
			comp_remark = ComplaintRemark.objects.create(complaint_id_id = complaint_id, remark = remark)

		if comp_remark:
			message = "status updated successfully"
		else:
			message = "Request not successful, Please try again"
		context = {
			'complaint_id' : complaint_id,
			'message' : message
		}
		return render(request, self.template,context)
