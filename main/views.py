from email.message import EmailMessage

from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.template.loader import get_template

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

#
# def contactus(request):
#     if request.method == 'POST':
#         text = request.POST.get('text')
#         title = request.POST.get('title')
#         emamil = request.POST.get('email')
#
#     return render(request, 'contactus.html')


def contactus(request):
    form_class = ContactForm

    # new logic!
    if request.method == 'POST':
        form = form_class(data=request.POST)

    def contact(request):
        if form.is_valid():
            # title = request.POST.get(
            #     'title'
            #     , '')
            # email = request.POST.get(
            #     'email'
            #     , '')
            # text = request.POST.get('text', '')
            #
            # # Email the profile with the
            # # contact information
            # template = get_template('contact_template.txt')
            # context = {
            #     'text': text,
            #     'email': email,
            #     'text': text,
            # }
            # content = template.render(context)
            #
            # email = EmailMessage(
            #     "New contact form submission",
            #     content,
            #     "Your website" + '',
            #     ['youremail@gmail.com'],
            #     headers={'Reply-To': email}
            # )
            # email.send()
            return redirect('')

    return render(request, 'contactus.html', {
        'form': form_class,
    })


def logout_(request):
    logout(request)
    return render(request, 'error.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def home(request):
    return render(request, 'home.html')
