from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.checks import messages
from django.core.exceptions import ValidationError

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
# Create your views here.


from main.form import SignUpForm, ContactForm


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

            # Email the profile with the
            # contact information
            # template = get_template('contact_template.txt')
            # context = {
            #     'title': title,
            #     'email': email,
            #     'text': text,
            # }
            # content = template.render(context)

            # email = EmailMessage(
            #     title,
            #     text,
            #     myemail,
            #     ['ostadju@fastmail.com'],
            #     '',
            #     reply_to=[],
            #     headers={'Message-ID': 'foo'},

            # )
            # email.send()
            return render(request, 'itsok.html', )
    return render(request, 'contactus.html', {
        'form': form_class,
    })


def logout_(request):
    logout(request)
    return HttpResponseRedirect("/")


def signup(request):
    context = {
        "error1":False,
        "error2":False,
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
            return render(request, "signup.html", context)
        if form.is_valid():
            form.save()
            return redirect('')

    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    return render(request, 'home.html', )


def profile(request):
    return render(request, 'profile.html', {'username': request.user.username, 'firstname': request.user.first_name,
                                            'lastname': request.user.last_name})


def editnameandusername(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        gender = request.POST.get('gender')
        bio = request.POST.get('bio')
        request.user.first_name = firstname
        request.user.last_name = lastname

        request.user.save();
        return render(request, 'profile.html', {'username': request.user.username, 'firstname': request.user.first_name,
                                                'lastname': request.user.last_name, 'bio': request.user.bio,
                                                'gender': request.user.gender})
    return render(request, 'editnameandusername.html', )
