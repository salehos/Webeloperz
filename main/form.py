from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    type = forms.TypedChoiceField(widget=forms.RadioSelect, choices=(("Student", "دانشجو"), ("Teacher", "استاد")))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'type',)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email__iexact=email, is_active=True).exists():
            pass
            # raise ValidationError("There is no user registered with the specified email address!")
        return email

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'type',)


class ContactForm(forms.Form):
    title = forms.CharField(required=True)
    text = forms.CharField(
        required=True,
        widget=forms.Textarea
    )
    email = forms.EmailField(required=True)


class NavSearchForm(forms.Form):
    query = forms.CharField(max_length=30, required=False)


def ProductsPage(request):
    search_form = NavSearchForm()
    if request.GET.has_key('query'):
        query = request.GET['query'].strip()
    # deal with 'Products' here...


def ServicePage(request):
    search_form = NavSearchForm()
    if request.GET.has_key('query'):
        query = request.GET['query'].strip()
    # deal with 'Service' here...
