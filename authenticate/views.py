from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages  # Import messages framework
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordResetView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import default_token_generator

def index(request):
    return render(request, "authenticate/index.html")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect('register')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1,
                                            first_name=first_name, last_name=last_name)
            user.is_active = False  # Deactivate account until it is confirmed
            user.save()

            # Send email verification
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
            verification_url = f"{request.scheme}://{request.get_host()}{verification_link}"

            htmly = get_template('authenticate/Email.html')
            context = {'username': username, 'verification_url': verification_url}
            subject, from_email, to = 'Verify your email', 'your_email@gmail.com', email
            html_content = htmly.render(context)
            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            messages.success(request, "Registration successful! Please verify your email.")
            return redirect('signin')

        except Exception as e:
            messages.error(request, f"Error during registration: {e}")
            return redirect('register')

    return render(request, "authenticate/register.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now log in.")
        return redirect('signin')
    else:
        messages.error(request, "Activation link is invalid!")
        return render(request, 'authenticate/activation_invalid.html')


def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the provided email exists
        try:
            user = User.objects.get(email=email)
            username = user.username  # Retrieve the username associated with the email
        except User.DoesNotExist:
            messages.error(request, "Bad Credentials!")
            return redirect('homepage')

        # Authenticate using the retrieved username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, "authenticate/homepage.html", {'fname': fname})
        else:
            messages.error(request, "Bad Credentials!")
            return redirect('signin')
    

    return render(request, "authenticate/signin.html")

def logout_view(request):
    logout(request)
    messages.success(request, "Logged  out successfully!")
    return redirect('index')

def password_reset(request):
    if request.method == 'POST':
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'authenticate/password_reset.html')

        user = request.user
        if user.is_authenticated:
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # Keep user logged in after password change
            messages.success(request, "Your password has been reset successfully.")
            return redirect('signin')  # Redirect to login 
        else:
            messages.error(request, "User not authenticated.")
            return redirect('signin')  # Redirect to login 

    return render(request, 'authenticate/password_reset.html')

def homepage(requst):
    return render(requst, 'authenticate/homepage.html')

def profile(request):
    return render(request, 'authenticate/profile.html')

def dashboard(request):
    return render(request, 'authenticate/dashboard.html')

def help(request):
    return render(request, 'authenticate/help.html')

