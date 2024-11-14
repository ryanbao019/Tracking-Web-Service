from django.shortcuts import render

# Create your views here.


from .forms import RegisterForm


from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm  # Import UserCreationForm here
from service.models import Profile

from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .models import EmailVerificationCode
from .forms import EmailVerificationForm

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .models import EmailVerificationCode
from .forms import EmailVerificationForm

def home(request):
    return render(request, 'home.html')
'''
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create profile only if it doesn't exist
            Profile.objects.get_or_create(user=user)
            login(request, user)
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
'''
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # or another appropriate page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
'''
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('service_home')  # Ensure 'home' is a valid URL name
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
'''


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            # Clear any existing verification session
            if 'pending_user_id' in request.session:
                del request.session['pending_user_id']

            # Set new verification session
            request.session['pending_user_id'] = user.id

            # Send verification email
            if send_verification_email(request, user):
                messages.success(request, 'Verification code sent to your email.')
                return redirect('verify_email')
            else:
                messages.error(request, 'Failed to send verification code. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def send_verification_email(request, user):
    try:
        # Delete any existing unused codes for this user
        EmailVerificationCode.objects.filter(user=user, is_verified=False).delete()

        # Generate new verification code
        code = EmailVerificationCode.generate_code()
        EmailVerificationCode.objects.create(user=user, code=code)

        # Send email
        subject = 'Your Verification Code'
        message = f'Your verification code is: {code}\nThis code will expire in 5 minutes.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, 'Verification code sent! Please check your email.')
        return True
    except Exception as e:
        print(f"Email sending error: {str(e)}")  # For debugging
        messages.error(request, f'Failed to send verification code. Error: {str(e)}')
        return False

def verify_email(request):
    user_id = request.session.get('pending_user_id')
    if not user_id:
        return redirect('login')

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect('login')

    if request.method == 'POST':
        if 'resend' in request.POST:
            if send_verification_email(request, user):
                messages.success(request, 'New verification code sent!')
            return redirect('verify_email')

        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            submitted_code = form.cleaned_data['verification_code']
            try:
                verification = EmailVerificationCode.objects.get(
                    user=user,
                    code=submitted_code,
                    is_verified=False
                )

                if verification.is_expired():
                    messages.error(request, 'Verification code has expired. Please request a new one.')
                    return redirect('verify_email')

                verification.is_verified = True
                verification.save()
                login(request, user)
                del request.session['pending_user_id']
                return redirect('service_home')

            except EmailVerificationCode.DoesNotExist:
                messages.error(request, 'Invalid verification code.')
    else:
        form = EmailVerificationForm()

    return render(request, 'verify_email.html', {'form': form})