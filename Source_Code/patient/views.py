from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from module.models import Patient, Appointment
from patient.forms import PatientForm


def patient_dashboard(request):
    # past_appointments = Appointment.objects.filter(patient=obj.patient)
    past_appointments = Appointment.objects.filter(patient_id=24).order_by('-date')


    context={
        'past_appointments': past_appointments,
    }

    return render(request, 'patient/dashboard.html', context)

def editProfile(request):
    obj = get_object_or_404(Patient, id=24)
    form = PatientForm(request.POST or None, instance=obj)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Update Successful !")
        return HttpResponseRedirect("dashboard")
    return render(request, 'patient/editform.html', {'form': form, 'title': "hello"})


def view_appointment_history(request):
    obj = Appointment.objects.filter(id=24).order_by('-date')

    context={
        'object': obj
    }

    return render(request,'patient/view_appointment_history.html',context)

