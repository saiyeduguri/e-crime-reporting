from django.shortcuts import render
from django.contrib.auth.hashers import make_password, Argon2PasswordHasher,check_password
from .models import Incident, Officer, User
from .models import Officer, User
from django.contrib import messages,auth
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
import logging
from django.contrib.auth.signals import user_logged_in
from django.views.decorators.cache import never_cache
from django.dispatch import receiver
import os
import logging,secrets
import uuid 
from django.urls import reverse



logging.basicConfig(filename='logs/logs.log', encoding='utf-8', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def officer_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_officer:
            return redirect(settings.OFFICER_LOGIN_URL)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Create your views here.
def index(request):
    logging.info('Some user in home page ')
    return render(request,'index.html') 
from django.contrib.auth.hashers import check_password
@never_cache
def user_login(request):
    if request.user.is_authenticated:
        return redirect('/user_home/')
    logging.info('User in login page')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        try:
            if user and check_password(password, user.password):
                logging.info(f"Successful Login attempt from: {email}")
                request.session.set_expiry(0)
                request.session['email'] = email
                return redirect('user_home')
            else:
                raise ValidationError("Invalid credentials")
        except Exception as e:
            logging.warning(f"Unsuccessful Login attempt from: {email} - {str(e)}")
            messages.error(request, 'Invalid credentials')
            return redirect('/user_login/')

    else:
        return render(request, 'user_login.html')

        
@never_cache
def officer_login(request):
    if request.method == 'POST':
        
        
        officer_id = request.POST['officer_id']
        password = request.POST['password']
        try:
            officer = Officer.objects.get(officer_id=officer_id)
           
        except Officer.DoesNotExist:
            officer = None
        if check_password(password, officer.password):
           
            logging.info(f"Successful Login attempt from officer ID: {officer_id}")
            officer2 = authenticate(officer_id=officer.officer_id, password=officer.password)
           
            login(request, officer)
            request.session.set_expiry(0)  # Set the session to expire when the user closes the browser
            request.session['officer_id'] = officer_id
            officer=Officer.objects.get(officer_id=officer_id)
           
            zip_code=officer.zip
            inc=Incident.objects.filter(zip=zip_code)
            return redirect('officer_home')
            
        else:
         
            messages.error(request, 'Invalid credentials')
            logging.warning(f"Unsuccessful Login attempt from officer ID: {officer_id}")
            return redirect('officer_login')
    return render(request, 'officer_login.html')

def officer_home(request):
    officer_id = request.session.get('officer_id', None)
   
    officer = Officer.objects.filter(officer_id=officer_id).first()
    
    if officer:
        zip = officer.zip
       
        inc = Incident.objects.filter(zip=zip)
        return render(request, 'officer_home.html', {'inc': inc})
    else:
        # Handle the case where no officer was found for the given ID
        return render(request, 'officer_login.html', {'error_message': 'Officer not found'})

def user_registration(request):
  
    if request.method=='POST':
       
        name=request.POST['name']
        id=request.POST['id']
        email=request.POST['email']
        address=request.POST['address']
        phone_number=request.POST['phone_number']
        zip=request.POST['zip']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if password==confirm_password:
            
            if User.objects.filter(email=email).exists():
                logging.warning(f"Registration unsuccessful - account with this email exists already: {email}")
                messages.info(request,'An Account with this email already exists')
                return redirect('/')
            else: 
                hashed_password = make_password(password, hasher=Argon2PasswordHasher())
                user=User.objects.create(name=name, identity=id, password=hashed_password, email=email, phone_number=phone_number, address=address, zip=zip,)
                user.save()
                logging.info(f"User Successful registered: {email} and DB updated")
                
                
               
                return redirect('user_login')
        else:
            messages.info(request,"password not matching")
            return redirect('/')
    return render(request,'user_registration.html')

def user_home(request):
    return render(request,'user_home.html')

def user_report_incident(request):
    if 'email'not in request.session:
        return redirect('user_login')
        
    logged_email=request.session.get('email', None)
   
    if request.method == 'POST':
        try:
            name = request.POST['name']
            incident_type = request.POST['incident_type']
            email = request.POST['email']
            incident_spot = request.POST['incident_spot']
            phone_number = request.POST['phone_number']
            zip_code = request.POST['zip']
            date = request.POST['date']
            time = request.POST['time']
            victim_details = request.POST['victim_details']
            culprit_details = request.POST['culprit_details']
            
            logged_email=request.session.get('email', None)
        
            user_exists = User.objects.filter(email=email).exists()
            if not user_exists or email!=logged_email:
                messages.error(request, 'Email is not registered. Please register first.')
                logging.warning(f"Incident submission unsuccessful  - user does not exists: {email}")
                return redirect('user_report_incident')
            elif  email!=logged_email:
                messages.error(request, 'Check your email.')
                logging.warning(f"Incident submission unsuccessful  - email did not match: {email}")
                return redirect('user_report_incident')
            else:
                inc = Incident.objects.create(
                name=name,  
                type=incident_type, 
                email=email, 
                incident_spot=incident_spot, 
                phone_number=phone_number, 
                zip=zip_code,
                date=date,
                time=time,
                victim_details=victim_details,
                culprit_details=culprit_details
            )
           
            inc.save()
            logging.info(f"Incident submission successful {email}")
            messages.info(request, 'Incident reporting successful')
          
            return redirect('user_home')

        except ValidationError as e:
            logging.error('Error saving the incident report')
            messages.error(request, 'Error saving the incident report')
            return render(request, 'user_report_incident.html')

    else:
        return render(request, 'user_report_incident.html')

def user_check_status(request):
    email = request.session.get('email', None)
    if email:
        user_incident = Incident.objects.filter(email=email)
        logging.info(f"Incident status check from  {email}")
        logging.info(f"Data pulled from DB")
        return render(request,'user_check_status.html',{'user_incident': user_incident})
    else:
        return redirect('user_login')


def user_check_crime_rate(request):
    if request.method == 'POST':
        zip = request.POST['zip_code']
        zip_inc = Incident.objects.filter(zip=zip)
        logging.info(f"Data pulled from DB")
        if not zip_inc:
            messages.info(request, 'No crime data found for this zip code.')
            logging.info(f"Crime rate check failed")
        logging.info(f"Crime rate check")
        return render(request, 'user_check_crime_rate.html', {'zip_inc': zip_inc})
    else:
        return render(request, 'user_check_crime_rate.html')
def update_status(request):
    if request.method == 'POST':
        officer_id = request.session.get('officer_id', None)
      
        try:
            
            incident_id = request.POST.get('incident_id')
            email = request.POST.get('email_' + incident_id)
            status = request.POST.get('status_' + incident_id)
            
            incident = Incident.objects.get(pk=incident_id)
            incident.status = status
            incident.save()
            
            
            subject = 'An update on your reported Incident'
            message = f'Hey, Thanks for reporting. Your reported incident is {status}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            logging.info(f"Incident status of user : {email} is update by{officer_id} ")
           
            messages.success(request, "Incident is updated, and the user is notified")
            logging.info(f"Data pushed to DB")

            
        except Incident.DoesNotExist:
            messages.error(request, "Incident not found.")
            logging.info(f"Incident does not exists ")
        except Exception as e:
            logging.info(f"Error in incidnet updation ")
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('officer_home')
    return redirect('officer_login')

def send_emergency_alert(request):

    if request.method == 'POST':
        officer_id = request.session.get('officer_id', None)
        try:
            emergency_message = request.POST.get('emergency_alert')
            if emergency_message:

                officer_id = request.session.get('officer_id', None)
             
                officer = Officer.objects.filter(officer_id=officer_id).first()
    
                if officer:
                    zip = officer.zip
                   
                    recipients = User.objects.filter(zip=zip).values_list('email', flat=True)
               
                subject = 'Emergency Alert'
                message = f'Emergency Alert: {emergency_message}'
                from_email = settings.EMAIL_HOST_USER  # Use your email settings
                for recipient_email in recipients:
                  
                    send_mail(subject, emergency_message, from_email, [recipient_email], fail_silently=False)

                logging.info(f"Data pulled from DB")
                messages.success(request, "Emergency alert sent successfully")
                
                logging.info(f"Emergency alert is sent  by{officer_id} ")
            else:
                messages.error(request, "Emergency alert message is empty")
                logging.info(f"Emergency alert is failed by {officer_id} ")

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            logging.error(f"Error occured in sending emergency alert {officer_id} ")

        return redirect('officer_home')
    return redirect('officer_home')


def logout(request):
    logging.info("Logged out successfully")
    request.session.clear()
    auth.logout(request)
    return redirect('/')

def custom_404(request, exception):
    return render(request, 'error.html', status=404)

def custom_500(request):
    
    return render(request, 'error.html', status=500)


def forgot_password(request):
  
    if request.method == 'POST':
        logging.info(f"")
      
        email = request.POST.get('email')
        user= User.objects.filter(email=email).exists()
        logging.info(f"attempt to change the password by {email}")
        if user:
            otp = str(secrets.randbelow(1000000)).zfill(6)
            request.session.clear()
            request.session['reset_otp'] = otp
            request.session['email'] = email

            subject = 'OTP for resetting the password'
            message = f'Hey, Your OTP is {otp}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
           
            messages.success(request, 'If you are a registered user, check your email for the OTP.')
            logging.info(f"OTP send successfully by email")
            return redirect('enter_otp') 
        else:
            messages.error(request, 'If you are a registered user, check your email for the OTP.')
            logging.warning(f"Unregistered user trying to change the password {email}") 
            return render(request, 'enter_otp.html')
    return render(request, 'forgot_password.html')

def enter_otp(request):

    if request.method == 'POST':
      
       
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('reset_otp')
       
        
        if entered_otp == stored_otp:
           
         
            messages.success(request, 'OTP authenticated')
            return redirect('change_password')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            logging.warning(f"wrong otp")
            return render(request, 'enter_otp.html')
    return render(request, 'enter_otp.html')

def change_password(request):
    if request.method == 'POST':
        email = request.session.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password and email:
            hashed_password = make_password(password)
            
            try:
                user = User.objects.get(email=email)
                user.password=hashed_password
                user.save()
                messages.success(request, 'Password reset successful.')
                request.session.flush()
                logging.info(f"User password successfully changed: {email} and DB updated")
                request.session.flush()
                request.session.clear()
                return redirect('user_login')
            except User.DoesNotExist:
                logging.warning(f"Unsuccessful password change attempt")
                messages.error(request, 'User does not exist.')
        else:
            messages.error(request, 'Passwords do not match or invalid email.')
    else:
        messages.error(request, 'Invalid request method.')

    return render(request, 'change_password.html')

