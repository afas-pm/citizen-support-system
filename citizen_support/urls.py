 
from django.contrib import admin
from django.urls import path
from myapp import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login),
    path('citizenRegister/', views.citizenRegister),

#------------------------------------------------admin_dashboard-----------------------------------------------
    path('admin_dashboard/', views.admin_dashboard),
    path('viewUsers/', views.viewUsers),
    path('delete_user/', views.delete_user),
    
    path('AddAuthorities/', views.AddAuthorities),
    path('ViewAuthorities/', views.ViewAuthorities),

    path('adminViewComplaints/', views.adminViewComplaints),

#------------------------------------------------citizen_dashboard-----------------------------------------------
    path('citizen_dashboard/', views.citizen_dashboard),
    path('userProfile/', views.userProfile),
    path('reportComplaint/', views.reportComplaint),
    path('citizenComplaintStatus/', views.citizenComplaintStatus),
    path('view_complaintToPrint/', views.view_complaintToPrint),


#------------------------------------------------authority_dashboard-----------------------------------------------
    path('authority_dashboard/', views.authority_dashboard),
    path('kwaProfile/', views.kwaProfile),
    path('kwaViewComplaints/', views.kwaViewComplaints),
    path('kwaViewAllComplaint/', views.kwaViewAllComplaint),

 

]
