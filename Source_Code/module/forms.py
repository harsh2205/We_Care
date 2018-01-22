# ================================================= Accounts =========================================================

from django import forms
from django.forms import ModelForm

from module.models import Supplier, Batch, Product, Appointment_Status
from .models import Appointment, Manufacturer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)

User_Model = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        user = User.objects.filter(username=username)
        user = user.first()

        if not user:
            raise forms.ValidationError("This User Does not exist")
        elif not user.is_active:
            raise forms.ValidationError("This User no longer Active.")
        elif not user.check_password(password):
            print(user.password)
            raise forms.ValidationError("Incorrect Username / Password")

        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User_Model
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.is_active = False
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


# ================================================= Accounts =========================================================


class AppointmentForm(ModelForm):
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(groups__name="Doctors"))
    date = forms.DateField(widget=forms.TextInput(attrs={'picker': 'Date-Picker'}))
    startTime = forms.CharField(widget=forms.TextInput(attrs={'picker': 'Clock-Picker'}))
    status = forms.ModelChoiceField(queryset=Appointment_Status.objects.all())

    class Meta:
        model = Appointment
        fields = ('patient','doctor','symptoms','date','startTime','status')

# ================================================= Pharma =========================================================
class ManufacturerForm(ModelForm):
    # doctor = forms.ModelChoiceField(queryset=User.objects.filter(groups__name="Doctors"))
    # date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datetime-input'}))
    class Meta:
        model = Manufacturer
        fields = "__all__"

class SupplierForm(ModelForm):
    # doctor = forms.ModelChoiceField(queryset=User.objects.filter(groups__name="Doctors"))
    # date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datetime-input'}))
    class Meta:
        model = Supplier
        fields = "__all__"

class BatchForm(ModelForm):
    # doctor = forms.ModelChoiceField(queryset=User.objects.filter(groups__name="Doctors"))
    manufacturing_date = forms.DateField(widget=forms.TextInput(attrs={'picker': 'Date-Picker'}))
    expire_date = forms.DateField(widget=forms.TextInput(attrs={'picker': 'Date-Picker'}))
    purchase_date = forms.DateField(widget=forms.TextInput(attrs={'picker': 'Date-Picker'}))
    class Meta:
        model = Batch
        fields = "__all__"

class ProductForm(ModelForm):
    # doctor = forms.ModelChoiceField(queryset=User.objects.filter(groups__name="Doctors"))
    # date = forms.DateField(widget=forms.TextInput(attrs={'class': 'datetime-input'}))
    class Meta:
        model = Product
        fields = "__all__"