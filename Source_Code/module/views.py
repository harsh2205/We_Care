# Create your views here.




# ================================================= Accounts =========================================================
import datetime
import re
from sqlite3 import IntegrityError

import simplejson as simplejson
from django.contrib import messages
from django.contrib.auth import (
    authenticate,
    login,
    logout,

)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect

# API--------------------------------------------------
from module import time4, dts
from module.SetOp import OrderedSet
from module.forms import ManufacturerForm, SupplierForm, BatchForm, ProductForm
from module.models import Appointment, Product, Batch, Manufacturer, Supplier, Appointment_Status, Prescription_List, \
    Prescription_Details
from .models import Patient
from .forms import UserLoginForm, UserCreateForm, AppointmentForm

# Create your views here.

TITLE = "We Care"

Login_URL = '/login/'


def login_view(request):
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)

        login(request, user)
        if user.groups.filter(name="Admin").exists():
            return redirect(reverse('home'))
        elif user.groups.filter(name="Doctors").exists():
            return redirect('doctors')
        elif user.groups.filter(name="receptionist").exists():
            return redirect('receptionist')
        elif user.groups.filter(name="pharmacy").exists():
            return redirect('pharmacy')
        return render(request, "home.html", {"form": form, "title": title})

    return render(request, "accounts/login.html", {"form": form, "title": title})


def register_view(request):
    return render(request, "form.html", {})


@login_required(login_url=Login_URL)
def logout_view(request):
    logout(request)
    return redirect(reverse('login'))


@login_required(login_url=Login_URL)
def home(request):
    return render(request, "home.html", {})


@login_required(login_url=Login_URL)
def doctors(request):
    vdatetime = datetime.datetime.now() - datetime.timedelta(hours=4)
    vtime = vdatetime.time()
    vdate = vdatetime.date()
    doc_id = request.user.id
    print(doc_id)
    user = request.user
    obj = Appointment.objects.filter(date__gte=vdate, startTime__gte=vtime, doctor_id=doc_id, status=1)
    return render(request, "doctor/dashboard.html", {'object': obj, 'user': user})


@login_required(login_url=Login_URL)
def receptionist(request):
    return render(request, "receptionist/dashboard.html", {})


@login_required(login_url=Login_URL)
def receptionist_dev(request):
    vdatetime = datetime.datetime.now() - datetime.timedelta(hours=4)
    vtime = vdatetime.time()
    vdate = vdatetime.date()
    userName = request.user
    obj = Appointment.objects.filter(date__gte=vdate, startTime__gte=vtime, status_id=1)

    return render(request, "receptionist/receptionist_dev.html", {'object': obj, 'userName': userName})


@login_required(login_url=Login_URL)
def receptionist_appointment_history(request):
    vdatetime = datetime.datetime.now() - datetime.timedelta(6 * 365 / 12)
    vtime = vdatetime.time()
    vdate = vdatetime.date()
    userName = request.user
    obj = Appointment.objects.filter(date__gte=vdate,status__in=(1,3,4)).order_by('-date')
    context = {
        'object': obj,
        'userName': userName,
        'title': "Appointments"
    }

    return render(request, "receptionist/appointment_history.html", context)

@login_required(login_url=Login_URL)
def receptionist_appointment_history_archive(request):
    vdatetime = datetime.datetime.now() - datetime.timedelta(6 * 365 / 12)
    vtime = vdatetime.time()
    vdate = vdatetime.date()
    userName = request.user
    obj = Appointment.objects.all().order_by('-date')
    context = {
        'object': obj,
        'userName': userName,
        'title': "Archived Appointments"
    }

    return render(request, "receptionist/appointment_history.html", context)


@login_required(login_url=Login_URL)
def pharmacy(request):
    return render(request, "pharmacy/dashboard.html", {})


# ---------------------------------------------------- Development Testing Methods --------------------
@login_required(login_url=Login_URL)
def PasswordReset(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            # user = form.save()
            # update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/login.html', {
        'form': form
    })


@login_required(login_url=Login_URL)
def test2(request):
    title = "Sign Up"
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():

            user = form.save()
            # update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'title': title
    })


def xx(request):
    data = Appointment.objects.filter(doctor__username='jas', date=datetime.datetime.now().date()).values_list(
        'startTime')
    form = AppointmentForm
    print(data)
    print(time4)
    return render(request, 'form.html', {"form": form, "title": "hi"})


# ================================================= Doctor =========================================================

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]


def doctor_dashboard_que(request):
    id = request.POST.get('doctor_id', None)
    id = 3

    user = get_object_or_404(User, id=4)

    print(user.username)

    if user.groups.filter(name="Doctors").exists():
        # x= Appointment.objects.raw('SELECT * FROM module_appointment INNER JOIN module_patient ON module_appointment.patient_id = module_patient.id where doctor_id = 4 ')
        # appointment = get_object_or_404(Appointment, )
        appoientment = Appointment.objects.filter(doctor=4)
        print(appoientment.values())
        data = {str(appoientment[0].doctor): 'doctor', str(appoientment[0].patient): 'patient',
                str(appoientment[0].date): 'app_date', str(appoientment[0].symptoms): 'symptoms',
                appoientment[0].patient.phone_number: 'Number', appoientment[0].patient.email: 'email',

                }
        data_dict = ValuesQuerySetToDict(data)
        qs_json = json.dumps(data_dict)

    else:
        print("error")
        qs_json = serializers.serialize('json', [])

    return HttpResponse(qs_json, content_type='application/json')


def patient_file(request, id=None):
    obj = get_object_or_404(Appointment, id=id)

    past_appointments = Appointment.objects.filter(patient=obj.patient).order_by('-date')

    # patient = Patient.objects.filter(id=obj.patient)
    presID = []
    for data in past_appointments:
        presID = Prescription_List.objects.filter(appointment_id=39)

    print(presID)

    Context_dictonary = {
        'object': obj,
        # 'patient': patient
        'past_appointments': past_appointments

    }

    return render(request, "doctor/patient_file.html", Context_dictonary)


# ================================================= Patient =========================================================

import json
from django.core import serializers
from django.http import HttpResponse


def search_patient(request):
    query_type = request.POST.get('type', None)

    if query_type == "fl":
        data = Patient.objects.filter(first_name__iexact=request.POST.get('first_name', None),
                                      last_name__iexact=request.POST.get('last_name', None))
    elif query_type == "f":
        data = Patient.objects.filter(first_name__icontains=request.POST.get('first_name', None))
    elif query_type == "p":
        data = Patient.objects.filter(phone_number__iexact=request.POST.get('phone_number', None))
    elif query_type == "e":
        data = Patient.objects.filter(email__iexact=request.POST.get('email', None))

    if not data:
        qs_json = serializers.serialize('json', data)
    else:
        print(data)
        qs_json = serializers.serialize('json', data)

    return HttpResponse(qs_json, content_type='application/json')


def book_appointment(request):
    doctors = User.objects.filter(groups__name='Doctors')

    if not doctors:
        qs_json = serializers.serialize('json', doctors)
    else:
        print(doctors)
        qs_json = serializers.serialize('json', doctors)

    return HttpResponse(qs_json, content_type='application/json')


def search_slot(request):
    doctor_id = request.POST.get('doctor_id', None)
    appdate = datetime.datetime.strptime(request.POST.get('appdate', None), '%m/%d/%Y').date()
    startTime = request.POST.get('startTime', None)
    endTime = request.POST.get('endTime', None)

    existing_appoitnments = Appointment.objects.filter(doctor_id=doctor_id, date=appdate).values('startTime')

    dtx = [dt['startTime'].strftime("%I:%M %p") for dt in existing_appoitnments]

    available_slotslist = list(OrderedSet(dts) - OrderedSet(dtx))

    print(type(available_slotslist))

    if not available_slotslist:
        qs_json = json.dumps(available_slotslist)
    else:
        qs_json = json.dumps(available_slotslist)

    return HttpResponse(qs_json, content_type='application/json')


def final_book(request):
    appdate = datetime.datetime.strptime(request.POST.get('date', None), '%m/%d/%Y').date()
    x = request.POST.get('time', None);
    sym = request.POST.get('symptoms', None)
    apptime = datetime.datetime.strptime(x, "%I:%M %p").time()
    duration = 30

    model = Appointment(patient_id=request.POST.get('patient_id', None),
                        startTime=apptime,
                        doctor_id=request.POST.get('doctor_id', None),
                        date=appdate,
                        symptoms=sym,
                        duration=duration,
                        created_by=request.user)

    model.save()

    data = []

    if not data:
        qs_json = json.dumps(data)
    else:
        qs_json = json.dumps(data)

    import time
    # time.sleep(50000)

    return HttpResponse(qs_json, content_type='application/json')


def register_patient(request):
    first_name = request.POST.get('first_name', None)
    last_name = request.POST.get('last_name', None)
    dob = request.POST.get('dob', None)
    email = request.POST.get('email', None)
    blood_group = request.POST.get('blood_group', None)
    phone_number = request.POST.get('phone_number', None)
    response = []

    if Patient.objects.filter(email__contains=email):
        data = {}
        data['message'] = 'User Already Exists'
        response = json.dumps(data)
    else:
        patient = Patient(first_name=first_name, last_name=last_name, dob=dob, blood_group=blood_group, email=email,
                          phone_number=phone_number)
        patient.save()
        data = {}
        data['message'] = 'Patient Registered !'
        response = json.dumps(data)

    return HttpResponse(response, content_type='application/json')


# ================================================= Pharma =========================================================



def search_medicine(request):
    qs_json = []
    name = request.POST.get('medicine_name', None)
    power = request.POST.get('power', None)

    out = get_object_or_404(Product, product_name=name)

    batch = Batch.objects.filter(product__product_name__icontains=out, power=power)

    # batch = list(batch)

    qs_json = serializers.serialize('json', batch, indent=2, use_natural_foreign_keys=True,
                                    use_natural_primary_keys=True)

    # data = {str(out.product_name): 'name',
    #         str(out.manufacturer): 'patient',
    #         str(batch[0].manufacturing_date): 'app_date',
    #         str(batch[0].expire_date):'symptoms',
    #         str(batch[0].power): 'symptoms',
    #         str(batch[0].cost): 'symptoms',
    #                 }
    #
    # data_dict = ValuesQuerySetToDict(data)
    # qs_json = json.dumps(data_dict)

    # final = out.objects.filter(power=power)


    # if user.groups.filter(name="Doctors").exists():
    # x= Appointment.objects.raw('SELECT * FROM module_appointment INNER JOIN module_patient ON module_appointment.patient_id = module_patient.id where doctor_id = 4 ')
    # appointment = get_object_or_404(Appointment, )

    # print(appoientment.values())
    # data = {str(appoientment[0].doctor):'doctor', str(appoientment[0].patient):'patient',
    #         str(appoientment[0].date): 'app_date', str(appoientment[0].symptoms):'symptoms',
    #         appoientment[0].patient.phone_number : 'Number', appoientment[0].patient.email : 'email',
    #
    #         }
    # data_dict = ValuesQuerySetToDict(data)
    # qs_json = json.dumps(data_dict)

    # else:
    #      print("error")
    # qs_json = serializers.serialize('json', x)

    return HttpResponse(qs_json, content_type='application/json')


def manufacturer_list_view(request):
    obj = Manufacturer.objects.all()

    Context_dictonary = {
        'object': obj,
        'title': "Medicine Manufacturer(s)",
        "create_link": "/xpharma/create_manufacturer",
        'xedit': "manufacturer"

    }

    return render(request, 'pharmacy/List_View.html', Context_dictonary)


def manufacturer_detail_view(request):
    obj = get_object_or_404(Manufacturer, id=1)

    Context_dictonary = {
        'object': obj,

    }

    return render(request, 'pharmacy/Detail_View.html', Context_dictonary)


def supplier_list_view(request):
    obj = Supplier.objects.all()

    Context_dictonary = {
        'object': obj,
        'title': "Medicine Suppliers(s)",
        "create_link": "/xpharma/create_supp",
        'xedit': "supplier"

    }

    return render(request, 'pharmacy/List_View.html', Context_dictonary)


@login_required(login_url=Login_URL)
def edit_appointment(request, id=None):
    obj = get_object_or_404(Appointment, id=id)
    form = AppointmentForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Update Successful !")
        return HttpResponseRedirect("/receptionist_his")

    placeholder = ['Patient', 'Doctor', 'Symptoms', 'Date', 'Time', 'Status']
    zipped_data = zip(form, placeholder)
    context = {
        'form': form,
        'title': "Edit Appointment",
        'title_1': "Appointment Details",
        'zipped_data': zipped_data,
        'back_link': '/receptionist_his'
    }
    return render(request, 'form_templates/edit_form.html', context)


@login_required(login_url=Login_URL)
def cancle_appointment(request, id=None):
    data = get_object_or_404(Appointment, id=id)
    if data.status.status == "Booked" or data.status.status == "Queued":
        status = "Canceled"
        data.status = get_object_or_404(Appointment_Status, status=status)
        data.save()
    return HttpResponseRedirect("/receptionist_his")


def View_appointment(request, id=None):
    obj = get_object_or_404(Appointment, id=id)

    return render(request, 'list_view.html', {'obj': obj, 'title': "hello"})


def view_batch(request, id=None):
    obj = Batch.objects.all()

    return render(request, 'pharmacy/list_batch.html', {'object': obj, 'title': "Batch", "create_link": "create_batch"})


def view_all_products(request, id=None):
    obj = Product.objects.all()

    return render(request, 'pharmacy/list_product.html',
                  {'object': obj, 'title': "All Medicines", "create_link": "new_product"})


def create_manufacturer(request):
    form = ManufacturerForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Created Manufacturer Successful !")
        return HttpResponseRedirect("/xpharma/manufacturer")
    return render(request, 'pharmacy/create_mfg.html', {'form': form, 'title': "hello"})


def create_supplier(request):
    form = SupplierForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Created supplier Successful !")
        return HttpResponseRedirect("/xpharma/supplier")
    return render(request, 'pharmacy/create_mfg.html', {'form': form, 'title': "hello"})


def create_batch(request):
    form = BatchForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Created supplier Successful !")
        return HttpResponseRedirect("/xpharma/batch")
    return render(request, 'pharmacy/create_mfg.html', {'form': form, 'title': "hello", })


def new_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Created supplier Successful !")
        return HttpResponseRedirect("/xpharma/product")
    return render(request, 'pharmacy/create_mfg.html', {'form': form, 'title': "hello"})


def edit_product(request, id=None):
    obj = get_object_or_404(Product, id=id)
    form = ProductForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Update Successful !")
        return HttpResponseRedirect("/xpharma/product")

    placeholder = ['Product Name', 'Manufacturer', 'Minimum Quantity Required']
    zipped_data = zip(form, placeholder)
    context = {
        'form': form,
        'title': "Edit Product Details",
        'title_1': "Product Details",
        'zipped_data': zipped_data,
        'back_link': '/xpharma/product'
    }
    return render(request, 'form_templates/edit_form.html', context)


def edit_batch(request, id=None):
    obj = get_object_or_404(Batch, id=id)
    form = BatchForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Update Successful !")
        return HttpResponseRedirect("/xpharma/batch")

    placeholder = ['Product Name', 'Supplier', 'Initial Count', 'Available Count', 'Manufacturing Date', 'Expire Date',
                   'Cost', 'Purchase Date', 'Power']
    zipped_data = zip(form, placeholder)
    context = {
        'form': form,
        'title': "Edit Product Details",
        'title_1': "Product Details",
        'zipped_data': zipped_data,
        'back_link': '/xpharma/batch'
    }
    return render(request, 'form_templates/edit_form.html', context)


def edit_supplier(request, id=None):
    obj = get_object_or_404(Supplier, id=id)
    form = SupplierForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Update Successful !")
        return HttpResponseRedirect("/xpharma/supplier")
    placeholder = ['Supplier Name', 'Location', 'Phone Number', 'Address', 'Email']
    zipped_data = zip(form, placeholder)
    context = {
        'form': form,
        'title': "Edit Supplier Details",
        'title_1': "Supplier Details",
        'zipped_data': zipped_data,
        'back_link': '/xpharma/supplier'
    }
    return render(request, 'form_templates/edit_form.html', context)


def edit_manufacturer(request, id=None):
    obj = get_object_or_404(Manufacturer, id=id)
    form = ManufacturerForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Update Successful !")
        return HttpResponseRedirect("/xpharma/manufacturer")
    placeholder = ['Manufacturer Name', 'Location', 'Phone Number', 'Address', 'Email']
    zipped_data = zip(form, placeholder)
    context = {
        'form': form,
        'title': "Edit Supplier Details",
        'title_1': "Supplier Details",
        'zipped_data': zipped_data,
        'back_link': '/xpharma/manufacturer'
    }
    return render(request, 'form_templates/edit_form.html', context)


def endapp(request):
    diagnostics = request.POST.get('diagnostics', None)
    appid = request.POST.get('appid', None)
    appid = str(appid)
    data = get_object_or_404(Appointment, id=appid)
    data.diagnostics = diagnostics
    data.status = get_object_or_404(Appointment_Status, status="Billing")
    data.save()

    data = {}
    data['message'] = 'App Ended !'
    response = json.dumps(data)

    return HttpResponse(response, content_type='application/json')


# ---------------------------------------------------------- Patient ----------------------------------------

def app_end(request):
    ids = json.loads(request.POST.get('ids', None))
    name = json.loads(request.POST.get('name', None))
    power = json.loads(request.POST.get('power', None))
    quant = json.loads(request.POST.get('quant', None))
    referer = request.META.get('HTTP_REFERER')
    referer = re.sub('^https?:\/\/', '', referer).split('/')
    Appointment_id = referer[2]

    Prescription = Prescription_List()
    Prescription.appointment = get_object_or_404(Appointment, id=Appointment_id)
    Prescription.save()

    Prescription_details_list = []

    pt=0
    print(type(ids))

    for i,value in ids.items():
        Prescription_details = Prescription_Details()
        x = get_object_or_404(Product,id=value)
        Prescription_details.product = get_object_or_404(Product, id=x.id)
        Prescription_details.power = power[i]
        Prescription_details.quantity = quant[i]
        Prescription_details.prescription = Prescription
        Prescription_details.batch_id = 0
        Prescription_details_list.append(Prescription_details)

    try:
        with transaction.atomic():
            # Prescription.save()
            for Prescription_details in Prescription_details_list:
                Prescription_details.save()
    except IntegrityError:
        print("Error")

    data = {}
    data['message'] = 'App Ended !'
    response = json.dumps(data)

    return HttpResponse(response, content_type='application/json')
