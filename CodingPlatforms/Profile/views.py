from django.shortcuts import render
from Profile.models import Profile
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from Profile.details_soup import UserData, UsernameError, PlatformError, BrokenChangesError

def index(request):
    return render(request, 'index.html')

# Create your views here.

@login_required
def home(request):
    return render(request , 'home.html')

def view_profile(request, username):
    user_obj = User.objects.filter(username = username).first()
    profile_obj = Profile.objects.filter(user = user_obj ).first()
    user_data = UserData("SaiMhatre321")
    print(user_data.get_details("leetcode", "SaiMhatre"))
    #print(user_data.get_details("codechef", "saimhatre_321"))
    #print(user_data.get_details("codeforces", "saimhatre243"))
    return render(request, 'dummy.html')
    #try:

        #return user_data.get_details("leetcode")

    """except UsernameError:
            return {'status': 'Failed', 'details': 'Invalid username'}

        except PlatformError:
            return {'status': 'Failed', 'details': 'Invalid Platform'}
        
        except BrokenChangesError:
            return {'status': 'Failed', 'details': 'API broken due to site changes'}"""

def edit_profile(request, username):
    if request.method == 'POST':
        fn = request.POST.get('fname')
        ln = request.POST.get('lname')
        gh = request.POST.get('git')
        LinkedIn = request.POST.get('LinkedIn')
        cf = request.POST.get('CodeForces')
        cc = request.POST.get('CodeChef')
        sj = request.POST.get('SPOJ')
        lc = request.POST.get('LeetCode')
        user_obj = User.objects.filter(username = username).first()
        profile_obj = Profile.objects.filter(user = user_obj ).first()
        profile_obj.fn = fn
        profile_obj.ln = ln
        profile_obj.gh = gh
        profile_obj.LinkedIn = LinkedIn
        profile_obj.cf = cf
        profile_obj.cc = cc
        profile_obj.sj = sj
        profile_obj.lc = lc
        profile_obj.save()
        return render(request, 'thanku.html')

    return render(request, 'multi_form.html')

def ResetPass(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            auth_token1 = str(uuid.uuid4())
            user_obj = User.objects.filter(email = email).first()
            profile_obj = Profile.objects.filter(user = user_obj ).first()
            profile_obj.auth_token= auth_token1
            profile_obj.save()
            send_mail_to_change_password(email , auth_token1)
            return redirect('/token')
        except Exception as e:
            print(e)

    return render(request, 'reset.html')

def send_mail_to_change_password(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/change_password/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)

def change_password(request, auth_token):
    if request.method == 'POST':
        new_password= request.POST.get('new_password')
        confirm_password= request.POST.get('confirm_password')
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
        if new_password != confirm_password:
            messages.success(request, 'Both fields have different Psssword.')
            return redirect(f'/change_password/{auth_token}')
        
        try:
            if profile_obj:
                #user_obj = User.objects.filter(profile_obj == user_obj)
                user_obj= profile_obj.user
                user_obj.set_password(new_password)
                user_obj.save()
                profile_obj.is_verified = True
                profile_obj.save()
                messages.success(request, 'Successfully Changed Password')
                return redirect('/accounts/login')
            else:
                return redirect('/error')
        except Exception as e:
            print(e)
            return redirect('/')
        
    return render(request, 'new_password.html')


def login_attempt(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.success(request, 'User not found.')
            return redirect('/accounts/login')
        
        
        profile_obj = Profile.objects.filter(user = user_obj ).first()

        if not profile_obj.is_verified:
            messages.success(request, 'Profile is not verified check your mail.')
            return redirect('/accounts/login')

        user = authenticate(username = username , password = password)
        if user is None:
            messages.success(request, 'Wrong password.')
            return redirect('/accounts/login')
        
        login(request , user)
        return redirect(f'/edit_profile/{username}')

    return render(request , 'login.html')

def register_attempt(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            if User.objects.filter(username = username).first():
                messages.success(request, 'Username is taken.')
                return redirect('/register')

            if User.objects.filter(email = email).first():
                messages.success(request, 'Email is taken.')
                return redirect('/register')
            
            user_obj = User(username = username , email = email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
            profile_obj.save()
            send_mail_after_registration(email , auth_token)
            return redirect('/token')

        except Exception as e:
            print(e)


    return render(request , 'register.html')

def success(request):
    return render(request , 'success.html')

def token_send(request):
    return render(request , 'token_send.html')

def verify(request , auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token = auth_token).first()
    

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('/accounts/login')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('/accounts/login')
        else:
            return redirect('/error')
    except Exception as e:
        print(e)
        return redirect('/')

def error_page(request):
    return  render(request , 'error.html')

def send_mail_after_registration(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )
# Create your views here.
