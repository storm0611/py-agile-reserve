# AgileReserveSys/views.py
import json
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render, redirect
from django.http import (
    HttpResponse,
    JsonResponse
)
from django.conf import settings
import requests
from .decorators import (
    redirect_authenticated_user,
    only_authenticated_user,
)
from .utils import (
    gen_strong_password,
    is_strong_password,
    send_verification_mail,
    send_general_mail,
    default_token_generator,
    custom_token_generator,
    urlsafe_base64_decode,
    send_subscribe_confirmation_mail,
    fernet
)
from datetime import datetime, date, timedelta
from .models import (
    Q,
    Subscriber,
    MachineList,
    CustomUser
)


# Create your views here.

def get_suggested_strong_password(request):
    if request.method == "POST":
        suggested_strong_password = gen_strong_password()
        return JsonResponse({'suggested_password': suggested_strong_password})
    else:
        return HttpResponse("Invalid request: Not supported GET")

def subscription(request):
    if request.method == "POST":
        email = request.POST.get('email')
        status = send_subscribe_confirmation_mail(request=request, user=request.user, email_template='email_templates/subscription_confirm_email_template.html', subject="Confirm Subscribe", email=email)
        if status:
            messages.error(request, 'Subscription confirm link sent to your email. Follow the instructions to confirm.', extra_tags='success')
        else:
            messages.error(request, 'Cannot send confirmation email', extra_tags='danger')
        return JsonResponse({'status': status})
    else:
        return HttpResponse("Invalid request: Not supported GET")


def subscription_confirm(request, uidb64, token):
    
    email = fernet.decrypt(uidb64.encode('utf-8')).decode('utf-8')

    if not custom_token_generator.check_token(email, token):
        return HttpResponse("Invalid Token.")
    
    try:
        subscriber = Subscriber.objects.get(email=email)
    except:
        subscriber = Subscriber()
        subscriber.email = email
    subscriber.is_active = True
    subscriber.save()    
    return render(request, 'active_templates/active_subscribed_successfully.html')


def subscription_cancel_confirm(request, uidb64, token):

    return render(request, 'active_templates/active_cancel_subscribed_successfully.html')


def subscription_remove_confirm(request, uidb64, token):
    email = fernet.decrypt(uidb64.encode('utf-8')).decode('utf-8')

    if not custom_token_generator.check_token(email, token):
        return HttpResponse("Invalid Token.")
    
    try:
        subscriber = Subscriber.objects.get(email=email)
        subscriber.is_active = False
        subscriber.save()           
    except:
        pass
    return render(request, 'active_templates/active_remove_subscribed_successfully.html')


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        status = send_general_mail(
            user=request.user, 
            email_template="email_templates/contact_us_email_template.html", 
            subject=subject, 
            from_email=email, 
            recipient_list=[settings.DEFAULT_CONTACT_EMAIL, "devstar0611@gmail.com"], 
            info={
                "email": email,
                "name": name,
                "subject": subject,
                "content": content
            }
        )
        if status:
            messages.error(request, 'Thank you! We\'ve received your message and will get back to you shortly.', extra_tags='success')
        else:
            messages.error(request, 'Cannot send email to Study Stash Team. Try again please.', extra_tags='danger')
        return JsonResponse({'status': status})
    else:
        return HttpResponse("Invalid request: Not supported GET")

@redirect_authenticated_user
def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)

        if user:
            string_user = str(user) 
            if string_user == 'admin':
                login(request, user)
                return redirect('admin_active_index')
            else:
                login(request, user)
                return redirect('active_index')
        else:
            messages.error(request, 'Invalid username or password', extra_tags='danger')

    return render(request, 'registration/login.html')


@redirect_authenticated_user
def index_view(request):
    machine_lists = MachineList.objects.all()
    return render(request, 'normal_templates/index.html',  {"machine_lists": machine_lists})

@redirect_authenticated_user
def normal_register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        # Use get_user_model() to get the appropriate user model
        User = get_user_model()

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!', extra_tags='danger')

        # Check if the username is already taken
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken!', extra_tags='danger')

        # Check if the passwords match
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match!', extra_tags='danger')

        # Check if the password is strong
        elif not is_strong_password(password):
            messages.error(request, 'Password not strong! It should have at least 6 characters, '
                                    'one uppercase letter, one lowercase letter, one digit, '
                                    'and one special character (@$#!%*?&)', extra_tags='danger')
        else:
            user = User(email=email, username=username)
            user.set_password(password)  # Use set_password to hash the password
            user.save()

            messages.success(request, '"Account created successfully!, You can now login', extra_tags='success')
            return redirect('login')  # Assuming you have a 'login' URL defined for the login page
           
        return render(request, 'normal_templates/normal_register.html', {"email": email})
    else:
        return render(request, 'normal_templates/normal_register.html')

@redirect_authenticated_user
def normal_forgot_password(request):
    if request.method == 'POST':
        username = request.POST['username']
        oldPassword = request.POST['oldPassword']
        newPassword = request.POST['newPassword']
        confirmPassword = request.POST['confirmPassword']

        # Use get_user_model() to get the appropriate user model
        User = get_user_model()

        try:
            user = User.objects.get(username=username)
            if newPassword != confirmPassword:
                messages.error(request, 'Passwords do not match!', extra_tags='danger')

            # Check if the password is strong
            elif not is_strong_password(newPassword):
                messages.error(request, 'Password not strong! It should have at least 6 characters, '
                                        'one uppercase letter, one lowercase letter, one digit, '
                                        'and one special character (@$!#%*?&)', extra_tags='danger')
                
            else:
                # Create a new user object and save it to the database
                user.set_password(newPassword)  # Use set_password to hash the password
                user.save()

                messages.success(request, 'Password reset successfully!, You can now login', extra_tags='success')
                return redirect('login')  # Assuming you have a 'login' URL defined for the login page
        except User.DoesNotExist:
            messages.error(request, 'Invalid user provided. Please use a registered user.', extra_tags='danger')
            return render(request, 'normal_templates/normal_forgot_password.html')
        
    # Your view code here
    return render(request, 'normal_templates/normal_forgot_password.html')


@redirect_authenticated_user
def password_reset_confirm(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64)
    # Use get_user_model() to get the appropriate user model
    User = get_user_model()
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return HttpResponse("Invaild User Id.")
    
    if not default_token_generator.check_token(user, token):
        return HttpResponse("Invalid Token.")
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('password_confirm')

        # Check if the passwords match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match!', extra_tags='danger')

        # Check if the password is strong
        elif not is_strong_password(password):
            messages.error(request, 'Password not strong! It should have at least 6 characters, '
                                    'one uppercase letter, one lowercase letter, one digit, '
                                    'and one special character (@$!#%*?&)', extra_tags='danger')
            
        else:
            # Create a new user object and save it to the database
            user.set_password(password)  # Use set_password to hash the password
            user.save()

            messages.success(request, 'Password reset successfully!, You can now login', extra_tags='success')
            return redirect('login')  # Assuming you have a 'login' URL defined for the login page
    
    return render(request, 'normal_templates/password_reset_confirm.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect('index')  # Redirect to the desired page after logout


@only_authenticated_user
def send_verify_mail(request):
    if request.method == "POST":
        status = send_verification_mail(request=request, user=request.user, email_template='email_templates/activate_account_email_template.html', subject="Activate Account Reqeust")
        # return HttpResponse(json.dumps({'status': status}), content_type='application/json')
        return JsonResponse({'status': status})
    else:
        return HttpResponse("Invalid request: Not supported GET")


@login_required
def account_activate_confirm(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64)
    # Use get_user_model() to get the appropriate user model
    User = get_user_model()
    try:
        user = User.objects.get(pk=uid)
    except User.DoesNotExist:
        return HttpResponse("Invaild User Id.")
    
    if not default_token_generator.check_token(user, token):
        return HttpResponse("Invalid Token.")
    
    user.verified_at = datetime.now()
    user.deactivated_at = None
    user.save()
    request.user = user
    send_general_mail(user=user, email_template='email_templates/thank_you_for_joining_email_template.html', subject="Activated Successfully")
    return render(request, 'active_templates/account_activated_successfully.html')

@login_required
def active_index(request, *args, **kwargs):
    # Add any logic you want for this view
    # For example, you can retrieve data from the database or perform other actions
    machine_lists = MachineList.objects.all()
    user = request.user
    print(user.username)
    matching_user = 0
    current_booked_num = 0
    for machine in machine_lists:
        if machine.user == user.username:
            current_booked_num += 1
            if user.can_book_num == current_booked_num:
                matching_user = 1
    if user == "admin":
        return render(request, 'normal_templates/404.html')
    else:
        return render(request, 'active_templates/active_index.html', {"user": user.username, 'active_msg': kwargs.get("verify_msg", False), 'machine_lists': machine_lists, "matching_user": matching_user})  

@login_required
def admin_active_index(request, *args, **kwargs):

    # Add any logic you want for this view
    # For example, you can retrieve data from the database or perform other actions
    machine_lists = MachineList.objects.all()
    user = str(request.user)
    print(user)
    if str(user) == "admin":
        return render(request, 'active_templates/admin_active_index.html', {"user": user, 'active_msg': kwargs.get("verify_msg", False), 'machine_lists': machine_lists})  
    else:
        return render(request, 'normal_templates/404.html')
    
@login_required
def admin_machine_end(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        messages.error(request, 'Successful End booked machine', extra_tags='success')
        if request.method == 'POST':
            data = json.load(request)
            ip_address = data.get('data')

            machine = MachineList.objects.get(ip_address=ip_address)
            machine.book_date = ""
            machine.user = ""
            machine.save()
            response_data = {'result': 'success'}
            return JsonResponse(response_data)

@login_required
def admin_machine_book(request):

    booking_date = request.POST['booking_date']
    ip_address = request.POST['ipAddress']
    sn = request.POST['sn']
    booking_duration = request.POST['booking_duration']

    booking_date = int(booking_date)

    now = datetime.now()

    user = str(request.user)

    if booking_duration == "hour":
        if booking_date > 24:
            messages.error(request, 'You can not put over 24 hours. Please select days', extra_tags='danger')
        else:
            new_time = now + timedelta(hours=booking_date)
            formatted_time = new_time.strftime("%d-%m-%Y %H:%M")
            machine = MachineList.objects.get(serial_no=sn)
            machine.book_date = f"{ formatted_time }"
            machine.user = user
            machine.save()
            messages.error(request, 'Your booking until ' + formatted_time + ' is successful', extra_tags='success')
            return redirect('admin_active_index') 

    elif booking_duration == "day":
        if booking_date > 30:
            messages.error(request, 'You can not use over 30 days. Please contact support team', extra_tags='danger')
        else:
            new_time = now + timedelta(days=booking_date)
            formatted_time = new_time.strftime("%d-%m-%Y %H:%M")
            machine = MachineList.objects.get(ip_address=ip_address)
            machine.book_date = f"{ formatted_time }"
            machine.user = user
            machine.save()
            messages.error(request, 'Your booking until ' + formatted_time + ' is successful', extra_tags='success')
            return redirect('admin_active_index') 

def statements_view(request):
    # Add any logic or data processing here if needed
    return render(request, 'normal_templates/statements.html')


def normal_studystash_store(request):
     # You can add any additional logic or data processing here if needed
     return render(request, 'normal_templates/normal_studystash_store.html')  


@login_required
def active_studystash_store(request):
    return render(request, 'active_templates/active_studystash_store.html')


@login_required
def active_session_expired(request):
    # Add any logic or data processing you need for the view here
    return render(request, 'active_templates/active_session_expired.html')    

@login_required
def active_session_membership(request):
    # Add any necessary logic here
    return render(request, 'active_templates/active_session_membership.html')

@only_authenticated_user
def machine_book(request):
    booking_date = request.POST['booking_date']
    ip_address = request.POST['ipAddress']
    sn = request.POST['sn']
    booking_duration = request.POST['booking_duration']

    booking_date = int(booking_date)

    now = datetime.now()

    user = str(request.user)

    if booking_duration == "hour":
        if booking_date > 24:
            messages.error(request, 'You can not put over 24 hours. Please select days', extra_tags='danger')
        else:
            new_time = now + timedelta(hours=booking_date)
            formatted_time = new_time.strftime("%d-%m-%Y %H:%M")
            machine = MachineList.objects.get(ip_address=ip_address)
            machine.book_date = f"{ formatted_time }"
            machine.user = user
            machine.save()
            messages.error(request, 'Your booking until ' + formatted_time + ' is successful', extra_tags='success')
            return redirect('active_index') 

    elif booking_duration == "day":
        if booking_date > 30:
            messages.error(request, 'You can not use over 30 days. Please contact support team', extra_tags='danger')
        else:
            new_time = now + timedelta(days=booking_date)
            formatted_time = new_time.strftime("%d-%m-%Y %H:%M")
            machine = MachineList.objects.get(ip_address=ip_address)
            machine.book_date = f"{ formatted_time }"
            machine.user = user
            machine.save()
            messages.error(request, 'Your booking until ' + formatted_time + ' is successful', extra_tags='success')
            return redirect('active_index') 

@only_authenticated_user
def machine_end(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if is_ajax:
        messages.error(request, 'Successful End booked machine', extra_tags='success')
        if request.method == 'POST':
            data = json.load(request)
            ip_address = data.get('data')
            sn = data.get('sn')

            machine = MachineList.objects.get(serial_no=sn)
            machine.book_date = ""
            machine.user = ""
            machine.save()
            response_data = {'result': 'success'}
            return JsonResponse(response_data)

@login_required
def user_manage(request):
    user = str(request.user)

    if user == "admin":
        users = CustomUser.objects.exclude(username='admin')
        return render(request, 'active_templates/user_manage.html', {"user_list": users})
    else:
        return render(request, 'normal_templates/404.html')
    
@login_required
def delete_user(request):
    delete_user = request.POST['delete_user']
    CustomUser.objects.filter(username=delete_user).delete()
    print(delete_user)
    messages.error(request, 'Delete ' + delete_user + ' Successful', extra_tags='success')
    return redirect('user_manage')



    