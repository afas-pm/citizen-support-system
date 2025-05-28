from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib import messages
from datetime import date as date, datetime as dt
from .models import *
from django.db.models import Q, Min, Max
from django.core.mail import send_mail
from django.urls import reverse
# Create your views here.

today =dt.now().date()
print('Today-->>',today)
districts = ["Thiruvananthapuram", "Kollam", "Pathanamthitta", "Alappuzha", "Kottayam", "Idukki", "Ernakulam", "Thrissur", "Palakkad", "Malappuram", "Kozhikode", "Wayanad", "Kannur", "Kasaragod"]

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username', username, password,'password')
        user = authenticate(request, username=username, password=password)

        print("Authenticated User:", user)  # Debugging
        if user:
            print("User Type:", user.user_type)  # This will now only print if user is not None

        if user is not None:
            if user.user_type == 'admin':
                return redirect('/admin_dashboard')
            elif user.user_type == 'Citizen':
                request.session['uid'] = user.id
                return redirect('/citizen_dashboard')
            elif user.user_type == 'KSEB':
                request.session['uid'] = user.id
                return redirect('/authority_dashboard')
            elif user.user_type == 'KWA':
                request.session['uid'] = user.id
                return redirect('/authority_dashboard')
            elif user.user_type == 'PWD':
                request.session['uid'] = user.id
                return redirect('/authority_dashboard')
        else:
            messages.info(request, 'Username or password is incorrect')

    return render(request, 'login.html')


def index(request):
   
    return render(request, 'index.html')

def citizenRegister(request):
    if request.POST:
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        district = request.POST['district']
        image = request.FILES['image']
        
        if Login.objects.filter(username=email, password=password).exists():
            messages.info(request, 'User already exists')
            return redirect('/citizen_register')
        else:
            login = Login.objects.create_user(username=email, password=password, user_type='Citizen', view_password=password)
            Citizen.objects.create(loginId=login, name=name, email=email, phone=phone, address=address, district=district, image=image)
            return redirect('/login')
    return render(request, 'citizen_register.html')
        
        
#------------------------------------------------admin_dashboard-----------------------------------------------


def admin_dashboard(request):
    return render(request, 'ADMIN/admin_dashboard.html')

def viewUsers(request):
    users = Citizen.objects.all()
    return render(request, 'ADMIN/view_users.html', {'users': users})

def delete_user(request):
    id = request.GET.get('id')
    Login.objects.filter(id=id).delete()
    messages.info(request, 'User deleted successfully')
    return redirect('/viewUsers')


def AddAuthorities(request):
    if request.POST:
        authority = request.POST['authority']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']
        district = request.POST['district']
        image = request.FILES['image']
        
        if Login.objects.filter(username=email, password=password).exists():
            messages.info(request, 'User already exists')
            return redirect('/AddAuthorities')
        
        else:
            if Authority.objects.filter(district=district, authority=authority).exists():
                messages.info(request, 'District already has an authority')
                return redirect('/AddAuthorities')
            else:
                login = Login.objects.create_user(username=email,
                                                password=password,
                                                user_type=authority,
                                                view_password=password)
                Authority.objects.create(loginId=login,
                                        authority=authority,
                                        email=email,
                                        phone=phone,
                                        address=address,
                                        district=district,
                                        image=image)                        
                return redirect('/ViewAuthorities')
    return render(request, 'ADMIN/AddAuthorities.html')


def ViewAuthorities(request):
    authorities = Authority.objects.all()
    return render(request, 'ADMIN/ViewAuthorities.html', {'authorities': authorities})


def adminViewComplaints(request):
    complaints = Complaint.objects.all()
    authorities = Authority.objects.all()
    context = {'authorities': authorities, 'complaints': complaints, 'districts': districts}
    return render(request, 'ADMIN/complaints.html', context)


#------------------------------------------------citizen_dashboard-----------------------------------------------

def citizen_dashboard(request):
    return render(request, 'CITIZEN/citizen_dashboard.html')
 
def userProfile(request):
    uid = request.session.get('uid')
    
    if not uid:
        messages.error(request, "User not found. Please log in again.")
        return redirect('/login')  # Redirect to login if no session ID

    try:
        user = Citizen.objects.get(loginId=uid)
    except Citizen.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('/login')

    if request.method == "POST":
        name = request.POST.get('name', user.name)
        email = request.POST.get('email', user.email)
        phone = request.POST.get('phone', user.phone)
        address = request.POST.get('address', user.address)
        district = request.POST.get('district', user.district)
        password = request.POST.get('password')
        image = request.FILES.get('image')  # Avoid KeyError

        # Update Citizen model fields
        user.name = name
        user.phone = phone
        user.address = address
        user.district = district
        if image:
            user.image = image

        user.save()
       # Update password if provided
        if password:
            try:
                login_user = Login.objects.get(id=uid)
                login_user.view_password = password
                login_user.set_password(password)
                login_user.save()
                user.save()
                messages.success(request, "Password changed successfully")
            except Login.DoesNotExist:
                messages.error(request, "User login details not found.")
        # Update email in Login model
        if email:
            try:
                user.email = email
                
                login_user = Login.objects.get(id=uid)
                login_user.username = email
                login_user.save()
                user.save()
            except Login.DoesNotExist:
                messages.error(request, "User login details not found.")

        messages.success(request, "Profile updated successfully")
        return redirect('/userProfile')

    return render(request, 'CITIZEN/userProfile.html', {'user': user,'districts':districts})
 
def citizenComplaintStatus(request):
    uid = request.session.get('uid')
    print(uid,'<<<---uid')
    uid = Citizen.objects.get(loginId=uid)
    complaints = Complaint.objects.filter(citizenId=uid.id)
    authorities = Authority.objects.all()
    context = {'authorities': authorities, 'complaints': complaints, 'districts': districts}
    print(context,'<<<---context')
    return render(request, 'CITIZEN/complaintStatus.html', context)


def view_complaintToPrint(request):
    uid = request.session.get('uid')
    id = request.GET.get('id')
    print(id,'<<<---id')
    print(uid,'<<<---uid')
    uid = Citizen.objects.get(loginId=uid)
    complaints = Complaint.objects.get(id=id)
    authorities = Authority.objects.all()
    context = {'authorities': authorities, 'complaint': complaints, 'districts': districts}
    # print(context,'<<<---context')
    print(complaints,'<<<---complaints')
    return render(request, 'CITIZEN/view_complaintToPrint.html', context)


def reportComplaint(request):
    if request.method == "POST":
        uid = request.session.get('uid')
        title = request.POST['title']
        description = request.POST['description']
        complaintImage = request.FILES.get('complaintImage')
        district = request.POST['district']
        authority = request.POST['authority']
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        try:
            authorityId = Authority.objects.get(authority=authority, district=district)
            loginId = Login.objects.get(id=uid)
            loginId = Citizen.objects.get(loginId=loginId)
            Complaint.objects.create(
                citizenId=loginId,
                authorityId=authorityId,
                title=title,
                description=description,
                complaintImage=complaintImage,
                status='Pending',
                date=today,
                latitude=latitude,
                longitude=longitude
            )

            messages.success(request, 'Complaint reported successfully')
            return redirect('/reportComplaint')

        except Authority.DoesNotExist:
            messages.error(request, "Selected authority does not exist in the given district.")
        except Login.DoesNotExist:
            messages.error(request, "User session expired. Please log in again.")
    
    return render(request, 'CITIZEN/reportComplaint.html', {'districts': districts})


#------------------------------------------------authority_dashboard-----------------------------------------------

from django.core.mail import send_mail
from django.conf import settings

def authority_dashboard(request):
   
    return render(request, 'AUTHORITY/authority_dashboard.html')
 

def kwaProfile(request):
    uid = request.session.get('uid')
    
    if not uid:
        messages.error(request, "User not found. Please log in again.")
        return redirect('/login')

    try:
        user = Authority.objects.get(loginId=uid)
    except Authority.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('/login')

    if request.method == "POST":
        email = request.POST.get('email', user.email)
        phone = request.POST.get('phone', user.phone)
        address = request.POST.get('address', user.address)
        district = request.POST.get('district', user.district)
        image = request.FILES.get('image')
        password = request.POST.get('password')

        # Update user profile details
        user.phone = phone
        user.address = address
        user.district = district
        if image:
            user.image = image
        user.save()

        # Update password if provided
        if password:
            try:
                login_user = Login.objects.get(id=uid)
                login_user.set_password(password)
                login_user.view_password = password
                login_user.save()
                user.save()
                # messages.success(request, "Password changed successfully")
            except Login.DoesNotExist:
                messages.error(request, "User login details not found.")

        # Update email if provided
        if email:
            try:
                login_user = Login.objects.get(id=uid)
                login_user.username = email
                login_user.save()
                user.email = email
                user.save()
            except Login.DoesNotExist:
                messages.error(request, "User login details not found.")

        messages.success(request, "Profile updated successfully")
        return redirect('/kwaProfile')

    return render(request, 'AUTHORITY/Profile.html', {'user': user})



 
import os

from django.conf import settings


def kwaViewComplaints(request):
    authority_id = request.session.get('uid')  # Assume authority logs in
    authority = Authority.objects.get(loginId=authority_id)
    complaints = Complaint.objects.filter(authorityId=authority.id).exclude(status='Resolved')
    print(complaints, '<<<====authority_id')

    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        status = request.POST.get("status")

        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.status = status
        complaint.save()

        # Construct email details
        user_email = complaint.citizenId.email # Ensure it's an email field
        
        print(user_email,"<<<====USER EMAIL_/////////////////////////////////////// <<")
        maps_link = f"https://www.google.com/maps?q={complaint.latitude},{complaint.longitude}"


        subject = "Update on Your Complaint Status"
        
        message = f"""Dear {complaint.citizenId.name},

        We wanted to update you regarding your complaint (ID: {complaint.id}) about "{complaint.title}" regarding {complaint.description}.
        
        The status of your complaint has been updated to: {status}.
                
        📍 View the location on Google Maps:  
        
        {maps_link}

        Thank you for your patience and for bringing this to our attention. If you have any further concerns, please don't hesitate to reach out.

        Best regards,  
        AUTHORITY Support Team
        """

        print(f"""
            Email Message: {message}
            SUBJECT: {subject}
            username: {user_email}
              """)
        
        # Send email
        a = send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
        print(a)
     
        # a=send_mail('Test Subject', 'Test Message', settings.EMAIL_HOST_USER, ['arkr0724@gmail.com'])
        messages.success(request, "Complaint updated successfully! Email notification sent.")
        return redirect("/kwaViewComplaints")

    return render(request, "AUTHORITY/complaints.html", {"complaints": complaints})

def kwaViewAllComplaint(request):
    uid = request.session.get('uid')
    authority=Authority.objects.get(loginId=uid)
    print(authority)
    complaints = Complaint.objects.filter(authorityId=authority.id)
    print(complaints)
    
    return render(request, 'AUTHORITY/viewAllComplaints.html', {'complaints': complaints})


#------------------------------------------------kseb_dashboard-----------------------------------------------

def kseb_dashboard(request):
    return render(request, 'KSEB/kseb_dashboard.html')
 
def ksebProfile(request):
    uid = request.session.get('uid')
    
    if not uid:
        messages.error(request, "User not found. Please log in again.")
        return redirect('/login')

    try:
        user = Authority.objects.get(loginId=uid)
    except Authority.DoesNotExist:
        messages.error(request, "Profile not found.")
        return redirect('/login')

    if request.method == "POST":
        email = request.POST.get('email', user.email)
        phone = request.POST.get('phone', user.phone)
        address = request.POST.get('address', user.address)
        district = request.POST.get('district', user.district)
        image = request.FILES.get('image')
        password = request.POST.get('password')

        # Update user profile details
        user.phone = phone
        user.address = address
        user.district = district
        if image:
            user.image = image
        user.save()

        # Update password if provided
        if password:
            try:
                login_user = Login.objects.get(id=uid)
                login_user.set_password(password)
                login_user.view_password = password
                login_user.save()
                user.save()
                # messages.success(request, "Password changed successfully")
            except Login.DoesNotExist:
                messages.error(request, "User login details not found.")

        # Update email if provided
        if email:
            try:
                login_user = Login.objects.get(id=uid)
                login_user.username = email
                login_user.save()
                user.email = email
                user.save()
            except Login.DoesNotExist:
                messages.error(request, "User login details not found.")

        messages.success(request, "Profile updated successfully")
        return redirect('/ksebProfile')

    return render(request, 'KSEB/Profile.html', {'user': user})


from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import EmailMessage
from django.contrib import messages

def ksebViewComplaints(request):
    authority_id = request.session.get('uid')  # Assume authority logs in
    authority_id = Authority.objects.get(loginId=authority_id)
    complaints = Complaint.objects.filter(authorityId=authority_id.id)
    print(complaints, '<<<====authority_id')
    if request.method == "POST":
        complaint_id = request.POST.get("complaint_id")
        status = request.POST.get("status")

        complaint = get_object_or_404(Complaint, id=complaint_id)
        complaint.status = status
        complaint.save()

        # Construct email details
        user_email = complaint.citizenId.email # Ensure it's an email field
        
        print(user_email,"<<<====USER EMAIL_/////////////////////////////////////// <<")
        maps_link = f"https://www.google.com/maps?q={complaint.latitude},{complaint.longitude}"


        subject = "Update on Your Complaint Status"
        
        message = f"""Dear {complaint.citizenId.name},

        We wanted to update you regarding your complaint (ID: {complaint.id}) about "{complaint.title}" regarding {complaint.description}.
        
        The status of your complaint has been updated to: {status}.
                
        📍 View the location on Google Maps:  
        
        {maps_link}

        Thank you for your patience and for bringing this to our attention. If you have any further concerns, please don't hesitate to reach out.

        Best regards,  
        AUTHORITY Support Team
        """

        print(f"""
            Email Message: {message}
            SUBJECT: {subject}
            username: {user_email}
              """)
        
        # Send email
        a = send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
        print(a)
     
        # a=send_mail('Test Subject', 'Test Message', settings.EMAIL_HOST_USER, ['arkr0724@gmail.com'])
        messages.success(request, "Complaint updated successfully! Email notification sent.")

        return redirect("/ksebViewComplaints")

    return render(request, "KSEB/complaints.html", {"complaints": complaints})



