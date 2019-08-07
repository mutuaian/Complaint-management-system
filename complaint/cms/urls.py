from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

app_name = "cms"
urlpatterns = [
	path('cms/index', views.Index.as_view(), name='index'),
	path('cms/login', views.Login.as_view(), name='login'),
	path('cms/logout', views.Logout.as_view(), name ='logout'),
	path('cms/register', views.Register.as_view(), name = 'register'),
	
	###############admin urls######################
	path('cms/admin/inprocesscomplaints', views.InProcessComplaints.as_view(), name='inprocesscomplaints'),
	path('cms/admin/notprocessedcomplaints',views.NotProcessedComplaints.as_view(), name ='notprocessedcomplaints'),
	path('cms/admin/closedcomplaints', views.ClosedComplaints.as_view(), name='closedcomplaints'),
	path('cms/admin/manageusers', views.ManageUsers.as_view(), name='manageusers'),
	path('cms/admin/categories', views.ManageCategories.as_view(), name = 'categories'),
	path('cms/admin/subcategories', views.ManageSubCategories.as_view(), name = 'subcategories'),
	path('cms/admin/newcategory', views.NewCategory.as_view(), name = 'newcategory'),
	path('cms/admin/newsubcategory', views.NewSubcategory.as_view(), name = 'newsubcategory'),
	path('cms/admin/changepassword', views.ChangePassword.as_view(), name = 'changepassword'),
	path('cms/admin/complaintdetails/<int:complaint_id>', views.AdminComplaintDetails.as_view(), name = 'admincomplaintdetails'),
	path('cms/admin/editcategory/<int:category_id>', views.EditCategory.as_view(), name = 'editcategory'),
	path('cms/admin/editsubcategory/<int:subcategory_id>', views.EditSubcategory.as_view(), name = 'editsubcategory'),
	path('cms/admin/updatecomplaint/<int:complaint_id>', views.UpdateState.as_view(), name = 'updatestate'),
	path('cms/admin/report', views.AdminReport.as_view(), name = 'adminreport'),
	path('cms/admin/userdetails/<path:complainant_id>', views.UserDetails.as_view(), name = 'userdetails'),


	###############user urls########################
	path('cms/users/dashboard', views.Dashboard.as_view(), name = 'dashboard'),
	path('cms/users/complainthistory', views.ComplaintHistory.as_view(), name = 'complainthistory'),
	path('cms/users/profile', views.UserProfile.as_view(), name = 'profile'),
	# path('cms/users/updateprofile/<path:complainant_id>', views.UpdateProfile.as_view(), name = 'updateprofile'),
	path('cms/users/changepassword', views.UserChangePassword.as_view(), name = 'userchangepassword'),
	# path('cms/users/newpassword', views.NewPassword.as_view(), name = 'usernewpassword'),
	path('cms/users/registercomplaint', views.RegisterComplaint.as_view(), name = 'registercomplaint'),
	path('cms/users/categories/<int:category_id>/all_json_subcategories', views.filterSubcategories.as_view(), name = 'filtersubcategories'),
	path('cms/users/complaintdetails/<int:complaint_id>', views.ComplaintDetails.as_view(), name = 'complaintdetails'),
	path('cms/users/complaintreport', views.UserReport.as_view(), name = 'complaintreport'),

	path('cms/dept', views.DepNotProcessComplaints.as_view(), name = 'department'),

	#####################department urls #################
	path('cms/department/notprocessed', views.DepNotProcessComplaints.as_view(), name = 'depnotprocessed'),
	path('cms/department/closed', views.DepClosedComplaints.as_view(), name = 'depclosed'),
	path('cms/department/inprocess', views.DepInProcessComplaints.as_view(), name = 'depinprocess'),
	path('cms/department/complaintdetails/<int:complaint_id>', views.DepComplaintDetails.as_view(), name = 'depcomplaintdetails'),
	path('cms/department/updatecomplaint/<int:complaint_id>', views.DepUpdateState.as_view(), name = 'depupdatestate'),


]