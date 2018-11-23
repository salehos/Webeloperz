from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User, Group
from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.
from main.form import SignUpForm, ContactForm
from main.models import create_user_profile, Profile


def login_(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect("/")
        else:
            return render(request, 'error.html')
    return render(request, 'login.html')


def contactus(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)
        if form.is_valid:
            title = request.POST.get(
                'title'
                , '')
            myemail = request.POST.get(
                'email'
                , '')
            text = request.POST.get('text', '')

            send_mail(title, text, myemail, 'ostadju@fastmail.com')
            return render(request, 'itsok.html', )
    return render(request, 'contactus.html', {
        'form': form_class,
    })


def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")


def signup(request):
    context = {
        "error1": False,
        "error2": False,
        "error3": False
    }

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if User.objects.filter(email=request.POST.get('email')).exists():
            context["error3"] = True
        if request.POST.get('password1') != request.POST.get('password2'):
            context["error2"] = True
        if User.objects.filter(username=request.POST.get('username')).exists():
            context["error1"] = True
        if context["error1"] or context["error2"] or context["error3"]:
            return render(request, "blank.html", context)
        if form.is_valid():
            user = form.save()
            level = form.cleaned_data['type']
            if level == 'Teacher':
                user.groups.add(Group.objects.get(name='Teacher'))
            else:
                user.groups.add(Group.objects.get(name='Student'))
            return redirect('')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    return render(request, 'home.html', )


def profile(request):
    if request.user.groups.filter(name='Teacher').exists():
        group = "استاد"
    else:
        group = "دانشجو"
    return render(request, 'profile.html', {'username': request.user.username, 'firstname': request.user.first_name,
                                            'lastname': request.user.last_name, 'bio': request.user.profile.bio,
                                            'gender': request.user.profile.gender , 'group' : group})


def editnameandusername(request):
    if request.method == 'POST':
        user = User.objects.get(username=request.user.username)
        user.first_name = request.POST.get('firstname')
        user.last_name = request.POST.get('lastname')
        user.profile.gender = request.POST.get('gender')
        user.profile.bio = request.POST.get('bio')
        user.profile.gender = 'مرد'
        if user.profile.gender == 'F':
            user.profile.gender = 'زن'
        user.save()
        return render(request, 'profile.html', {'username': request.user.username, 'firstname': request.user.first_name,
                                                'lastname': request.user.last_name,
                                                'gender': request.user.profile.gender,
                                                'bio': request.user.profile.bio})
    return render(request, 'editnameandusername.html', )
